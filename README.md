# README — Vacation Planner PoC (AI + Mock Booking API)

Proof-of-Concept untuk AssistX Technical Assessment
Author: Widi Sayyid Fadhil Muhammad

🚀 Overview

Project ini adalah sebuah Proof-of-Concept (PoC) untuk membangun Vacation Planner berbasis LLM open source (Ollama Llama 3.2).

Sistem ini dapat:

Memahami permintaan pengguna dalam natural language

Menghasilkan itinerary liburan lengkap dalam format JSON

Menyusun booking plan berdasarkan opsi nyata dari mock API

Menjalankan pemesanan hanya setelah user memberikan konfirmasi & payment token

PoC ini menunjukkan bagaimana AI agent + grounding + mock API dapat bekerja untuk menghasilkan pengalaman perencanaan liburan yang cerdas dan aman.

🧱 Project Structure
assistx-vacation-planner/
├─ src/
│  ├─ mock_api.py                   # FastAPI mock server (hotels, flights, activities, booking)
│  ├─ tools.py                      # API wrappers (search_* and book_item)
│  ├─ agent_planner_ollama_simple.py# LLM agent (prompt engineered, CLI-based)
│  ├─ run_flow_ask.py               # Full flow: plan → confirm → book
│  └─ planner_demo.py               # Simple baseline planner (non-LLM)
├─ mock_data/
│  ├─ hotels.json
│  ├─ flights.json
│  └─ activities.json
├─ docs/
│  ├─ SOLUTION.md                   # Full solution document (technical writeup)
│  └─ DEMO_SCRIPT.md (optional)
├─ requirements.txt
└─ README.md

🧠 Tech Stack
Komponen	Teknologi
LLM	Ollama — llama3.2:latest
Bahasa pemrograman	Python 3.x
Agent orchestration	Custom Python + subprocess (stabil)
API	FastAPI + Uvicorn
Data fetching	requests
Environment	Python venv
Dataset	local mock JSON
⚙️ Setup Environment
1. Clone repository
git clone https://github.com/<your-username>/assistx-vacation-planner.git
cd assistx-vacation-planner

2. Setup Virtual Environment
python -m venv .venv


Windows:

.venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Install required LLM model in Ollama

Pastikan Ollama sudah terinstall.

ollama pull llama3.2

🏦 Running the Mock API

Di terminal pertama:

uvicorn src.mock_api:app --reload


API tersedia di:
👉 http://127.0.0.1:8000/docs

🤖 Running the Vacation Planner Agent

Di terminal kedua:

.venv\Scripts\activate
python src/agent_planner_ollama_simple.py


Masukkan contoh permintaan:

3 days in Bali, for 2 people, budget 6,000,000 IDR, must do snorkeling


Hasil:

JSON itinerary

total_cost

booking_plan

🛒 Running Full Booking Flow (Plan → Confirm → Book)
python src/run_flow_ask.py


Contoh alur:

Masukkan permintaan user

Sistem menampilkan itinerary

User menjawab: yes

Masukkan payment_token → gunakan: tok_test

Mock API melakukan booking dan mengembalikan booking_id

Output contoh:

- Booking hotel hotel_bali_01: {'status': 'booked', 'booking_id': 'BK-user123-hotel_bali_01'}
- Booking flight flight_jkt_dps_02: {...}
- Booking activity activity_snorkel_ubud: {...}

🔒 Security Considerations

LLM tidak pernah mengeksekusi booking.

Booking hanya dilakukan Python setelah user menyetujui.

payment_token tidak pernah dikirim ke LLM.

Prompt grounding digunakan untuk mencegah hallucination.

Data sensitif tidak dicatat di log.

Detail lengkap berada di docs/SOLUTION.md.

📹 Demo Video

Rekaman demo CLI + mock booking (2–3 menit)

Link akan disertakan dalam submission (Drive/YouTube Unlisted)

📄 Solution Document

Dokumen lengkap tersedia di:

docs/SOLUTION.md


Termasuk:

Arsitektur

Risiko & mitigasi

Alur end-to-end

Penjelasan prompt engineering

Penjelasan grounding

📌 Recommended Commands for Quick Testing

Jalankan semuanya sekali jalan:

# Terminal 1
uvicorn src.mock_api:app --reload

# Terminal 2
.venv\Scripts\activate
python src/agent_planner_ollama_simple.py

# Terminal 3
python src/run_flow_ask.py

🧪 Sample Prompt
Plan a 3-day relaxing trip to Bali for two people, with a budget of six million rupiah and must-do snorkeling.

📨 Submission Format

GitHub repo link

SOLUTION.md (atau PDF)

Demo video

README.md (file ini)

Semua kode bisa dijalankan (mock API + agent)

🤝 Contact

Widi Sayyid Fadhil Muhammad
email@example.com

+62-8XX-XXXX-XXXX
