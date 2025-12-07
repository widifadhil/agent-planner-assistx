# src/tools.py
import requests

API_BASE = "http://127.0.0.1:8000"

def search_hotels(location: str = None, max_price: int = None):
    """
    Call mock API /search/hotels
    """
    params = {}
    if location:
        params["location"] = location
    if max_price:
        params["max_price"] = max_price

    r = requests.get(f"{API_BASE}/search/hotels", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def search_flights(_from: str = None, to: str = None, max_price: int = None):
    """
    Call mock API /search/flights
    """
    params = {}
    if _from:
        params["_from"] = _from
    if to:
        params["to"] = to
    if max_price:
        params["max_price"] = max_price

    r = requests.get(f"{API_BASE}/search/flights", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def search_activities(location: str = None, max_price: int = None):
    """
    Call mock API /search/activities
    """
    params = {}
    if location:
        params["location"] = location
    if max_price:
        params["max_price"] = max_price

    r = requests.get(f"{API_BASE}/search/activities", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def book_item(user_id: str, item_type: str, item_id: str, payment_token: str = None):
    """
    Call mock API /book
    """
    payload = {
        "user_id": user_id,
        "item_type": item_type,
        "item_id": item_id,
        "payment_token": payment_token
    }

    r = requests.post(f"{API_BASE}/book", json=payload, timeout=10)

    # If API rejects booking (ex: payment_token missing), return friendly error response
    if r.status_code >= 400:
        return {
            "error": True,
            "status_code": r.status_code,
            "message": r.text
        }

    return r.json()
