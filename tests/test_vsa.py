"""
Tests for VSA (Volume Spread Analysis)
"""

import pytest
import pandas as pd
import numpy as np
from ichi_vsa.vsa import VSA


def create_sample_data_with_volume(n=100):
    """Create sample OHLCV data for testing."""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=n, freq='D')
    
    # Generate synthetic price data
    close = 100 + np.cumsum(np.random.randn(n) * 2)
    high = close + np.random.uniform(0.5, 2, n)
    low = close - np.random.uniform(0.5, 2, n)
    open_price = close + np.random.uniform(-1, 1, n)
    volume = np.random.uniform(1000000, 5000000, n)
    
    df = pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }, index=dates)
    
    return df


class TestVSA:
    """Test cases for VSA indicator."""
    
    def test_initialization(self):
        """Test VSA initialization with default parameters."""
        vsa = VSA()
        assert vsa.volume_ma_period == 20
        assert vsa.high_volume_factor == 1.5
        assert vsa.low_volume_factor == 0.7
    
    def test_initialization_custom(self):
        """Test VSA initialization with custom parameters."""
        vsa = VSA(volume_ma_period=14, high_volume_factor=2.0, low_volume_factor=0.5)
        assert vsa.volume_ma_period == 14
        assert vsa.high_volume_factor == 2.0
        assert vsa.low_volume_factor == 0.5
    
    def test_calculate(self):
        """Test VSA calculation."""
        df = create_sample_data_with_volume(100)
        vsa = VSA()
        result = vsa.calculate(df)
        
        # Check that VSA columns are added
        assert 'spread' in result.columns
        assert 'avg_spread' in result.columns
        assert 'avg_volume' in result.columns
        assert 'high_volume' in result.columns
        assert 'low_volume' in result.columns
        assert 'narrow_spread' in result.columns
        assert 'wide_spread' in result.columns
        assert 'close_position' in result.columns
        
        # Check that original columns are preserved
        assert 'volume' in result.columns
    
    def test_spread_calculation(self):
        """Test spread calculation."""
        df = create_sample_data_with_volume(100)
        vsa = VSA()
        result = vsa.calculate(df)
        
        # Spread should equal high - low
        expected_spread = result['high'] - result['low']
        pd.testing.assert_series_equal(result['spread'], expected_spread, check_names=False)
    
    def test_close_position(self):
        """Test close position calculation."""
        df = create_sample_data_with_volume(100)
        vsa = VSA()
        result = vsa.calculate(df)
        
        # Close position should be between 0 and 1
        valid_data = result.dropna(subset=['close_position'])
        assert (valid_data['close_position'] >= 0).all()
        assert (valid_data['close_position'] <= 1).all()
    
    def test_get_signals(self):
        """Test VSA signal generation."""
        df = create_sample_data_with_volume(100)
        vsa = VSA()
        result = vsa.get_signals(df)
        
        # Check that signal columns are added
        assert 'no_demand' in result.columns
        assert 'no_supply' in result.columns
        assert 'stopping_volume' in result.columns
        assert 'selling_climax' in result.columns
        assert 'buying_climax' in result.columns
        assert 'weakness' in result.columns
        assert 'vsa_bullish' in result.columns
        assert 'vsa_bearish' in result.columns
        assert 'vsa_signal' in result.columns
    
    def test_up_down_bars(self):
        """Test up and down bar identification."""
        df = create_sample_data_with_volume(100)
        vsa = VSA()
        result = vsa.calculate(df)
        
        # Up bars should have close > open
        up_bars = result[result['up_bar']]
        assert (up_bars['close'] > up_bars['open']).all()
        
        # Down bars should have close < open
        down_bars = result[result['down_bar']]
        assert (down_bars['close'] < down_bars['open']).all()
