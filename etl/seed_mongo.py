from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

fake = Faker('en_IN')

client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('MONGO_DATABASE')]
events = db['events']

# Get user and product IDs from env (we'll use same range as MySQL)
user_ids = list(range(1, 101))
product_ids = list(range(1, 31))
devices = ['mobile', 'desktop', 'tablet']
cities = ['Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']

def random_timestamp():
    start = datetime.now() - timedelta(days=30)
    return start + timedelta(seconds=random.randint(0, 30*24*3600))

print("Inserting events...")

all_events = []

for _ in range(2000):
    user_id = random.choice(user_ids)
    product_id = random.choice(product_ids)
    session_id = fake.uuid4()
    device = random.choice(devices)
    city = random.choice(cities)
    timestamp = random_timestamp()

    # page_view always happens
    all_events.append({
        "event_type": "page_view",
        "user_id": user_id,
        "product_id": product_id,
        "session_id": session_id,
        "timestamp": timestamp,
        "metadata": {
            "device": device,
            "city": city
        }
    })

    # 70% chance add to cart
    if random.random() < 0.7:
        all_events.append({
            "event_type": "add_to_cart",
            "user_id": user_id,
            "product_id": product_id,
            "session_id": session_id,
            "timestamp": timestamp + timedelta(seconds=random.randint(10, 120)),
            "metadata": {
                "device": device,
                "city": city
            }
        })

        # 50% chance checkout started
        if random.random() < 0.5:
            all_events.append({
                "event_type": "checkout_started",
                "user_id": user_id,
                "product_id": product_id,
                "session_id": session_id,
                "timestamp": timestamp + timedelta(seconds=random.randint(120, 300)),
                "metadata": {
                    "device": device,
                    "city": city
                }
            })

            # 60% chance order placed
            if random.random() < 0.6:
                all_events.append({
                    "event_type": "order_placed",
                    "user_id": user_id,
                    "product_id": product_id,
                    "session_id": session_id,
                    "timestamp": timestamp + timedelta(seconds=random.randint(300, 600)),
                    "metadata": {
                        "device": device,
                        "city": city
                    }
                })

events.insert_many(all_events)
print(f"{len(all_events)} events inserted")

client.close()
print("Done!")