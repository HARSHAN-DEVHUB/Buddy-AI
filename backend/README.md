# Backend API Quick Start

## Setup Complete! ✅

The PostgreSQL database is now running with all tables created.

### Current Status

- **Database**: PostgreSQL with TimescaleDB (Running)
- **Tables Created**: 8 tables (users, market_data, ohlcv_data, predictions, watchlists, alerts, positions, alembic_version)
- **API Server**: Running on http://0.0.0.0:8000
- **Migrations**: Up to date

### Quick Test

Test the API and database connection:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### API Endpoints

- `GET /` - API info
- `GET /health` - Health check with database connection test
- `GET /api/market/price/{market}/{symbol}` - Get price (placeholder)
- `GET /api/market/overview/{market}` - Get market overview (placeholder)
- `POST /api/prediction/predict` - Create prediction (placeholder)

### API Documentation

Interactive API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database Access

**Connect to PostgreSQL:**
```bash
docker exec -it buddy-ai-postgres psql -U postgres -d buddy_ai
```

**View tables:**
```sql
\dt
```

**Query example:**
```sql
SELECT * FROM users LIMIT 10;
```

### Next Development Steps

1. **Implement Authentication**
   - User registration endpoint
   - Login with JWT tokens
   - Password hashing with bcrypt
   - Protected routes

2. **Market Data Integration**
   - Connect to real-time data sources (Binance, Alpha Vantage, MT5)
   - Store market data in database
   - Implement WebSocket for live updates

3. **AI Model Integration**
   - Load trained ML models
   - Create prediction endpoints
   - Store predictions in database

4. **Repository Layer**
   - Create data access layer
   - Implement CRUD operations for all models
   - Add business logic

5. **Background Tasks**
   - Set up Celery for async tasks
   - Schedule data fetching
   - Prediction generation

### File Structure

```
backend/
├── alembic/                    # Database migrations
│   └── versions/              # Migration files
├── src/
│   ├── api/
│   │   ├── main.py           # FastAPI app ✅
│   │   └── routes/           # API routes (TODO)
│   ├── config/
│   │   └── database.py       # DB config ✅
│   ├── models/               # SQLAlchemy models ✅
│   │   ├── user.py
│   │   ├── market.py
│   │   ├── prediction.py
│   │   └── watchlist.py
│   ├── services/             # Business logic (TODO)
│   └── utils/                # Helpers (TODO)
├── .env                      # Environment variables ✅
├── .env.example             # Example env file ✅
├── alembic.ini              # Alembic config ✅
└── requirements.txt         # Python packages ✅
```

### Environment Variables

`.env` file created with:
- `DATABASE_URL` - PostgreSQL connection
- `SECRET_KEY` - JWT secret (change in production!)
- `CORS_ORIGINS` - Allowed origins
- API keys placeholders (Binance, Alpha Vantage, MT5)

### Useful Commands

**Start backend:**
```bash
cd backend
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Create migration:**
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

**Stop database:**
```bash
docker-compose stop postgres
```

**View logs:**
```bash
docker logs buddy-ai-postgres
```

### Database Models Summary

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| User | Authentication | email, username, role |
| MarketData | Real-time prices | symbol, market, price, timestamp |
| OHLCV | Candlestick data | symbol, timeframe, open/high/low/close |
| Prediction | AI predictions | symbol, predicted_price, confidence |
| Watchlist | User watchlists | user_id, symbol, market |
| Alert | Price alerts | user_id, symbol, condition, target_value |
| Position | Virtual trading | user_id, symbol, entry_price, pnl |

### Dependencies Installed

✅ FastAPI & Uvicorn  
✅ SQLAlchemy & PostgreSQL driver  
✅ Alembic (migrations)  
✅ Pydantic (validation)  
✅ python-dotenv (environment)  

### Resources

- Full DB Documentation: `/docs/DATABASE_SETUP.md`
- Frontend: `/frontend`
- Docker Compose: `/docker-compose.yml`

---

**Ready to build! The database foundation is set up and the API server is running.**
