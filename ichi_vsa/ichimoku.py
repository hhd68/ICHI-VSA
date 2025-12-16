"""
Ichimoku Kinko Hyo (Ichimoku Cloud) Indicator Implementation

The Ichimoku indicator consists of five main components:
1. Tenkan-sen (Conversion Line): (9-period high + 9-period low) / 2
2. Kijun-sen (Base Line): (26-period high + 26-period low) / 2
3. Senkou Span A (Leading Span A): (Tenkan-sen + Kijun-sen) / 2, plotted 26 periods ahead
4. Senkou Span B (Leading Span B): (52-period high + 52-period low) / 2, plotted 26 periods ahead
5. Chikou Span (Lagging Span): Close price plotted 26 periods in the past
"""

import pandas as pd
import numpy as np


class Ichimoku:
    """
    Ichimoku Kinko Hyo indicator calculator.
    
    This class calculates all five components of the Ichimoku indicator.
    """
    
    def __init__(self, tenkan_period=9, kijun_period=26, senkou_b_period=52, displacement=26):
        """
        Initialize Ichimoku indicator with custom periods.
        
        Args:
            tenkan_period (int): Period for Tenkan-sen calculation (default: 9)
            kijun_period (int): Period for Kijun-sen calculation (default: 26)
            senkou_b_period (int): Period for Senkou Span B calculation (default: 52)
            displacement (int): Displacement for Senkou Spans (default: 26)
        """
        self.tenkan_period = tenkan_period
        self.kijun_period = kijun_period
        self.senkou_b_period = senkou_b_period
        self.displacement = displacement
    
    def _calculate_midpoint(self, high, low, period):
        """
        Calculate the midpoint of high and low over a given period.
        
        Args:
            high (pd.Series): High prices
            low (pd.Series): Low prices
            period (int): Number of periods
            
        Returns:
            pd.Series: Midpoint values
        """
        period_high = high.rolling(window=period).max()
        period_low = low.rolling(window=period).min()
        return (period_high + period_low) / 2
    
    def calculate(self, df):
        """
        Calculate all Ichimoku components for the given data.
        
        Args:
            df (pd.DataFrame): DataFrame with 'high', 'low', and 'close' columns
            
        Returns:
            pd.DataFrame: Original DataFrame with added Ichimoku columns
        """
        result = df.copy()
        
        # Calculate Tenkan-sen (Conversion Line)
        result['tenkan_sen'] = self._calculate_midpoint(
            result['high'], result['low'], self.tenkan_period
        )
        
        # Calculate Kijun-sen (Base Line)
        result['kijun_sen'] = self._calculate_midpoint(
            result['high'], result['low'], self.kijun_period
        )
        
        # Calculate Senkou Span A (Leading Span A)
        senkou_span_a = (result['tenkan_sen'] + result['kijun_sen']) / 2
        result['senkou_span_a'] = senkou_span_a.shift(self.displacement)
        
        # Calculate Senkou Span B (Leading Span B)
        senkou_span_b = self._calculate_midpoint(
            result['high'], result['low'], self.senkou_b_period
        )
        result['senkou_span_b'] = senkou_span_b.shift(self.displacement)
        
        # Calculate Chikou Span (Lagging Span)
        result['chikou_span'] = result['close'].shift(-self.displacement)
        
        return result
    
    def get_signals(self, df):
        """
        Generate trading signals based on Ichimoku indicator.
        
        Args:
            df (pd.DataFrame): DataFrame with Ichimoku indicators calculated
            
        Returns:
            pd.DataFrame: DataFrame with added signal columns
        """
        result = df.copy()
        
        # Ensure Ichimoku columns exist
        if 'tenkan_sen' not in result.columns:
            result = self.calculate(result)
        
        # TK Cross: Bullish when Tenkan crosses above Kijun
        result['tk_cross'] = np.where(
            (result['tenkan_sen'] > result['kijun_sen']) & 
            (result['tenkan_sen'].shift(1) <= result['kijun_sen'].shift(1)),
            1,  # Bullish signal
            np.where(
                (result['tenkan_sen'] < result['kijun_sen']) & 
                (result['tenkan_sen'].shift(1) >= result['kijun_sen'].shift(1)),
                -1,  # Bearish signal
                0  # No signal
            )
        )
        
        # Price vs Kijun: Position relative to Kijun-sen
        result['price_vs_kijun'] = np.where(
            result['close'] > result['kijun_sen'], 1, -1
        )
        
        # Cloud analysis
        result['cloud_top'] = result[['senkou_span_a', 'senkou_span_b']].max(axis=1)
        result['cloud_bottom'] = result[['senkou_span_a', 'senkou_span_b']].min(axis=1)
        
        # Price position relative to cloud
        result['price_vs_cloud'] = np.where(
            result['close'] > result['cloud_top'], 1,
            np.where(result['close'] < result['cloud_bottom'], -1, 0)
        )
        
        # Cloud color (bullish when Senkou A > Senkou B)
        result['cloud_bullish'] = np.where(
            result['senkou_span_a'] > result['senkou_span_b'], 1, 0
        )
        
        return result
