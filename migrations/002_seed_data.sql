-- QuickBite: Seed Data Migration
-- Using generate_series for performance and volume.

BEGIN;

-- 1. Categories
INSERT INTO categories (name) VALUES 
('Appetizers'), ('Main Course'), ('Desserts'), ('Beverages'), ('Salads'), 
('Sides'), ('Pizza'), ('Burgers'), ('Sushi'), ('Pasta');

-- 2. Users (1,000)
INSERT INTO users (name, email, password_hash, address)
SELECT 
    'User ' || i,
    'user' || i || '@example.com',
    '$2a$12$R9h/lIPzHZ7.3m8.6u8/G.8.m.h.P.f.X.P.P.P.P.P.P.P.P.P.P', -- 'password123'
    i || ' Main St, Townsville'
FROM generate_series(1, 1000) AS i;

-- 3. Restaurants (100)
INSERT INTO restaurants (name, city, cuisine, rating)
SELECT 
    'Restaurant ' || i || ' QuickBite',
    CASE (i % 5) 
        WHEN 0 THEN 'New York' 
        WHEN 1 THEN 'Los Angeles' 
        WHEN 2 THEN 'Chicago'
        WHEN 3 THEN 'Houston'
        ELSE 'Miami'
    END,
    CASE (i % 4)
        WHEN 0 THEN 'Italian'
        WHEN 1 THEN 'Mexican'
        WHEN 2 THEN 'Japanese'
        ELSE 'American'
    END,
    3.0 + (i % 20) / 10.0
FROM generate_series(1, 100) AS i;

-- 4. Menu Items (500)
INSERT INTO menu_items (restaurant_id, category_id, name, description, price)
SELECT 
    (i % 100) + 1,
    (i % 10) + 1,
    'Menu Item ' || i,
    'Delicious food item number ' || i,
    10.0 + (i % 40)
FROM generate_series(1, 500) AS i;

-- 5. Orders (5,000)
INSERT INTO orders (user_id, restaurant_id, status, total_amount, delivery_fee)
SELECT 
    (i % 1000) + 1,
    (i % 100) + 1,
    CASE (i % 3)
        WHEN 0 THEN 'completed'
        WHEN 1 THEN 'delivered'
        ELSE 'pending'
    END,
    0, -- updated later
    3.99
FROM generate_series(1, 5000) AS i;

-- 6. Order Items (25,000)
INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price, subtotal)
SELECT 
    (i % 5000) + 1,
    (i % 500) + 1,
    (i % 3) + 1,
    15.00,
    15.00 * ((i % 3) + 1)
FROM generate_series(1, 25000) AS i;

-- 7. Update Order Totals
UPDATE orders o 
SET total_amount = (SELECT COALESCE(SUM(subtotal), 0) FROM order_items WHERE order_id = o.id) + delivery_fee;

-- 8. Reviews (2,000)
INSERT INTO reviews (restaurant_id, user_id, rating, comment)
SELECT 
    (i % 100) + 1,
    (i % 1000) + 1,
    (i % 5) + 1,
    'Great experience! Item was fresh and tasty.'
FROM generate_series(1, 2000) AS i;

COMMIT;
