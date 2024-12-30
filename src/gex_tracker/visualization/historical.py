"""Module for visualizing historical GEX data and analytics."""

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots

from .config import PLOT_COLORS
from .utils import setup_plot_style, format_billions

class HistoricalGEXVisualizer:
    """Visualizes historical GEX data and analytics with various plot types."""
    
    def __init__(self, ticker: str) -> None:
        """
        Initialize the historical visualizer.
        
        Args:
            ticker: The ticker symbol to visualize.
        """
        self.ticker = ticker
        setup_plot_style()
        
    def plot_historical_gex(self, historical_data: pd.DataFrame) -> None:
        """
        Plot historical GEX time series.
        
        Args:
            historical_data: DataFrame containing historical GEX data.
        """
        plt.figure(figsize=(12, 8))
        
        # Plot total GEX
        plt.plot(
            historical_data["date"],
            historical_data["total_gex"] / 1e9,
            color=PLOT_COLORS["bars"],
            label="Total GEX",
            linewidth=2
        )
        
        # Plot call and put GEX
        plt.plot(
            historical_data["date"],
            historical_data["call_gex"] / 1e9,
            color="#1f77b4",
            label="Call GEX",
            alpha=0.7
        )
        plt.plot(
            historical_data["date"],
            historical_data["put_gex"] / 1e9,
            color="#d62728",
            label="Put GEX",
            alpha=0.7
        )
        
        plt.grid(color=PLOT_COLORS["grid"])
        plt.title(f"{self.ticker} Historical GEX", fontweight="heavy")
        plt.xlabel("Date", fontweight="heavy")
        plt.ylabel("Gamma Exposure (Bn$)", fontweight="heavy")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    def plot_gex_vs_price(self, historical_data: pd.DataFrame) -> None:
        """
        Plot GEX vs price movement correlation.
        
        Args:
            historical_data: DataFrame containing historical GEX and price data.
        """
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=(
                f"{self.ticker} Price vs GEX",
                "Daily Changes Correlation"
            )
        )
        
        # Price and GEX time series
        fig.add_trace(
            go.Scatter(
                x=historical_data["date"],
                y=historical_data["spot_price"],
                name="Price",
                line=dict(color="#2ca02c")
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=historical_data["date"],
                y=historical_data["total_gex"] / 1e9,
                name="GEX (Bn$)",
                line=dict(color=PLOT_COLORS["bars"]),
                yaxis="y2"
            ),
            row=1, col=1
        )
        
        # Daily changes scatter
        fig.add_trace(
            go.Scatter(
                x=historical_data["gex_change"],
                y=historical_data["price_change"],
                mode="markers",
                name="Daily Changes",
                marker=dict(
                    color=PLOT_COLORS["bars"],
                    size=8,
                    opacity=0.6
                )
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text=f"{self.ticker} GEX vs Price Analysis",
            yaxis2=dict(
                title="GEX (Bn$)",
                overlaying="y",
                side="right"
            )
        )
        
        fig.show()
        
    def plot_heatmap(self, strike_data: pd.DataFrame) -> None:
        """
        Plot GEX heatmap (strike vs expiry).
        
        Args:
            strike_data: DataFrame containing strike-level GEX data.
        """
        # Pivot data for heatmap
        heatmap_data = strike_data.pivot_table(
            values="gex",
            index="strike",
            columns="expiry",
            aggfunc="sum"
        ) / 1e9
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            heatmap_data,
            cmap="RdBu",
            center=0,
            cbar_kws={"label": "GEX (Bn$)"}
        )
        
        plt.title(f"{self.ticker} GEX Heatmap", fontweight="heavy")
        plt.xlabel("Expiration Date", fontweight="heavy")
        plt.ylabel("Strike Price", fontweight="heavy")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    def plot_gamma_profile(self, strike_data: pd.DataFrame) -> None:
        """
        Plot gamma profile showing flip points.
        
        Args:
            strike_data: DataFrame containing strike-level GEX data.
        """
        # Calculate net gamma by strike
        net_gamma = strike_data.groupby("strike")["gex"].sum() / 1e9
        
        plt.figure(figsize=(12, 6))
        plt.plot(
            net_gamma.index,
            net_gamma.values,
            color=PLOT_COLORS["bars"],
            linewidth=2
        )
        
        # Add horizontal line at y=0
        plt.axhline(y=0, color="white", linestyle="--", alpha=0.5)
        
        # Find and mark flip points
        signs = np.sign(net_gamma)
        sign_changes = ((signs.shift(1) * signs) < 0)
        flip_points = net_gamma[sign_changes]
        
        if not flip_points.empty:
            plt.scatter(
                flip_points.index,
                flip_points.values,
                color="#d62728",
                s=100,
                label="Flip Points",
                zorder=5
            )
            
        plt.grid(color=PLOT_COLORS["grid"])
        plt.title(f"{self.ticker} Gamma Profile", fontweight="heavy")
        plt.xlabel("Strike Price", fontweight="heavy")
        plt.ylabel("Net Gamma (Bn$)", fontweight="heavy")
        plt.legend()
        plt.show()
        
    def print_historical_analysis(self, analysis_results: Dict) -> None:
        """
        Print historical analysis results.
        
        Args:
            analysis_results: Dictionary containing analysis metrics.
        """
        print("\nHistorical GEX Analysis:")
        print(f"GEX vs Price Correlation: {analysis_results['correlation']:.3f}")
        print("\nGEX Percentiles:")
        print(f"5th percentile: {format_billions(analysis_results['gex_percentiles'][0.05])}")
        print(f"95th percentile: {format_billions(analysis_results['gex_percentiles'][0.95])}")
        
        print("\nExtreme GEX Days:")
        for _, row in analysis_results["extreme_days"].iterrows():
            print(f"Date: {row['date']}, GEX: {format_billions(row['total_gex'])}")
            
    def print_dominant_expiry(self, dominant_expiry_info: Dict) -> None:
        """
        Print dominant expiry information.
        
        Args:
            dominant_expiry_info: Dictionary containing dominant expiry metrics.
        """
        print(f"\nDominant Expiration Date: {dominant_expiry_info['dominant_expiry']}")
        print(f"Total GEX: {format_billions(dominant_expiry_info['gex'])}")
        print(f"Absolute GEX: {format_billions(dominant_expiry_info['abs_gex'])}") 