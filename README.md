# GammaForge

A professional-grade Python toolkit for analyzing Gamma Exposure (GEX) in options markets. GammaForge provides comprehensive tools for real-time tracking, historical analysis, and visualization of options market gamma exposure.

## Features

- Real-time GEX tracking using Polygon.io WebSocket feed
- Historical GEX analysis and visualization
- Advanced analytics including:
  - Call vs Put GEX separation
  - GEX by moneyness analysis
  - Cumulative GEX distribution
  - Zero gamma point detection
  - Weighted metrics calculation
- Scenario analysis capabilities
- Flow analysis and tracking
- Interactive visualizations
- Customizable dark/light themes
- Command-line interface
- Modular, extensible design

## Installation

```bash
# Clone the repository
git clone https://github.com/cenab/GammaForge.git
cd GammaForge

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]
```

## Usage

### Basic GEX Analysis

```python
from gammaforge import GEXAnalyzer

# Initialize analyzer
analyzer = GEXAnalyzer()

# Analyze single ticker
analyzer.analyze('SPY')

# Plot GEX by strike
analyzer.plot_gex_by_strike()

# Plot GEX by expiration
analyzer.plot_gex_by_expiration()

# Plot GEX surface
analyzer.plot_gex_surface()
```

### Real-time Tracking

```bash
# Start real-time tracking for SPY
gammaforge-rt SPY

# Start with custom update interval
gammaforge-rt SPY --interval 60
```

### Historical Analysis

```python
from gammaforge import HistoricalTracker

# Initialize tracker
tracker = HistoricalTracker()

# Load historical data
tracker.load_data('SPY', days=30)

# Plot historical GEX
tracker.plot_historical_gex()

# Analyze GEX vs price correlation
tracker.analyze_correlation()
```

## Configuration

Create a `.env` file in the project root:

```
# Polygon.io API configuration
POLYGON_API_KEY=your_api_key_here
```

## Development

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run type checking
mypy src

# Run linting
flake8 src

# Format code
black src
isort src
```

## Documentation

For detailed documentation of all features and APIs, please see the [DOCUMENTATION.md](DOCUMENTATION.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 