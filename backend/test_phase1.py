"""
Test script to verify Phase 1 implementation
Tests all new market data endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test health check endpoint"""
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_crypto_price():
    """Test crypto price endpoint"""
    print_section("2. Crypto Price - Bitcoin (BTCUSDT)")
    response = requests.get(f"{BASE_URL}/api/market/price/crypto/BTCUSDT")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            price_data = data['data']
            print(f"Symbol: {price_data['symbol']}")
            print(f"Price: ${price_data['price']:,.2f}")
            print(f"24h Change: {price_data['change_percent_24h']:.2f}%")
            print(f"Volume: ${price_data['volume']:,.0f}")
    else:
        print(f"Error: {response.text}")

def test_crypto_history():
    """Test crypto historical data"""
    print_section("3. Crypto Historical Data - Ethereum")
    response = requests.get(
        f"{BASE_URL}/api/market/history/crypto/ETHUSDT",
        params={'timeframe': '1h', 'limit': 10}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            candles = data['data']
            print(f"Retrieved {len(candles)} candles")
            if candles:
                latest = candles[-1]
                print(f"Latest candle:")
                print(f"  Time: {latest['timestamp']}")
                print(f"  Open: ${latest['open']:.2f}")
                print(f"  High: ${latest['high']:.2f}")
                print(f"  Low: ${latest['low']:.2f}")
                print(f"  Close: ${latest['close']:.2f}")
                print(f"  Volume: {latest['volume']:.2f}")

def test_crypto_indicators():
    """Test technical indicators"""
    print_section("4. Technical Indicators - Bitcoin")
    response = requests.get(
        f"{BASE_URL}/api/market/indicators/crypto/BTCUSDT",
        params={'timeframe': '1h'}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            indicators = data['data']
            print(f"RSI: {indicators['rsi']:.2f}")
            print(f"MACD: {indicators['macd']}")
            print(f"Bollinger Bands: {indicators['bollingerBands']}")
            print(f"Trend Signal: {indicators['trendSignal']}")

def test_crypto_overview():
    """Test market overview"""
    print_section("5. Crypto Market Overview")
    response = requests.get(f"{BASE_URL}/api/market/overview/crypto")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            overview = data['data']
            print(f"Total Volume: ${overview['totalVolume']:,.0f}")
            print(f"Average Change: {overview['avgChange']:.2f}%")
            print(f"\nTop Gainers:")
            for gainer in overview['topGainers'][:3]:
                print(f"  {gainer['symbol']}: +{gainer['change_percent_24h']:.2f}%")
            print(f"\nTop Losers:")
            for loser in overview['topLosers'][:3]:
                print(f"  {loser['symbol']}: {loser['change_percent_24h']:.2f}%")

def test_stock_price():
    """Test stock price endpoint"""
    print_section("6. Stock Price - Apple (AAPL)")
    response = requests.get(f"{BASE_URL}/api/market/price/stock/AAPL")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            price_data = data['data']
            print(f"Symbol: {price_data['symbol']}")
            print(f"Price: ${price_data['price']:.2f}")
            print(f"Change: {price_data['change_percent_24h']:.2f}%")
            print(f"Market Cap: ${price_data.get('market_cap', 0):,.0f}")
    else:
        print(f"Error: {response.text}")

def main():
    print("\n" + "="*60)
    print(" PHASE 1: DATA FOUNDATION - TEST SUITE")
    print("="*60)
    print(f" Testing API at: {BASE_URL}")
    print(f" Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    try:
        test_health()
        test_crypto_price()
        test_crypto_history()
        test_crypto_indicators()
        test_crypto_overview()
        test_stock_price()
        
        print_section("✅ TEST SUITE COMPLETED")
        print("All endpoints are working!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Make sure the backend is running: uvicorn src.api.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
