import mysql.connector
from faker import Faker
import random
from dotenv import load_dotenv
import os

load_dotenv()

fake = Faker('en_IN')

conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    port=int(os.getenv('MYSQL_PORT')),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)

cursor = conn.cursor()

# --- Users ---
print("Inserting users...")
cities = ['Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
users = []
for _ in range(100):
    name = fake.name()
    email = fake.unique.email()
    phone = fake.phone_number()[:15]
    city = random.choice(cities)
    cursor.execute(
        "INSERT INTO users (name, email, phone, city) VALUES (%s, %s, %s, %s)",
        (name, email, phone, city)
    )
    users.append(cursor.lastrowid)
conn.commit()
print(f"{len(users)} users inserted")

# --- Products ---
print("Inserting products...")
categories = ['Electronics', 'Clothing', 'Groceries', 'Books', 'Home & Kitchen', 'Sports']
product_names = {
    'Electronics': ['Wireless Earbuds', 'Phone Case', 'USB Cable', 'Power Bank', 'Bluetooth Speaker'],
    'Clothing': ['Cotton T-Shirt', 'Denim Jeans', 'Casual Shirt', 'Sports Shoes', 'Ethnic Kurta'],
    'Groceries': ['Basmati Rice 5kg', 'Toor Dal 1kg', 'Sunflower Oil 1L', 'Atta 10kg', 'Masala Pack'],
    'Books': ['Python Programming', 'Data Structures', 'System Design', 'Clean Code', 'The Alchemist'],
    'Home & Kitchen': ['Steel Tiffin Box', 'Non-stick Pan', 'Water Bottle', 'Mixer Grinder', 'Pressure Cooker'],
    'Sports': ['Yoga Mat', 'Skipping Rope', 'Badminton Racket', 'Cricket Ball', 'Gym Gloves']
}
products = []
for category, names in product_names.items():
    for name in names:
        price = round(random.uniform(50, 5000), 2)
        stock = random.randint(10, 500)
        cursor.execute(
            "INSERT INTO products (name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)",
            (name, category, price, stock)
        )
        products.append(cursor.lastrowid)
conn.commit()
print(f"{len(products)} products inserted")

# --- Orders and Order Items ---
print("Inserting orders and order items...")
statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
for _ in range(500):
    user_id = random.choice(users)
    status = random.choice(statuses)
    num_items = random.randint(1, 5)
    selected_products = random.sample(products, num_items)

    total_amount = 0
    order_items_data = []
    for product_id in selected_products:
        quantity = random.randint(1, 3)
        cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
        unit_price = cursor.fetchone()[0]
        total_amount += unit_price * quantity
        order_items_data.append((product_id, quantity, unit_price))

    cursor.execute(
        "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s)",
        (user_id, round(total_amount, 2), status)
    )
    order_id = cursor.lastrowid

    for product_id, quantity, unit_price in order_items_data:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
            (order_id, product_id, quantity, unit_price)
        )

conn.commit()
print("500 orders inserted")

cursor.close()
conn.close()
print("Done!")