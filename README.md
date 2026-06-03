# Customer Data Migration & ETL Validation Project

## Project Overview

This project simulates a small customer data migration.

Legacy customer, account, billing, and payment data starts in messy CSV files. A Python ETL script reads those files, cleans the data, validates common issues, and writes cleaned target CSV files.

The project shows basic skills used in real data conversion work:

- Extracting data from source files
- Cleaning messy records
- Transforming dates into a standard format
- Removing duplicate records
- Validating missing and invalid values
- Creating cleaned target files
- Writing SQL checks for migration validation
- Creating a data quality report

## Why This Project Matters

Data migration projects often involve moving old data from legacy systems into a new system. Before the new system can use the data, the data must be cleaned and validated.

This project demonstrates that process in a simple way using Python, pandas, CSV files, and SQL validation queries.

## Folder Structure

```text
.
|-- data/
|   |-- raw/                 # Legacy source CSV files with data issues
|   |-- cleaned/             # Cleaned target CSV files created by the ETL script
|-- scripts/
|   |-- etl_migration.py     # Python ETL script
|-- sql/                     # SQL validation queries
|-- reports/                 # Data quality report created by the ETL script
|-- README.md
|-- requirements.txt
```

## Raw Data Files

The `data/raw` folder contains four legacy CSV files:

- `customers_legacy.csv`
- `accounts_legacy.csv`
- `bills_legacy.csv`
- `payments_legacy.csv`

These files include realistic data problems:

- Duplicate customers
- Missing emails
- Missing phone numbers
- Inconsistent date formats
- Invalid payment amounts
- Invalid bill amounts
- Inactive accounts
- Records linked to missing customers, accounts, or bills

## ETL Process

The ETL script is located at:

```text
scripts/etl_migration.py
```

It performs three main steps.

### 1. Extract

The script reads the legacy CSV files from `data/raw`.

### 2. Transform And Clean

The script:

- Removes duplicate customers
- Fills missing emails and phone numbers with clear placeholder values
- Converts dates to `YYYY-MM-DD`
- Removes accounts connected to unknown customers
- Excludes inactive accounts
- Removes bills connected to invalid accounts
- Removes payments connected to invalid bills
- Removes negative or non-numeric payment amounts

### 3. Load

The script writes cleaned files to `data/cleaned`:

- `customers_cleaned.csv`
- `accounts_cleaned.csv`
- `bills_cleaned.csv`
- `payments_cleaned.csv`

It also creates:

```text
reports/data_quality_report.txt
```

## SQL Validation Files

The `sql` folder contains basic validation queries:

- `01_row_counts.sql`: compares source and cleaned row counts
- `02_duplicate_checks.sql`: checks for duplicate customer IDs
- `03_missing_value_checks.sql`: checks missing or placeholder values
- `04_totals_comparison.sql`: compares bill and payment totals

These queries represent common checks used after data migration.

## How To Run The Project

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the ETL script

```bash
python scripts/etl_migration.py
```

### 5. Review the outputs

Cleaned CSV files:

```text
data/cleaned
```

Data quality report:

```text
reports/data_quality_report.txt
```

## Skills Demonstrated

- Python scripting
- pandas DataFrames
- CSV file processing
- ETL workflow design
- Data cleaning
- Data validation
- Date standardization
- Duplicate detection
- Missing value handling
- SQL validation checks
- Migration documentation

## Interview Explanation

You can explain this project like this:

"I built a beginner-friendly data migration project that simulates moving customer, account, billing, and payment records from legacy CSV files into cleaned target files. I used Python and pandas to extract the source data, clean duplicates and missing values, standardize dates, remove invalid records, and write cleaned CSV outputs. I also added SQL validation queries for row counts, duplicate checks, missing values, and financial totals. This project shows my understanding of ETL, data migration, and data validation."

## Disclaimer

This project uses sample data only. It is designed for learning and portfolio demonstration.
