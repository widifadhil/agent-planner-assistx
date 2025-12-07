# src/agent_planner_ollama_simple.py
# PoC simple agent: ground model dengan mock API options, panggil Ollama CLI, dan parse JSON output.
# Simpan file ini di folder src/ project kamu lalu jalankan:
# python src\agent_planner_ollama_simple.py

import json
import subprocess
from typing import Optional
import sys, os, pathlib

# tambahkan folder src ke sys.path (relatif ke root project)
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from tools import search_hotels, search_flights, search_activities

OLLAMA_MODEL = "llama3.2:latest"  # sesuai output ollama list

# tambahkan import baru di atas file jika belum ada
from math import ceil

# fungsi bantu: ringkas options supaya prompt tidak terlalu panjang dan mudah dibaca model
def summarize_options(hotels, flights, activities, max_items=5):
    """
    Mengambil daftar options dan merangkum hanya field penting.
    Mengembalikan dict dengan lists yang berisi dict ringkas.
    """
    def short_h(h):
        return {
            "id": h.get("id"),
            "name": h.get("name"),
            "location": h.get("location"),
            "price_per_night": h.get("price_per_night"),
            "stars": h.get("stars")
        }
    def short_f(f):
        return {
            "id": f.get("id"),
            "airline": f.get("airline"),
            "from": f.get("from"),
            "to": f.get("to"),
            "departure": f.get("departure"),
            "arrival": f.get("arrival"),
            "price": f.get("price")
        }
    def short_a(a):
        return {
            "id": a.get("id"),
            "title": a.get("title"),
            "location": a.get("location"),
            "duration_hours": a.get("duration_hours"),
            "price": a.get("price")
        }

    return {
        "hotels": [short_h(h) for h in hotels][:max_items],
        "flights": [short_f(f) for f in flights][:max_items],
        "activities": [short_a(a) for a in activities][:max_items]
    }

# ganti template lama dengan ini (lebih ketat + contoh)
PROMPT_TEMPLATE = """
You are VacationPlanner. You MUST produce a single valid JSON object and nothing else.
Your JSON output must have two top-level keys: "conversational_summary" and "plan_details".

RULES (strict):
1) For "plan_details", choose items only from AVAILABLE OPTIONS (use id fields). DO NOT invent prices or items.
2) Respect user's budget (if budget provided). If budget insufficient, return questions with needed info.
3) For hotels: pick ONE hotel for the whole stay. Use price_per_night * nights to compute hotel cost.
4) For flights: pick ONE outbound flight (cheapest that matches route) and include its price.
5) For activities: pick up to 2 activities that fit budget (optional).
6) total_cost = hotel_cost + flight_cost + sum(activity prices).
7) booking_plan should be a list of objects: {"type":"hotel|flight|activity","id":"<item_id>"}
8) If you need clarification (dates, number of nights, number of people), put them in questions list and STOP (do not make bookings).
9) Use currency IDR, integer numbers only.
10) For "conversational_summary", create a friendly and engaging narrative summarizing the plan for the user. Address them directly.

AVAILABLE OPTIONS (already filtered & summarized):
HOTELS:
__HOTELS__

FLIGHTS:
__FLIGHTS__

ACTIVITIES:
__ACTIVITIES__

EXAMPLE OUTPUT (format EXACTLY like this):
{
  "conversational_summary": "Halo! Saya sudah siapkan rencana liburan 3 hari yang seru di Bali untuk Anda, sesuai dengan budget dan keinginan untuk snorkeling. Total biayanya sekitar 1.850.000 IDR. Di hari pertama Anda akan tiba dan check-in di Bali Seaside Hotel. Hari kedua kita akan bersenang-senang dengan snorkeling di Nusa Lembongan. Menarik, bukan?",
  "plan_details": {
    "itinerary": [
      {"day":1,"activity":"arrival & check-in","hotel":"Bali Seaside Hotel"},
      {"day":2,"activity":"snorkeling (Nusa Lembongan)","hotel":"Bali Seaside Hotel"},
      {"day":3,"activity":"checkout & depart","hotel":"Bali Seaside Hotel"}
    ],
    "total_cost": 1850000,
    "booking_plan": [
      {"type":"hotel","id":"hotel_bali_01"},
      {"type":"flight","id":"flight_jkt_dps_02"},
      {"type":"activity","id":"activity_snorkel_ubud"}
    ],
    "questions": []
  }
}

USER REQUEST:
__USER_REQUEST__

Return only JSON.
"""


def call_ollama(prompt: str) -> str:
    """
    Calls Ollama CLI using UTF-8-safe subprocess handling for Windows.
    Sends prompt via stdin to avoid quoting issues.
    """
    cmd_list = ["ollama", "run", OLLAMA_MODEL]
    try:
        result = subprocess.run(
            cmd_list,
            input=prompt,          # kirim prompt via stdin, aman untuk quoting 
            text=True,
            encoding="utf-8",      # force utf-8 encoding
            capture_output=True,
            check=False,           # We will check the return code manually
            timeout=180
        )
        if result.returncode != 0:
            return f"Ollama error: {result.stderr}"
        return result.stdout
    except Exception as e:
        return f"CALL ERROR: {e}"

def plan_vacation_flow(user_request: str, destination: Optional[str]=None, max_price: Optional[int]=None):
    # Basic extraction: if user provided a destination in prompt, use it; else use parameter
    dest = destination
    if not dest:
        # crude parse: look for "in <Place>" or "to <Place>"
        tokens = user_request.lower().split()
        if "in" in tokens:
            idx = tokens.index("in")
            if idx+1 < len(tokens):
                dest = tokens[idx+1].capitalize()
        elif "to" in tokens:
            idx = tokens.index("to")
            if idx+1 < len(tokens):
                dest = tokens[idx+1].capitalize()
    if not dest:
        dest = "Bali"  # default assumption

    # try to extract numeric budget from user_request (IDR)
    if not max_price:
        import re
        # Regex yang lebih baik untuk menangani format seperti "6jt", "6 juta", "6.000.000"
        m = re.search(r'(\d[\d,.]*)\s*(k|rb|ribu|jt|juta|m|mio)?', user_request.lower())
        if m:
            num = m.group(1).replace(",", "").replace(".", "")
            suffix = m.group(2) or ""
            try:
                val = int(num)
                # handle common suffixes
                if suffix in ("juta", "m", "mio", "jt"):
                    val = val * 1000000
                elif suffix in ("k","rb","ribu"):
                    val = val * 1000
                max_price = val
            except:
                max_price = None

    # call tool wrappers to get options (grounding)
    hotels = search_hotels(location=dest, max_price=max_price)["results"]
    flights = search_flights(_from="CGK", to="DPS" if dest.lower()=="bali" else None, max_price=max_price or None)["results"]
    activities = search_activities(location=dest)["results"]

    # summarize options to reduce prompt size and focus the model
    summary = summarize_options(hotels, flights, activities, max_items=5)
    prompt = PROMPT_TEMPLATE.replace("__HOTELS__", json.dumps(summary["hotels"], ensure_ascii=False))\
                            .replace("__FLIGHTS__", json.dumps(summary["flights"], ensure_ascii=False))\
                            .replace("__ACTIVITIES__", json.dumps(summary["activities"], ensure_ascii=False))\
                            .replace("__USER_REQUEST__", user_request)

    # call ollama
    raw = call_ollama(prompt)
    # Try to extract JSON from output
    out_text = raw.strip()
    # if output starts with { or [, try parse
    try:
        start = out_text.find("{")
        end = out_text.rfind("}") + 1
        json_text = out_text[start:end]
        data = json.loads(json_text)
        return {"ok": True, "data": data, "raw": out_text}
    except Exception as e:
        return {"ok": False, "error": str(e), "raw": out_text, "prompt": prompt}

if __name__ == "__main__":
    # interactive quick test
    req = input("User request (e.g. '3 days in Bali, budget 6,000,000 IDR, snorkeling'): ").strip()
    res = plan_vacation_flow(req)
    print("-" * 20)
    if res["ok"]:
        # Cetak ringkasan percakapan dari output gabungan
        print(res["data"].get("conversational_summary", "Tidak ada ringkasan."))
    else:
        print("ERROR parsing model output:", res.get("error"))
        print("RAW model output:\n", res.get("raw")[:2000])
        # if parse failed, you can inspect full prompt in res["prompt"]
