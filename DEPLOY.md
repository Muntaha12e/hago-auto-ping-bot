# Panduan Deploy ke Railway / Render

## Opsi 1: Deploy ke Railway ✅ (Recommended)

### Step 1: Setup Railway Account
1. Buka https://railway.app
2. Sign up / Login dengan GitHub
3. Authorize Railway untuk akses repo kamu

### Step 2: Deploy Repo
1. Klik **"New Project"**
2. Pilih **"Deploy from GitHub repo"**
3. Authorize GitHub dan pilih `Muntaha12e/hago-auto-ping-bot`
4. Railway akan auto-detect Dockerfile dan mulai deploy

### Step 3: Setup Environment Variables
Di Railway dashboard:
1. Buka project kamu
2. Klik tab **"Variables"**
3. Isi environment variables:

```
HAGO_URL=<URL_ENDPOINT_KAMU>
HAGO_ROOM_ID=<ROOM_ID_KAMU>
PING_INTERVAL=30
MAX_RETRIES=3
BACKOFF_FACTOR=2.0
TIMEOUT=10
DEBUG=false
LOG_LEVEL=INFO
HEALTH_HOST=0.0.0.0
HEALTH_PORT=8080
HAGO_AUTH_TOKEN=<TOKEN_JIKA_ADA>
```

### Step 4: Monitor
- Railway akan otomatis deploy
- Check logs di tab **"Logs"**
- Service berjalan 24/7 dengan auto-restart

---

## Opsi 2: Deploy ke Render.com

### Step 1: Setup Render Account
1. Buka https://render.com
2. Sign up / Login dengan GitHub
3. Authorize Render untuk akses repo kamu

### Step 2: Deploy via render.yaml
1. Klik **"Create +"** → **"Web Service"**
2. Pilih **"Build and deploy from a Git repository"**
3. Authorize GitHub dan pilih `Muntaha12e/hago-auto-ping-bot`
4. Render akan otomatis baca `render.yaml` dan deploy

### Step 3: Setup Environment Variables
Di Render dashboard:
1. Klik project kamu
2. Buka **"Environment"** tab
3. Tambahkan variables (bisa override dari render.yaml)

### Step 4: Monitor
- Check logs di tab **"Logs"**
- Auto-restart jika crash

---

## Opsi 3: Deploy Manual ke Railway via CLI

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login ke Railway
railway login

# 3. Init project
cd hago-auto-ping-bot
railway init

# 4. Connect ke GitHub repo
railway link

# 5. Deploy
railway up

# 6. Set variables
railway variables set HAGO_URL=<YOUR_URL>
railway variables set HAGO_ROOM_ID=<YOUR_ROOM_ID>
# ... variables lainnya

# 7. Monitor logs
railway logs
```

---

## Environment Variables Penting

| Variable | Deskripsi | Default | Contoh |
|----------|-----------|---------|--------|
| `HAGO_URL` | URL endpoint untuk ping | https://httpbin.org/post | https://api.hago.net/ping |
| `HAGO_ROOM_ID` | Room/session ID | demo-room | room-123 |
| `PING_INTERVAL` | Interval ping (detik) | 30 | 60 |
| `MAX_RETRIES` | Max retry attempts | 3 | 5 |
| `BACKOFF_FACTOR` | Exponential backoff | 2.0 | 1.5 |
| `TIMEOUT` | Request timeout (detik) | 10 | 15 |
| `DEBUG` | Debug mode | false | true |
| `LOG_LEVEL` | Logging level | INFO | DEBUG |
| `HEALTH_PORT` | Health check port | 8080 | 3000 |
| `HAGO_AUTH_TOKEN` | Auth token (opsional) | (kosong) | Bearer xxx |

---

## Verifikasi Deployment

### Health Check
```bash
curl https://<your-app-url>/health
```

Response success:
```json
{
  "status": "healthy",
  "uptime_seconds": 3600,
  "total_pings": 120,
  "successful_pings": 118,
  "failed_pings": 2,
  "success_rate": "98.3%"
}
```

### Check Logs
- **Railway**: Dashboard → Logs tab
- **Render**: Dashboard → Logs tab

---

## Troubleshooting

### Bot tidak jalan
- Check env variables di dashboard
- Verifikasi `HAGO_URL` benar
- Check logs untuk error details

### Crash terus-menerus
- Pastikan `HEALTH_PORT` tidak bentrok
- Check `PING_INTERVAL` (jangan terlalu cepat)
- Lihat error di logs

### Memory/CPU tinggi
- Naikkan `PING_INTERVAL` (lebih jarang ping)
- Kurangi `MAX_RETRIES`
- Check `TIMEOUT` setting

---

## Monitoring & Maintenance

### Railway Metrics
- Buka project → Overview
- Lihat CPU, Memory, Network usage

### Render Metrics
- Buka project → Metrics tab

### Custom Monitoring
```bash
# Curl health endpoint secara berkala
watch -n 5 'curl -s https://<your-app-url>/health | jq'
```

---

## Auto-restart & Uptime

- **Railway**: Auto-restart on crash, 99.9% uptime
- **Render**: Auto-restart, free tier dapat suspend jika idle

Untuk persistent uptime di free tier:
- Setup monitoring external (UptimeRobot, etc)
- Ping health endpoint setiap 5 menit dari service lain

---

## Next Steps

1. ✅ Push code ke GitHub
2. ✅ Setup Railway/Render account
3. ✅ Deploy & atur env variables
4. ✅ Test via health endpoint
5. ✅ Monitor logs
6. ✅ (Optional) Setup external monitoring

Sukses! 🚀
