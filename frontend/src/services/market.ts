import { apiClient } from './api';
import type {
  MarketData,
  OHLCV,
  TechnicalIndicators,
  MarketType,
  TimeFrame,
} from '@/types';

class MarketService {
  private readonly basePath = '/api/market';

  /**
   * Get current market price for a symbol
   */
  async getCurrentPrice(symbol: string, market: MarketType): Promise<MarketData> {
    const response = await apiClient.get<MarketData>(
      `${this.basePath}/price/${market}/${symbol}`
    );
    return response.data;
  }

  /**
   * Get historical OHLCV data
   */
  async getHistoricalData(
    symbol: string,
    market: MarketType,
    timeframe: TimeFrame,
    limit: number = 500
  ): Promise<OHLCV[]> {
    const response = await apiClient.get<OHLCV[]>(
      `${this.basePath}/history/${market}/${symbol}`,
      { timeframe, limit }
    );
    return response.data;
  }

  /**
   * Get technical indicators for a symbol
   */
  async getTechnicalIndicators(
    symbol: string,
    market: MarketType,
    timeframe: TimeFrame
  ): Promise<TechnicalIndicators> {
    const response = await apiClient.get<TechnicalIndicators>(
      `${this.basePath}/indicators/${market}/${symbol}`,
      { timeframe }
    );
    return response.data;
  }

  /**
   * Get multiple market prices at once
   */
  async getMultiplePrices(symbols: string[], market: MarketType): Promise<MarketData[]> {
    const response = await apiClient.post<MarketData[]>(
      `${this.basePath}/prices/${market}`,
      { symbols }
    );
    return response.data;
  }

  /**
   * Search for symbols
   */
  async searchSymbols(query: string, market?: MarketType): Promise<string[]> {
    const response = await apiClient.get<string[]>(`${this.basePath}/search`, {
      query,
      market,
    });
    return response.data;
  }

  /**
   * Get top gainers/losers
   */
  async getTopMovers(market: MarketType, type: 'gainers' | 'losers' = 'gainers', limit: number = 10): Promise<MarketData[]> {
    const response = await apiClient.get<MarketData[]>(
      `${this.basePath}/movers/${market}`,
      { type, limit }
    );
    return response.data;
  }

  /**
   * Get market overview/summary
   */
  async getMarketOverview(market: MarketType): Promise<{
    totalVolume: number;
    avgChange: number;
    topGainers: MarketData[];
    topLosers: MarketData[];
    mostActive: MarketData[];
  }> {
    const response = await apiClient.get(`${this.basePath}/overview/${market}`);
    return response.data as {
      totalVolume: number;
      avgChange: number;
      topGainers: MarketData[];
      topLosers: MarketData[];
      mostActive: MarketData[];
    };
  }
}

export const marketService = new MarketService();
