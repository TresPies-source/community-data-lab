# Starter Kit

Parameterized Python scripts (stdlib only) for building spatial equity data infrastructure in any US city.

## Setup

1. Copy `config_example.json` to `config.json`
2. Edit `config.json` with your geography (state FIPS, county FIPS, city name)
3. Download your county's census tract GeoJSON (instructions in config)
4. Run scripts in order:

```bash
python3 01_fetch_census.py          # Demographics, income, housing, health insurance
python3 02_process_gtfs.py          # Transit frequency by tract (requires GTFS feed)
python3 03_composite_scoring.py     # Equity vulnerability scores
python3 04_build_viewer.py          # Standalone HTML data viewer
```

## Requirements

- Python 3.8+
- No external packages (stdlib only)
- Census API (no key required for small queries)
- GTFS feed from your local transit agency (download to `data/gtfs/`)
- Census tract GeoJSON for your county (download from Census TIGER/Line)

## File Structure

```
starter-kit/
  config_example.json       — Configuration template
  stats_lib.py              — Shared statistics library (OLS, Pearson r, scoring)
  geo_lib.py                — Shared geometry library (point-in-polygon, tract matching)
  01_fetch_census.py        — Census ACS data fetcher
  02_process_gtfs.py        — GTFS transit frequency processor
  03_composite_scoring.py   — Equity composite scoring engine
  04_build_viewer.py        — Standalone HTML viewer builder
```
