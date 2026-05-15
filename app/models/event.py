from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class EventType(str, Enum):
    page_view = "page_view"
    add_to_cart = "add_to_cart"
    checkout_started = "checkout_started"
    order_placed = "order_placed"

class EventMetadata(BaseModel):
    device: Optional[str] = None
    city: Optional[str] = None

class EventCreate(BaseModel):
    event_type: EventType
    user_id: int
    product_id: int
    session_id: str
    metadata: Optional[EventMetadata] = None