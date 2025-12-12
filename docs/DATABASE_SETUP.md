# Database Setup Documentation

## Overview
The Buddy AI backend uses PostgreSQL with TimescaleDB for efficient time-series data storage. This document outlines the database schema, setup process, and usage.

## Database Schema

### Tables

#### 1. **users**
User authentication and profile information
- `id` (Primary Key)
- `email` (Unique, Indexed)
- `username` (Unique, Indexed)
- `hashed_password`
- `full_name`
- `role` (Enum: USER, ADMIN, PREMIUM)
- `is_active`, `is_verified`
- `preferred_currency`, `preferred_theme`, `enable_notifications`
- `created_at`, `updated_at`, `last_login`

#### 2. **market_data**
Real-time market price data
- `id` (Primary Key)
- `symbol`, `market` (Enum: FOREX, CRYPTO, STOCK)
- `price`, `open_price`, `high`, `low`, `close`, `volume`
- `change_24h`, `change_percent_24h`
- `timestamp` (Indexed)
- Composite Index: `(symbol, market, timestamp)`

#### 3. **ohlcv_data**
Candlestick/OHLCV historical data
- `id` (Primary Key)
- `symbol`, `market`, `timeframe` (1m, 5m, 15m, 1h, 4h, 1d)
- `timestamp`, `open`, `high`, `low`, `close`, `volume`
- Unique Composite Index: `(symbol, market, timeframe, timestamp)`

#### 4. **predictions**
AI model predictions
- `id` (Primary Key)
- `user_id` (Foreign Key → users)
- `symbol`, `market`, `model` (Enum: TFT, LSTM, ENSEMBLE, PROPHET, MULTIMODAL)
- `current_price`, `predicted_price`, `direction` (Enum: BUY, SELL, HOLD, STRONG_BUY, STRONG_SELL)
- `confidence` (0.0 to 1.0)
- `target_price`, `stop_loss`, `take_profit`
- `timeframe`, `horizon_hours`
- `features_used` (JSON), `model_version`
- `actual_price`, `accuracy_score` (for backtesting)
- `created_at`, `prediction_for`, `evaluated_at`

#### 5. **watchlists**
User watchlists for symbols
- `id` (Primary Key)
- `user_id` (Foreign Key → users)
- `symbol`, `market`
- `notes`
- `created_at`

#### 6. **alerts**
Price and prediction alerts
- `id` (Primary Key)
- `user_id` (Foreign Key → users)
- `symbol`, `alert_type` (Enum: price, prediction, indicator)
- `condition` (Enum: above, below, cross)
- `target_value`
- `is_active`, `is_triggered`
- `message`
- `created_at`, `triggered_at`

#### 7. **positions**
Virtual trading positions
- `id` (Primary Key)
- `user_id` (Foreign Key → users)
- `symbol`, `market`, `side` (long/short)
- `entry_price`, `current_price`, `exit_price`
- `quantity`
- `pnl`, `pnl_percent`
- `is_open`
- `opened_at`, `closed_at`

## Setup Instructions

### 1. Start PostgreSQL
```bash
cd /workspaces/Buddy-AI
docker-compose up -d postgres
```

### 2. Verify Database Connection
```bash
docker exec buddy-ai-postgres pg_isready -U postgres
```

### 3. Run Migrations
```bash
cd backend
source ../.venv/bin/activate
alembic upgrade head
```

### 4. Verify Tables
```bash
docker exec buddy-ai-postgres psql -U postgres -d buddy_ai -c "\dt"
```

## Environment Variables

Create a `.env` file in `/backend` directory:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/buddy_ai
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

## Database Connection

### Python/SQLAlchemy
```python
from src.config.database import get_db
from sqlalchemy.orm import Session

def my_function(db: Session = Depends(get_db)):
    # Use db session
    pass
```

### Direct SQL
```python
from src.config.database import engine

with engine.connect() as conn:
    result = conn.execute("SELECT * FROM users")
```

## Creating Migrations

After modifying models in `src/models/`, create a new migration:

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Database Management Commands

### View Migration History
```bash
alembic history
```

### Downgrade Migration
```bash
alembic downgrade -1  # Rollback one migration
alembic downgrade base  # Rollback all
```

### Reset Database
```bash
# Drop all tables
docker exec buddy-ai-postgres psql -U postgres -d buddy_ai -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Recreate tables
alembic upgrade head
```

## Connection String Format

```
postgresql://[user]:[password]@[host]:[port]/[database]
```

- **Development**: `postgresql://postgres:postgres@localhost:5432/buddy_ai`
- **Docker**: `postgresql://postgres:postgres@postgres:5432/buddy_ai`

## TimescaleDB Features

The database uses TimescaleDB for enhanced time-series performance:

1. **Hypertables**: Automatically partition time-series data
2. **Compression**: Compress older data to save space
3. **Continuous Aggregates**: Pre-compute analytics
4. **Time-based Queries**: Optimized for time-range queries

To enable TimescaleDB features on `ohlcv_data` or `market_data`:

```sql
SELECT create_hypertable('ohlcv_data', 'timestamp');
```

## Best Practices

1. **Always use migrations** - Never manually modify database schema
2. **Index frequently queried columns** - Especially timestamp and symbol columns
3. **Use connection pooling** - Configured in `database.py`
4. **Close sessions properly** - Use `Depends(get_db)` dependency injection
5. **Validate data** - Use Pydantic models before inserting
6. **Backup regularly** - Especially before migrations in production

## Troubleshooting

### Connection Refused
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Start if not running
docker-compose up -d postgres
```

### Authentication Failed
- Verify credentials in `.env` match docker-compose.yml
- Default: `postgres:postgres`

### Table Already Exists
```bash
# Drop and recreate
alembic downgrade base
alembic upgrade head
```

### Migration Conflicts
```bash
# View current migration
alembic current

# Stamp to specific version
alembic stamp head
```

## Next Steps

1. Implement repository pattern for data access
2. Add database indexes for performance optimization
3. Set up database backups
4. Configure TimescaleDB hypertables
5. Implement caching layer with Redis
6. Add database health monitoring
