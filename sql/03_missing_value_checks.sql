-- Check for missing or placeholder values after migration.
-- These queries help identify records that still need review.

SELECT COUNT(*) AS missing_email_count
FROM customers_cleaned
WHERE email IS NULL OR email = '' OR email = 'missing_email';

SELECT COUNT(*) AS missing_phone_count
FROM customers_cleaned
WHERE phone IS NULL OR phone = '' OR phone = 'missing_phone';

SELECT COUNT(*) AS missing_account_open_date_count
FROM accounts_cleaned
WHERE open_date IS NULL OR open_date = '';

SELECT COUNT(*) AS missing_bill_date_count
FROM bills_cleaned
WHERE bill_date IS NULL OR bill_date = '';

SELECT COUNT(*) AS missing_payment_date_count
FROM payments_cleaned
WHERE payment_date IS NULL OR payment_date = '';
