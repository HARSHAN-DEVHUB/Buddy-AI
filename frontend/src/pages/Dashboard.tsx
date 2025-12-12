import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { TrendingUp, TrendingDown, DollarSign, Activity } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@components/common/Card';
import Loading from '@components/common/Loading';
import { marketService } from '@services/market';
import { formatCurrency, formatPercent, cn } from '@utils/helpers';
import type { MarketData } from '@/types';

export default function Dashboard() {
  const [selectedMarket, setSelectedMarket] = useState<'forex' | 'crypto' | 'stock'>('forex');

  // Fetch market overview
  const { data: marketOverview, isLoading: marketLoading } = useQuery({
    queryKey: ['marketOverview', selectedMarket],
    queryFn: () => marketService.getMarketOverview(selectedMarket),
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  // Fetch latest predictions - TODO: Implement when prediction API is ready
  // const { data: latestPredictions, isLoading: predictionsLoading } = useQuery({
  //   queryKey: ['latestPredictions'],
  //   queryFn: async () => {
  //     return predictionService.getLatestPredictions();
  //   },
  // });

  if (marketLoading) {
    return <Loading text="Loading dashboard..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Welcome back! Here's your market overview.
        </p>
      </div>

      {/* Market Selector */}
      <div className="flex gap-2">
        {['forex', 'crypto', 'stock'].map((market) => (
          <button
            key={market}
            onClick={() => setSelectedMarket(market as typeof selectedMarket)}
            className={cn(
              'rounded-lg px-4 py-2 text-sm font-medium transition-colors',
              selectedMarket === market
                ? 'bg-primary text-primary-foreground'
                : 'bg-card border border-border hover:bg-accent'
            )}
          >
            {market.charAt(0).toUpperCase() + market.slice(1)}
          </button>
        ))}
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Total Volume"
          value={formatCurrency(marketOverview?.totalVolume || 0)}
          icon={<DollarSign className="h-4 w-4" />}
          trend={{ value: 12.5, isPositive: true }}
        />
        <StatsCard
          title="Avg Change"
          value={formatPercent(marketOverview?.avgChange || 0)}
          icon={<Activity className="h-4 w-4" />}
          trend={{ value: marketOverview?.avgChange || 0, isPositive: (marketOverview?.avgChange || 0) > 0 }}
        />
        <StatsCard
          title="Top Gainer"
          value={marketOverview?.topGainers?.[0]?.symbol || 'N/A'}
          icon={<TrendingUp className="h-4 w-4" />}
          trend={{ 
            value: marketOverview?.topGainers?.[0]?.changePercent24h || 0, 
            isPositive: true 
          }}
        />
        <StatsCard
          title="Top Loser"
          value={marketOverview?.topLosers?.[0]?.symbol || 'N/A'}
          icon={<TrendingDown className="h-4 w-4" />}
          trend={{ 
            value: marketOverview?.topLosers?.[0]?.changePercent24h || 0, 
            isPositive: false 
          }}
        />
      </div>

      {/* Market Movers */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Top Gainers */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-bullish" />
              Top Gainers
            </CardTitle>
            <CardDescription>Best performing assets today</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {marketOverview?.topGainers?.slice(0, 5).map((asset: MarketData) => (
                <AssetRow key={asset.symbol} asset={asset} />
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Top Losers */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingDown className="h-5 w-5 text-bearish" />
              Top Losers
            </CardTitle>
            <CardDescription>Worst performing assets today</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {marketOverview?.topLosers?.slice(0, 5).map((asset: MarketData) => (
                <AssetRow key={asset.symbol} asset={asset} />
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Get started with predictions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <QuickActionCard
              title="Analyze Forex"
              description="Get predictions for XAUUSD, EURUSD, and more"
              href="/forex"
            />
            <QuickActionCard
              title="Crypto Insights"
              description="BTC, ETH, BNB market predictions"
              href="/crypto"
            />
            <QuickActionCard
              title="Indian Stocks"
              description="NSE/BSE stock market analysis"
              href="/stocks"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Stats Card Component
interface StatsCardProps {
  title: string;
  value: string;
  icon: React.ReactNode;
  trend: { value: number; isPositive: boolean };
}

function StatsCard({ title, value, icon, trend }: StatsCardProps) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <div className="rounded-full bg-primary/10 p-2 text-primary">
            {icon}
          </div>
        </div>
        <div className="mt-3">
          <p className="text-2xl font-bold">{value}</p>
          <p className={cn(
            'mt-1 text-sm flex items-center gap-1',
            trend.isPositive ? 'text-bullish' : 'text-bearish'
          )}>
            {trend.isPositive ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
            {formatPercent(Math.abs(trend.value))}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

// Asset Row Component
interface AssetRowProps {
  asset: MarketData;
}

function AssetRow({ asset }: AssetRowProps) {
  const isPositive = asset.changePercent24h > 0;
  
  return (
    <div className="flex items-center justify-between rounded-lg border border-border p-3 hover:bg-accent/50 transition-colors">
      <div>
        <p className="font-medium">{asset.symbol}</p>
        <p className="text-sm text-muted-foreground">{formatCurrency(asset.price)}</p>
      </div>
      <div className="text-right">
        <p className={cn(
          'font-semibold',
          isPositive ? 'text-bullish' : 'text-bearish'
        )}>
          {formatPercent(asset.changePercent24h)}
        </p>
        <p className="text-sm text-muted-foreground">
          {formatCurrency(asset.change24h)}
        </p>
      </div>
    </div>
  );
}

// Quick Action Card Component
interface QuickActionCardProps {
  title: string;
  description: string;
  href: string;
}

function QuickActionCard({ title, description, href }: QuickActionCardProps) {
  return (
    <a
      href={href}
      className="block rounded-lg border border-border p-4 hover:border-primary hover:shadow-lg transition-all"
    >
      <h3 className="font-semibold">{title}</h3>
      <p className="mt-1 text-sm text-muted-foreground">{description}</p>
      <p className="mt-3 text-sm font-medium text-primary">Get Started →</p>
    </a>
  );
}
