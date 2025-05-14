# Representative Weather Year Finder (rwy-finder)

## Overview
This tool identifies Representative Weather Years (RWYs) from historical weather data for use in power-market simulations. It ranks candidate years using multiple distance metrics and exports the top candidates and best RWYs for further analysis.

## Setup
1. Create a Python 3.12+ virtual environment in `.venv`:
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```
2. Ensure the `data/` directory contains:
   - `weather_history.parquet`
   - `weather_metric_weights.csv`
3. Set environment variables (already in `.env`):
   - `DATA_PATH=data`

## Usage
Run the main script:
```cmd
python main.py
```

Outputs will be written to a timestamped subdirectory under `data/`.

## Testing
Run all unit tests with:
```cmd
pytest
```

## Documentation
- See `docs/rwy-finder-prd.md` for requirements.
- See `docs/changelog.md` for changes.
