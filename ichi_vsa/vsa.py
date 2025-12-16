"""
Volume Spread Analysis (VSA) Implementation

VSA analyzes the relationship between volume and price spread to identify
professional money activity and potential market turning points.

Key concepts:
- High volume + narrow spread = potential weakness or strength absorption
- Low volume + wide spread = potential lack of interest
- Volume climax = potential reversal point
"""

import pandas as pd
import numpy as np


class VSA:
    """
    Volume Spread Analysis calculator.
    
    This class implements various VSA concepts and signals.
    """
    
    def __init__(self, volume_ma_period=20, high_volume_factor=1.5, low_volume_factor=0.7):
        """
        Initialize VSA analyzer with custom parameters.
        
        Args:
            volume_ma_period (int): Period for volume moving average (default: 20)
            high_volume_factor (float): Multiplier for high volume threshold (default: 1.5)
            low_volume_factor (float): Multiplier for low volume threshold (default: 0.7)
        """
        self.volume_ma_period = volume_ma_period
        self.high_volume_factor = high_volume_factor
        self.low_volume_factor = low_volume_factor
    
    def calculate(self, df):
        """
        Calculate VSA indicators for the given data.
        
        Args:
            df (pd.DataFrame): DataFrame with 'open', 'high', 'low', 'close', 'volume' columns
            
        Returns:
            pd.DataFrame: Original DataFrame with added VSA columns
        """
        result = df.copy()
        
        # Calculate spread (range)
        result['spread'] = result['high'] - result['low']
        
        # Calculate average spread
        result['avg_spread'] = result['spread'].rolling(window=self.volume_ma_period).mean()
        
        # Calculate volume moving average
        result['avg_volume'] = result['volume'].rolling(window=self.volume_ma_period).mean()
        
        # Identify high and low volume
        result['high_volume'] = result['volume'] > (result['avg_volume'] * self.high_volume_factor)
        result['low_volume'] = result['volume'] < (result['avg_volume'] * self.low_volume_factor)
        
        # Identify narrow and wide spreads
        result['narrow_spread'] = result['spread'] < (result['avg_spread'] * 0.7)
        result['wide_spread'] = result['spread'] > (result['avg_spread'] * 1.3)
        
        # Calculate close position within the bar
        result['close_position'] = (result['close'] - result['low']) / (result['spread'] + 1e-10)
        
        # Identify up and down bars
        result['up_bar'] = result['close'] > result['open']
        result['down_bar'] = result['close'] < result['open']
        
        return result
    
    def get_signals(self, df):
        """
        Generate VSA trading signals.
        
        Args:
            df (pd.DataFrame): DataFrame with VSA indicators calculated
            
        Returns:
            pd.DataFrame: DataFrame with added VSA signal columns
        """
        result = df.copy()
        
        # Ensure VSA columns exist
        if 'spread' not in result.columns:
            result = self.calculate(result)
        
        # No Demand (potential bullish): Down bar, low volume, narrow spread, close in upper half
        result['no_demand'] = (
            result['down_bar'] & 
            result['low_volume'] & 
            result['narrow_spread'] &
            (result['close_position'] > 0.5)
        ).astype(int)
        
        # No Supply (potential bullish): Up bar, low volume, narrow spread
        result['no_supply'] = (
            result['up_bar'] & 
            result['low_volume'] & 
            result['narrow_spread']
        ).astype(int)
        
        # Stopping Volume (potential bullish reversal): Down bar, high volume, narrow spread
        result['stopping_volume'] = (
            result['down_bar'] & 
            result['high_volume'] & 
            result['narrow_spread'] &
            (result['close_position'] > 0.3)
        ).astype(int)
        
        # Selling Climax (potential bullish reversal): Down bar, high volume, wide spread
        result['selling_climax'] = (
            result['down_bar'] & 
            result['high_volume'] & 
            result['wide_spread'] &
            (result['close_position'] < 0.5)
        ).astype(int)
        
        # Buying Climax (potential bearish reversal): Up bar, high volume, wide spread, close not at high
        result['buying_climax'] = (
            result['up_bar'] & 
            result['high_volume'] & 
            result['wide_spread'] &
            (result['close_position'] < 0.9)
        ).astype(int)
        
        # Weakness (potential bearish): Up bar, high volume, narrow spread
        result['weakness'] = (
            result['up_bar'] & 
            result['high_volume'] & 
            result['narrow_spread']
        ).astype(int)
        
        # No Result (potential bearish): Up bar, high volume, close in middle
        result['no_result'] = (
            result['up_bar'] & 
            result['high_volume'] & 
            (result['close_position'] > 0.4) &
            (result['close_position'] < 0.6)
        ).astype(int)
        
        # Aggregate bullish and bearish signals
        result['vsa_bullish'] = (
            result['no_demand'] + 
            result['no_supply'] + 
            result['stopping_volume'] + 
            result['selling_climax']
        )
        
        result['vsa_bearish'] = (
            result['buying_climax'] + 
            result['weakness'] + 
            result['no_result']
        )
        
        # Net VSA signal
        result['vsa_signal'] = result['vsa_bullish'] - result['vsa_bearish']
        
        return result
