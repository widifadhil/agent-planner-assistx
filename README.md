# AssistX - Vacation Planner PoC
Repository untuk proof-of-concept Vacation Planner (LLM + Booking mock).
Structure:
- src/             # kode planner & agent
- mock_data/       # mock hotels/flights/activities json
- docs/SOLUTION.md # solution document (draft)
- notebooks/       # prototyping (opsional)

Cara mulai:
1. python -m venv .venv
2. source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
3. pip install -r requirements.txt
4. uvicorn src.mock_api:app --reload
5. jalankan script planner di src/
