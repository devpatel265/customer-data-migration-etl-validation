-- Compare source row counts to cleaned target row counts.
-- These checks help confirm how many records were loaded after cleaning.

SELECT 'customers_legacy' AS table_name, COUNT(*) AS row_count FROM customers_legacy
UNION ALL
SELECT 'customers_cleaned' AS table_name, COUNT(*) AS row_count FROM customers_cleaned
UNION ALL
SELECT 'accounts_legacy' AS table_name, COUNT(*) AS row_count FROM accounts_legacy
UNION ALL
SELECT 'accounts_cleaned' AS table_name, COUNT(*) AS row_count FROM accounts_cleaned
UNION ALL
SELECT 'bills_legacy' AS table_name, COUNT(*) AS row_count FROM bills_legacy
UNION ALL
SELECT 'bills_cleaned' AS table_name, COUNT(*) AS row_count FROM bills_cleaned
UNION ALL
SELECT 'payments_legacy' AS table_name, COUNT(*) AS row_count FROM payments_legacy
UNION ALL
SELECT 'payments_cleaned' AS table_name, COUNT(*) AS row_count FROM payments_cleaned;
