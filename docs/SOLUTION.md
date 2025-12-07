# Solution Document - Vacation Planner PoC

## 1. Problem Statement
Pengguna membutuhkan sebuah asisten cerdas yang dapat secara otonom merencanakan liburan sesuai preferensi (tujuan, budget, aktivitas) dan melakukan pemesanan (booking) jika diizinkan. Solusi ini bertujuan untuk menyederhanakan proses perencanaan liburan yang kompleks dengan memanfaatkan teknologi Generative AI.

## 2. Assumptions
Untuk lingkup Proof-of-Concept (PoC) ini, beberapa asumsi dibuat:
- **Sumber Data**: Ketersediaan hotel, penerbangan, dan aktivitas disediakan melalui API internal (mock).
- **Preferensi Pengguna**: Preferensi dasar seperti tujuan dan budget diekstrak dari input teks sederhana. Asumsi yang lebih kompleks seperti kalender atau profil pengguna tidak diimplementasikan.
- **Konteks Penerbangan**: Rute penerbangan diasumsikan dari Jakarta (CGK) ke Bali (DPS) jika tujuan adalah Bali.
- **Pembayaran**: Proses pembayaran disimulasikan menggunakan token statis (`tok_test`).
- **Model AI**: Menggunakan model LLM open-source (Llama 3.2) yang berjalan secara lokal melalui Ollama.

## 3. High-level Architecture
Solusi ini menggunakan arsitektur **Retrieval-Augmented Generation (RAG)** untuk memastikan respons dari LLM relevan dan faktual.

1.  **User Input**: Pengguna memberikan permintaan dalam bahasa alami (misal: "3 hari di Bali, budget 6 juta, mau snorkeling").
2.  **Parameter Extraction**: Sistem mengekstrak entitas penting seperti `tujuan` dan `budget` dari permintaan pengguna.
3.  **Retrieval (Tool Calling)**: Berdasarkan parameter yang diekstrak, sistem memanggil serangkaian API (tools) untuk mengambil data relevan: `search_hotels()`, `search_flights()`, dan `search_activities()`.
4.  **Augmentation (Prompting)**: Data yang telah diambil (opsi hotel, penerbangan, aktivitas) disuntikkan ke dalam sebuah *prompt template* yang terstruktur. Prompt ini juga berisi instruksi ketat bagi LLM untuk menghasilkan output JSON yang valid dan hanya menggunakan data yang disediakan.
5.  **Generation (LLM Call)**: Prompt yang sudah diperkaya dikirim ke model LLM (via Ollama) untuk menghasilkan rencana perjalanan dalam format JSON.
6.  **User Confirmation & Execution**: Rencana perjalanan ditampilkan kepada pengguna. Jika pengguna setuju (`yes`), sistem akan mengeksekusi pemesanan dengan memanggil `book_item()` untuk setiap item dalam `booking_plan`.

## 4. Use Cases
1.  **Perencanaan Liburan**: Pengguna memasukkan permintaan, sistem memberikan proposal itinerary, total biaya, dan daftar item untuk dibooking.
2.  **Eksekusi Booking**: Setelah mendapat konfirmasi dari pengguna, sistem secara otomatis melakukan "pemesanan" melalui API yang sesuai.

## 5. Tech Stack
- **Programming Language**: Python 3.12
- **GenAI Technology**: Ollama (untuk menjalankan LLM secara lokal), Model: `llama3.2:latest`.
- **Core Libraries**: `subprocess` (untuk memanggil Ollama CLI), `json`, `re`.
- **Development Environment**: Python Virtual Environment (`venv`).

## 6. Implementation Steps
1.  **Mock APIs (`tools.py`)**: Membuat fungsi-fungsi mock untuk `search_hotels`, `search_flights`, `search_activities`, dan `book_item` sebagai simulasi backend service.
2.  **Planner Agent (`agent_planner_ollama_simple.py`)**: Mengimplementasikan alur RAG. Ini adalah komponen inti yang bertanggung jawab untuk memahami permintaan, mengambil data, dan berinteraksi dengan LLM.
3.  **Booking Executor (`run_flow_ask.py`)**: Membuat skrip *entrypoint* yang mengelola interaksi dengan pengguna, memanggil planner, dan mengeksekusi booking setelah mendapat persetujuan.

## 7. Security & Risks (detailed)
### Risk 1: Command Injection pada `call_ollama`
- **Attack Scenario**: Seorang penyerang dengan akses ke `OLLAMA_MODEL` environment variable bisa menyisipkan perintah shell berbahaya. Contoh: `OLLAMA_MODEL="llama3; rm -rf /"`. Karena `subprocess.run` menggunakan `shell=True`, perintah tambahan tersebut akan dieksekusi.
- **Likelihood/Impact**: Likelihood: Rendah (membutuhkan akses ke environment server). Impact: Kritis (bisa menyebabkan penghapusan data atau eksekusi kode arbitrer).
- **Mitigation**: Hindari `shell=True`. Gunakan `shlex.split(cmd)` untuk memecah perintah menjadi daftar argumen yang aman. Ini memastikan input diperlakukan sebagai argumen, bukan perintah shell.
- **Monitoring**: Lakukan audit kode secara berkala untuk mendeteksi penggunaan `shell=True` yang tidak aman. Gunakan static analysis tools (seperti `bandit` di Python) yang dapat mendeteksi pola ini.

### Risk 2: Parsing Entitas yang Tidak Aman dari User Input
- **Attack Scenario**: Pengguna bisa memasukkan input yang dirancang untuk mengacaukan logika parsing, misalnya dengan menyisipkan karakter atau kata kunci yang tidak terduga yang menyebabkan error atau perilaku aneh pada `plan_vacation_flow`.
- **Likelihood/Impact**: Likelihood: Sedang. Impact: Rendah-Sedang (dapat menyebabkan kegagalan layanan untuk satu permintaan atau respons yang salah).
- **Mitigation**: Gunakan metode parsing yang lebih kuat dan terstruktur. Daripada regex manual, pertimbangkan menggunakan LLM lain (atau LLM yang sama dengan prompt khusus) untuk mengekstrak entitas secara andal ke dalam format JSON yang tervalidasi. Lakukan validasi dan sanitasi input sebelum diproses lebih lanjut.
- **Monitoring**: Log semua permintaan yang gagal di tahap parsing. Jika tingkat kegagalan meningkat, ini bisa menjadi indikasi adanya upaya untuk mengeksploitasi parser.

## 8. Demo Plan & How to Run
### How to Run
1.  Pastikan Ollama sudah terinstal dan model `llama3.2` sudah diunduh (`ollama pull llama3.2`).
2.  Clone repository: `git clone <URL_REPOSITORY_ANDA>`
3.  Masuk ke direktori project: `cd assistx-vacation-planner`
4.  Buat dan aktifkan virtual environment: `python -m venv .venv` lalu `.venv\Scripts\activate` (Windows) atau `source .venv/bin/activate` (Linux/macOS).
5.  Instal dependensi: `pip install -r requirements.txt` (Anda perlu membuat file `requirements.txt`).
6.  Jalankan aplikasi: `python src/run_flow_ask.py`

### Demo Video
*(Sertakan link ke video demo Anda di sini setelah diunggah ke YouTube/Vimeo/platform lain)*

## 9. Conclusion
PoC ini berhasil menunjukkan kelayakan penggunaan arsitektur RAG dengan LLM open-source untuk membangun agen perencana liburan otonom. Solusi ini mampu memahami permintaan pengguna, mengambil data relevan dari tools eksternal, menghasilkan rencana yang koheren, dan mengeksekusi tindakan (booking) dengan persetujuan pengguna. Meskipun masih dalam skala PoC, arsitektur ini menyediakan fondasi yang kuat untuk pengembangan lebih lanjut.
