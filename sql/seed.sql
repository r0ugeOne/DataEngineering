-- Seed data for testing

INSERT INTO users (username, email) VALUES
('alice', 'alice@example.com'),
('bob', 'bob@example.com'),
('charlie', 'charlie@example.com'),
('diana', 'diana@example.com'),
('eve', 'eve@example.com');

INSERT INTO transactions (user_id, amount, transaction_date, status, description) VALUES
(1, 100.00, '2024-01-15 10:30:00', 'completed', 'Purchase - Electronics'),
(1, 50.00, '2024-01-20 14:45:00', 'completed', 'Refund'),
(2, 250.00, '2024-01-18 09:15:00', 'completed', 'Purchase - Books'),
(3, 75.50, '2024-01-22 16:20:00', 'completed', 'Purchase - Clothing'),
(4, 125.00, '2024-01-25 11:00:00', 'pending', 'Purchase - Furniture');

INSERT INTO events (user_id, event_type, occurred_at) VALUES
(1, 'login', '2024-01-25 10:00:00'),
(2, 'login', '2024-01-25 10:30:00'),
(1, 'purchase', '2024-01-25 10:15:00'),
(3, 'login', '2024-01-25 11:00:00'),
(4, 'logout', '2024-01-25 11:30:00');
