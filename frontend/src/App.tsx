import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect } from 'react';
import { Toaster } from 'sonner';
import { useAppStore } from '@store/appStore';
import { wsService } from '@services/websocket';

// Layout
import MainLayout from '@components/layout/MainLayout';

// Pages
import Dashboard from '@pages/Dashboard';
import ForexPage from '@pages/Forex';
import CryptoPage from '@pages/Crypto';
import StocksPage from '@pages/Stocks';
import PortfolioPage from '@pages/Portfolio';
import AnalyticsPage from '@pages/Analytics';
import SettingsPage from '@pages/Settings';

function App() {
  const { theme, setWebSocketConnected } = useAppStore();

  // Initialize theme
  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    
    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }
  }, [theme]);

  // Initialize WebSocket
  useEffect(() => {
    const initWebSocket = async () => {
      try {
        await wsService.connect();
        setWebSocketConnected(true);
      } catch (error) {
        console.error('Failed to connect to WebSocket:', error);
        setWebSocketConnected(false);
      }
    };

    initWebSocket();

    return () => {
      wsService.disconnect();
      setWebSocketConnected(false);
    };
  }, [setWebSocketConnected]);

  return (
    <Router>
      <div className="min-h-screen bg-background text-foreground">
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="forex" element={<ForexPage />} />
            <Route path="crypto" element={<CryptoPage />} />
            <Route path="stocks" element={<StocksPage />} />
            <Route path="portfolio" element={<PortfolioPage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Routes>
        <Toaster 
          position="top-right" 
          richColors 
          closeButton
          theme={theme === 'dark' ? 'dark' : 'light'}
        />
      </div>
    </Router>
  );
}

export default App;
