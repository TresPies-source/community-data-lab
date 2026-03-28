#!/usr/bin/env python3
"""
Community Data Lab — Composite Equity Scoring Engine
Parameterized by config.json. stdlib only.

Combines demographics, housing, health, and transit data into a single
equity vulnerability score per census tract, with A-F grades.

Usage: python3 03_composite_scoring.py
Requires:
  - config.json
  - data/processed/demographics.json (from 01_fetch_census.py)
  - data/processed/cost_burden.json (from 01_fetch_census.py)
  - data/processed/transit_frequency.json (from 02_process_gtfs.py)

Output:
  data/processed/equity_scores.json — Tract-level composite scores and grades
"""

import json
import os
from datetime import datetime

from geo_lib import load_config
from stats_lib import normalize_01, composite_score, assign_grades


def main():
    config = load_config()
    paths = config["data_paths"]
    scoring = config["scoring"]

    processed = paths["processed"]

    # Load data files
    print("Loading processed data...")

    demo_path = os.path.join(processed, "demographics.json")
    cb_path = os.path.join(processed, "cost_burden.json")
    transit_path = os.path.join(processed, "transit_frequency.json")

    for path, label in [(demo_path, "demographics"), (cb_path, "cost_burden"), (transit_path, "transit_frequency")]:
        if not os.path.exists(path):
            print(f"WARNING: {label} not found at {path}. Run the prerequisite script first.")
            print(f"  demographics.json: run 01_fetch_census.py")
            print(f"  cost_burden.json: run 01_fetch_census.py")
            print(f"  transit_frequency.json: run 02_process_gtfs.py")

    with open(demo_path) as f:
        demographics = json.load(f)
    with open(cb_path) as f:
        cost_burden = json.load(f)
    with open(transit_path) as f:
        transit = json.load(f)

    # Index by GEOID
    demo_idx = {r["geoid"]: r for r in demographics}
    cb_idx = {r["geoid"]: r for r in cost_burden}
    transit_idx = {r["geoid"]: r for r in transit}

    # Build unified tract list
    all_geoids = sorted(demo_idx.keys())
    print(f"Tracts with demographics: {len(all_geoids)}")

    # Assemble indicator vectors (aligned by GEOID order)
    indicators = {
        "pct_nonwhite": [],
        "poverty_rate": [],
        "pct_cost_burdened": [],
        "transit_access_inverse": [],
    }

    tract_records = []
    for geoid in all_geoids:
        demo = demo_idx.get(geoid, {})
        cb = cb_idx.get(geoid, {})
        tr = transit_idx.get(geoid, {})

        pct_nw = demo.get("pct_nonwhite")
        pov = demo.get("poverty_rate")
        cost_b = cb.get("pct_cost_burdened")

        # Invert transit score (low transit = high vulnerability)
        transit_score = tr.get("transit_access_score", 0)
        transit_inv = 10.0 - transit_score if transit_score is not None else None

        indicators["pct_nonwhite"].append(pct_nw)
        indicators["poverty_rate"].append(pov)
        indicators["pct_cost_burdened"].append(cost_b)
        indicators["transit_access_inverse"].append(transit_inv)

        tract_records.append({
            "geoid": geoid,
            "name": demo.get("name", ""),
            "median_income": demo.get("median_income"),
            "total_population": demo.get("total_population"),
            "pct_nonwhite": pct_nw,
            "poverty_rate": pov,
            "pct_cost_burdened": cost_b,
            "transit_access_score": transit_score,
            "stop_count": tr.get("stop_count", 0),
            "mean_trips_per_hour": tr.get("mean_trips_per_hour", 0),
        })

    # Check which configured weights have matching data
    weights = scoring["weights"]
    available_weights = {}
    for name, w in weights.items():
        if name in indicators:
            available_weights[name] = w
        else:
            print(f"  Skipping weight '{name}' — no matching indicator data")

    # Renormalize weights to sum to 1.0
    w_total = sum(available_weights.values())
    if w_total > 0:
        available_weights = {k: v / w_total for k, v in available_weights.items()}

    print(f"Computing composite scores with {len(available_weights)} indicators...")

    # Compute scores
    scores = composite_score(indicators, available_weights)
    grades = assign_grades(scores, scoring["grade_thresholds"])

    # Attach scores to records
    for i, geoid in enumerate(all_geoids):
        tract_records[i]["equity_score"] = scores[i]
        tract_records[i]["equity_grade"] = grades[i]

    # Sort by score descending (highest need first)
    tract_records.sort(key=lambda r: r.get("equity_score") or 0, reverse=True)

    # Summary
    grade_counts = {}
    for g in grades:
        grade_counts[g] = grade_counts.get(g, 0) + 1
    print(f"\nGrade distribution:")
    for g in ["A", "B", "C", "D", "F", "N/A"]:
        if g in grade_counts:
            print(f"  {g}: {grade_counts[g]} tracts")

    # Write output
    output = {
        "metadata": {
            "organization": config["organization"]["name"],
            "geography": f"{config['geography']['county_name']}, {config['geography']['state_name']}",
            "generated": datetime.now().isoformat(),
            "n_tracts": len(tract_records),
            "weights": available_weights,
            "grade_thresholds": scoring["grade_thresholds"],
        },
        "tracts": tract_records,
    }

    out_path = os.path.join(processed, "equity_scores.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {len(tract_records)} scored tracts to {out_path}")

    # Top 10 highest-need tracts
    print(f"\nTop 10 highest-need tracts:")
    print(f"{'GEOID':<15} {'Grade':>5} {'Score':>7} {'Income':>8} {'%NonWh':>7} {'%CostB':>7} {'Transit':>7}")
    print("-" * 70)
    for r in tract_records[:10]:
        print(f"{r['geoid']:<15} {r['equity_grade']:>5} {r['equity_score'] or 0:>7.3f} "
              f"${r['median_income'] or 0:>7,} {r['pct_nonwhite'] or 0:>6.1f}% "
              f"{r['pct_cost_burdened'] or 0:>6.1f}% {r['transit_access_score'] or 0:>6.1f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
