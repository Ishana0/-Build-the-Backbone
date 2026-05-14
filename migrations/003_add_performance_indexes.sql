-- 003_add_performance_indexes.sql

-- Justification: Speeds up fetching orders for a specific user during order history requests.
CREATE INDEX IF NOT EXISTS idx_orders_user_id
ON orders(user_id);

-- Justification: Improves sorting performance when ordering user orders by creation date.
CREATE INDEX IF NOT EXISTS idx_orders_created_at
ON orders(created_at DESC);

-- Justification: Prevents sequential scans when fetching items belonging to an order.
CREATE INDEX IF NOT EXISTS idx_order_items_order
ON order_items(order_id);

-- Justification: Optimizes joins between order_items and menu_items tables.
CREATE INDEX IF NOT EXISTS idx_order_items_menu_item
ON order_items(menu_item_id);

-- Justification: Improves restaurant filtering queries by city.
CREATE INDEX IF NOT EXISTS idx_restaurants_city
ON restaurants(city);

-- Justification: Speeds up menu item lookup by restaurant.
CREATE INDEX IF NOT EXISTS idx_menu_items_restaurant
ON menu_items(restaurant_id);

-- Justification: Improves category-based menu filtering queries.
CREATE INDEX IF NOT EXISTS idx_menu_items_category
ON menu_items(category_id);