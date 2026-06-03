"""
Customer Data Migration & ETL Validation Project

This script reads legacy CSV files, cleans common data issues, validates the
records, writes cleaned target CSV files, and creates a data quality report.
"""

from pathlib import Path

import pandas as pd


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"
REPORTS_DIR = PROJECT_ROOT / "reports"


def load_csv(file_name):
    """Read a CSV file from the raw data folder."""
    return pd.read_csv(RAW_DIR / file_name)


def clean_date_column(df, column_name, report_lines):
    """
    Convert a date column into YYYY-MM-DD format.

    Invalid dates become blank values in the cleaned output.
    """
    original_missing = df[column_name].isna().sum()
    parsed_dates = pd.to_datetime(df[column_name], errors="coerce", format="mixed")
    invalid_dates = parsed_dates.isna().sum() - original_missing

    df[column_name] = parsed_dates.dt.strftime("%Y-%m-%d")

    if invalid_dates > 0:
        report_lines.append(f"- Fixed {invalid_dates} invalid date value(s) in {column_name}.")

    return df


def clean_customers(customers, report_lines):
    """Clean customer records."""
    starting_rows = len(customers)

    # Remove duplicate customer IDs and keep the row with the most complete data.
    customers["filled_fields"] = customers.notna().sum(axis=1)
    customers = customers.sort_values("filled_fields", ascending=False)
    customers = customers.drop_duplicates(subset=["customer_id"], keep="first")
    customers = customers.drop(columns=["filled_fields"])

    duplicate_rows_removed = starting_rows - len(customers)
    if duplicate_rows_removed > 0:
        report_lines.append(f"- Removed {duplicate_rows_removed} duplicate customer row(s).")

    # Standardize missing emails and phone numbers so they are easy to filter.
    missing_emails = customers["email"].isna().sum()
    missing_phones = customers["phone"].isna().sum()
    customers["email"] = customers["email"].fillna("missing_email")
    customers["phone"] = customers["phone"].fillna("missing_phone")

    if missing_emails > 0:
        report_lines.append(f"- Flagged {missing_emails} missing customer email value(s).")
    if missing_phones > 0:
        report_lines.append(f"- Flagged {missing_phones} missing customer phone value(s).")

    customers = clean_date_column(customers, "created_date", report_lines)

    return customers.sort_values("customer_id")


def clean_accounts(accounts, valid_customer_ids, report_lines):
    """Clean account records."""
    starting_rows = len(accounts)

    # Keep only accounts that belong to a valid customer.
    accounts = accounts[accounts["customer_id"].isin(valid_customer_ids)].copy()
    orphan_accounts_removed = starting_rows - len(accounts)
    if orphan_accounts_removed > 0:
        report_lines.append(f"- Removed {orphan_accounts_removed} account row(s) with unknown customer IDs.")

    # Keep active accounts only for the target migration file.
    inactive_count = (accounts["status"].str.lower() == "inactive").sum()
    accounts = accounts[accounts["status"].str.lower() == "active"].copy()
    if inactive_count > 0:
        report_lines.append(f"- Excluded {inactive_count} inactive account row(s).")

    accounts = clean_date_column(accounts, "open_date", report_lines)

    # Convert balances to numbers. Invalid balances become 0.
    accounts["balance"] = pd.to_numeric(accounts["balance"], errors="coerce").fillna(0)

    return accounts.sort_values("account_id")


def clean_bills(bills, valid_account_ids, report_lines):
    """Clean bill records."""
    starting_rows = len(bills)

    # Keep only bills connected to migrated accounts.
    bills = bills[bills["account_id"].isin(valid_account_ids)].copy()
    orphan_bills_removed = starting_rows - len(bills)
    if orphan_bills_removed > 0:
        report_lines.append(f"- Removed {orphan_bills_removed} bill row(s) with unknown or inactive account IDs.")

    bills = clean_date_column(bills, "bill_date", report_lines)
    bills = clean_date_column(bills, "due_date", report_lines)

    # Convert bill amounts to numbers and remove invalid negative bills.
    bills["bill_amount"] = pd.to_numeric(bills["bill_amount"], errors="coerce")
    invalid_bill_amounts = bills["bill_amount"].isna().sum() + (bills["bill_amount"] < 0).sum()
    bills = bills[bills["bill_amount"].notna() & (bills["bill_amount"] >= 0)].copy()

    if invalid_bill_amounts > 0:
        report_lines.append(f"- Removed {invalid_bill_amounts} bill row(s) with invalid bill amounts.")

    return bills.sort_values("bill_id")


def clean_payments(payments, valid_bill_ids, report_lines):
    """Clean payment records."""
    starting_rows = len(payments)

    # Keep only payments connected to migrated bills.
    payments = payments[payments["bill_id"].isin(valid_bill_ids)].copy()
    orphan_payments_removed = starting_rows - len(payments)
    if orphan_payments_removed > 0:
        report_lines.append(f"- Removed {orphan_payments_removed} payment row(s) with unknown bill IDs.")

    payments = clean_date_column(payments, "payment_date", report_lines)

    # Convert payment amounts to numbers and remove invalid negative/non-numeric values.
    payments["payment_amount"] = pd.to_numeric(payments["payment_amount"], errors="coerce")
    invalid_payment_amounts = payments["payment_amount"].isna().sum() + (payments["payment_amount"] < 0).sum()
    payments = payments[payments["payment_amount"].notna() & (payments["payment_amount"] >= 0)].copy()

    if invalid_payment_amounts > 0:
        report_lines.append(f"- Removed {invalid_payment_amounts} payment row(s) with invalid payment amounts.")

    return payments.sort_values("payment_id")


def write_outputs(customers, accounts, bills, payments, report_lines):
    """Write cleaned CSV files and the data quality report."""
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    customers.to_csv(CLEANED_DIR / "customers_cleaned.csv", index=False)
    accounts.to_csv(CLEANED_DIR / "accounts_cleaned.csv", index=False)
    bills.to_csv(CLEANED_DIR / "bills_cleaned.csv", index=False)
    payments.to_csv(CLEANED_DIR / "payments_cleaned.csv", index=False)

    report_path = REPORTS_DIR / "data_quality_report.txt"
    with report_path.open("w", encoding="utf-8") as report:
        report.write("Customer Data Migration & ETL Validation Report\n")
        report.write("================================================\n\n")
        report.write("Cleaned row counts:\n")
        report.write(f"- Customers: {len(customers)}\n")
        report.write(f"- Accounts: {len(accounts)}\n")
        report.write(f"- Bills: {len(bills)}\n")
        report.write(f"- Payments: {len(payments)}\n\n")
        report.write("Data quality fixes:\n")
        report.write("\n".join(report_lines))
        report.write("\n")


def main():
    """Run the full extract, transform, load, and validation process."""
    report_lines = []

    # Extract: read legacy CSV files.
    customers = load_csv("customers_legacy.csv")
    accounts = load_csv("accounts_legacy.csv")
    bills = load_csv("bills_legacy.csv")
    payments = load_csv("payments_legacy.csv")

    # Transform and validate each dataset in dependency order.
    customers_cleaned = clean_customers(customers, report_lines)
    accounts_cleaned = clean_accounts(accounts, customers_cleaned["customer_id"], report_lines)
    bills_cleaned = clean_bills(bills, accounts_cleaned["account_id"], report_lines)
    payments_cleaned = clean_payments(payments, bills_cleaned["bill_id"], report_lines)

    # Load: write cleaned target files and a simple report.
    write_outputs(customers_cleaned, accounts_cleaned, bills_cleaned, payments_cleaned, report_lines)

    print("ETL completed successfully.")
    print(f"Cleaned files created in: {CLEANED_DIR}")
    print(f"Report created in: {REPORTS_DIR / 'data_quality_report.txt'}")


if __name__ == "__main__":
    main()
