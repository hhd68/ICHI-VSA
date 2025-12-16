# ICHI-VSA

**Ichimoku + Volume Spread Analysis Technical Indicator**

A Python library that combines the powerful Ichimoku Kinko Hyo indicator with Volume Spread Analysis (VSA) to provide comprehensive trading signals for technical analysis.

## Features

- **Ichimoku Kinko Hyo Indicator**: Complete implementation with all five components
  - Tenkan-sen (Conversion Line)
  - Kijun-sen (Base Line)
  - Senkou Span A (Leading Span A)
  - Senkou Span B (Leading Span B)
  - Chikou Span (Lagging Span)

- **Volume Spread Analysis (VSA)**: Detect professional money activity
  - No Demand / No Supply patterns
  - Stopping Volume
  - Selling Climax / Buying Climax
  - Weakness signals
  - Volume and spread analysis

- **Combined Signals**: Integrated analysis providing:
  - Strong Buy / Buy / Neutral / Sell / Strong Sell signals
  - Signal strength indicators
  - Multi-confirmation trading signals

## Installation

### From source

```bash
git clone https://github.com/hhd68/ICHI-VSA.git
cd ICHI-VSA
pip install -r requirements.txt
pip install -e .
```

### Requirements

- Python >= 3.7
- numpy >= 1.19.0
- pandas >= 1.1.0

## Quick Start

```python
import pandas as pd
from ichi_vsa import ICHIVSA

# Prepare your OHLCV data
df = pd.DataFrame({
    'open': [...],
    'high': [...],
    'low': [...],
    'close': [...],
    'volume': [...]
})

# Initialize the indicator
ichi_vsa = ICHIVSA()

# Analyze the data
result = ichi_vsa.analyze(df)

# Get the latest signal
signal = ichi_vsa.get_latest_signal(df)
print(f"Signal: {signal['signal']}")
print(f"Strength: {signal['signal_strength']}")
```

## Usage Examples

### Basic Usage

```python
from ichi_vsa import ICHIVSA

# Initialize with default parameters
ichi_vsa = ICHIVSA()

# Perform complete analysis
result = ichi_vsa.analyze(df)

# Access individual components
print(result[['close', 'signal', 'signal_strength']].tail())
```

### Custom Parameters

```python
from ichi_vsa import ICHIVSA

# Initialize with custom Ichimoku and VSA parameters
ichi_vsa = ICHIVSA(
    tenkan_period=9,        # Conversion line period
    kijun_period=26,        # Base line period
    senkou_b_period=52,     # Leading span B period
    displacement=26,        # Displacement for Senkou spans
    volume_ma_period=20,    # Volume MA period for VSA
    high_volume_factor=1.5, # High volume threshold
    low_volume_factor=0.7   # Low volume threshold
)

result = ichi_vsa.analyze(df)
```

### Individual Components

```python
from ichi_vsa import Ichimoku, VSA

# Use Ichimoku alone
ichimoku = Ichimoku()
ichi_result = ichimoku.calculate(df)
ichi_signals = ichimoku.get_signals(ichi_result)

# Use VSA alone
vsa = VSA()
vsa_result = vsa.calculate(df)
vsa_signals = vsa.get_signals(vsa_result)
```

## Signal Interpretation

### Signal Levels

- **Strong Buy (2)**: Multiple bullish confirmations from both Ichimoku and VSA
- **Buy (1)**: Bullish signal with partial confirmation
- **Neutral (0)**: No clear direction
- **Sell (-1)**: Bearish signal with partial confirmation
- **Strong Sell (-2)**: Multiple bearish confirmations from both Ichimoku and VSA

### Ichimoku Signals

- **TK Cross**: Tenkan-sen crossing Kijun-sen (bullish when above, bearish when below)
- **Price vs Cloud**: Price position relative to the Kumo (cloud)
- **Cloud Color**: Bullish when Senkou Span A > Senkou Span B

### VSA Patterns

- **No Demand**: Down bar on low volume with narrow spread (potentially bullish)
- **No Supply**: Up bar on low volume with narrow spread (potentially bullish)
- **Stopping Volume**: Down bar with high volume and narrow spread (bullish reversal)
- **Selling Climax**: Down bar with high volume and wide spread (bullish reversal)
- **Buying Climax**: Up bar with high volume but close not at high (bearish reversal)
- **Weakness**: Up bar with high volume but narrow spread (bearish)

## Examples

Run the provided examples:

```bash
# Basic usage example
python examples/basic_usage.py

# Advanced usage with backtesting
python examples/advanced_usage.py
```

## Testing

Run the test suite:

```bash
pip install -r requirements-dev.txt
pytest tests/
```

Run tests with coverage:

```bash
pytest --cov=ichi_vsa tests/
```

## Documentation

### Ichimoku Kinko Hyo

The Ichimoku indicator provides a complete view of support/resistance levels, trend direction, and momentum. It consists of five lines that work together to provide trading signals.

### Volume Spread Analysis (VSA)

VSA analyzes the relationship between volume and price spread to identify the activities of professional traders. It helps detect accumulation, distribution, and potential reversal points.

### Combined Analysis

The ICHI-VSA indicator combines both methodologies to provide more reliable signals by requiring confirmation from both volume-based and price-based analysis.

## Project Structure

```
ICHI-VSA/
├── ichi_vsa/
│   ├── __init__.py
│   ├── ichimoku.py      # Ichimoku indicator implementation
│   ├── vsa.py           # VSA implementation
│   └── ichi_vsa.py      # Combined ICHI-VSA indicator
├── tests/
│   ├── test_ichimoku.py
│   ├── test_vsa.py
│   └── test_ichi_vsa.py
├── examples/
│   ├── basic_usage.py
│   └── advanced_usage.py
├── requirements.txt
├── requirements-dev.txt
├── setup.py
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Disclaimer

This software is for educational and research purposes only. Do not use it for actual trading without thorough testing and understanding. Trading carries risk, and you should never trade with money you cannot afford to lose.

## Author

hhd68

## Links

- GitHub: https://github.com/hhd68/ICHI-VSA
- Issues: https://github.com/hhd68/ICHI-VSA/issues
