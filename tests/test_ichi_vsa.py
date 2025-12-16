"""
Tests for ICHI-VSA combined indicator
"""

import pytest
import pandas as pd
import numpy as np
from ichi_vsa.ichi_vsa import ICHIVSA


def create_sample_data(n=100):
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


class TestICHIVSA:
    """Test cases for ICHI-VSA combined indicator."""
    
    def test_initialization(self):
        """Test ICHI-VSA initialization."""
        ichi_vsa = ICHIVSA()
        assert ichi_vsa.ichimoku is not None
        assert ichi_vsa.vsa is not None
    
    def test_calculate(self):
        """Test combined calculation."""
        df = create_sample_data(100)
        ichi_vsa = ICHIVSA()
        result = ichi_vsa.calculate(df)
        
        # Check Ichimoku columns
        assert 'tenkan_sen' in result.columns
        assert 'kijun_sen' in result.columns
        
        # Check VSA columns
        assert 'spread' in result.columns
        assert 'vsa_signal' in result.columns
    
    def test_get_combined_signals(self):
        """Test combined signal generation."""
        df = create_sample_data(100)
        ichi_vsa = ICHIVSA()
        result = ichi_vsa.get_combined_signals(df)
        
        # Check combined signal columns
        assert 'strong_bullish' in result.columns
        assert 'strong_bearish' in result.columns
        assert 'moderate_bullish' in result.columns
        assert 'moderate_bearish' in result.columns
        assert 'signal_strength' in result.columns
        assert 'signal' in result.columns
    
    def test_analyze(self):
        """Test complete analysis."""
        df = create_sample_data(100)
        ichi_vsa = ICHIVSA()
        result = ichi_vsa.analyze(df)
        
        # Should have all indicators and signals
        assert 'tenkan_sen' in result.columns
        assert 'vsa_signal' in result.columns
        assert 'signal' in result.columns
    
    def test_get_latest_signal(self):
        """Test getting the latest signal."""
        df = create_sample_data(100)
        ichi_vsa = ICHIVSA()
        signal = ichi_vsa.get_latest_signal(df)
        
        # Check signal structure
        assert 'date' in signal
        assert 'close' in signal
        assert 'signal' in signal
        assert 'signal_strength' in signal
        assert 'ichimoku' in signal
        assert 'vsa' in signal
        
        # Check nested structures
        assert 'tenkan_sen' in signal['ichimoku']
        assert 'vsa_signal' in signal['vsa']
    
    def test_signal_strength_range(self):
        """Test that signal strength is within expected range."""
        df = create_sample_data(100)
        ichi_vsa = ICHIVSA()
        result = ichi_vsa.get_combined_signals(df)
        
        # Signal strength should be between -2 and 2
        assert result['signal_strength'].min() >= -2
        assert result['signal_strength'].max() <= 2
    
    def test_signal_categories(self):
        """Test that signal categories are correct."""
        df = create_sample_data(100)
        ichi_vsa = ICHIVSA()
        result = ichi_vsa.get_combined_signals(df)
        
        # Check signal categories
        valid_signals = ['Strong Sell', 'Sell', 'Neutral', 'Buy', 'Strong Buy']
        valid_data = result.dropna(subset=['signal'])
        assert valid_data['signal'].isin(valid_signals).all()
