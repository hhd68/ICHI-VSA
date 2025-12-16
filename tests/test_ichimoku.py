"""
Tests for Ichimoku indicator
"""

import pytest
import pandas as pd
import numpy as np
from ichi_vsa.ichimoku import Ichimoku


def create_sample_data(n=100):
    """Create sample OHLC data for testing."""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=n, freq='D')
    
    # Generate synthetic price data
    close = 100 + np.cumsum(np.random.randn(n) * 2)
    high = close + np.random.uniform(0.5, 2, n)
    low = close - np.random.uniform(0.5, 2, n)
    open_price = close + np.random.uniform(-1, 1, n)
    
    df = pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close
    }, index=dates)
    
    return df


class TestIchimoku:
    """Test cases for Ichimoku indicator."""
    
    def test_initialization(self):
        """Test Ichimoku initialization with default parameters."""
        ichi = Ichimoku()
        assert ichi.tenkan_period == 9
        assert ichi.kijun_period == 26
        assert ichi.senkou_b_period == 52
        assert ichi.displacement == 26
    
    def test_initialization_custom(self):
        """Test Ichimoku initialization with custom parameters."""
        ichi = Ichimoku(tenkan_period=7, kijun_period=22, senkou_b_period=44, displacement=22)
        assert ichi.tenkan_period == 7
        assert ichi.kijun_period == 22
        assert ichi.senkou_b_period == 44
        assert ichi.displacement == 22
    
    def test_calculate(self):
        """Test Ichimoku calculation."""
        df = create_sample_data(100)
        ichi = Ichimoku()
        result = ichi.calculate(df)
        
        # Check that all Ichimoku columns are added
        assert 'tenkan_sen' in result.columns
        assert 'kijun_sen' in result.columns
        assert 'senkou_span_a' in result.columns
        assert 'senkou_span_b' in result.columns
        assert 'chikou_span' in result.columns
        
        # Check that original columns are preserved
        assert 'open' in result.columns
        assert 'high' in result.columns
        assert 'low' in result.columns
        assert 'close' in result.columns
    
    def test_tenkan_sen_calculation(self):
        """Test Tenkan-sen calculation."""
        df = create_sample_data(100)
        ichi = Ichimoku()
        result = ichi.calculate(df)
        
        # Tenkan-sen should not be NaN after sufficient data
        assert result['tenkan_sen'].notna().sum() > 0
        
        # Tenkan-sen values should be numeric
        valid_data = result.dropna(subset=['tenkan_sen'])
        assert valid_data['tenkan_sen'].dtype in ['float64', 'float32']
    
    def test_get_signals(self):
        """Test signal generation."""
        df = create_sample_data(100)
        ichi = Ichimoku()
        result = ichi.get_signals(df)
        
        # Check that signal columns are added
        assert 'tk_cross' in result.columns
        assert 'price_vs_kijun' in result.columns
        assert 'price_vs_cloud' in result.columns
        assert 'cloud_bullish' in result.columns
        
        # Check signal values are within expected range
        assert result['tk_cross'].isin([-1, 0, 1]).all()
        assert result['price_vs_kijun'].isin([-1, 1]).all()
    
    def test_cloud_calculation(self):
        """Test cloud (Kumo) calculation."""
        df = create_sample_data(100)
        ichi = Ichimoku()
        result = ichi.get_signals(df)
        
        # Check cloud top and bottom
        assert 'cloud_top' in result.columns
        assert 'cloud_bottom' in result.columns
        
        # Cloud top should always be >= cloud bottom
        valid_data = result.dropna(subset=['cloud_top', 'cloud_bottom'])
        assert (valid_data['cloud_top'] >= valid_data['cloud_bottom']).all()
