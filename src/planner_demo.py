import requests, json

API_BASE = "http://127.0.0.1:8000"

def plan_vacation(destination, max_price):
    hotels = requests.get(f"{API_BASE}/search/hotels", params={"location": destination, "max_price": max_price}).json()
    flights = requests.get(f"{API_BASE}/search/flights", params={"to": "DPS", "_from": "CGK", "max_price": max_price}).json()
    activities = requests.get(f"{API_BASE}/search/activities", params={"location": destination}).json()

    hotel = hotels["results"][0] if hotels["results"] else None
    flight = flights["results"][0] if flights["results"] else None

    itinerary = {
        "days": [
            {"day":1, "activity": "arrival & check-in", "hotel": hotel["name"] if hotel else None},
            {"day":2, "activity": "snorkeling", "hotel": hotel["name"] if hotel else None},
            {"day":3, "activity": "checkout & depart", "hotel": hotel["name"] if hotel else None}
        ],
        "total_estimated": (hotel["price_per_night"]*2 if hotel else 0) + (flight["price"] if flight else 0)
    }

    booking_plan = []
    if hotel:
        booking_plan.append({"type":"hotel", "id":hotel["id"]})
    if flight:
        booking_plan.append({"type":"flight", "id":flight["id"]})

    return itinerary, booking_plan

if __name__ == "__main__":
    it, plan = plan_vacation("Bali", max_price=1000000)
    print(json.dumps({"itinerary": it, "booking_plan": plan}, indent=2, ensure_ascii=False))
