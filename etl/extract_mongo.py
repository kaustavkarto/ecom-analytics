from app.db.mongo import get_events_collection

def extract_events():
    collection = get_events_collection()
    
    events = list(collection.find({}, {
        "_id": 0,
        "event_type": 1,
        "user_id": 1,
        "product_id": 1,
        "session_id": 1,
        "timestamp": 1,
        "metadata.device": 1,
        "metadata.city": 1
    }))
    
    print(f"Extracted {len(events)} events from MongoDB")
    return events