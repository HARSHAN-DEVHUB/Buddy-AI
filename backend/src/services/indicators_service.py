"""
Technical Indicators Service
Calculates various technical indicators for market analysis
"""
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from pandas_ta import rsi, macd, bbands, ema, sma, stoch, atr, adx, vwap, obv
import logging

logger = logging.getLogger(__name__)


class TechnicalIndicatorsService:
    """Service for calculating technical indicators"""
    
    def __init__(self):
        """Initialize technical indicators service"""
        pass
    
    def calculate_all_indicators(
        self, 
        ohlcv_data: List[Dict[str, Any]],
        symbol: str
    ) -> Dict[str, Any]:
        """
        Calculate all technical indicators for given OHLCV data
        
        Args:
            ohlcv_data: List of OHLCV dictionaries
            symbol: Trading symbol
            
        Returns:
            Dictionary with all calculated indicators
        """
        try:
            if not ohlcv_data or len(ohlcv_data) < 50:
                raise ValueError("Insufficient data for indicator calculation (need at least 50 candles)")
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Ensure numeric types
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate indicators
            indicators = {
                'symbol': symbol,
                'timestamp': int(df['timestamp'].iloc[-1].timestamp() * 1000),
                'rsi': self._calculate_rsi(df),
                'macd': self._calculate_macd(df),
                'bollingerBands': self._calculate_bollinger_bands(df),
                'ema': self._calculate_ema(df),
                'sma': self._calculate_sma(df),
                'stochastic': self._calculate_stochastic(df),
                'atr': self._calculate_atr(df),
                'adx': self._calculate_adx(df),
                'vwap': self._calculate_vwap(df),
                'obv': self._calculate_obv(df)
            }
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
            raise
    
    def _calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> float:
        """Calculate RSI (Relative Strength Index)"""
        try:
            rsi_series = rsi(df['close'], length=period)
            return float(rsi_series.iloc[-1]) if not pd.isna(rsi_series.iloc[-1]) else 50.0
        except Exception as e:
            logger.warning(f"RSI calculation failed: {e}")
            return 50.0
    
    def _calculate_macd(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            macd_data = macd(df['close'], fast=12, slow=26, signal=9)
            
            if macd_data is None or macd_data.empty:
                return {'value': 0.0, 'signal': 0.0, 'histogram': 0.0}
            
            # Get the last values
            last_row = macd_data.iloc[-1]
            
            return {
                'value': float(last_row[f'MACD_12_26_9']) if f'MACD_12_26_9' in macd_data.columns else 0.0,
                'signal': float(last_row[f'MACDs_12_26_9']) if f'MACDs_12_26_9' in macd_data.columns else 0.0,
                'histogram': float(last_row[f'MACDh_12_26_9']) if f'MACDh_12_26_9' in macd_data.columns else 0.0
            }
        except Exception as e:
            logger.warning(f"MACD calculation failed: {e}")
            return {'value': 0.0, 'signal': 0.0, 'histogram': 0.0}
    
    def _calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        try:
            bb_data = bbands(df['close'], length=period, std=2)
            
            if bb_data is None or bb_data.empty:
                current_price = float(df['close'].iloc[-1])
                return {'upper': current_price, 'middle': current_price, 'lower': current_price}
            
            last_row = bb_data.iloc[-1]
            
            return {
                'upper': float(last_row[f'BBU_{period}_2.0']) if f'BBU_{period}_2.0' in bb_data.columns else 0.0,
                'middle': float(last_row[f'BBM_{period}_2.0']) if f'BBM_{period}_2.0' in bb_data.columns else 0.0,
                'lower': float(last_row[f'BBL_{period}_2.0']) if f'BBL_{period}_2.0' in bb_data.columns else 0.0
            }
        except Exception as e:
            logger.warning(f"Bollinger Bands calculation failed: {e}")
            current_price = float(df['close'].iloc[-1])
            return {'upper': current_price, 'middle': current_price, 'lower': current_price}
    
    def _calculate_ema(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate Exponential Moving Averages"""
        try:
            return {
                'ema12': float(ema(df['close'], length=12).iloc[-1]),
                'ema26': float(ema(df['close'], length=26).iloc[-1]),
                'ema50': float(ema(df['close'], length=50).iloc[-1]),
                'ema200': float(ema(df['close'], length=200).iloc[-1]) if len(df) >= 200 else 0.0
            }
        except Exception as e:
            logger.warning(f"EMA calculation failed: {e}")
            current_price = float(df['close'].iloc[-1])
            return {'ema12': current_price, 'ema26': current_price, 'ema50': current_price, 'ema200': 0.0}
    
    def _calculate_sma(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate Simple Moving Averages"""
        try:
            return {
                'sma20': float(sma(df['close'], length=20).iloc[-1]),
                'sma50': float(sma(df['close'], length=50).iloc[-1]),
                'sma200': float(sma(df['close'], length=200).iloc[-1]) if len(df) >= 200 else 0.0
            }
        except Exception as e:
            logger.warning(f"SMA calculation failed: {e}")
            current_price = float(df['close'].iloc[-1])
            return {'sma20': current_price, 'sma50': current_price, 'sma200': 0.0}
    
    def _calculate_stochastic(self, df: pd.DataFrame, k_period: int = 14) -> Dict[str, float]:
        """Calculate Stochastic Oscillator"""
        try:
            stoch_data = stoch(df['high'], df['low'], df['close'], k=k_period, d=3)
            
            if stoch_data is None or stoch_data.empty:
                return {'k': 50.0, 'd': 50.0}
            
            last_row = stoch_data.iloc[-1]
            
            return {
                'k': float(last_row[f'STOCHk_{k_period}_3_3']) if f'STOCHk_{k_period}_3_3' in stoch_data.columns else 50.0,
                'd': float(last_row[f'STOCHd_{k_period}_3_3']) if f'STOCHd_{k_period}_3_3' in stoch_data.columns else 50.0
            }
        except Exception as e:
            logger.warning(f"Stochastic calculation failed: {e}")
            return {'k': 50.0, 'd': 50.0}
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range"""
        try:
            atr_series = atr(df['high'], df['low'], df['close'], length=period)
            return float(atr_series.iloc[-1]) if not pd.isna(atr_series.iloc[-1]) else 0.0
        except Exception as e:
            logger.warning(f"ATR calculation failed: {e}")
            return 0.0
    
    def _calculate_adx(self, df: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average Directional Index"""
        try:
            adx_data = adx(df['high'], df['low'], df['close'], length=period)
            
            if adx_data is None or adx_data.empty:
                return 25.0
            
            adx_col = f'ADX_{period}'
            if adx_col in adx_data.columns:
                return float(adx_data[adx_col].iloc[-1])
            return 25.0
        except Exception as e:
            logger.warning(f"ADX calculation failed: {e}")
            return 25.0
    
    def _calculate_vwap(self, df: pd.DataFrame) -> float:
        """Calculate Volume Weighted Average Price"""
        try:
            vwap_series = vwap(df['high'], df['low'], df['close'], df['volume'])
            return float(vwap_series.iloc[-1]) if not pd.isna(vwap_series.iloc[-1]) else float(df['close'].iloc[-1])
        except Exception as e:
            logger.warning(f"VWAP calculation failed: {e}")
            return float(df['close'].iloc[-1])
    
    def _calculate_obv(self, df: pd.DataFrame) -> float:
        """Calculate On-Balance Volume"""
        try:
            obv_series = obv(df['close'], df['volume'])
            return float(obv_series.iloc[-1]) if not pd.isna(obv_series.iloc[-1]) else 0.0
        except Exception as e:
            logger.warning(f"OBV calculation failed: {e}")
            return 0.0
    
    def get_trend_signal(self, indicators: Dict[str, Any]) -> str:
        """
        Determine overall trend signal based on indicators
        
        Args:
            indicators: Dictionary of calculated indicators
            
        Returns:
            Trend signal: 'STRONG_BUY', 'BUY', 'NEUTRAL', 'SELL', 'STRONG_SELL'
        """
        try:
            signals = []
            
            # RSI analysis
            rsi = indicators['rsi']
            if rsi > 70:
                signals.append(-1)  # Overbought
            elif rsi > 60:
                signals.append(-0.5)
            elif rsi < 30:
                signals.append(1)  # Oversold
            elif rsi < 40:
                signals.append(0.5)
            else:
                signals.append(0)
            
            # MACD analysis
            macd_data = indicators['macd']
            if macd_data['histogram'] > 0:
                signals.append(1)
            elif macd_data['histogram'] < 0:
                signals.append(-1)
            
            # Moving Average analysis
            ema = indicators['ema']
            if ema['ema12'] > ema['ema26']:
                signals.append(1)  # Bullish
            else:
                signals.append(-1)  # Bearish
            
            # Average signal
            avg_signal = sum(signals) / len(signals)
            
            if avg_signal > 0.6:
                return 'STRONG_BUY'
            elif avg_signal > 0.2:
                return 'BUY'
            elif avg_signal < -0.6:
                return 'STRONG_SELL'
            elif avg_signal < -0.2:
                return 'SELL'
            else:
                return 'NEUTRAL'
                
        except Exception as e:
            logger.error(f"Error determining trend signal: {e}")
            return 'NEUTRAL'


# Singleton instance
indicators_service = TechnicalIndicatorsService()
