# GammaForge

A professional-grade Python toolkit for analyzing Gamma Exposure (GEX) in options markets. GammaForge provides comprehensive tools for real-time tracking, historical analysis, and visualization of options market gamma exposure.

## Features

### Basic GEX Analysis
1. **Total GEX Calculation**
   - Computes aggregate gamma exposure across all option contracts
   - Accounts for both calls and puts with proper sign adjustment
   - Automatically filters for relevant strikes within ±15% of spot price
   - Results displayed in billions of dollars for easy interpretation

### Core Visualizations

1. **GEX by Strike Price**
   - Bar plot visualization showing gamma exposure at each strike price
   - Positive values indicate dealer long gamma (need to sell into strength)
   - Negative values indicate dealer short gamma (need to buy into weakness)
   - Automatically filters for strikes within ±15% of current price
   - Clear gridlines and labels for professional presentation
   - Y-axis scaled in billions of dollars for easy interpretation

2. **GEX by Expiration**
   - Bar plot showing gamma exposure distribution across expiration dates
   - Helps identify which expiration dates have the most significant impact
   - Rotated x-axis labels for better readability
   - Automatic date formatting and sorting
   - Includes all expirations up to one year out
   - Y-axis scaled in billions of dollars

3. **GEX Surface (3D)**
   - Three-dimensional surface plot combining strikes and expirations
   - X-axis: Strike prices
   - Y-axis: Expiration dates
   - Z-axis: Gamma exposure magnitude
   - Uses seismic color scheme (red/blue) for intuitive visualization
   - Includes colorbar for reference
   - Proper axis labeling and title formatting

4. **Interactive GEX Surface**
   - Interactive 3D surface plot powered by Plotly
   - Features:
     - Zoom in/out capability
     - Rotation in any direction
     - Hover tooltips with exact values
     - Pan and reset view options
   - Professional RdBu color scheme
   - Customizable plot size (default: 1000x800)
   - Responsive design for different screen sizes

### Advanced Analytics

1. **Put vs Call GEX Comparison**
   - Bar plot comparing three key metrics:
     - Call option gamma exposure
     - Put option gamma exposure
     - Net gamma exposure (calls + puts)
   - Color-coded bars for easy distinction
   - Value labels on top of each bar
   - Gridlines for better readability
   - Values scaled in billions of dollars

2. **Cumulative GEX Distribution**
   - Line plot showing cumulative gamma exposure across strikes
   - Helps identify:
     - Key gamma levels
     - Areas of gamma accumulation
     - Potential support/resistance levels
   - Smooth line rendering with appropriate thickness
   - Professional gridlines and formatting
   - Values scaled in billions of dollars

3. **Implied Volatility Profile**
   - Scatter plot of implied volatility across strikes
   - Separate visualization for calls and puts
   - Features:
     - Blue dots for calls
     - Red dots for puts
     - Clear legend
     - Strike price on x-axis
     - IV percentage on y-axis
   - Limited to options expiring within 30 days
   - Helps identify volatility skew and term structure

4. **Top Strikes Analysis**
   - Detailed breakdown of most significant gamma strikes
   - Shows:
     - Top positive GEX strikes (dealer long gamma)
     - Top negative GEX strikes (dealer short gamma)
     - Exact GEX value at each strike
   - Default: top 5 strikes in each category
   - Values formatted in billions with proper sign

5. **Weighted Expiration Analysis**
   - Calculates average days to expiration weighted by gamma exposure
   - Helps understand the temporal concentration of gamma
   - Takes into account:
     - Days to expiration for each option
     - Absolute gamma exposure as weights
   - Results displayed in days with one decimal precision

### Data Provider Support

1. **CBOE Integration**
   - Primary data source for delayed options quotes
   - Features:
     - Automatic handling of different URL patterns
     - Support for both standard and underscore-prefixed symbols
     - Robust error handling and fallback mechanisms
     - Automatic retry logic
     - Proper parsing of option symbols

2. **Polygon.io Support**
   - Alternative data source for real-time and historical data
   - Requires API key configuration
   - Features:
     - Real-time WebSocket connection for live data
     - Historical data access
     - Complete options chain retrieval
     - Greeks calculation
     - Volume and open interest tracking

3. **Caching System**
   - Intelligent caching to minimize API calls
   - Features:
     - Configurable cache duration (default: 1 hour)
     - Automatic cache invalidation
     - JSON-based storage format
     - Proper error handling
     - Cache directory management

### Command-Line Interface

The toolkit provides a powerful CLI with various options:

```bash
# Basic GEX analysis
gammaforge SPY

# Specific plot type
gammaforge SPY --plot-type strike
gammaforge SPY --plot-type expiry
gammaforge SPY --plot-type surface
gammaforge SPY --plot-type interactive

# All standard plots
gammaforge SPY --plot-type all

# Extended analysis (includes all plots plus advanced analytics)
gammaforge SPY --plot-type extended

# Use Polygon.io as data source
gammaforge SPY --use-polygon

# Set custom log level
gammaforge SPY --log-level DEBUG
```

### Plot Customization

All visualizations feature professional styling:
- Consistent color scheme across all plots
- Heavy font weights for better readability
- Clear axis labels and titles
- Proper scaling of values (Billions/Millions)
- Grid lines for better data reading
- Alpha transparency for overlapping elements
- Automatic figure sizing
- Date formatting for time-based plots
- Color schemes optimized for both light and dark themes

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