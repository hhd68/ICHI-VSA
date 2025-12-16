"""
ICHI-VSA: Combined Ichimoku and Volume Spread Analysis

This module combines the Ichimoku indicator with Volume Spread Analysis
to provide comprehensive trading signals.
"""

import pandas as pd
import numpy as np
from .ichimoku import Ichimoku
from .vsa import VSA


class ICHIVSA:
    """
    Combined Ichimoku and VSA indicator.
    
    This class integrates both Ichimoku and VSA analysis to generate
    more robust trading signals.
    """
    
    def __init__(self, 
                 tenkan_period=9, 
                 kijun_period=26, 
                 senkou_b_period=52, 
                 displacement=26,
                 volume_ma_period=20,
                 high_volume_factor=1.5,
                 low_volume_factor=0.7):
        """
        Initialize ICHI-VSA with custom parameters.
        
        Args:
            tenkan_period (int): Ichimoku Tenkan-sen period
            kijun_period (int): Ichimoku Kijun-sen period
            senkou_b_period (int): Ichimoku Senkou Span B period
            displacement (int): Ichimoku displacement
            volume_ma_period (int): VSA volume MA period
            high_volume_factor (float): VSA high volume threshold multiplier
            low_volume_factor (float): VSA low volume threshold multiplier
        """
        self.ichimoku = Ichimoku(tenkan_period, kijun_period, senkou_b_period, displacement)
        self.vsa = VSA(volume_ma_period, high_volume_factor, low_volume_factor)
    
    def calculate(self, df):
        """
        Calculate both Ichimoku and VSA indicators.
        
        Args:
            df (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with all indicators
        """
        result = df.copy()
        
        # Calculate Ichimoku indicators
        result = self.ichimoku.calculate(result)
        result = self.ichimoku.get_signals(result)
        
        # Calculate VSA indicators
        result = self.vsa.calculate(result)
        result = self.vsa.get_signals(result)
        
        return result
    
    def get_combined_signals(self, df):
        """
        Generate combined trading signals from both Ichimoku and VSA.
        
        Args:
            df (pd.DataFrame): DataFrame with all indicators calculated
            
        Returns:
            pd.DataFrame: DataFrame with combined signal columns
        """
        result = df.copy()
        
        # Ensure all indicators are calculated
        if 'tenkan_sen' not in result.columns or 'vsa_signal' not in result.columns:
            result = self.calculate(result)
        
        # Strong bullish signal: Multiple confirmations
        result['strong_bullish'] = (
            # Ichimoku conditions
            (result['tk_cross'] == 1) |
            ((result['price_vs_cloud'] == 1) & (result['cloud_bullish'] == 1)) |
            ((result['price_vs_kijun'] == 1) & (result['tenkan_sen'] > result['kijun_sen']))
        ) & (
            # VSA confirmation
            (result['vsa_signal'] > 0)
        )
        
        # Strong bearish signal: Multiple confirmations
        result['strong_bearish'] = (
            # Ichimoku conditions
            (result['tk_cross'] == -1) |
            ((result['price_vs_cloud'] == -1) & (result['cloud_bullish'] == 0)) |
            ((result['price_vs_kijun'] == -1) & (result['tenkan_sen'] < result['kijun_sen']))
        ) & (
            # VSA confirmation
            (result['vsa_signal'] < 0)
        )
        
        # Moderate signals: One indicator confirms
        result['moderate_bullish'] = (
            ~result['strong_bullish'] &
            (
                ((result['price_vs_cloud'] == 1) & (result['vsa_signal'] > 0)) |
                ((result['tk_cross'] == 1) & (result['vsa_signal'] >= 0))
            )
        )
        
        result['moderate_bearish'] = (
            ~result['strong_bearish'] &
            (
                ((result['price_vs_cloud'] == -1) & (result['vsa_signal'] < 0)) |
                ((result['tk_cross'] == -1) & (result['vsa_signal'] <= 0))
            )
        )
        
        # Overall signal strength
        result['signal_strength'] = (
            result['strong_bullish'].astype(int) * 2 +
            result['moderate_bullish'].astype(int) * 1 -
            result['moderate_bearish'].astype(int) * 1 -
            result['strong_bearish'].astype(int) * 2
        )
        
        # Signal interpretation
        result['signal'] = pd.cut(
            result['signal_strength'],
            bins=[-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf],
            labels=['Strong Sell', 'Sell', 'Neutral', 'Buy', 'Strong Buy']
        )
        
        return result
    
    def analyze(self, df):
        """
        Perform complete ICHI-VSA analysis.
        
        Args:
            df (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: Complete analysis with all indicators and signals
        """
        result = self.calculate(df)
        result = self.get_combined_signals(result)
        return result
    
    def get_latest_signal(self, df):
        """
        Get the latest trading signal.
        
        Args:
            df (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            dict: Latest signal information
        """
        analyzed = self.analyze(df)
        latest = analyzed.iloc[-1]
        
        return {
            'date': latest.name if isinstance(analyzed.index, pd.DatetimeIndex) else len(analyzed) - 1,
            'close': latest['close'],
            'signal': latest['signal'],
            'signal_strength': latest['signal_strength'],
            'ichimoku': {
                'tenkan_sen': latest['tenkan_sen'],
                'kijun_sen': latest['kijun_sen'],
                'tk_cross': latest['tk_cross'],
                'price_vs_cloud': latest['price_vs_cloud'],
                'cloud_bullish': latest['cloud_bullish']
            },
            'vsa': {
                'vsa_signal': latest['vsa_signal'],
                'vsa_bullish': latest['vsa_bullish'],
                'vsa_bearish': latest['vsa_bearish']
            }
        }
