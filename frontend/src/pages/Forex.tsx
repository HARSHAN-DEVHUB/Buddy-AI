import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@components/common/Card';
import { Button } from '@components/common/Button';
import Loading from '@components/common/Loading';
import { Search, TrendingUp } from 'lucide-react';
import { marketService } from '@services/market';
import { predictionService } from '@services/prediction';
import { formatCurrency, formatPercent, cn } from '@utils/helpers';
import { useRealTimePrice } from '@hooks/useMarket';
import type { Prediction } from '@/types';

const POPULAR_FOREX = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD'];

export default function ForexPage() {
  const [selectedSymbol, setSelectedSymbol] = useState('XAUUSD');
  const [searchQuery, setSearchQuery] = useState('');

  // Real-time price
  const { price } = useRealTimePrice(selectedSymbol);

  // Fetch current price
  const { data: currentPrice, isLoading: priceLoading } = useQuery({
    queryKey: ['forexPrice', selectedSymbol],
    queryFn: () => marketService.getCurrentPrice(selectedSymbol, 'forex'),
    refetchInterval: 5000,
  });

  // Fetch prediction
  const { data: prediction, isLoading: predictionLoading, refetch: refetchPrediction } = useQuery({
    queryKey: ['forexPrediction', selectedSymbol],
    queryFn: () => predictionService.getPrediction({
      symbol: selectedSymbol,
      market: 'forex',
      timeframe: '1h',
      horizon: 24,
    }),
    enabled: false, // Only fetch when button clicked
  });

  const handleGetPrediction = () => {
    refetchPrediction();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Forex Market</h1>
        <p className="text-muted-foreground mt-2">
          AI-powered predictions for major forex pairs
        </p>
      </div>

      {/* Symbol Selector */}
      <Card>
        <CardHeader>
          <CardTitle>Select Forex Pair</CardTitle>
          <CardDescription>Choose a currency pair to analyze</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search forex pairs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value.toUpperCase())}
                className="w-full rounded-lg border border-border bg-background pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            {/* Popular Pairs */}
            <div className="flex flex-wrap gap-2">
              {POPULAR_FOREX.map((symbol) => (
                <button
                  key={symbol}
                  onClick={() => setSelectedSymbol(symbol)}
                  className={cn(
                    'rounded-lg px-4 py-2 text-sm font-medium transition-colors',
                    selectedSymbol === symbol
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-card border border-border hover:bg-accent'
                  )}
                >
                  {symbol}
                </button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Price Display */}
      <Card>
        <CardContent className="p-6">
          {priceLoading ? (
            <Loading text="Loading price..." />
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold">{selectedSymbol}</h2>
                  <p className="text-sm text-muted-foreground">Currency Pair</p>
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold">
                    {price ? formatCurrency(price.price) : formatCurrency(currentPrice?.price || 0)}
                  </p>
                  {currentPrice && (
                    <p className={cn(
                      'text-sm font-medium flex items-center gap-1 justify-end',
                      currentPrice.changePercent24h > 0 ? 'text-bullish' : 'text-bearish'
                    )}>
                      <TrendingUp className={cn(
                        'h-3 w-3',
                        currentPrice.changePercent24h < 0 && 'rotate-180'
                      )} />
                      {formatPercent(currentPrice.changePercent24h)}
                    </p>
                  )}
                </div>
              </div>

              {/* Additional Info */}
              {currentPrice && (
                <div className="grid grid-cols-2 gap-4 pt-4 border-t border-border">
                  <div>
                    <p className="text-sm text-muted-foreground">24h High</p>
                    <p className="font-semibold">{formatCurrency(currentPrice.high24h)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">24h Low</p>
                    <p className="font-semibold">{formatCurrency(currentPrice.low24h)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">24h Volume</p>
                    <p className="font-semibold">{formatCurrency(currentPrice.volume24h)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Last Update</p>
                    <p className="font-semibold">
                      {new Date(currentPrice.lastUpdate).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Prediction Section */}
      <Card>
        <CardHeader>
          <CardTitle>AI Prediction</CardTitle>
          <CardDescription>
            Get AI-powered price prediction for the next 24 hours
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!prediction ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground mb-4">
                Click the button below to generate a prediction
              </p>
              <Button onClick={handleGetPrediction} isLoading={predictionLoading}>
                Generate Prediction
              </Button>
            </div>
          ) : (
            <PredictionDisplay prediction={prediction} />
          )}
        </CardContent>
      </Card>

      {/* Chart Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>Price Chart</CardTitle>
          <CardDescription>Historical price data and trends</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-center justify-center bg-muted/20 rounded-lg">
            <p className="text-muted-foreground">Chart will be displayed here</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Prediction Display Component
interface PredictionDisplayProps {
  prediction: Prediction;
}

function PredictionDisplay({ prediction }: PredictionDisplayProps) {
  const priceChange = prediction.predictedPrice - prediction.currentPrice;
  const changePercent = (priceChange / prediction.currentPrice) * 100;
  const isPositive = priceChange > 0;

  return (
    <div className="space-y-6">
      {/* Main Prediction */}
      <div className="rounded-lg border-2 border-border p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="text-sm text-muted-foreground">Predicted Price</p>
            <p className="text-3xl font-bold">{formatCurrency(prediction.predictedPrice)}</p>
          </div>
          <div className={cn(
            'rounded-full px-4 py-2 font-semibold',
            isPositive ? 'bg-bullish/10 text-bullish' : 'bg-bearish/10 text-bearish'
          )}>
            {prediction.direction}
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <p className={cn('text-lg font-semibold', isPositive ? 'text-bullish' : 'text-bearish')}>
            {isPositive ? '+' : ''}{formatCurrency(priceChange)}
          </p>
          <p className={cn('text-sm', isPositive ? 'text-bullish' : 'text-bearish')}>
            ({formatPercent(changePercent)})
          </p>
        </div>
      </div>

      {/* Details Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div>
          <p className="text-sm text-muted-foreground">Confidence</p>
          <p className="text-lg font-semibold">{(prediction.confidence * 100).toFixed(0)}%</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Target Price</p>
          <p className="text-lg font-semibold">{formatCurrency(prediction.targetPrice)}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Stop Loss</p>
          <p className="text-lg font-semibold">{formatCurrency(prediction.stopLoss)}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Model</p>
          <p className="text-lg font-semibold">{prediction.model}</p>
        </div>
      </div>

      {/* Info */}
      <div className="rounded-lg bg-muted/50 p-4">
        <p className="text-sm text-muted-foreground">
          <strong>Note:</strong> This prediction is for the next {prediction.horizon} hours 
          using {prediction.model} model with {prediction.timeframe} timeframe.
          Always do your own research before making trading decisions.
        </p>
      </div>
    </div>
  );
}
