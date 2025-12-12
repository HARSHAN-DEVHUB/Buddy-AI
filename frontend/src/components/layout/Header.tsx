import { Bell, Moon, Sun, Wifi, WifiOff } from 'lucide-react';
import { useAppStore } from '@store/appStore';
import { cn } from '@utils/helpers';

export default function Header() {
  const { 
    theme, 
    setTheme, 
    isWebSocketConnected,
    enableNotifications,
    toggleNotifications 
  } = useAppStore();

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b border-border bg-card px-6 backdrop-blur">
      {/* Left Section */}
      <div className="flex items-center gap-4">
        <div>
          <h1 className="text-lg font-semibold">Market Prediction Platform</h1>
          <p className="text-xs text-muted-foreground">
            Real-time AI-powered trading insights
          </p>
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-2">
        {/* WebSocket Status */}
        <div className="flex items-center gap-2 rounded-lg border border-border px-3 py-1.5">
          {isWebSocketConnected ? (
            <>
              <Wifi className="h-4 w-4 text-bullish" />
              <span className="text-xs font-medium text-bullish">Live</span>
            </>
          ) : (
            <>
              <WifiOff className="h-4 w-4 text-bearish" />
              <span className="text-xs font-medium text-bearish">Offline</span>
            </>
          )}
        </div>

        {/* Notifications */}
        <button
          onClick={toggleNotifications}
          className={cn(
            'flex h-9 w-9 items-center justify-center rounded-lg border border-border transition-colors',
            enableNotifications
              ? 'bg-primary text-primary-foreground'
              : 'hover:bg-accent'
          )}
          aria-label="Toggle notifications"
        >
          <Bell className="h-4 w-4" />
        </button>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-border hover:bg-accent transition-colors"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? (
            <Sun className="h-4 w-4" />
          ) : (
            <Moon className="h-4 w-4" />
          )}
        </button>

        {/* User Avatar */}
        <div className="ml-2 flex h-9 w-9 items-center justify-center rounded-full bg-primary text-primary-foreground font-semibold text-sm">
          HD
        </div>
      </div>
    </header>
  );
}
