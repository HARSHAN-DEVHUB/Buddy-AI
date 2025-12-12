import { Outlet } from 'react-router-dom';
import { useEffect } from 'react';
import Sidebar from './Sidebar.tsx';
import Header from './Header.tsx';
import { useWebSocket } from '@hooks/useMarket';

export default function MainLayout() {
  // const { isSidebarOpen } = useAppStore();
  const { isConnected } = useWebSocket();

  useEffect(() => {
    // Any layout-level initialization
    console.log('MainLayout mounted');
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <Header />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto bg-background p-4 md:p-6 lg:p-8">
          <div className="mx-auto max-w-[1920px]">
            <Outlet />
          </div>
        </main>

        {/* WebSocket Status Indicator */}
        {!isConnected && (
          <div className="fixed bottom-4 right-4 z-50">
            <div className="glass rounded-lg px-4 py-2 shadow-lg">
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-bearish animate-pulse" />
                <span className="text-sm text-muted-foreground">
                  Reconnecting...
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
