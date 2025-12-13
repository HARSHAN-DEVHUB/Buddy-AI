"""
Frontend Integration Test
Tests if frontend can fetch real data from backend
"""
import requests
import json
from time import sleep

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3001"

def test_backend_endpoints():
    """Test all backend endpoints that frontend uses"""
    
    print("\n" + "="*70)
    print("FRONTEND-BACKEND INTEGRATION TEST")
    print("="*70)
    
    tests = {
        "Health Check": f"{BACKEND_URL}/health",
        "Crypto Price (BTC)": f"{BACKEND_URL}/api/market/price/crypto/BTCUSDT",
        "Crypto Overview": f"{BACKEND_URL}/api/market/overview/crypto",
        "Stock Price (AAPL)": f"{BACKEND_URL}/api/market/price/stock/AAPL",
        "Crypto History": f"{BACKEND_URL}/api/market/history/crypto/ETHUSDT?timeframe=1h&limit=50",
        "Technical Indicators": f"{BACKEND_URL}/api/market/indicators/crypto/BTCUSDT?timeframe=1h",
    }
    
    passed = 0
    failed = 0
    
    for name, url in tests.items():
        try:
            print(f"\n▶ Testing: {name}")
            print(f"  URL: {url}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Pretty print first 200 chars of response
                response_str = json.dumps(data, indent=2)
                if len(response_str) > 300:
                    response_str = response_str[:300] + "\n  ... (truncated)"
                
                print(f"  ✅ Status: {response.status_code}")
                print(f"  Response: {response_str}")
                passed += 1
            else:
                print(f"  ❌ Status: {response.status_code}")
                print(f"  Error: {response.text[:200]}")
                failed += 1
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*70)
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED! Frontend can now fetch real data from backend.")
        print(f"\n🌐 Open your browser to: {FRONTEND_URL}")
        print("   - Dashboard should show real crypto/stock prices")
        print("   - Charts should display actual market data")
        print("   - Technical indicators should be calculated from real data")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the backend logs.")
    
    return passed == len(tests)

def check_cors():
    """Check if CORS is properly configured"""
    print("\n" + "="*70)
    print("CORS CONFIGURATION CHECK")
    print("="*70)
    
    try:
        response = requests.options(
            f"{BACKEND_URL}/api/market/price/crypto/BTCUSDT",
            headers={
                'Origin': FRONTEND_URL,
                'Access-Control-Request-Method': 'GET',
            }
        )
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print(f"CORS Headers: {json.dumps(cors_headers, indent=2)}")
        
        if cors_headers.get('Access-Control-Allow-Origin'):
            print("✅ CORS is configured - Frontend can make requests to backend")
        else:
            print("⚠️  CORS headers not found - Frontend may have issues")
            
    except Exception as e:
        print(f"Error checking CORS: {e}")

if __name__ == "__main__":
    print("\n🚀 Starting Frontend Integration Tests...\n")
    sleep(1)
    
    success = test_backend_endpoints()
    check_cors()
    
    if success:
        print("\n" + "="*70)
        print("NEXT STEPS:")
        print("="*70)
        print("1. Open http://localhost:3001 in your browser")
        print("2. Navigate to Dashboard - check if real prices are displayed")
        print("3. Go to Crypto page - verify BTC, ETH prices are real")
        print("4. Check Stocks page - see if AAPL, TSLA prices are live")
        print("5. Look at charts - they should show actual market data")
        print("="*70)
