#!/bin/bash

# Create necessary directories
mkdir -p src/gex_tracker/{core,data,visualization,utils,cli}

# Move files to their new locations
mv src/gex_tracker/gex_calculator.py src/gex_tracker/core/calculator.py
mv src/gex_tracker/data_fetcher.py src/gex_tracker/data/fetcher.py
mv src/gex_tracker/historical_tracker.py src/gex_tracker/data/storage.py
mv src/gex_tracker/realtime_handler.py src/gex_tracker/data/realtime.py
mv src/gex_tracker/visualizer.py src/gex_tracker/visualization/plots.py
mv src/gex_tracker/historical_visualizer.py src/gex_tracker/visualization/historical.py
mv src/gex_tracker/main.py src/gex_tracker/cli/main.py
mv src/gex_tracker/realtime_cli.py src/gex_tracker/cli/realtime.py
mv src/gex_tracker/config.py src/gex_tracker/utils/config.py 