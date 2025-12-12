// Market Types
export type MarketType = 'forex' | 'crypto' | 'stock';
export type TimeFrame = '1m' | '5m' | '15m' | '30m' | '1h' | '4h' | '1d' | '1w';
export type PredictionDirection = 'BUY' | 'SELL' | 'HOLD' | 'STRONG_BUY' | 'STRONG_SELL';

// Price Data
export interface OHLCV {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface TickData {
  symbol: string;
  bid: number;
  ask: number;
  last: number;
  volume: number;
  timestamp: number;
  spread: number;
}

// Prediction Types
export interface Prediction {
  id: string;
  symbol: string;
  market: MarketType;
  currentPrice: number;
  predictedPrice: number;
  direction: PredictionDirection;
  confidence: number;
  targetPrice: number;
  stopLoss: number;
  takeProfit: number;
  timeframe: TimeFrame;
  horizon: number; // hours
  timestamp: number;
  accuracy?: number;
  model: ModelType;
}

export type ModelType = 'TFT' | 'LSTM' | 'ENSEMBLE' | 'PROPHET' | 'MULTIMODAL';

export interface PredictionRequest {
  symbol: string;
  market: MarketType;
  timeframe: TimeFrame;
  horizon: number;
  models?: ModelType[];
}

// Technical Indicators
export interface TechnicalIndicators {
  rsi: number;
  macd: {
    value: number;
    signal: number;
    histogram: number;
  };
  bollingerBands: {
    upper: number;
    middle: number;
    lower: number;
  };
  ema: {
    ema12: number;
    ema26: number;
    ema50: number;
    ema200: number;
  };
  sma: {
    sma20: number;
    sma50: number;
    sma200: number;
  };
  stochastic: {
    k: number;
    d: number;
  };
  atr: number;
  adx: number;
  vwap: number;
  obv: number;
}

// Market Data
export interface MarketData {
  symbol: string;
  market: MarketType;
  price: number;
  change24h: number;
  changePercent24h: number;
  high24h: number;
  low24h: number;
  volume24h: number;
  marketCap?: number;
  lastUpdate: number;
}

export interface OrderBookLevel {
  price: number;
  quantity: number;
  total: number;
}

export interface OrderBook {
  symbol: string;
  bids: OrderBookLevel[];
  asks: OrderBookLevel[];
  timestamp: number;
}

// Chart Data
export interface CandlestickData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
}

export interface ChartIndicator {
  name: string;
  type: 'line' | 'histogram' | 'area';
  color: string;
  data: Array<{ time: number; value: number }>;
}

// WebSocket Types
export interface WebSocketMessage<T = unknown> {
  type: 'price' | 'prediction' | 'indicator' | 'alert' | 'orderbook';
  data: T;
  timestamp: number;
}

export interface PriceUpdate {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
}

// Alert Types
export interface Alert {
  id: string;
  symbol: string;
  type: 'price' | 'prediction' | 'indicator';
  condition: 'above' | 'below' | 'cross';
  value: number;
  isActive: boolean;
  createdAt: number;
  triggeredAt?: number;
}

// Portfolio/Watchlist
export interface WatchlistItem {
  id: string;
  symbol: string;
  market: MarketType;
  addedAt: number;
  notes?: string;
}

export interface Position {
  id: string;
  symbol: string;
  market: MarketType;
  side: 'long' | 'short';
  entryPrice: number;
  currentPrice: number;
  quantity: number;
  pnl: number;
  pnlPercent: number;
  openedAt: number;
}

// User Preferences
export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  defaultMarket: MarketType;
  defaultTimeframe: TimeFrame;
  enableNotifications: boolean;
  enableSound: boolean;
  chartType: 'candlestick' | 'line' | 'area';
  indicators: string[];
  currency: 'USD' | 'INR' | 'EUR';
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
  timestamp: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

// Model Performance
export interface ModelPerformance {
  model: ModelType;
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  mae: number; // Mean Absolute Error
  rmse: number; // Root Mean Square Error
  sharpeRatio?: number;
  winRate?: number;
  profitFactor?: number;
}

// Backtest Results
export interface BacktestResult {
  id: string;
  symbol: string;
  strategy: string;
  startDate: number;
  endDate: number;
  initialCapital: number;
  finalCapital: number;
  totalReturn: number;
  totalReturnPercent: number;
  sharpeRatio: number;
  maxDrawdown: number;
  winRate: number;
  totalTrades: number;
  profitableTrades: number;
  trades: Trade[];
}

export interface Trade {
  id: string;
  entryTime: number;
  exitTime: number;
  entryPrice: number;
  exitPrice: number;
  quantity: number;
  side: 'long' | 'short';
  pnl: number;
  pnlPercent: number;
  reason: string;
}

// Sentiment Analysis
export interface SentimentData {
  symbol: string;
  score: number; // -1 to 1
  label: 'very_bearish' | 'bearish' | 'neutral' | 'bullish' | 'very_bullish';
  sources: {
    news: number;
    social: number;
    technical: number;
  };
  volume: number;
  timestamp: number;
}

// Error Types
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
  timestamp: number;
}
