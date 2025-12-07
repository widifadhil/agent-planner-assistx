from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mock Booking API")

with open("mock_data/hotels.json", "r", encoding="utf-8") as f:
    HOTELS = json.load(f)
with open("mock_data/flights.json", "r", encoding="utf-8") as f:
    FLIGHTS = json.load(f)
with open("mock_data/activities.json", "r", encoding="utf-8") as f:
    ACTIVITIES = json.load(f)

class BookingRequest(BaseModel):
    user_id: str
    item_type: str
    item_id: str
    payment_token: Optional[str] = None

@app.get("/search/hotels")
def search_hotels(location: str = None, max_price: int = None):
    results = [h for h in HOTELS if (location is None or location.lower() in h["location"].lower())]
    if max_price:
        results = [h for h in results if h["price_per_night"] <= max_price]
    return {"results": results}

@app.get("/search/flights")
def search_flights(_from: str = None, to: str = None, max_price: int = None):
    results = [f for f in FLIGHTS if (_from is None or f["from"] == _from) and (to is None or f["to"] == to)]
    if max_price:
        results = [f for f in results if f["price"] <= max_price]
    return {"results": results}

@app.get("/search/activities")
def search_activities(location: str = None, max_price: int = None):
    results = [a for a in ACTIVITIES if (location is None or location.lower() in a["location"].lower())]
    if max_price:
        results = [a for a in results if a["price"] <= max_price]
    return {"results": results}

@app.post("/book")
def book(req: BookingRequest):
    if req.item_type not in ("hotel","flight","activity"):
        raise HTTPException(400, "invalid item_type")
    if not req.payment_token:
        raise HTTPException(403, "payment_token required for booking")
    return {"status": "booked", "booking_id": f"BK-{req.user_id}-{req.item_id}"}
