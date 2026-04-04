#!/usr/bin/env python3
"""
Community Data Lab — Census ACS Data Fetcher
Parameterized by config.json. stdlib only.

Fetches tract-level demographics, income, housing cost burden, and uninsured
rates for the configured county from the Census ACS 5-Year API.

Usage: python3 01_fetch_census.py
Requires: config.json (copy from config_example.json)

Output:
  data/processed/demographics.json   — Income, poverty, race by tract
  data/processed/cost_burden.json    — Housing cost burden by tract
  data/processed/uninsured.json      — Uninsured rate by tract
  data/processed/fetch_manifest.json — Record of all fetched data
"""

import urllib.request
import json
import os
import datetime

from geo_lib import load_config, load_tracts


def fetch_api(url, label):
    """Fetch data from Census API. Returns list of rows (first row is header)."""
    print(f"Fetching {label}...")
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                raise RuntimeError(f"{label} API returned status {resp.status}")
            data = json.loads(resp.read().decode())
        print(f"  Received {len(data) - 1} rows")
        return data
    except Exception as e:
        print(f"  ERROR fetching {label}: {e}")
        return None


def safe_int(val):
    if val is None:
        return None
    try:
        v = int(val)
        return None if v == -666666666 else v
    except (ValueError, TypeError):
        return None


def safe_pct(num, denom):
    if num is None or denom is None or denom == 0:
        return None
    return round(num / denom * 100, 1)


def main():
    config = load_config()
    geo = config["geography"]
    census = config["census"]
    paths = config["data_paths"]

    state = geo["state_fips"]
    county = geo["county_fips"]
    year = census["acs_year"]

    # Ensure output directories exist
    os.makedirs(paths["processed"], exist_ok=True)
    os.makedirs(paths["raw"], exist_ok=True)

    # Load valid GEOIDs from tracts GeoJSON (if available)
    valid_geoids = None
    tracts_path = paths.get("tracts_geojson")
    if tracts_path and os.path.exists(tracts_path):
        _, valid_geoids = load_tracts(tracts_path)
        print(f"Loaded {len(valid_geoids)} valid tract GEOIDs from {tracts_path}")

    manifest = {"fetched_at": datetime.datetime.now().isoformat(), "datasets": {}}

    # ── 1. Demographics (income, poverty, race) ──

    demo_vars = "B19013_001E,B17001_001E,B17001_002E,B03002_001E,B03002_003E,B01001_001E"
    demo_url = (
        f"https://api.census.gov/data/{year}/acs/acs5"
        f"?get=NAME,{demo_vars}"
        f"&for=tract:*&in=state:{state}%20county:{county}"
    )

    raw = fetch_api(demo_url, f"ACS {year} Demographics")
    demographics = []
    if raw:
        header = raw[0]
        for row in raw[1:]:
            geoid = row[header.index("state")] + row[header.index("county")] + row[header.index("tract")]
            if valid_geoids and geoid not in valid_geoids:
                continue

            total_pop = safe_int(row[header.index("B03002_001E")])
            white_nh = safe_int(row[header.index("B03002_003E")])
            pov_total = safe_int(row[header.index("B17001_001E")])
            pov_below = safe_int(row[header.index("B17001_002E")])

            pct_nonwhite = None
            if total_pop and white_nh is not None:
                pct_nonwhite = round((total_pop - white_nh) / total_pop * 100, 1) if total_pop > 0 else None

            demographics.append({
                "geoid": geoid,
                "name": row[header.index("NAME")],
                "median_income": safe_int(row[header.index("B19013_001E")]),
                "total_population": total_pop,
                "pct_nonwhite": pct_nonwhite,
                "poverty_rate": safe_pct(pov_below, pov_total),
                "vintage": f"ACS {year} 5-Year"
            })

        demo_path = os.path.join(paths["processed"], "demographics.json")
        with open(demo_path, "w") as f:
            json.dump(demographics, f, indent=2)
        print(f"Wrote {len(demographics)} tracts to {demo_path}")
        manifest["datasets"]["demographics"] = {
            "count": len(demographics), "source": f"ACS {year} 5-Year", "success": True
        }

    # ── 2. Housing Cost Burden ──

    cb_vars = "B25106_002E,B25106_006E,B25106_024E,B25106_028E"
    cb_url = (
        f"https://api.census.gov/data/{year}/acs/acs5"
        f"?get=NAME,{cb_vars}"
        f"&for=tract:*&in=state:{state}%20county:{county}"
    )

    raw_cb = fetch_api(cb_url, f"ACS {year} Cost Burden")
    cost_burden = []
    if raw_cb:
        header = raw_cb[0]
        for row in raw_cb[1:]:
            geoid = row[header.index("state")] + row[header.index("county")] + row[header.index("tract")]
            if valid_geoids and geoid not in valid_geoids:
                continue

            owner_total = safe_int(row[header.index("B25106_002E")])
            owner_burdened = safe_int(row[header.index("B25106_006E")])
            renter_total = safe_int(row[header.index("B25106_024E")])
            renter_burdened = safe_int(row[header.index("B25106_028E")])
            total_burdened = None
            total_hh = None
            if owner_burdened is not None and renter_burdened is not None:
                total_burdened = owner_burdened + renter_burdened
            if owner_total is not None and renter_total is not None:
                total_hh = owner_total + renter_total

            cost_burden.append({
                "geoid": geoid,
                "owner_total": owner_total,
                "owner_cost_burdened": owner_burdened,
                "renter_total": renter_total,
                "renter_cost_burdened": renter_burdened,
                "total_cost_burdened": total_burdened,
                "pct_cost_burdened": safe_pct(total_burdened, total_hh),
                "vintage": f"ACS {year} 5-Year"
            })

        cb_path = os.path.join(paths["processed"], "cost_burden.json")
        with open(cb_path, "w") as f:
            json.dump(cost_burden, f, indent=2)
        print(f"Wrote {len(cost_burden)} tracts to {cb_path}")
        manifest["datasets"]["cost_burden"] = {
            "count": len(cost_burden), "source": f"ACS {year} 5-Year (B25106)", "success": True
        }

    # ── 3. Uninsured Rate ──

    ui_url = (
        f"https://api.census.gov/data/{year}/acs/acs5/subject"
        f"?get=NAME,S2701_C01_001E,S2701_C05_001E"
        f"&for=tract:*&in=state:{state}%20county:{county}"
    )

    raw_ui = fetch_api(ui_url, f"ACS {year} Uninsured Rate")
    uninsured = []
    if raw_ui:
        header = raw_ui[0]
        for row in raw_ui[1:]:
            geoid = row[header.index("state")] + row[header.index("county")] + row[header.index("tract")]
            if valid_geoids and geoid not in valid_geoids:
                continue

            total_pop = safe_int(row[header.index("S2701_C01_001E")])
            # S2701_C05_001E returns a percentage, not a count
            raw_pct = row[header.index("S2701_C05_001E")]
            pct_uninsured = None
            unins_count = None
            try:
                if raw_pct is not None and raw_pct not in ("", "*", "-"):
                    val = float(raw_pct)
                    if val != -666666666 and 0 <= val <= 100:
                        pct_uninsured = round(val, 1)
                        if total_pop is not None:
                            unins_count = int(round(total_pop * pct_uninsured / 100))
            except (ValueError, TypeError):
                pass

            uninsured.append({
                "geoid": geoid,
                "total_population": total_pop,
                "uninsured_count": unins_count,
                "pct_uninsured": pct_uninsured,
                "vintage": f"ACS {year} 5-Year"
            })

        ui_path = os.path.join(paths["processed"], "uninsured.json")
        with open(ui_path, "w") as f:
            json.dump(uninsured, f, indent=2)
        print(f"Wrote {len(uninsured)} tracts to {ui_path}")
        manifest["datasets"]["uninsured"] = {
            "count": len(uninsured), "source": f"ACS {year} 5-Year (S2701)", "success": True
        }
    else:
        print("  Subject table failed. Trying fallback B27001...")
        fb_url = (
            f"https://api.census.gov/data/{year}/acs/acs5"
            f"?get=NAME,B27001_001E,B27001_005E"
            f"&for=tract:*&in=state:{state}%20county:{county}"
        )
        raw_fb = fetch_api(fb_url, "ACS B27001 fallback")
        if raw_fb:
            header = raw_fb[0]
            for row in raw_fb[1:]:
                geoid = row[header.index("state")] + row[header.index("county")] + row[header.index("tract")]
                if valid_geoids and geoid not in valid_geoids:
                    continue
                total_pop = safe_int(row[header.index("B27001_001E")])
                unins_count = safe_int(row[header.index("B27001_005E")])
                uninsured.append({
                    "geoid": geoid,
                    "total_population": total_pop,
                    "uninsured_count": unins_count,
                    "pct_uninsured": safe_pct(unins_count, total_pop),
                    "vintage": f"ACS {year} 5-Year"
                })
            ui_path = os.path.join(paths["processed"], "uninsured.json")
            with open(ui_path, "w") as f:
                json.dump(uninsured, f, indent=2)
            print(f"Wrote {len(uninsured)} tracts to {ui_path}")
            manifest["datasets"]["uninsured"] = {
                "count": len(uninsured), "source": f"ACS {year} 5-Year (B27001 fallback)", "success": True
            }

    # Write manifest
    manifest_path = os.path.join(paths["processed"], "fetch_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest written to {manifest_path}")
    print("Done.")


if __name__ == "__main__":
    main()
