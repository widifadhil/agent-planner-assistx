# src/run_flow_ask.py
import json
from agent_planner_ollama_simple import plan_vacation_flow
from tools import book_item

def run():
    req = input("User request (e.g. '3 days in Bali, budget 6,000,000 IDR, snorkeling'): ").strip()
    res = plan_vacation_flow(req)
    if not res["ok"]:
        print("Planner error:", res)
        return

    full_data = res["data"]
    plan_details = full_data.get("plan_details", {})
    print("\n=== Planner Suggestion ===")
    print(full_data.get("conversational_summary", "Tidak ada ringkasan."))

    plan = plan_details.get("booking_plan", [])
    if not plan:
        print("\nNo booking plan proposed (nothing to book).")
        return

    confirm = input("\nProceed to book these items? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Booking cancelled by user.")
        return

    token = input("Enter payment_token (use 'tok_test' for PoC): ").strip()
    print("\nExecuting bookings (mock API)...")
    for item in plan:
        resp = book_item(user_id="user123", item_type=item["type"], item_id=item["id"], payment_token=token)
        print(f"- Booking {item['type']} {item['id']}: {resp}")

if __name__ == "__main__":
    run()
