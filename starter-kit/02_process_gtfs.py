#!/usr/bin/env python3
"""
Community Data Lab — GTFS Transit Frequency Processor
Parameterized by config.json. stdlib only.

Computes AM peak weekday transit frequency per census tract from a GTFS feed.

Usage: python3 02_process_gtfs.py
Requires:
  - config.json
  - GTFS feed extracted to data/gtfs/ (calendar.txt, trips.txt, stop_times.txt, stops.txt)
  - Census tract GeoJSON at configured path

Output:
  data/processed/transit_frequency.json — Tract-level transit access metrics
"""

import csv
import json
import os
from collections import defaultdict
from datetime import datetime

from geo_lib import load_config, load_tracts, point_in_polygon


def parse_time_seconds(t):
    """Parse GTFS time string to seconds. Clamps hours >= 24."""
    h, m, s = t.strip().split(':')
    h, m, s = int(h), int(m), int(s)
    if h >= 24:
        return 23 * 3600 + 59 * 60 + 59
    return h * 3600 + m * 60 + s


def main():
    config = load_config()
    geo = config["geography"]
    gtfs_config = config["gtfs"]
    paths = config["data_paths"]

    gtfs_dir = paths["gtfs"]
    am_start = gtfs_config["am_peak_start_hour"] * 3600
    am_end = gtfs_config["am_peak_end_hour"] * 3600

    # Verify GTFS files exist
    required_files = ["calendar.txt", "trips.txt", "stop_times.txt", "stops.txt"]
    for f in required_files:
        if not os.path.exists(os.path.join(gtfs_dir, f)):
            print(f"ERROR: {f} not found in {gtfs_dir}")
            print(f"Download your transit agency's GTFS feed and extract to {gtfs_dir}/")
            raise SystemExit(1)

    # 1. Weekday service IDs
    weekday_sids = set()
    with open(os.path.join(gtfs_dir, "calendar.txt")) as f:
        for r in csv.DictReader(f):
            if r.get("monday") == "1" and r.get("friday") == "1":
                weekday_sids.add(r["service_id"])
    print(f"Weekday service IDs: {len(weekday_sids)}")

    if not weekday_sids:
        print("WARNING: No weekday services found. Check calendar.txt format.")
        print("Trying all service IDs as fallback...")
        with open(os.path.join(gtfs_dir, "calendar.txt")) as f:
            for r in csv.DictReader(f):
                weekday_sids.add(r["service_id"])

    # 2. Trip → service mapping
    trip_svc = {}
    with open(os.path.join(gtfs_dir, "trips.txt")) as f:
        for r in csv.DictReader(f):
            trip_svc[r["trip_id"]] = r["service_id"]
    print(f"Trips loaded: {len(trip_svc)}")

    # 3. Count AM peak weekday departures per stop
    stop_trips = defaultdict(int)
    kept = 0
    with open(os.path.join(gtfs_dir, "stop_times.txt")) as f:
        for r in csv.DictReader(f):
            sid = trip_svc.get(r["trip_id"])
            if sid not in weekday_sids:
                continue
            secs = parse_time_seconds(r["departure_time"])
            if am_start <= secs <= am_end:
                stop_trips[r["stop_id"]] += 1
                kept += 1
    print(f"AM peak stop-times: {kept}, unique stops with service: {len(stop_trips)}")

    # 4. Trips per hour (2-hour AM peak window)
    peak_hours = (am_end - am_start) / 3600
    stop_tph = {sid: cnt / peak_hours for sid, cnt in stop_trips.items()}

    # 5. Stop coordinates
    stop_coords = {}
    with open(os.path.join(gtfs_dir, "stops.txt")) as f:
        for r in csv.DictReader(f):
            try:
                stop_coords[r["stop_id"]] = (float(r["stop_lat"]), float(r["stop_lon"]))
            except (ValueError, KeyError):
                continue
    print(f"Stop locations loaded: {len(stop_coords)}")

    # 6. Load tract geometries
    tracts_path = paths["tracts_geojson"]
    if not os.path.exists(tracts_path):
        print(f"ERROR: Tract GeoJSON not found at {tracts_path}")
        print("Download from Census TIGER/Line or use Census Cartographic Boundaries.")
        raise SystemExit(1)

    features, all_geoids = load_tracts(tracts_path)
    print(f"Census tracts loaded: {len(all_geoids)}")

    # 7. Assign stops to tracts
    print("Assigning stops to tracts (this may take a minute)...")
    stop_to_geoid = {}
    for sid, (lat, lon) in stop_coords.items():
        for feat in features:
            geoid = feat["properties"].get("GEOID")
            if geoid and point_in_polygon(lon, lat, feat["geometry"]):
                stop_to_geoid[sid] = geoid
                break
        else:
            stop_to_geoid[sid] = None

    matched = sum(1 for v in stop_to_geoid.values() if v is not None)
    print(f"  Stops matched to tracts: {matched}/{len(stop_to_geoid)}")

    # 8. Aggregate to tract level
    tract_stops = {g: [] for g in all_geoids}
    for sid, tph in stop_tph.items():
        geoid = stop_to_geoid.get(sid)
        if geoid and geoid in tract_stops:
            tract_stops[geoid].append(tph)

    results = []
    for geoid in sorted(all_geoids):
        vals = tract_stops[geoid]
        stop_count = len(vals)
        if stop_count == 0:
            mean_tph = 0.0
            pct_frequent = 0.0
        else:
            mean_tph = sum(vals) / stop_count
            pct_frequent = sum(1 for v in vals if v >= 4) / stop_count

        # Transit access score: 0-10 scale
        transit_score = min(10.0, round(mean_tph * 1.5, 1))

        results.append({
            "geoid": geoid,
            "stop_count": stop_count,
            "mean_trips_per_hour": round(mean_tph, 2),
            "pct_stops_frequent": round(pct_frequent, 2),
            "transit_access_score": transit_score,
            "source": gtfs_config["agency_name"],
            "vintage": datetime.now().strftime("%Y-%m-%d")
        })

    # 9. Write output
    os.makedirs(paths["processed"], exist_ok=True)
    out_path = os.path.join(paths["processed"], "transit_frequency.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {len(results)} tract records to {out_path}")

    # 10. Update manifest
    manifest_path = os.path.join(paths["processed"], "fetch_manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            manifest = json.load(f)
    if "datasets" not in manifest:
        manifest["datasets"] = {}
    manifest["datasets"]["transit_frequency"] = {
        "fetched": datetime.now().isoformat(),
        "count": len(results),
        "source": f"{gtfs_config['agency_name']} GTFS",
        "success": True
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print("Updated fetch_manifest.json")
    print("Done.")


if __name__ == "__main__":
    main()
