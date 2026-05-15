from datetime import datetime

def transform_orders(rows):
    transformed = []
    for row in rows:
        transformed.append({
            "order_id": row["order_id"],
            "user_id": row["user_id"],
            "total_amount": float(row["total_amount"]),
            "status": row["status"],
            "city": row["city"] or "Unknown",
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "category": row["category"],
            "quantity": row["quantity"],
            "unit_price": float(row["unit_price"]),
            "order_date": row["created_at"].date().isoformat(),
            "order_hour": row["created_at"].hour,
            "order_month": row["created_at"].strftime("%Y-%m"),
            "revenue": float(row["unit_price"]) * row["quantity"]
        })
    print(f"Transformed {len(transformed)} order rows")
    return transformed


def transform_events(events):
    transformed = []
    for event in events:
        metadata = event.get("metadata", {})
        transformed.append({
            "event_type": event["event_type"],
            "user_id": event["user_id"],
            "product_id": event["product_id"],
            "session_id": event["session_id"],
            "timestamp": event["timestamp"].isoformat(),
            "event_date": event["timestamp"].date().isoformat(),
            "event_hour": event["timestamp"].hour,
            "device": metadata.get("device") or "Unknown",
            "city": metadata.get("city") or "Unknown"
        })
    print(f"Transformed {len(transformed)} event rows")
    return transformed