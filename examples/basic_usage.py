"""
Basic usage example for ICHI-VSA

This example demonstrates how to use the ICHI-VSA indicator
with sample data.
"""

import pandas as pd
import numpy as np
from ichi_vsa import ICHIVSA


def create_sample_data(n=100):
    """Create sample OHLCV data."""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=n, freq='D')
    
    # Generate synthetic price data with an uptrend
    trend = np.linspace(0, 20, n)
    noise = np.random.randn(n) * 2
    close = 100 + trend + noise
    
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


def main():
    """Run the basic example."""
    print("ICHI-VSA Basic Usage Example")
    print("=" * 50)
    
    # Create sample data
    print("\n1. Creating sample OHLCV data...")
    df = create_sample_data(100)
    print(f"   Generated {len(df)} bars of data")
    print(f"   Date range: {df.index[0]} to {df.index[-1]}")
    
    # Initialize ICHI-VSA
    print("\n2. Initializing ICHI-VSA indicator...")
    ichi_vsa = ICHIVSA()
    
    # Perform analysis
    print("\n3. Analyzing data...")
    result = ichi_vsa.analyze(df)
    
    # Display latest signal
    print("\n4. Latest Signal:")
    print("-" * 50)
    latest_signal = ichi_vsa.get_latest_signal(df)
    
    print(f"   Date: {latest_signal['date']}")
    print(f"   Close Price: ${latest_signal['close']:.2f}")
    print(f"   Signal: {latest_signal['signal']}")
    print(f"   Signal Strength: {latest_signal['signal_strength']}")
    
    print("\n   Ichimoku Details:")
    print(f"      Tenkan-sen: {latest_signal['ichimoku']['tenkan_sen']:.2f}")
    print(f"      Kijun-sen: {latest_signal['ichimoku']['kijun_sen']:.2f}")
    print(f"      TK Cross: {latest_signal['ichimoku']['tk_cross']}")
    print(f"      Price vs Cloud: {latest_signal['ichimoku']['price_vs_cloud']}")
    print(f"      Cloud Bullish: {latest_signal['ichimoku']['cloud_bullish']}")
    
    print("\n   VSA Details:")
    print(f"      VSA Signal: {latest_signal['vsa']['vsa_signal']}")
    print(f"      VSA Bullish Signals: {latest_signal['vsa']['vsa_bullish']}")
    print(f"      VSA Bearish Signals: {latest_signal['vsa']['vsa_bearish']}")
    
    # Display last 5 signals
    print("\n5. Last 5 Trading Signals:")
    print("-" * 50)
    last_5 = result[['close', 'signal', 'signal_strength']].tail(5)
    print(last_5.to_string())
    
    # Show some specific VSA signals
    print("\n6. Recent VSA Patterns (last 10 bars):")
    print("-" * 50)
    vsa_patterns = result[['no_demand', 'no_supply', 'stopping_volume', 
                           'selling_climax', 'buying_climax', 'weakness']].tail(10)
    print(vsa_patterns.to_string())
    
    print("\n" + "=" * 50)
    print("Analysis complete!")


if __name__ == "__main__":
    main()
