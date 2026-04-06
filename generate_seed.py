import random
from faker import Faker

fake = Faker()

def generate_seed_data():
    num_users = 1000
    num_restaurants = 100
    num_menu_items = 500
    num_categories = 10
    num_orders = 5000
    num_order_items = 25000
    num_reviews = 2000

    sql_output = []

    # Categories
    categories = ['Appetizers', 'Main Course', 'Desserts', 'Beverages', 'Salads', 'Sides', 'Pizza', 'Burgers', 'Sushi', 'Pasta']
    for cat in categories:
        sql_output.append(f"INSERT INTO categories (name) VALUES ('{cat}');")

    # Users
    for i in range(1, num_users + 1):
        name = fake.name().replace("'", "''")
        email = f"user{i}@example.com"
        # Bcrypt hash for 'password123'
        password_hash = '$2a$12$R9h/lIPzHZ7.3m8.6u8/G.8.m.h.P.f.X.P.P.P.P.P.P.P.P.P.P' 
        address = fake.address().replace("'", "''")
        sql_output.append(f"INSERT INTO users (name, email, password_hash, address) VALUES ('{name}', '{email}', '{password_hash}', '{address}');")

    # Restaurants
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    cuisines = ['Italian', 'Mexican', 'Chinese', 'Japanese', 'Indian', 'American', 'French', 'Thai', 'Korean', 'Greek']
    for i in range(1, num_restaurants + 1):
        name = fake.company().replace("'", "''") + " QuickBite"
        city = random.choice(cities)
        cuisine = random.choice(cuisines)
        rating = round(random.uniform(3.0, 5.0), 1)
        sql_output.append(f"INSERT INTO restaurants (name, city, cuisine, rating) VALUES ('{name}', '{city}', '{cuisine}', {rating});")

    # Menu Items
    for i in range(1, num_menu_items + 1):
        restaurant_id = random.randint(1, num_restaurants)
        category_id = random.randint(1, num_categories)
        name = (fake.word() + " " + fake.word()).title().replace("'", "''")
        description = fake.sentence().replace("'", "''")
        price = round(random.uniform(5.0, 50.0), 2)
        sql_output.append(f"INSERT INTO menu_items (restaurant_id, category_id, name, description, price) VALUES ({restaurant_id}, {category_id}, '{name}', '{description}', {price});")

    # Orders
    for i in range(1, num_orders + 1):
        user_id = random.randint(1, num_users)
        restaurant_id = random.randint(1, num_restaurants)
        status = random.choice(['pending', 'completed', 'cancelled', 'delivered'])
        total_amount = 0 # Will update after order items
        delivery_fee = round(random.uniform(2.0, 10.0), 2)
        sql_output.append(f"INSERT INTO orders (user_id, restaurant_id, status, total_amount, delivery_fee) VALUES ({user_id}, {restaurant_id}, '{status}', 0, {delivery_fee});")

    # Order Items (This might be tricky to match total order amount, but for performance, we just need the queries)
    for i in range(1, num_order_items + 1):
        order_id = random.randint(1, num_orders)
        menu_item_id = random.randint(1, num_menu_items)
        quantity = random.randint(1, 5)
        # In a real app, unit_price would come from menu_item, but for seed data, we just want queries.
        unit_price = round(random.uniform(5.0, 50.0), 2)
        subtotal = round(unit_price * quantity, 2)
        sql_output.append(f"INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price, subtotal) VALUES ({order_id}, {menu_item_id}, {quantity}, {unit_price}, {subtotal});")

    # Update total_amount in orders based on items (approximate calculation for realism)
    sql_output.append("UPDATE orders o SET total_amount = (SELECT COALESCE(SUM(subtotal), 0) FROM order_items WHERE order_id = o.id) + delivery_fee;")

    # Reviews
    for i in range(1, num_reviews + 1):
        restaurant_id = random.randint(1, num_restaurants)
        user_id = random.randint(1, num_users)
        rating = random.randint(1, 5)
        comment = fake.text(max_nb_chars=100).replace("'", "''")
        sql_output.append(f"INSERT INTO reviews (restaurant_id, user_id, rating, comment) VALUES ({restaurant_id}, {user_id}, {rating}, '{comment}');")

    with open('migrations/002_seed_data.sql', 'w') as f:
        f.write("\n".join(sql_output))

if __name__ == "__main__":
    generate_seed_data()
