import { create } from 'zustand';
import type { WatchlistItem, Alert, Position } from '@/types';

interface PortfolioState {
  // Watchlist
  watchlist: WatchlistItem[];
  addToWatchlist: (item: Omit<WatchlistItem, 'id' | 'addedAt'>) => void;
  removeFromWatchlist: (id: string) => void;
  isInWatchlist: (symbol: string) => boolean;

  // Alerts
  alerts: Alert[];
  addAlert: (alert: Omit<Alert, 'id' | 'createdAt'>) => void;
  removeAlert: (id: string) => void;
  updateAlert: (id: string, updates: Partial<Alert>) => void;
  getActiveAlerts: () => Alert[];

  // Positions (for tracking virtual positions)
  positions: Position[];
  addPosition: (position: Omit<Position, 'id' | 'openedAt'>) => void;
  removePosition: (id: string) => void;
  updatePosition: (id: string, updates: Partial<Position>) => void;
  getTotalPnL: () => number;
}

export const usePortfolioStore = create<PortfolioState>((set, get) => ({
  // Watchlist
  watchlist: [],
  addToWatchlist: (item) =>
    set((state) => ({
      watchlist: [
        ...state.watchlist,
        {
          ...item,
          id: crypto.randomUUID(),
          addedAt: Date.now(),
        },
      ],
    })),
  removeFromWatchlist: (id) =>
    set((state) => ({
      watchlist: state.watchlist.filter((item) => item.id !== id),
    })),
  isInWatchlist: (symbol) => {
    const { watchlist } = get();
    return watchlist.some((item) => item.symbol === symbol);
  },

  // Alerts
  alerts: [],
  addAlert: (alert) =>
    set((state) => ({
      alerts: [
        ...state.alerts,
        {
          ...alert,
          id: crypto.randomUUID(),
          createdAt: Date.now(),
        },
      ],
    })),
  removeAlert: (id) =>
    set((state) => ({
      alerts: state.alerts.filter((alert) => alert.id !== id),
    })),
  updateAlert: (id, updates) =>
    set((state) => ({
      alerts: state.alerts.map((alert) =>
        alert.id === id ? { ...alert, ...updates } : alert
      ),
    })),
  getActiveAlerts: () => {
    const { alerts } = get();
    return alerts.filter((alert) => alert.isActive);
  },

  // Positions
  positions: [],
  addPosition: (position) =>
    set((state) => ({
      positions: [
        ...state.positions,
        {
          ...position,
          id: crypto.randomUUID(),
          openedAt: Date.now(),
        },
      ],
    })),
  removePosition: (id) =>
    set((state) => ({
      positions: state.positions.filter((position) => position.id !== id),
    })),
  updatePosition: (id, updates) =>
    set((state) => ({
      positions: state.positions.map((position) =>
        position.id === id ? { ...position, ...updates } : position
      ),
    })),
  getTotalPnL: () => {
    const { positions } = get();
    return positions.reduce((total, position) => total + position.pnl, 0);
  },
}));
