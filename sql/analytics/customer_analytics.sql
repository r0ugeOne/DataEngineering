# Analytics Queries

## Customer Lifetime Value
```sql
SELECT 
    u.user_id,
    u.username,
    COUNT(t.transaction_id) as transaction_count,
    SUM(t.amount) as lifetime_value,
    AVG(t.amount) as avg_transaction_value,
    MAX(t.transaction_date) as last_transaction_date
FROM users u
LEFT JOIN transactions t ON u.user_id = t.user_id
GROUP BY u.user_id, u.username
ORDER BY lifetime_value DESC;
```

## Monthly Trends
```sql
SELECT 
    DATE_TRUNC('month', transaction_date) as month,
    COUNT(*) as num_transactions,
    SUM(amount) as total_revenue,
    COUNT(DISTINCT user_id) as unique_users
FROM transactions
WHERE status = 'completed'
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY month DESC;
```

## Event Analysis
```sql
SELECT 
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users,
    MAX(created_at) as last_event
FROM events
GROUP BY event_type
ORDER BY event_count DESC;
```

## User Segments
```sql
SELECT 
    CASE 
        WHEN SUM(t.amount) > 500 THEN 'High-Value'
        WHEN SUM(t.amount) > 100 THEN 'Medium-Value'
        ELSE 'Low-Value'
    END as segment,
    COUNT(DISTINCT u.user_id) as user_count,
    AVG(SUM(t.amount)) as avg_value
FROM users u
LEFT JOIN transactions t ON u.user_id = t.user_id
GROUP BY segment
ORDER BY avg_value DESC;
```
