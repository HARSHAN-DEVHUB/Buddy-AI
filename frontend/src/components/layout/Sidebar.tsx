import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  TrendingUp, 
  Bitcoin, 
  IndianRupee,
  Briefcase,
  BarChart3,
  Settings,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { useAppStore } from '@store/appStore';
import { cn } from '@utils/helpers';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Forex', href: '/forex', icon: TrendingUp },
  { name: 'Crypto', href: '/crypto', icon: Bitcoin },
  { name: 'Stocks', href: '/stocks', icon: IndianRupee },
  { name: 'Portfolio', href: '/portfolio', icon: Briefcase },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export default function Sidebar() {
  const location = useLocation();
  const { isSidebarOpen, toggleSidebar } = useAppStore();

  return (
    <>
      {/* Sidebar */}
      <aside
        className={cn(
          'relative flex h-screen flex-col border-r border-border bg-card transition-all duration-300',
          isSidebarOpen ? 'w-64' : 'w-20'
        )}
      >
        {/* Logo */}
        <div className="flex h-16 items-center justify-between border-b border-border px-6">
          {isSidebarOpen ? (
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold">
                B
              </div>
              <span className="text-lg font-bold">Buddy AI</span>
            </div>
          ) : (
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold mx-auto">
              B
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-3 py-4 overflow-y-auto scrollbar-thin">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all',
                  isActive
                    ? 'bg-primary text-primary-foreground shadow-sm'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
                  !isSidebarOpen && 'justify-center'
                )}
                title={!isSidebarOpen ? item.name : undefined}
              >
                <item.icon className="h-5 w-5 flex-shrink-0" />
                {isSidebarOpen && <span>{item.name}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Toggle Button */}
        <button
          onClick={toggleSidebar}
          className="absolute -right-3 top-20 z-10 flex h-6 w-6 items-center justify-center rounded-full border border-border bg-background shadow-md hover:bg-accent transition-colors"
          aria-label={isSidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
        >
          {isSidebarOpen ? (
            <ChevronLeft className="h-4 w-4" />
          ) : (
            <ChevronRight className="h-4 w-4" />
          )}
        </button>

        {/* Footer */}
        {isSidebarOpen && (
          <div className="border-t border-border p-4">
            <div className="text-xs text-muted-foreground">
              <p className="font-semibold">Buddy AI v1.0</p>
              <p className="mt-1">© 2025 HARSHAN-DEVHUB</p>
            </div>
          </div>
        )}
      </aside>
    </>
  );
}
