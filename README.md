# Vacation Planner PoC (AI + Mock Booking API)

**Proof-of-Concept untuk AssistX Technical Assessment** **Author:** Widi Sayyid Fadhil Muhammad

---

## 🚀 Overview

Project ini adalah sebuah **Proof-of-Concept (PoC)** untuk membangun Vacation Planner berbasis LLM open source (**Ollama Llama 3.2**).

Sistem ini dirancang untuk:
* ✅ Memahami permintaan pengguna dalam *natural language*.
* ✅ Menghasilkan itinerary liburan lengkap dalam format JSON.
* ✅ Menyusun *booking plan* berdasarkan opsi nyata dari Mock API.
* ✅ Menjalankan pemesanan hanya setelah user memberikan konfirmasi & *payment token*.

PoC ini menunjukkan bagaimana **AI agent + grounding + mock API** dapat bekerja untuk menghasilkan pengalaman perencanaan liburan yang cerdas dan aman.

---

## 🧱 Project Structure

```text
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
│  └─ DEMO_SCRIPT.md                # (Optional) Script for demo
├─ requirements.txt
└─ README.md
