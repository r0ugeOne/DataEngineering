# SQL Practice Queries

## Basic Queries
```sql
-- Get unique categories
SELECT DISTINCT category FROM transactions;

-- Count records by type
SELECT type, COUNT(*) as count FROM events GROUP BY type;
```

## Aggregations
```sql
-- Daily totals
SELECT 
    DATE(transaction_date) as date,
    COUNT(*) as num_transactions,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM transactions
GROUP BY DATE(transaction_date)
ORDER BY date DESC;
```

## Joins
```sql
-- User transactions with details
SELECT 
    u.username,
    COUNT(t.transaction_id) as num_transactions,
    SUM(t.amount) as total_spent
FROM users u
LEFT JOIN transactions t ON u.user_id = t.user_id
GROUP BY u.username
ORDER BY total_spent DESC;
```

## Window Functions
```sql
-- Running totals
SELECT 
    transaction_date,
    amount,
    SUM(amount) OVER (
        ORDER BY transaction_date
    ) as running_total
FROM transactions
ORDER BY transaction_date;
```

## Subqueries
```sql
-- Users with above average spending
SELECT username, email
FROM users
WHERE user_id IN (
    SELECT user_id
    FROM transactions
    GROUP BY user_id
    HAVING SUM(amount) > (
        SELECT AVG(total) FROM (
            SELECT user_id, SUM(amount) as total
            FROM transactions
            GROUP BY user_id
        ) sub
    )
);
```
