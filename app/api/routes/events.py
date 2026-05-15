from fastapi import APIRouter, HTTPException
from app.models.event import EventCreate
from app.db.mongo import get_events_collection
from datetime import datetime

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/")
def log_event(event: EventCreate):
    try:
        collection = get_events_collection()
        event_doc = {
            "event_type": event.event_type.value,
            "user_id": event.user_id,
            "product_id": event.product_id,
            "session_id": event.session_id,
            "timestamp": datetime.utcnow(),
            "metadata": {
                "device": event.metadata.device if event.metadata else None,
                "city": event.metadata.city if event.metadata else None
            }
        }
        result = collection.insert_one(event_doc)
        return {"message": "Event logged", "event_id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}")
def get_user_events(user_id: int, event_type: str = None):
    try:
        collection = get_events_collection()
        query = {"user_id": user_id}
        if event_type:
            query["event_type"] = event_type

        events = list(collection.find(query, {"_id": 0}).sort("timestamp", -1).limit(50))
        return {"user_id": user_id, "events": events}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))