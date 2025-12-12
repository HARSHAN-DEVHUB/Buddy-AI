import { apiClient } from './api';
import type {
  Prediction,
  PredictionRequest,
  ModelPerformance,
  ModelType,
  BacktestResult,
} from '@/types';

class PredictionService {
  private readonly basePath = '/api/prediction';

  /**
   * Get prediction for a symbol
   */
  async getPrediction(request: PredictionRequest): Promise<Prediction> {
    const response = await apiClient.post<Prediction>(`${this.basePath}/predict`, request);
    return response.data;
  }

  /**
   * Get multiple predictions (batch)
   */
  async getBatchPredictions(requests: PredictionRequest[]): Promise<Prediction[]> {
    const response = await apiClient.post<Prediction[]>(
      `${this.basePath}/predict/batch`,
      { requests }
    );
    return response.data;
  }

  /**
   * Get latest prediction for a symbol
   */
  async getLatestPrediction(symbol: string): Promise<Prediction | null> {
    const response = await apiClient.get<Prediction | null>(
      `${this.basePath}/latest/${symbol}`
    );
    return response.data;
  }

  /**
   * Get prediction history for a symbol
   */
  async getPredictionHistory(
    symbol: string,
    limit: number = 50
  ): Promise<Prediction[]> {
    const response = await apiClient.get<Prediction[]>(
      `${this.basePath}/history/${symbol}`,
      { limit }
    );
    return response.data;
  }

  /**
   * Get model performance metrics
   */
  async getModelPerformance(model: ModelType): Promise<ModelPerformance> {
    const response = await apiClient.get<ModelPerformance>(
      `${this.basePath}/performance/${model}`
    );
    return response.data;
  }

  /**
   * Get all models performance comparison
   */
  async getAllModelsPerformance(): Promise<ModelPerformance[]> {
    const response = await apiClient.get<ModelPerformance[]>(
      `${this.basePath}/performance`
    );
    return response.data;
  }

  /**
   * Run backtest for a strategy
   */
  async runBacktest(params: {
    symbol: string;
    strategy: string;
    startDate: number;
    endDate: number;
    initialCapital: number;
  }): Promise<BacktestResult> {
    const response = await apiClient.post<BacktestResult>(
      `${this.basePath}/backtest`,
      params
    );
    return response.data;
  }

  /**
   * Get backtest history
   */
  async getBacktestHistory(limit: number = 20): Promise<BacktestResult[]> {
    const response = await apiClient.get<BacktestResult[]>(
      `${this.basePath}/backtest/history`,
      { limit }
    );
    return response.data;
  }

  /**
   * Compare multiple models for a symbol
   */
  async compareModels(
    symbol: string,
    models: ModelType[]
  ): Promise<{
    symbol: string;
    predictions: Array<{ model: ModelType; prediction: Prediction }>;
    consensus: Prediction;
  }> {
    const response = await apiClient.post(
      `${this.basePath}/compare`,
      { symbol, models }
    );
    return response.data as {
      symbol: string;
      predictions: Array<{ model: ModelType; prediction: Prediction }>;
      consensus: Prediction;
    };
  }
}

export const predictionService = new PredictionService();
