-- Compare financial totals between source and cleaned target files.
-- Some totals may change because invalid or orphan records are removed.
-- TRY_CAST safely handles non-numeric legacy values such as "abc".

SELECT 'bills_legacy' AS table_name, SUM(TRY_CAST(bill_amount AS DECIMAL(10, 2))) AS total_bill_amount
FROM bills_legacy
WHERE TRY_CAST(bill_amount AS DECIMAL(10, 2)) >= 0
UNION ALL
SELECT 'bills_cleaned' AS table_name, SUM(bill_amount) AS total_bill_amount
FROM bills_cleaned;

SELECT 'payments_legacy' AS table_name, SUM(TRY_CAST(payment_amount AS DECIMAL(10, 2))) AS total_payment_amount
FROM payments_legacy
WHERE TRY_CAST(payment_amount AS DECIMAL(10, 2)) >= 0
UNION ALL
SELECT 'payments_cleaned' AS table_name, SUM(payment_amount) AS total_payment_amount
FROM payments_cleaned;
