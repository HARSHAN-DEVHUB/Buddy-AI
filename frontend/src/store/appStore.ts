import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { MarketType, TimeFrame, UserPreferences } from '@/types';

interface AppState {
  // Theme
  theme: 'light' | 'dark' | 'system';
  setTheme: (theme: 'light' | 'dark' | 'system') => void;

  // Market Selection
  selectedMarket: MarketType;
  setSelectedMarket: (market: MarketType) => void;

  // Timeframe
  selectedTimeframe: TimeFrame;
  setSelectedTimeframe: (timeframe: TimeFrame) => void;

  // Sidebar
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (isOpen: boolean) => void;

  // WebSocket Status
  isWebSocketConnected: boolean;
  setWebSocketConnected: (isConnected: boolean) => void;

  // User Preferences
  preferences: UserPreferences;
  updatePreferences: (preferences: Partial<UserPreferences>) => void;

  // Selected Symbol
  selectedSymbol: string | null;
  setSelectedSymbol: (symbol: string | null) => void;

  // Loading States
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;

  // Notifications
  enableNotifications: boolean;
  toggleNotifications: () => void;

  // Sound
  enableSound: boolean;
  toggleSound: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      // Theme
      theme: 'dark',
      setTheme: (theme) => set({ theme }),

      // Market Selection
      selectedMarket: 'forex',
      setSelectedMarket: (selectedMarket) => set({ selectedMarket }),

      // Timeframe
      selectedTimeframe: '1h',
      setSelectedTimeframe: (selectedTimeframe) => set({ selectedTimeframe }),

      // Sidebar
      isSidebarOpen: true,
      toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
      setSidebarOpen: (isSidebarOpen) => set({ isSidebarOpen }),

      // WebSocket Status
      isWebSocketConnected: false,
      setWebSocketConnected: (isWebSocketConnected) => set({ isWebSocketConnected }),

      // User Preferences
      preferences: {
        theme: 'dark',
        defaultMarket: 'forex',
        defaultTimeframe: '1h',
        enableNotifications: true,
        enableSound: false,
        chartType: 'candlestick',
        indicators: ['RSI', 'MACD', 'BB'],
        currency: 'USD',
      },
      updatePreferences: (newPreferences) =>
        set((state) => ({
          preferences: { ...state.preferences, ...newPreferences },
        })),

      // Selected Symbol
      selectedSymbol: null,
      setSelectedSymbol: (selectedSymbol) => set({ selectedSymbol }),

      // Loading States
      isLoading: false,
      setIsLoading: (isLoading) => set({ isLoading }),

      // Notifications
      enableNotifications: true,
      toggleNotifications: () =>
        set((state) => ({ enableNotifications: !state.enableNotifications })),

      // Sound
      enableSound: false,
      toggleSound: () => set((state) => ({ enableSound: !state.enableSound })),
    }),
    {
      name: 'buddy-ai-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        theme: state.theme,
        selectedMarket: state.selectedMarket,
        selectedTimeframe: state.selectedTimeframe,
        preferences: state.preferences,
        enableNotifications: state.enableNotifications,
        enableSound: state.enableSound,
        isSidebarOpen: state.isSidebarOpen,
      }),
    }
  )
);
