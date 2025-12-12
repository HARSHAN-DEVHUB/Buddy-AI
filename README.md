# Buddy AI – AI-Powered Market Prediction Platform

**Buddy AI** is a 100% **FREE** machine learning platform for predicting price movements in Forex, Cryptocurrency, and Indian Stock markets. Built with advanced AI models and integrated with your trading platforms (MT5/Exness, Binance, and Groww alternative data sources), Buddy AI helps traders make data-driven decisions.

> ⚠️ **Disclaimer:** Predictions are for educational purposes only. No model guarantees 100% accuracy. Markets are influenced by unpredictable events. Always conduct your own research and manage risk appropriately.

---

## 🎯 Features

- **Multi-Market Predictions**
  - 📊 **Forex**: XAUUSD, EURUSD, GBPUSD, USDJPY (via MT5/Exness)
  - 💰 **Crypto**: Bitcoin, Ethereum, BNB, and more (via Binance)
  - 🇮🇳 **Indian Stocks**: NIFTY 50, NSE/BSE stocks (via NSEpy/Yahoo Finance)

- **Advanced AI Models**
  - Temporal Fusion Transformers (TFT)
  - LSTM & GRU Networks
  - Ensemble Methods (Random Forest + Gradient Boosting)
  - Facebook Prophet for time-series forecasting
  - Multi-modal prediction (Price + Sentiment + Order Flow)

- **Real-Time Data**
  - Live price feeds from MT5, Binance API
  - Technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
  - Volume analysis and market microstructure
  - Historical data for backtesting

- **100% Free**
  - No API costs or subscriptions
  - Open-source libraries only
  - Free data sources
  - Free hosting options (Google Colab, Render, Vercel)

---

## 🛠️ Tech Stack

### **Backend**
| Technology | Purpose | Cost |
|------------|---------|------|
| **Python 3.10+** | Core language | FREE |
| **FastAPI** | REST API framework | FREE |
| **PyTorch** | Deep learning models | FREE |
| **scikit-learn** | Machine learning algorithms | FREE |
| **Prophet** | Time-series forecasting | FREE |
| **pandas/numpy** | Data manipulation | FREE |
| **MetaTrader5** | MT5/Exness integration | FREE |
| **python-binance** | Binance API client | FREE |
| **nsepy** | Indian stocks data | FREE |
| **yfinance** | Yahoo Finance data | FREE |

### **Frontend**
| Technology | Purpose | Cost |
|------------|---------|------|
| **React 18** | UI framework | FREE |
| **TypeScript** | Type safety | FREE |
| **TradingView Charts** | Professional charting | FREE |
| **Plotly** | Interactive visualizations | FREE |
| **Tailwind CSS** | Styling | FREE |
| **shadcn/ui** | UI components | FREE |

### **Data & Storage**
| Service | Purpose | Cost |
|---------|---------|------|
| **MongoDB Atlas** | Database (512MB) | FREE |
| **PostgreSQL (Supabase)** | Alternative DB | FREE |
| **Redis (Upstash)** | Caching | FREE |

### **Deployment**
| Platform | Purpose | Cost |
|----------|---------|------|
| **Google Colab** | Model training (GPU) | FREE |
| **Kaggle Notebooks** | GPU compute (30hrs/week) | FREE |
| **Render** | Backend hosting | FREE |
| **Vercel/Netlify** | Frontend hosting | FREE |
| **GitHub Pages** | Static hosting | FREE |

---

## 📁 Project Structure

```
Buddy-AI/
│
├── backend/
│   ├── src/
│   │   ├── services/
│   │   │   ├── mt5_service.py          # MT5/Exness integration
│   │   │   ├── binance_service.py      # Binance crypto data
│   │   │   ├── stocks_service.py       # Indian stocks (NSEpy)
│   │   │   ├── prediction_service.py   # AI prediction engine
│   │   │   └── technical_indicators.py # TA calculations
│   │   ├── models/
│   │   │   ├── tft_model.py           # Temporal Fusion Transformer
│   │   │   ├── lstm_model.py          # LSTM networks
│   │   │   ├── ensemble_model.py      # Ensemble predictions
│   │   │   └── prophet_model.py       # Facebook Prophet
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── forex.py           # Forex endpoints
│   │   │   │   ├── crypto.py          # Crypto endpoints
│   │   │   │   └── stocks.py          # Stocks endpoints
│   │   │   └── main.py                # FastAPI app
│   │   ├── utils/
│   │   │   ├── data_fetcher.py        # Data collection
│   │   │   ├── feature_engineering.py # Feature creation
│   │   │   └── validators.py          # Input validation
│   │   └── config/
│   │       ├── settings.py            # App configuration
│   │       └── credentials.py         # API credentials
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx          # Main dashboard
│   │   │   ├── TradingChart.tsx       # Price charts
│   │   │   ├── PredictionCard.tsx     # Prediction display
│   │   │   ├── MarketOverview.tsx     # Market summary
│   │   │   └── TechnicalIndicators.tsx # Indicator charts
│   │   ├── pages/
│   │   │   ├── Forex.tsx              # Forex predictions
│   │   │   ├── Crypto.tsx             # Crypto predictions
│   │   │   ├── Stocks.tsx             # Stock predictions
│   │   │   └── Portfolio.tsx          # Watchlist
│   │   ├── services/
│   │   │   ├── api.ts                 # API client
│   │   │   └── websocket.ts           # Real-time updates
│   │   ├── hooks/
│   │   │   ├── useRealTimePrice.ts    # Live price hook
│   │   │   └── usePrediction.ts       # Prediction hook
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   └── tailwind.config.js
│
├── notebooks/
│   ├── data_exploration.ipynb         # EDA
│   ├── model_training.ipynb           # Train models
│   └── backtesting.ipynb              # Strategy testing
│
├── scripts/
│   ├── setup.sh                       # Initial setup
│   ├── train_model.py                 # Model training
│   └── backtest.py                    # Backtesting
│
├── data/
│   ├── raw/                           # Raw market data
│   ├── processed/                     # Cleaned data
│   └── models/                        # Trained models
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm
- Git
- MT5 account (Exness) - Optional for forex
- Binance account - Optional for crypto

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/HARSHAN-DEVHUB/Buddy-AI.git
cd Buddy-AI
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
```

#### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

#### 4. Configuration

Create a `.env` file in the root directory:

```env
# MT5/Exness Configuration (Optional)
MT5_ACCOUNT=your_account_number
MT5_PASSWORD=your_password
MT5_SERVER=Exness-MT5Real

# Binance API (Optional - Leave empty for public data)
BINANCE_API_KEY=
BINANCE_API_SECRET=

# Database
MONGODB_URI=mongodb://localhost:27017/buddy-ai
# Or use MongoDB Atlas free tier
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/buddy-ai

# Redis (Optional for caching)
REDIS_URL=redis://localhost:6379

# App Settings
DEBUG=True
API_PORT=8000
FRONTEND_PORT=3000
```

#### 5. Run the Application

**Start Backend:**
```bash
cd backend
uvicorn src.api.main:app --reload --port 8000
```

**Start Frontend:**
```bash
cd frontend
npm run dev
```

Access the application at `http://localhost:3000`

---

## 📊 Platform Integrations

### MT5/Exness (Forex)

```python
from services.mt5_service import MT5Service

# Initialize MT5
mt5 = MT5Service()
mt5.connect(
    account=12345678,
    password="your_password",
    server="Exness-MT5Real"
)

# Get forex data
data = mt5.get_forex_data("XAUUSD", timeframe="H1", bars=500)

# Get live price
price = mt5.get_live_price("EURUSD")
print(f"EUR/USD: {price['bid']} / {price['ask']}")
```

### Binance (Cryptocurrency)

```python
from services.binance_service import BinanceService

# Initialize (no keys needed for public data)
binance = BinanceService()

# Get crypto data
data = binance.get_crypto_data("BTCUSDT", interval="1h", limit=500)

# Get live price
price = binance.get_live_price("ETHUSDT")
print(f"ETH: ${price['price']}")

# Get top gainers
gainers = binance.get_top_gainers(limit=10)
```

### Indian Stocks (NSE/BSE)

```python
from services.stocks_service import IndianStocksService

# Initialize
stocks = IndianStocksService()

# Get NSE stock data
data = stocks.get_nse_data("RELIANCE", days=365)

# Get live price
price = stocks.get_live_nse_price("TCS")
print(f"TCS: ₹{price['price']}")

# Get NIFTY 50 stocks
nifty_stocks = stocks.get_nifty_50_stocks()
```

---

## 🤖 AI Models & Techniques

### Available Models

1. **Temporal Fusion Transformer (TFT)**
   - Multi-horizon forecasting
   - Attention mechanisms
   - Uncertainty quantification

2. **LSTM Networks**
   - Time-series patterns
   - Long-term dependencies
   - Sequence prediction

3. **Ensemble Methods**
   - Random Forest
   - Gradient Boosting
   - XGBoost

4. **Facebook Prophet**
   - Trend decomposition
   - Seasonality detection
   - Holiday effects

5. **Multi-Modal Predictor**
   - Price data (CNN)
   - Sentiment analysis
   - Order flow

### Making Predictions

```python
from services.prediction_service import PredictionService

predictor = PredictionService()

# Predict forex
forex_pred = predictor.predict_forex("XAUUSD", horizon=24)
print(f"XAUUSD Prediction: {forex_pred['predicted_price']}")

# Predict crypto
crypto_pred = predictor.predict_crypto("BTCUSDT", horizon=24)
print(f"BTC Prediction: ${crypto_pred['predicted_price']}")

# Predict stock
stock_pred = predictor.predict_stock("RELIANCE", horizon=5)
print(f"Reliance Prediction: ₹{stock_pred['predicted_price']}")
```

---

## 📈 Technical Indicators

Buddy AI includes 50+ free technical indicators:

- **Trend**: SMA, EMA, MACD, ADX
- **Momentum**: RSI, Stochastic, CCI, Williams %R
- **Volatility**: Bollinger Bands, ATR, Keltner Channels
- **Volume**: OBV, CMF, VWAP
- **Custom**: Smart Money Concepts, Order Flow

```python
from utils.technical_indicators import TechnicalIndicators

ti = TechnicalIndicators(data)

# Add all indicators
data_with_indicators = ti.add_all_indicators()

# Or add specific ones
ti.add_rsi(period=14)
ti.add_macd(fast=12, slow=26, signal=9)
ti.add_bollinger_bands(period=20, std=2)
```

---

## 🧪 Model Training & Backtesting

### Train Custom Models

```bash
# Train TFT model
python scripts/train_model.py --model tft --symbol XAUUSD --epochs 100

# Train ensemble
python scripts/train_model.py --model ensemble --symbol BTCUSDT --epochs 50
```

### Backtest Strategies

```bash
# Backtest predictions
python scripts/backtest.py --symbol EURUSD --start 2024-01-01 --end 2024-12-31
```

### Use Google Colab for GPU Training

1. Upload `notebooks/model_training.ipynb` to Google Colab
2. Enable GPU: Runtime → Change runtime type → GPU
3. Run cells to train models with free GPU

---

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access:
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## 🌐 Free Hosting Options

### Backend (API)

**Render** (Free Tier):
```bash
# Deploy to Render
git push origin main
# Connect GitHub repo to Render dashboard
```

**Railway** (Free $5/month credit):
```bash
railway login
railway init
railway up
```

### Frontend

**Vercel**:
```bash
cd frontend
vercel login
vercel --prod
```

**Netlify**:
```bash
cd frontend
npm run build
netlify deploy --prod
```

---

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

```
GET  /api/forex/price/{symbol}           # Live forex price
POST /api/forex/predict                  # Forex prediction
GET  /api/crypto/price/{symbol}          # Live crypto price
POST /api/crypto/predict                 # Crypto prediction
GET  /api/stocks/price/{symbol}          # Live stock price
POST /api/stocks/predict                 # Stock prediction
GET  /api/indicators/{symbol}            # Technical indicators
```

---

## 🔒 Security Best Practices

- Never commit `.env` file with credentials
- Use environment variables for all secrets
- Enable 2FA on MT5, Binance, and GitHub
- Rotate API keys regularly
- Use read-only API keys when possible

---

## 🐛 Troubleshooting

### MT5 Connection Issues

```python
# Check if MT5 is installed
import MetaTrader5 as mt5
print(mt5.__version__)

# Verify server name (common issue)
# Exness servers: "Exness-MT5Real", "Exness-MT5Demo"
```

### Binance Rate Limits

```python
# Use free public endpoints (no auth)
# Limited to 1200 requests/minute
# Add delays between requests if needed
import time
time.sleep(0.1)
```

### Indian Stocks Data Issues

```python
# NSEpy might fail, fallback to Yahoo Finance
# Add .NS for NSE or .BO for BSE
# Example: "RELIANCE.NS" or "RELIANCE.BO"
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Risk Disclaimer

**IMPORTANT**: This software is for educational and research purposes only.

- Trading forex, crypto, and stocks involves substantial risk of loss
- Past performance does not guarantee future results
- No prediction model is 100% accurate
- Always do your own research (DYOR)
- Never invest more than you can afford to lose
- Consider seeking advice from licensed financial advisors
- The developers are not responsible for any financial losses

---

## 🙏 Acknowledgments

- **MetaTrader 5** - Forex trading platform
- **Binance** - Cryptocurrency exchange
- **NSE India** - Stock market data
- **Facebook Prophet** - Time-series forecasting
- **PyTorch** - Deep learning framework
- **scikit-learn** - Machine learning library

---

## 📧 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/HARSHAN-DEVHUB/Buddy-AI/issues)
- **Developer**: HARSHAN-DEVHUB
- **Repository**: https://github.com/HARSHAN-DEVHUB/Buddy-AI

---

## 🎯 Roadmap

- [ ] Real-time WebSocket price feeds
- [ ] Mobile app (React Native)
- [ ] Automated trading signals (Telegram bot)
- [ ] Advanced sentiment analysis (FinBERT)
- [ ] Options flow analysis
- [ ] Portfolio optimization
- [ ] Risk management tools
- [ ] Multi-timeframe analysis
- [ ] Custom indicator builder
- [ ] Social trading features

---

## 💰 100% Free Forever

This project uses only free and open-source tools:
- ✅ No subscription fees
- ✅ No API costs (public endpoints)
- ✅ No hidden charges
- ✅ Free hosting options
- ✅ Free GPU training (Google Colab)
- ✅ Free data sources

**Total Cost: $0.00** 🎉

---

Made with ❤️ for traders, by traders.

**Happy Trading! 📈💰**
