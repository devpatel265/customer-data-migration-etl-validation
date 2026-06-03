-- Find duplicate business keys in source or cleaned files.
-- Cleaned results should not have duplicate customer IDs.

SELECT customer_id, COUNT(*) AS duplicate_count
FROM customers_legacy
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT customer_id, COUNT(*) AS duplicate_count
FROM customers_cleaned
GROUP BY customer_id
HAVING COUNT(*) > 1;
