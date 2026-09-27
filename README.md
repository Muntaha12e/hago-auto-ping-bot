# Hago Auto Ping Bot

Project edukasi untuk belajar keep-alive / heartbeat sederhana, yang bisa dikembangkan menjadi bot otomatis untuk menjaga koneksi tetap aktif dalam aplikasi atau room tertentu.

Catatan penting:
- Project ini dibuat untuk pembelajaran dan eksperimen teknis.
- Ini bukan bot siap pakai untuk aplikasi Hago secara langsung tanpa modifikasi.
- Integrasi dengan aplikasi tertentu membutuhkan dokumentasi API, protokol komunikasi, atau tooling yang sesuai.

## Tujuan

Project ini dibuat untuk membantu pemula mempelajari:
- cara menjaga koneksi tetap aktif,
- mekanisme ping / heartbeat,
- logging dan debugging,
- struktur project Python yang rapi.

## Struktur project

```bash
hago-auto-ping-bot/
├── README.md
├── requirements.txt
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── ping_service.py
│   └── main.py
├── tests/
│   └── test_ping_service.py
└── venv/
```

## Prasyarat

- Python 3.10+
- Git
- Internet (untuk dependency)

## Instalasi

```bash
git clone https://github.com/Muntaha12e/hago-auto-ping-bot.git
cd hago-auto-ping-bot
python -m venv venv
source venv/bin/activate      # Linux/macOS
# atau
venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

## Menjalankan project

```bash
python -m app.main
```

## Konfigurasi

Buka file `app/config.py` untuk mengubah:
- interval ping,
- URL target,
- mode debug,
- room ID atau parameter tambahan.

## Cara kerja

Program ini bekerja dengan cara sederhana:

1. membaca konfigurasi,
2. menjalankan service heartbeat,
3. mengirim request secara berkala ke endpoint yang ditentukan,
4. mencatat log setiap aktivitas,
5. bisa dikembangkan menjadi bot yang lebih kompleks.

## Cara kerja ping service

Fungsi utama adalah mengirim payload yang berisi data seperti:

```python
{
    "event": "heartbeat",
    "status": "alive",
    "room_id": "demo-room",
    "timestamp": "2026-09-27T00:00:00Z"
}
```

## Roadmap

- menambahkan file konfigurasi JSON/YAML,
- menambahkan retry saat request gagal,
- menambahkan log ke file,
- membuat mode simulasi koneksi,
- mengintegrasikan ke aplikasi tertentu dengan API yang valid.

## Lisensi

Project ini dibuat untuk pembelajaran. Silakan sesuaikan lisensi jika ingin dipakai untuk proyek yang lebih serius.

## Disclaimer

Project ini bersifat eksperimen edukatif. Penulis tidak bertanggung jawab atas penyalahgunaan, pelanggaran kebijakan platform, atau kerugian yang diakibatkan dari penggunaan project ini.

## Langkah berikutnya

Kalau kamu mau, saya bisa lanjutkan membuat:
- `requirements.txt`
- `app/config.py`
- `app/logger.py`
- `app/ping_service.py`
- `app/main.py`
- test untuk project ini

Semua akan dibuat langsung di repo ini.
