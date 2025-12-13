# Buddy AI - Quick Start Guide

## 🚀 One-Command Startup

```bash
./start.sh
```

That's it! The entire platform will start automatically.

---

## 📋 What You Need

1. **Docker** - For PostgreSQL database
2. **Python 3.10+** - For backend
3. **Node.js 18+** - For frontend

---

## ⚡ Quick Commands

```bash
# Start everything
./start.sh

# Check status
./status.sh

# Stop everything
./stop.sh

# View backend logs
tail -f logs/backend.log

# View frontend logs
tail -f logs/frontend.log
```

---

## 🌐 Access URLs

After running `./start.sh`:

- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🔧 Manual Startup (Optional)

If you prefer manual control:

```bash
# 1. Start database
docker-compose up -d postgres

# 2. Run migrations
cd backend
source ../.venv/bin/activate
pip install -r requirements.txt
alembic upgrade head

# 3. Start backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 4. Start frontend (in new terminal)
cd frontend
npm install
npm run dev
```

---

## ✅ Verify It's Working

Run this to test:

```bash
# Check health
curl http://localhost:8000/health

# Get Bitcoin price
curl http://localhost:8000/api/market/price/crypto/BTCUSDT

# Check status
./status.sh
```

---

## 🛑 Troubleshooting

**"Port already in use" error:**
```bash
./stop.sh
./start.sh
```

**Database connection error:**
```bash
docker-compose down
docker-compose up -d postgres
sleep 10
cd backend && alembic upgrade head
```

**Frontend won't start:**
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

---

## 📚 What's Next?

Once everything is running:
1. Open http://localhost:3001
2. Check Dashboard for live crypto/stock prices
3. Explore Crypto and Stocks pages
4. Ready for Phase 2 (ML models & trading)!

---

## 🎯 Current Features

✅ Live crypto prices (Binance)  
✅ Live stock prices (Yahoo Finance)  
✅ Technical indicators (RSI, MACD, etc.)  
✅ Historical charts  
✅ Market overviews  

**Coming in Phase 2:**
- ML price predictions
- Trading signals
- MT5/Exness integration
- Binance trading
- Automated trading

---

Need help? Check the logs or run `./status.sh`
