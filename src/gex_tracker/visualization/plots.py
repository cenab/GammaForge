import matplotlib.pyplot as plt
from matplotlib import dates
import plotly.graph_objects as go
import numpy as np
from .config import PLOT_COLORS
from .utils import setup_plot_style, format_billions

class GEXVisualizer:
    """Class to handle GEX visualization."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        setup_plot_style()
        
    def plot_gex_by_strike(self, gex_by_strike):
        """Plot gamma exposure by strike price."""
        plt.figure(figsize=(12, 6))
        plt.bar(
            gex_by_strike.index,
            gex_by_strike.values,
            color=PLOT_COLORS["bars"],
            alpha=0.5
        )
        plt.grid(color=PLOT_COLORS["grid"])
        plt.xticks(fontweight="heavy")
        plt.yticks(fontweight="heavy")
        plt.xlabel("Strike Price", fontweight="heavy")
        plt.ylabel("Gamma Exposure (Bn$ / %)", fontweight="heavy")
        plt.title(f"{self.ticker} GEX by Strike", fontweight="heavy")
        plt.show()
        
    def plot_gex_by_expiry(self, gex_by_expiry):
        """Plot gamma exposure by expiration date."""
        plt.figure(figsize=(12, 6))
        plt.bar(
            gex_by_expiry.index,
            gex_by_expiry.values,
            color=PLOT_COLORS["bars"],
            alpha=0.5
        )
        plt.grid(color=PLOT_COLORS["grid"])
        plt.xticks(rotation=45, fontweight="heavy")
        plt.yticks(fontweight="heavy")
        plt.xlabel("Expiration Date", fontweight="heavy")
        plt.ylabel("Gamma Exposure (Bn$ / %)", fontweight="heavy")
        plt.title(f"{self.ticker} GEX by Expiration", fontweight="heavy")
        plt.tight_layout()
        plt.show()
        
    def plot_gex_surface(self, gex_surface):
        """Plot 3D surface of gamma exposure."""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection="3d")
        
        X, Y = np.meshgrid(gex_surface.columns, gex_surface.index)
        Z = gex_surface.values
        
        surf = ax.plot_surface(
            X, Y, Z,
            cmap="seismic_r",
            alpha=0.8
        )
        
        ax.set_xlabel("Strike Price", fontweight="heavy")
        ax.set_ylabel("Expiration Date", fontweight="heavy")
        ax.set_zlabel("Gamma Exposure (M$ / %)", fontweight="heavy")
        
        plt.colorbar(surf)
        plt.title(f"{self.ticker} GEX Surface", fontweight="heavy")
        plt.show()
        
    def plot_interactive_surface(self, gex_surface):
        """Create interactive 3D surface plot using plotly."""
        fig = go.Figure(data=[
            go.Surface(
                x=gex_surface.columns,
                y=gex_surface.index,
                z=gex_surface.values,
                colorscale="RdBu"
            )
        ])
        
        fig.update_layout(
            title=f"{self.ticker} Interactive GEX Surface",
            scene=dict(
                xaxis_title="Strike Price",
                yaxis_title="Expiration Date",
                zaxis_title="Gamma Exposure (M$ / %)"
            ),
            width=1000,
            height=800
        )
        
        fig.show()
        
    def plot_put_call_comparison(self, put_call_gex):
        """Plot comparison of put vs call GEX."""
        plt.figure(figsize=(8, 6))
        labels = ["Calls", "Puts", "Net"]
        values = [
            put_call_gex["calls"] / 1e9,
            put_call_gex["puts"] / 1e9,
            put_call_gex["net"] / 1e9
        ]
        colors = ["#1f77b4", "#d62728", "#2ca02c"]
        
        plt.bar(labels, values, color=colors, alpha=0.7)
        plt.grid(color=PLOT_COLORS["grid"], axis="y", linestyle="--")
        plt.title(f"{self.ticker} Call vs Put GEX", fontweight="heavy")
        plt.ylabel("Gamma Exposure (Bn$)", fontweight="heavy")
        
        # Add value labels on top of bars
        for i, v in enumerate(values):
            plt.text(i, v, f"{v:.2f}B", ha="center", va="bottom", fontweight="heavy")
            
        plt.show()
        
    def plot_cumulative_gex(self, cumulative_data):
        """Plot cumulative GEX distribution."""
        plt.figure(figsize=(12, 6))
        plt.plot(
            cumulative_data["strike"],
            cumulative_data["cumulative_gex"] / 1e9,
            color=PLOT_COLORS["bars"],
            linewidth=2
        )
        plt.grid(color=PLOT_COLORS["grid"])
        plt.title(f"{self.ticker} Cumulative GEX Distribution", fontweight="heavy")
        plt.xlabel("Strike Price", fontweight="heavy")
        plt.ylabel("Cumulative GEX (Bn$)", fontweight="heavy")
        plt.show()
        
    def plot_iv_profile(self, iv_data):
        """Plot implied volatility profile."""
        if iv_data is None:
            return
            
        plt.figure(figsize=(12, 6))
        
        # Separate calls and puts
        calls = iv_data[iv_data["type"] == "C"]
        puts = iv_data[iv_data["type"] == "P"]
        
        plt.scatter(calls["strike"], calls["iv"], color="#1f77b4", alpha=0.7, label="Calls IV")
        plt.scatter(puts["strike"], puts["iv"], color="#d62728", alpha=0.7, label="Puts IV")
        
        plt.grid(color=PLOT_COLORS["grid"])
        plt.title(f"{self.ticker} Implied Volatility Profile (Next 30 Days)", fontweight="heavy")
        plt.xlabel("Strike Price", fontweight="heavy")
        plt.ylabel("Implied Volatility", fontweight="heavy")
        plt.legend()
        plt.show()
        
    def print_top_strikes(self, top_strikes):
        """Print top strikes information."""
        print(f"\nTop Positive GEX Strikes for {self.ticker}:")
        for strike, gex in top_strikes["positive"].items():
            print(f"Strike {strike}: {format_billions(gex)}")
            
        print(f"\nTop Negative GEX Strikes for {self.ticker}:")
        for strike, gex in top_strikes["negative"].items():
            print(f"Strike {strike}: {format_billions(gex)}")
            
    def print_weighted_expiration(self, weighted_days: float):
        """Print weighted average expiration information."""
        print(f"\nWeighted Average Days to Expiration: {weighted_days:.1f} days") 