"""
Advanced usage example for ICHI-VSA

This example demonstrates advanced features including:
- Custom parameters
- Backtesting signals
- Signal filtering
"""

import pandas as pd
import numpy as np
from ichi_vsa import ICHIVSA


def create_realistic_data(n=200):
    """Create more realistic OHLCV data with trends and reversals."""
    np.random.seed(123)
    dates = pd.date_range(start='2023-01-01', periods=n, freq='D')
    
    # Create price data with multiple trend phases
    price = 100
    prices = []
    
    for i in range(n):
        # Add trend component
        if i < 50:
            trend = 0.2  # Uptrend
        elif i < 100:
            trend = -0.15  # Downtrend
        elif i < 150:
            trend = 0.25  # Strong uptrend
        else:
            trend = 0.05  # Sideways
        
        # Add noise
        noise = np.random.randn() * 1.5
        price += trend + noise
        prices.append(price)
    
    close = np.array(prices)
    high = close + np.random.uniform(0.3, 1.5, n)
    low = close - np.random.uniform(0.3, 1.5, n)
    open_price = close + np.random.uniform(-0.8, 0.8, n)
    
    # Volume with spikes during trend changes
    base_volume = 2000000
    volume = []
    for i in range(n):
        if i in [50, 100, 150]:  # Trend change points
            vol = base_volume * np.random.uniform(2.5, 3.5)
        else:
            vol = base_volume * np.random.uniform(0.7, 1.3)
        volume.append(vol)
    
    df = pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }, index=dates)
    
    return df


def backtest_signals(df):
    """Simple backtest of the signals."""
    results = {
        'total_signals': 0,
        'strong_buy': 0,
        'buy': 0,
        'sell': 0,
        'strong_sell': 0,
        'neutral': 0
    }
    
    for signal in df['signal']:
        if pd.notna(signal):
            results['total_signals'] += 1
            if signal == 'Strong Buy':
                results['strong_buy'] += 1
            elif signal == 'Buy':
                results['buy'] += 1
            elif signal == 'Sell':
                results['sell'] += 1
            elif signal == 'Strong Sell':
                results['strong_sell'] += 1
            else:
                results['neutral'] += 1
    
    return results


def main():
    """Run the advanced example."""
    print("ICHI-VSA Advanced Usage Example")
    print("=" * 60)
    
    # Create realistic data
    print("\n1. Creating realistic market data...")
    df = create_realistic_data(200)
    print(f"   Generated {len(df)} bars with multiple trend phases")
    
    # Initialize with custom parameters
    print("\n2. Initializing ICHI-VSA with custom parameters...")
    ichi_vsa = ICHIVSA(
        tenkan_period=9,
        kijun_period=26,
        senkou_b_period=52,
        displacement=26,
        volume_ma_period=20,
        high_volume_factor=1.5,
        low_volume_factor=0.7
    )
    
    # Perform analysis
    print("\n3. Performing complete analysis...")
    result = ichi_vsa.analyze(df)
    
    # Backtest signals
    print("\n4. Signal Distribution:")
    print("-" * 60)
    backtest_results = backtest_signals(result)
    print(f"   Total Signals: {backtest_results['total_signals']}")
    print(f"   Strong Buy: {backtest_results['strong_buy']}")
    print(f"   Buy: {backtest_results['buy']}")
    print(f"   Neutral: {backtest_results['neutral']}")
    print(f"   Sell: {backtest_results['sell']}")
    print(f"   Strong Sell: {backtest_results['strong_sell']}")
    
    # Find strong signals
    print("\n5. Strong Buy Signals:")
    print("-" * 60)
    strong_buys = result[result['signal'] == 'Strong Buy']
    if len(strong_buys) > 0:
        print(strong_buys[['close', 'signal_strength', 'vsa_signal', 
                          'tk_cross', 'price_vs_cloud']].head(5).to_string())
    else:
        print("   No strong buy signals found")
    
    print("\n6. Strong Sell Signals:")
    print("-" * 60)
    strong_sells = result[result['signal'] == 'Strong Sell']
    if len(strong_sells) > 0:
        print(strong_sells[['close', 'signal_strength', 'vsa_signal', 
                           'tk_cross', 'price_vs_cloud']].head(5).to_string())
    else:
        print("   No strong sell signals found")
    
    # VSA pattern analysis
    print("\n7. VSA Pattern Statistics:")
    print("-" * 60)
    print(f"   No Demand signals: {result['no_demand'].sum()}")
    print(f"   No Supply signals: {result['no_supply'].sum()}")
    print(f"   Stopping Volume: {result['stopping_volume'].sum()}")
    print(f"   Selling Climax: {result['selling_climax'].sum()}")
    print(f"   Buying Climax: {result['buying_climax'].sum()}")
    print(f"   Weakness signals: {result['weakness'].sum()}")
    
    # Trend analysis with Ichimoku
    print("\n8. Ichimoku Trend Analysis (last 30 bars):")
    print("-" * 60)
    recent = result.tail(30)
    above_cloud = (recent['price_vs_cloud'] == 1).sum()
    below_cloud = (recent['price_vs_cloud'] == -1).sum()
    in_cloud = (recent['price_vs_cloud'] == 0).sum()
    bullish_cloud = recent['cloud_bullish'].sum()
    
    print(f"   Above Cloud: {above_cloud} bars ({above_cloud/30*100:.1f}%)")
    print(f"   Below Cloud: {below_cloud} bars ({below_cloud/30*100:.1f}%)")
    print(f"   In Cloud: {in_cloud} bars ({in_cloud/30*100:.1f}%)")
    print(f"   Bullish Cloud: {bullish_cloud} bars ({bullish_cloud/30*100:.1f}%)")
    
    # Latest comprehensive analysis
    print("\n9. Latest Comprehensive Analysis:")
    print("-" * 60)
    latest_signal = ichi_vsa.get_latest_signal(df)
    print(f"   Date: {latest_signal['date']}")
    print(f"   Close: ${latest_signal['close']:.2f}")
    print(f"   Overall Signal: {latest_signal['signal']}")
    print(f"   Signal Strength: {latest_signal['signal_strength']}")
    
    print("\n" + "=" * 60)
    print("Advanced analysis complete!")


if __name__ == "__main__":
    main()
