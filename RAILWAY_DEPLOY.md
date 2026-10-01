# Deploy ke Railway + Cloudflare DNS

## 🚀 Step 1: Deploy ke Railway (5 menit)

### 1.1 Buka Railway
- Kunjungi: https://railway.app
- Login dengan GitHub account kamu

### 1.2 Buat Project Baru
1. Klik **"New Project"**
2. Pilih **"Deploy from GitHub repo"**
3. Authorize Railway untuk akses GitHub
4. Cari & select: `Muntaha12e/hago-auto-ping-bot`
5. Railway akan auto-detect Dockerfile dan mulai deploy

### 1.3 Set Environment Variables
1. Di Railway dashboard, buka project `hago-auto-ping-bot`
2. Klik tab **"Variables"**
3. Tambahkan semua variable dari `.env.example`:

```
HAGO_URL=https://api.ihago.net/heartbeat
HAGO_ROOM_ID=C_20453632134829821442_V2_ID_0_ID
HAGO_ROOM_TOKEN=6Fc5x1mhrD6xHezGGBt83zHgPP_kgN6vFwNwfKDQcpa1pKw
HAGO_USER_ID=12903446120
HAGO_INVITE_ID=258161887
HAGO_OWNER_ID=245862072
HAGO_AUTH_TOKEN=your_token_here
PING_INTERVAL=30
MAX_RETRIES=3
BACKOFF_FACTOR=2.0
TIMEOUT=10
DEBUG=false
LOG_LEVEL=INFO
HEALTH_HOST=0.0.0.0
HEALTH_PORT=8080
```

### 1.4 Monitor Deployment
1. Klik tab **"Logs"** untuk lihat build & deploy progress
2. Tunggu sampai status jadi **"Running"** (warna hijau)
3. Railway akan assign domain otomatis, contoh: `hago-auto-ping-bot-production.up.railway.app`

✅ **Bot sudah jalan 24/7 di Railway!**

---

## 🌐 Step 2: Setup Cloudflare DNS (3 menit)

### 2.1 Copy Railway Domain
1. Di Railway dashboard → tab **"Settings"**
2. Scroll ke section **"Domains"**
3. Copy domain yang di-assign Railway, contoh:
   ```
   hago-auto-ping-bot-production.up.railway.app
   ```

### 2.2 Buka Cloudflare Dashboard
1. Login ke https://dash.cloudflare.com
2. Pilih domain kamu (misal: `mydomain.com`)
3. Klik tab **"DNS"** di sidebar kiri

### 2.3 Tambah CNAME Record
1. Klik **"Add record"**
2. Isi form:
   ```
   Type:    CNAME
   Name:    bot (atau nama lain yg kamu prefer)
   Content: hago-auto-ping-bot-production.up.railway.app
   TTL:     Auto
   Proxy:   Proxied (icon orange cloud)
   ```
3. Klik **"Save"**

### 2.4 Verifikasi DNS
Tunggu 1-2 menit, lalu test:

```bash
# Test DNS resolve
nslookup bot.mydomain.com

# Expected output:
# Address: xxx.xxx.xxx.xxx (Cloudflare IP)
```

✅ **Domain kamu sekarang pointing ke Railway!**

---

## ✅ Step 3: Verify Bot is Running

### 3.1 Test Health Endpoint
```bash
# Via Railway domain
curl https://hago-auto-ping-bot-production.up.railway.app/health | jq

# Via Cloudflare DNS (custom domain)
curl https://bot.mydomain.com/health | jq
```

Response harusnya:
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

### 3.2 Monitor Logs
**Via Railway:**
- Dashboard → Logs tab
- Lihat real-time logs

**Via CLI:**
```bash
npm install -g @railway/cli
railway login
railway logs --tail
```

---

## 🔧 Optional: Setup SSL/TLS di Cloudflare

1. Di Cloudflare dashboard → **"SSL/TLS"** tab
2. Pilih **"Full"** atau **"Full (strict)"**
3. Railway sudah provide SSL certificate, Cloudflare akan auto-match

✅ HTTPS siap untuk domain custom kamu!

---

## 📊 Monitoring & Maintenance

### Railway Metrics
1. Dashboard → **"Metrics"** tab
2. Monitor: CPU, Memory, Network usage
3. Set alert jika resource tinggi

### Custom Monitoring
```bash
# Watch health endpoint setiap 5 detik
watch -n 5 'curl -s https://bot.mydomain.com/health | jq'

# Or setup external monitoring (UptimeRobot)
# URL: https://bot.mydomain.com/health
# Check interval: 5 minutes
```

---

## 🆘 Troubleshooting

### Bot crash di Railway
```bash
# Check logs di Railway dashboard
# Error biasanya di:
# 1. Missing env variables
# 2. Invalid HAGO_URL
# 3. Token expired
```

### Domain tidak resolve
```bash
# Verify Cloudflare DNS
dig bot.mydomain.com +short

# Should return Cloudflare IP, then Railway IP
# If not, wait 5-10 minutes untuk DNS propagate
```

### SSL error
- Pastikan Cloudflare SSL mode: **"Full"**
- Railway provide SSL, Cloudflare proxy dengan SSL
- Error 525/526 berarti Railway SSL issue → contact Railway support

---

## 📝 Summary

| Komponen | URL | Status |
|----------|-----|--------|
| **Railway Service** | `hago-auto-ping-bot-production.up.railway.app` | Public |
| **Custom Domain (Cloudflare)** | `bot.mydomain.com` | Public via CNAME proxy |
| **Health Check** | `https://bot.mydomain.com/health` | 24/7 monitoring |
| **Bot Status** | Running 24/7 dengan auto-restart | ✅ Active |

---

## 🎯 Next Steps

1. ✅ Deploy ke Railway
2. ✅ Setup Cloudflare DNS
3. ✅ Verify health endpoint
4. ✅ Monitor logs
5. ✅ (Optional) Setup external monitoring
6. ✅ Done! Bot jalan 24/7

**Happy pinging!** 🤖✨
