#!/usr/bin/env python3
"""
Community Data Lab — Shared Geometry Library
stdlib only. No shapely, geopandas, or external geo libraries.

Provides:
  - point_in_ring: Ray-casting point-in-polygon for a single ring
  - point_in_polygon: Check point against GeoJSON Polygon/MultiPolygon geometry
  - load_tracts: Load census tract GeoJSON and build polygon index
  - assign_point_to_tract: Map a lat/lon point to its containing tract GEOID
  - batch_assign_points: Map multiple points to tracts efficiently
"""

import json
import os


def point_in_ring(px, py, ring):
    """Ray-casting algorithm for point-in-polygon.
    ring: list of [lon, lat] coordinate pairs (GeoJSON order).
    px, py: point longitude, latitude."""
    n = len(ring)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def point_in_polygon(px, py, geometry):
    """Check if a point is in a GeoJSON Polygon or MultiPolygon geometry.
    px: longitude, py: latitude.
    Handles holes (interior rings) correctly."""
    gtype = geometry["type"]
    coords = geometry["coordinates"]

    if gtype == "Polygon":
        if not point_in_ring(px, py, coords[0]):
            return False
        for hole in coords[1:]:
            if point_in_ring(px, py, hole):
                return False
        return True
    elif gtype == "MultiPolygon":
        for poly in coords:
            if point_in_ring(px, py, poly[0]):
                in_hole = False
                for hole in poly[1:]:
                    if point_in_ring(px, py, hole):
                        in_hole = True
                        break
                if not in_hole:
                    return True
        return False
    return False


def load_tracts(geojson_path):
    """Load census tract GeoJSON and return (features_list, geoid_set).

    Each feature must have properties.GEOID (11-digit FIPS).
    Returns:
        features: list of GeoJSON features
        geoids: set of all GEOIDs
    """
    with open(geojson_path) as f:
        data = json.load(f)
    features = data["features"]
    geoids = set()
    for feat in features:
        geoid = feat["properties"].get("GEOID")
        if geoid:
            geoids.add(geoid)
    return features, geoids


def assign_point_to_tract(lon, lat, features):
    """Find which tract a point falls in. Returns GEOID or None."""
    for feat in features:
        geoid = feat["properties"].get("GEOID")
        if geoid and point_in_polygon(lon, lat, feat["geometry"]):
            return geoid
    return None


def batch_assign_points(points, features):
    """Assign multiple points to census tracts.

    Args:
        points: list of dicts with 'lat' and 'lon' keys (and any other fields)
        features: list of GeoJSON tract features

    Returns:
        dict mapping point index to GEOID (or None if unmatched)
    """
    assignments = {}
    for i, pt in enumerate(points):
        lat = pt.get("lat")
        lon = pt.get("lon")
        if lat is not None and lon is not None:
            assignments[i] = assign_point_to_tract(lon, lat, features)
        else:
            assignments[i] = None
    matched = sum(1 for v in assignments.values() if v is not None)
    print(f"  Matched {matched}/{len(points)} points to tracts")
    return assignments


def load_config(config_path="config.json"):
    """Load the starter kit configuration file."""
    if not os.path.exists(config_path):
        print(f"ERROR: {config_path} not found.")
        print("Copy config_example.json to config.json and fill in your geography.")
        raise SystemExit(1)
    with open(config_path) as f:
        return json.load(f)
