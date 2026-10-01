# Hago Auto Ping Bot

Auto ping bot untuk mempertahankan koneksi jaringan dan session di aplikasi Hago ketika offline.

## 📋 Daftar Isi

- [Tujuan](#tujuan)
- [Prasyarat](#prasyarat)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Menjalankan](#menjalankan)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## 🎯 Tujuan

Project ini adalah educational bot yang mempelajari:
- Cara menjaga koneksi tetap aktif dengan heartbeat/ping
- Implementasi retry logic dengan exponential backoff
- Logging dan monitoring bot 24/7
- Deployment ke production (Railway/Render)

**Catatan**: Project ini untuk pembelajaran dan development. Gunakan sesuai kebijakan Hago.

## 📦 Prasyarat

- Python 3.10+
- pip
- Git
- Internet connection

## 🚀 Instalasi

```bash
# Clone repository
git clone https://github.com/Muntaha12e/hago-auto-ping-bot.git
cd hago-auto-ping-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate      # Linux/macOS
# atau
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Konfigurasi

### Langkah 1: Copy template `.env`

```bash
cp .env.example .env
```

### Langkah 2: Isi environment variables

Edit `.env` dan isi dengan data dari DevTools Browser:

```env
# Endpoint yang ingin dipang
HAGO_URL=https://api.ihago.net/heartbeat

# Info room dari DevTools
HAGO_ROOM_ID=C_20453632134829821442_V2_ID_0_ID
HAGO_ROOM_TOKEN=6Fc5x1mhrD6xHezGGBt83zHgPP_kgN6vFwNwfKDQcpa1pKw

# User info dari DevTools
HAGO_USER_ID=12903446120
HAGO_INVITE_ID=258161887
HAGO_OWNER_ID=245862072

# Authentication
HAGO_AUTH_TOKEN=your_token_here

# Ping interval (detik)
PING_INTERVAL=30

# Logging
DEBUG=true
LOG_LEVEL=INFO
```

### Cara Ambil Data dari DevTools

1. Buka aplikasi Hago di browser
2. Buka DevTools (`F12` atau `Ctrl+Shift+I`)
3. Buka tab `Console`
4. Cari variable global yang berisi:
   - `APP_USER_INFO` → `uid`, `inviteId`, `ownerId`
   - `CUR_ROOM_INFO` → `roomId`, `roomToken`
   - `REQUEST_HOST` → API endpoint
5. Copy nilai yang diperlukan ke `.env`

## ▶️ Menjalankan

### Lokal

```bash
python -m app.main
```

Output:
```
2026-10-01 13:37:00 | INFO     | main                | Health endpoint: http://0.0.0.0:8080/health
2026-10-01 13:37:00 | INFO     | ping_service        | Ping service started
2026-10-01 13:37:00 | INFO     | ping_service        | Config: URL=https://..., Room=C_204..., Interval=30s
2026-10-01 13:37:01 | INFO     | ping_service        | Sending ping to https://... (attempt 1/3)
```

### Check Health

```bash
# Di terminal lain
curl http://localhost:8080/health | jq
```

Response:
```json
{
  "status": "ok",
  "total_pings": 5,
  "successful_pings": 5,
  "failed_pings": 0,
  "success_rate": "100.0%",
  "uptime_seconds": 150,
  "room_id": "C_20453632134829821442_V2_ID_0_ID",
  "ping_interval": 30
}
```

## 🌐 Deployment

Repo ini sudah siap deploy ke **Railway** atau **Render**.

### Deploy ke Railway

1. Buka https://railway.app
2. Login dengan GitHub
3. Klik **"New Project"** → **"Deploy from GitHub repo"**
4. Pilih `Muntaha12e/hago-auto-ping-bot`
5. Set environment variables di dashboard:
   - `HAGO_URL`
   - `HAGO_ROOM_ID`
   - `HAGO_ROOM_TOKEN`
   - `HAGO_USER_ID`
   - `HAGO_INVITE_ID`
   - `HAGO_OWNER_ID`
   - `HAGO_AUTH_TOKEN`
   - `PING_INTERVAL=30`
   - `MAX_RETRIES=3`
   - `DEBUG=false`

6. Railway akan auto-deploy dan bot jalan 24/7

### Deploy ke Render

1. Buka https://render.com
2. Login dengan GitHub
3. Klik **"Create +"** → **"Web Service"**
4. Pilih `Muntaha12e/hago-auto-ping-bot`
5. Render akan auto-read `render.yaml`
6. Set environment variables sesuai di atas
7. Deploy & monitor di logs

### Deploy via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Init & deploy
cd hago-auto-ping-bot
railway init
railway link
railway up

# Set env variables
railway variables set HAGO_URL=https://...
railway variables set HAGO_ROOM_ID=...
# ... variables lainnya

# Monitor logs
railway logs --tail
```

## 📊 Monitoring

### Health Endpoint

```bash
# Check status
curl https://your-app.up.railway.app/health

# Watch realtime
watch -n 5 'curl -s https://your-app.up.railway.app/health | jq'
```

### Metrics

- **Railway**: Dashboard → Metrics tab
- **Render**: Dashboard → Metrics tab

### Custom Monitoring (Optional)

Gunakan UptimeRobot atau Betterstack untuk monitor:
- Health endpoint setiap 5 menit
- Alert jika bot down

## 📁 Struktur Project

```
hago-auto-ping-bot/
├── README.md
├── DEPLOY.md
├── requirements.txt
├── .env.example
├── Dockerfile
├── Procfile
├── railway.json
├── render.yaml
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py         # Configuration management
│   ├── logger.py         # Logging setup
│   ├── health.py         # Health check server
│   ├── ping_service.py   # Main ping logic
│   └── main.py           # Entry point
├── tests/
│   └── test_ping_service.py
└── venv/
```

## 🔧 Troubleshooting

### Bot tidak jalan

```bash
# Check env variables
cat .env

# Check logs lokal
DEBUG=true LOG_LEVEL=DEBUG python -m app.main

# Check syntax
python -m py_compile app/*.py
```

### Crash terus-menerus

- **Memory tinggi**: Naikkan `PING_INTERVAL`
- **CPU tinggi**: Kurangi `MAX_RETRIES`
- **Network error**: Check `HAGO_URL` dan token masih valid
- **Timeout**: Naikkan `TIMEOUT` value

### Request rejected

- Token sudah expired → ambil token baru dari DevTools
- URL endpoint berubah → update `HAGO_URL`
- Rate limit → naikkan `PING_INTERVAL`

## 📝 Environment Variables

| Variable | Deskripsi | Required | Default |
|----------|-----------|----------|---------|
| `HAGO_URL` | Endpoint untuk ping | Ya | - |
| `HAGO_ROOM_ID` | Room ID | Ya | - |
| `HAGO_ROOM_TOKEN` | Room token | Tidak | "" |
| `HAGO_USER_ID` | User ID | Tidak | "" |
| `HAGO_INVITE_ID` | Invite ID | Tidak | "" |
| `HAGO_OWNER_ID` | Owner ID | Tidak | "" |
| `HAGO_AUTH_TOKEN` | Auth token | Tidak | "" |
| `PING_INTERVAL` | Interval (detik) | Tidak | 30 |
| `MAX_RETRIES` | Max retry | Tidak | 3 |
| `BACKOFF_FACTOR` | Retry backoff | Tidak | 2.0 |
| `TIMEOUT` | Request timeout (detik) | Tidak | 10 |
| `DEBUG` | Debug mode | Tidak | false |
| `LOG_LEVEL` | Log level | Tidak | INFO |
| `HEALTH_HOST` | Health server host | Tidak | 0.0.0.0 |
| `HEALTH_PORT` | Health server port | Tidak | 8080 |

## 📄 Lisensi

Educational project. Sesuaikan dengan kebijakan platform yang digunakan.

## ⚠️ Disclaimer

- Project ini untuk pembelajaran & research
- Gunakan sesuai ToS aplikasi target
- Penulis tidak bertanggung jawab atas penyalahgunaan
- Selalu backup token dan data sensitif

## 🔗 Resources

- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Python Requests Library](https://requests.readthedocs.io)

## 💬 Support

Ada pertanyaan atau issue? Buat issue di GitHub repo ini.

---

**Happy pinging!** 🤖✨
