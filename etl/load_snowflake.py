import snowflake.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from app.core.config import (
    SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER,
    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
)

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        authenticator="programmatic_access_token",
        token=os.getenv("SNOWFLAKE_TOKEN"),
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    return conn

def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders_fact (
            order_id INTEGER,
            user_id INTEGER,
            total_amount FLOAT,
            status VARCHAR(20),
            city VARCHAR(50),
            product_id INTEGER,
            product_name VARCHAR(200),
            category VARCHAR(50),
            quantity INTEGER,
            unit_price FLOAT,
            order_date DATE,
            order_hour INTEGER,
            order_month VARCHAR(7),
            revenue FLOAT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events_fact (
            event_type VARCHAR(50),
            user_id INTEGER,
            product_id INTEGER,
            session_id VARCHAR(100),
            timestamp VARCHAR(50),
            event_date DATE,
            event_hour INTEGER,
            device VARCHAR(20),
            city VARCHAR(50)
        )
    """)
    print("Tables created in Snowflake")

def load_orders(cursor, rows):
    cursor.execute("TRUNCATE TABLE orders_fact")
    for row in rows:
        cursor.execute("""
            INSERT INTO orders_fact VALUES (
                %(order_id)s, %(user_id)s, %(total_amount)s, %(status)s,
                %(city)s, %(product_id)s, %(product_name)s, %(category)s,
                %(quantity)s, %(unit_price)s, %(order_date)s, %(order_hour)s,
                %(order_month)s, %(revenue)s
            )
        """, row)
    print(f"Loaded {len(rows)} rows into orders_fact")

def load_events(cursor, rows):
    cursor.execute("TRUNCATE TABLE events_fact")
    for row in rows:
        cursor.execute("""
            INSERT INTO events_fact VALUES (
                %(event_type)s, %(user_id)s, %(product_id)s, %(session_id)s,
                %(timestamp)s, %(event_date)s, %(event_hour)s, %(device)s, %(city)s
            )
        """, row)
    print(f"Loaded {len(rows)} rows into events_fact")