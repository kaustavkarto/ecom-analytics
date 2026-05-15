from etl.extract_mysql import extract_orders
from etl.extract_mongo import extract_events
from etl.transform import transform_orders, transform_events
from etl.load_snowflake import get_snowflake_connection, create_tables, load_orders, load_events
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def run_pipeline():
    print(f"\n--- ETL Pipeline started at {datetime.now()} ---")

    try:
        # Extract
        raw_orders = extract_orders()
        raw_events = extract_events()

        # Transform
        transformed_orders = transform_orders(raw_orders)
        transformed_events = transform_events(raw_events)

        # Load
        conn = get_snowflake_connection()
        cursor = conn.cursor()

        create_tables(cursor)
        load_orders(cursor, transformed_orders)
        load_events(cursor, transformed_events)

        conn.commit()
        cursor.close()
        conn.close()

        print(f"--- ETL Pipeline completed at {datetime.now()} ---\n")

    except Exception as e:
        print(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Run once immediately
    run_pipeline()

    # Then schedule to run every 24 hours
    scheduler = BlockingScheduler()
    scheduler.add_job(run_pipeline, 'interval', hours=24)
    print("Scheduler started - pipeline will run every 24 hours")
    scheduler.start()