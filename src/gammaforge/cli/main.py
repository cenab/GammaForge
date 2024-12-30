import argparse
import logging
from datetime import datetime
from ..data.fetcher import OptionDataFetcher
from ..core.calculator import GEXCalculator
from ..visualization.plots import GEXVisualizer
from ..data.storage import HistoricalGEXTracker
from ..visualization.historical import HistoricalGEXVisualizer
from ..utils.logger import get_logger
from ..utils.formatting import format_billions

logger = get_logger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Gamma Exposure (GEX) Analysis Tool")
    
    parser.add_argument(
        "ticker",
        type=str,
        help="Ticker symbol to analyze (e.g., SPX, SPY)"
    )
    
    parser.add_argument(
        "--plot-type",
        choices=["strike", "expiry", "surface", "interactive", "all", "extended", "historical"],
        default="all",
        help="Type of plot to generate. 'extended' includes additional analyses, 'historical' includes historical analysis."
    )
    
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days for historical analysis"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level"
    )
    
    parser.add_argument(
        "--use-polygon",
        action="store_true",
        help="Use Polygon.io as data provider (requires API key)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the GEX analysis tool."""
    # Parse arguments
    args = parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(args.log_level)
    
    try:
        # Fetch data
        logger.info(f"Fetching option data for {args.ticker}")
        fetcher = OptionDataFetcher(args.ticker, use_polygon=args.use_polygon)
        spot_price, option_data = fetcher.get_option_data()
        
        logger.info(f"Option data shape: {option_data.shape}")
        logger.info(f"Option data columns: {option_data.columns}")
        logger.info(f"First few rows of option data:\n{option_data.head()}")
        
        # Calculate GEX
        calculator = GEXCalculator(spot_price, option_data)
        total_gex = calculator.get_total_gex()
        logger.info(f"Total GEX for {args.ticker}: {format_billions(total_gex)}")
        
        # Calculate GEX metrics
        gex_by_strike = calculator.get_gex_by_strike()
        gex_by_expiry = calculator.get_gex_by_expiry()
        gex_surface = calculator.get_gex_surface()
        
        logger.info(f"GEX surface shape: {gex_surface.shape}")
        logger.info(f"GEX surface index: {gex_surface.index}")
        logger.info(f"GEX surface columns: {gex_surface.columns}")
        
        # Create visualizer
        visualizer = GEXVisualizer(args.ticker)
        
        # Generate standard plots
        if args.plot_type in ["strike", "all", "extended", "historical"]:
            visualizer.plot_gex_by_strike(gex_by_strike)
            
        if args.plot_type in ["expiry", "all", "extended", "historical"]:
            visualizer.plot_gex_by_expiry(gex_by_expiry)
            
        if args.plot_type in ["surface", "all", "extended", "historical"]:
            visualizer.plot_gex_surface(gex_surface)
            
        if args.plot_type in ["interactive", "all", "extended", "historical"]:
            visualizer.plot_interactive_surface(gex_surface)
            
        # Generate extended analysis if requested
        if args.plot_type in ["extended", "historical"]:
            # Put/Call comparison
            put_call_gex = calculator.get_put_call_gex()
            visualizer.plot_put_call_comparison(put_call_gex)
            
            # Cumulative GEX
            cumulative_gex = calculator.get_cumulative_gex()
            visualizer.plot_cumulative_gex(cumulative_gex)
            
            # Weighted expiration
            weighted_days = calculator.get_weighted_expiration()
            visualizer.print_weighted_expiration(weighted_days)
            
            # IV profile
            iv_data = calculator.get_iv_profile()
            visualizer.plot_iv_profile(iv_data)
            
            # Top strikes
            top_strikes = calculator.get_top_strikes()
            visualizer.print_top_strikes(top_strikes)
            
        # Generate historical analysis if requested
        if args.plot_type == "historical":
            # Initialize historical tracker and visualizer
            historical_tracker = HistoricalGEXTracker(args.ticker, use_polygon=args.use_polygon)
            historical_visualizer = HistoricalGEXVisualizer(args.ticker)
            
            # Store today's data
            historical_tracker.store_daily_snapshot(calculator, spot_price)
            
            # Get historical data
            historical_data = historical_tracker.get_historical_gex(args.days)
            if not historical_data.empty:
                # Plot historical trends
                historical_visualizer.plot_historical_gex(historical_data)
                historical_visualizer.plot_gex_vs_price(historical_data)
                
                # Get today's strike data and plot heatmap
                strike_data = historical_tracker.get_historical_strikes(
                    datetime.now().strftime("%Y-%m-%d")
                )
                if not strike_data.empty:
                    historical_visualizer.plot_heatmap(strike_data)
                    historical_visualizer.plot_gamma_profile(strike_data)
                    
                # Print analysis results
                analysis = historical_tracker.analyze_gex_vs_price(args.days)
                historical_visualizer.print_historical_analysis(analysis)
                
                # Get and print dominant expiry info
                dominant_expiry = historical_tracker.get_dominant_expiry()
                historical_visualizer.print_dominant_expiry(dominant_expiry)
                
    except Exception as e:
        logger.error(f"Error running GEX analysis: {e}")
        raise

if __name__ == "__main__":
    main() 