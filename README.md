# GEX Tracker Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Core Functionality](#core-functionality)
3. [Advanced GEX Analysis](#advanced-gex-analysis)
4. [Black-Scholes Calculations](#black-scholes-calculations)
5. [Scenario Analysis](#scenario-analysis)
6. [Flow Analysis](#flow-analysis)
7. [Utilities](#utilities)

## Introduction

GEX Tracker is a comprehensive toolkit for analyzing Gamma Exposure (GEX) in options markets. GEX represents the rate of change in market makers' delta hedging requirements with respect to changes in the underlying asset's price. High positive GEX indicates potential resistance to upward price movement, while negative GEX suggests potential acceleration of downward moves.

## Core Functionality

### Data Models

#### `OptionData`
- Container for raw option data
- Fields: type (call/put), strike, expiration, open_interest, volume, gamma, etc.
- Used as input for GEX calculations

#### `GEXResult`
- Container for GEX calculation results
- Fields: total_gex, call_gex, put_gex, spot_price, timestamp
- Provides a standardized format for GEX analysis output

#### `HistoricalGEX`
- Container for historical GEX data
- Fields: date, gex_values, spot_prices
- Used for tracking GEX changes over time

#### `GEXSurface`
- Container for 3D GEX visualization data
- Fields: strikes, expirations, gex_values
- Used for creating GEX heatmaps and surface plots

### Basic Calculations

#### `GEXCalculator`
- Main class for GEX calculations
- Methods:
  - `calculate_total_gex()`: Computes net GEX across all options
  - `calculate_gex_by_strike()`: Groups GEX by strike price
  - `calculate_gex_by_expiry()`: Groups GEX by expiration date
  - `calculate_gex_surface()`: Creates 3D GEX surface

## Advanced GEX Analysis

### Call/Put GEX Separation (`compute_call_put_gex`)
```python
def compute_call_put_gex(df, spot_price, contract_size=100) -> tuple[float, float, float]
```
- Separates GEX into call and put components
- Helps identify whether dealers are net long/short gamma in calls vs puts
- Returns (call_gex, put_gex, total_gex)
- Interpretation:
  - Positive call GEX: Dealers are long calls, potential resistance
  - Negative put GEX: Dealers are short puts, potential acceleration

### GEX by Moneyness (`compute_gex_by_moneyness`)
```python
def compute_gex_by_moneyness(df, spot_price, bins=None) -> pd.Series
```
- Groups GEX by strike/spot price ratio
- Default bins: [0.8, 0.9, 1.0, 1.1, 1.2]
- Helps identify concentration of gamma exposure relative to spot
- Interpretation:
  - High GEX at-the-money: Strong pinning effect
  - High GEX out-of-the-money: Potential resistance/support levels

### Cumulative GEX (`compute_cumulative_gex`)
```python
def compute_cumulative_gex(df) -> pd.DataFrame
```
- Calculates running sum of GEX across strikes
- Shows total gamma exposure up to each strike level
- Useful for identifying major gamma levels
- Returns DataFrame with columns:
  - strike: Option strike price
  - GEX: GEX at that strike
  - cum_gex: Cumulative GEX up to that strike

### Zero Gamma Points (`find_zero_gamma`)
```python
def find_zero_gamma(df, spot_price, bounds_pct=(0.8, 1.2)) -> float
```
- Finds price level where net gamma exposure is zero
- Important for identifying potential market inflection points
- Uses numerical methods (bisection) to find the root
- Interpretation:
  - Above zero gamma: Positive gamma, stabilizing
  - Below zero gamma: Negative gamma, destabilizing

### Weighted Metrics (`compute_weighted_metrics`)
```python
def compute_weighted_metrics(df) -> dict
```
- Calculates GEX-weighted strike and expiration
- Helps identify center of gravity for options positioning
- Returns:
  - weighted_strike: Average strike weighted by absolute GEX
  - weighted_expiry_days: Average days to expiry weighted by absolute GEX

## Black-Scholes Calculations

### Option Greeks (`black_scholes_greeks`)
```python
def black_scholes_greeks(S, K, T, r, sigma, option_type='C') -> Dict[str, float]
```
- Calculates complete set of option Greeks
- Parameters:
  - S: Spot price
  - K: Strike price
  - T: Time to expiry (years)
  - r: Risk-free rate
  - sigma: Implied volatility
  - option_type: 'C' for call, 'P' for put
- Returns dictionary of Greeks:
  - delta: Price sensitivity
  - gamma: Delta sensitivity
  - theta: Time decay
  - vega: Volatility sensitivity
  - rho: Interest rate sensitivity
  - charm: Delta decay
  - vanna: Delta-volatility sensitivity
  - speed: Gamma sensitivity
  - color: Gamma decay

### Bulk Greeks Calculation (`compute_option_greeks`)
```python
def compute_option_greeks(df, spot_price, risk_free_rate=0.01) -> Dict[str, np.ndarray]
```
- Efficiently computes Greeks for multiple options
- Takes DataFrame with columns: type, strike, T, iv
- Returns arrays of Greeks for all options
- Used in scenario analysis and risk calculations

## Scenario Analysis

### Spot Price Shock (`scenario_spot_shock`)
```python
def scenario_spot_shock(df, spot_price, shift_pct=0.05) -> tuple[float, float]
```
- Simulates impact of spot price movement on GEX
- Default: ±5% price movement
- Returns new spot price and resulting GEX
- Useful for stress testing and risk assessment

### Volatility Shock (`scenario_vol_shock`)
```python
def scenario_vol_shock(df, spot_price, vol_shift=0.05) -> float
```
- Simulates impact of volatility change on GEX
- Default: ±5 volatility points
- Recalculates gamma using new volatility
- Important for volatility regime change analysis

### Time Decay (`scenario_time_decay`)
```python
def scenario_time_decay(df, spot_price, days_forward=7) -> float
```
- Projects GEX forward in time
- Accounts for theta decay and option expiration
- Helps understand evolution of gamma exposure
- Critical for expiration week planning

### Combined Scenarios (`scenario_all`)
```python
def scenario_all(df, spot_price, **kwargs) -> dict
```
- Runs multiple scenario analyses
- Combines spot, volatility, and time scenarios
- Returns comprehensive scenario results
- Perfect for risk reports and stress testing

## Flow Analysis

### Open Interest Changes (`compare_oi_changes`)
```python
def compare_oi_changes(df_today, df_yesterday) -> pd.DataFrame
```
- Tracks changes in open interest
- Identifies new positions vs closed positions
- Important for understanding dealer positioning changes
- Returns detailed OI change analysis

### Volume Analysis (`analyze_volume_vs_oi`)
```python
def analyze_volume_vs_oi(df, threshold=2.0) -> pd.DataFrame
```
- Analyzes trading volume relative to open interest
- Identifies unusual activity (volume > 2x OI)
- Groups analysis by strike and option type
- Critical for spotting significant options activity

### Large Trade Tracking (`track_large_trades`)
```python
def track_large_trades(df, min_volume=100, min_notional=1e6) -> pd.DataFrame
```
- Identifies significant options trades
- Filters by volume and notional value
- Helps spot institutional activity
- Returns sorted list of large trades

### Flow Metrics (`aggregate_flow_metrics`)
```python
def aggregate_flow_metrics(df) -> dict
```
- Calculates comprehensive flow statistics
- Includes:
  - Total volume and open interest
  - Call/put volume ratios
  - Volume/OI ratios
  - Percentage distribution of activity
- Essential for daily market overview

## Utilities

### Price Bounds (`calculate_price_bounds`)
```python
def calculate_price_bounds(spot_price, percentage=0.15) -> tuple[float, float]
```
- Calculates reasonable price ranges for analysis
- Used in scenario analysis and zero-gamma finding
- Default: ±15% from current spot
- Returns (lower_bound, upper_bound)

### Date Utilities (`get_one_year_date`)
```python
def get_one_year_date() -> datetime
```
- Calculates dates for various analyses
- Handles market calendar adjustments
- Used in historical analysis and time decay calculations

## Best Practices

1. **Data Quality**
   - Ensure clean, accurate options data
   - Check for missing values and outliers
   - Verify implied volatility calculations

2. **Risk Management**
   - Monitor GEX levels relative to historical ranges
   - Pay attention to expiration concentrations
   - Watch for unusual changes in dealer positioning

3. **Analysis Workflow**
   - Start with basic GEX calculations
   - Add scenario analysis for risk assessment
   - Monitor flow metrics for positioning changes
   - Use advanced analytics for deeper insights

4. **Interpretation Guidelines**
   - High positive GEX: Potential resistance/stability
   - High negative GEX: Potential acceleration/instability
   - Zero-gamma points: Possible inflection levels
   - Large OI changes: Significant positioning shifts 