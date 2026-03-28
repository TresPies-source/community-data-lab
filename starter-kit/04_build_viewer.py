#!/usr/bin/env python3
"""
Community Data Lab — Standalone Equity Viewer Builder
Parameterized by config.json. stdlib only.

Builds a self-contained HTML file with interactive Leaflet.js map,
sortable data tables, and embedded equity data. No server required.

Usage: python3 04_build_viewer.py
Requires:
  - config.json
  - data/processed/demographics.json
  - data/processed/cost_burden.json
  - data/processed/transit_frequency.json
  - data/processed/equity_scores.json
  - Census tract GeoJSON at configured path

Output:
  output/equity_viewer.html — Standalone interactive data viewer (~2-5 MB)
"""

import json
import os
import urllib.request
from datetime import datetime

from geo_lib import load_config


def fetch_library(url, label):
    """Fetch a JavaScript/CSS library for embedding."""
    print(f"Fetching {label}...")
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return resp.read().decode()
    except Exception as e:
        print(f"  WARNING: Could not fetch {label}: {e}")
        print(f"  The viewer will require internet to load {label} from CDN.")
        return None


def main():
    config = load_config()
    org = config["organization"]
    geo = config["geography"]
    paths = config["data_paths"]

    processed = paths["processed"]
    output_path = paths["output_viewer"]

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Load all data files
    print("Loading data files...")
    data = {}

    data_files = {
        "demographics": "demographics.json",
        "cost_burden": "cost_burden.json",
        "transit_frequency": "transit_frequency.json",
        "equity_scores": "equity_scores.json",
        "uninsured": "uninsured.json",
    }

    for key, filename in data_files.items():
        path = os.path.join(processed, filename)
        if os.path.exists(path):
            with open(path) as f:
                data[key] = json.load(f)
            size_kb = os.path.getsize(path) / 1024
            print(f"  {filename}: {size_kb:.0f} KB")
        else:
            print(f"  {filename}: not found (skipping)")
            data[key] = []

    # Load tract GeoJSON
    tracts_path = paths["tracts_geojson"]
    if os.path.exists(tracts_path):
        with open(tracts_path) as f:
            data["tracts_geo"] = json.load(f)
        size_kb = os.path.getsize(tracts_path) / 1024
        print(f"  tracts.geojson: {size_kb:.0f} KB")
    else:
        print(f"  ERROR: Tract GeoJSON not found at {tracts_path}")
        raise SystemExit(1)

    # Fetch Leaflet for embedding
    leaflet_css = fetch_library(
        "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css", "Leaflet CSS"
    )
    leaflet_js = fetch_library(
        "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js", "Leaflet JS"
    )

    # Index data by GEOID for map popup
    demo_idx = {}
    if isinstance(data.get("demographics"), list):
        demo_idx = {r["geoid"]: r for r in data["demographics"]}
    scores_idx = {}
    if isinstance(data.get("equity_scores"), dict):
        scores_idx = {r["geoid"]: r for r in data["equity_scores"].get("tracts", [])}
    elif isinstance(data.get("equity_scores"), list):
        scores_idx = {r["geoid"]: r for r in data["equity_scores"]}

    # Build the HTML
    print("\nBuilding viewer HTML...")

    # Determine Leaflet inclusion method
    if leaflet_css and leaflet_js:
        leaflet_css_tag = f"<style>{leaflet_css}</style>"
        leaflet_js_tag = f"<script>{leaflet_js}</script>"
    else:
        leaflet_css_tag = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />'
        leaflet_js_tag = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'

    # Serialize data for embedding
    embedded_json = json.dumps(data, separators=(",", ":"))

    # Grade colors
    grade_colors = {
        "A": "#d32f2f",  # Highest need — red
        "B": "#f57c00",  # High need — orange
        "C": "#fbc02d",  # Moderate — yellow
        "D": "#7cb342",  # Lower need — light green
        "F": "#388e3c",  # Lowest need — green
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{org['name']} — Equity Data Viewer</title>
{leaflet_css_tag}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }}
.header {{ background: #1a237e; color: white; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }}
.header h1 {{ font-size: 20px; font-weight: 600; }}
.header .subtitle {{ font-size: 13px; opacity: 0.85; }}
.tabs {{ display: flex; background: #283593; border-bottom: 2px solid #1a237e; }}
.tab {{ padding: 10px 20px; color: rgba(255,255,255,0.7); cursor: pointer; font-size: 14px; border: none; background: none; }}
.tab.active {{ color: white; border-bottom: 3px solid #ff9800; font-weight: 600; }}
.tab:hover {{ color: white; background: rgba(255,255,255,0.1); }}
.panel {{ display: none; padding: 20px; }}
.panel.active {{ display: block; }}
#map {{ height: 500px; border-radius: 8px; border: 1px solid #ddd; }}
.layer-controls {{ padding: 12px 0; display: flex; gap: 8px; flex-wrap: wrap; }}
.layer-btn {{ padding: 6px 14px; border: 1px solid #1a237e; border-radius: 16px; background: white; color: #1a237e; cursor: pointer; font-size: 13px; }}
.layer-btn.active {{ background: #1a237e; color: white; }}
table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
th {{ background: #1a237e; color: white; padding: 10px 12px; text-align: left; cursor: pointer; font-size: 13px; }}
th:hover {{ background: #283593; }}
td {{ padding: 8px 12px; border-bottom: 1px solid #eee; font-size: 13px; }}
tr:hover td {{ background: #e8eaf6; }}
.grade {{ display: inline-block; width: 28px; height: 28px; border-radius: 50%; text-align: center; line-height: 28px; font-weight: 700; color: white; font-size: 13px; }}
.grade-A {{ background: #d32f2f; }}
.grade-B {{ background: #f57c00; }}
.grade-C {{ background: #fbc02d; color: #333; }}
.grade-D {{ background: #7cb342; }}
.grade-F {{ background: #388e3c; }}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }}
.stat-card {{ background: white; padding: 16px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.stat-card .label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
.stat-card .value {{ font-size: 28px; font-weight: 700; color: #1a237e; margin-top: 4px; }}
.legend {{ display: flex; gap: 12px; margin: 12px 0; flex-wrap: wrap; }}
.legend-item {{ display: flex; align-items: center; gap: 4px; font-size: 12px; }}
.legend-color {{ width: 16px; height: 16px; border-radius: 3px; }}
.footer {{ padding: 16px 24px; background: #e8eaf6; font-size: 12px; color: #555; text-align: center; margin-top: 20px; }}
@media print {{
  .tabs, .layer-controls, .layer-btn {{ display: none; }}
  .panel {{ display: block !important; page-break-inside: avoid; }}
  .header {{ background: #1a237e !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
}}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>{org['name']} — Equity Data Viewer</h1>
    <div class="subtitle">{geo['county_name']}, {geo['state_name']} | Generated {datetime.now().strftime('%B %d, %Y')}</div>
  </div>
  <button onclick="window.print()" style="background:#ff9800;color:white;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;font-size:13px;">Export PDF</button>
</div>

<div class="tabs">
  <button class="tab active" onclick="showTab('overview')">Overview</button>
  <button class="tab" onclick="showTab('map')">Map</button>
  <button class="tab" onclick="showTab('table')">Data Table</button>
  <button class="tab" onclick="showTab('sources')">Data Sources</button>
</div>

<!-- Overview Panel -->
<div id="overview" class="panel active">
  <h2 style="margin-bottom:16px;">Equity Overview</h2>
  <div class="stats-grid" id="stats-grid"></div>
  <div class="legend" id="grade-legend"></div>
  <div id="grade-distribution" style="margin-top:16px;"></div>
</div>

<!-- Map Panel -->
<div id="map-panel" class="panel">
  <div class="layer-controls" id="layer-controls"></div>
  <div id="map"></div>
</div>

<!-- Table Panel -->
<div id="table-panel" class="panel">
  <div id="table-container"></div>
</div>

<!-- Sources Panel -->
<div id="sources" class="panel">
  <h2>Data Sources</h2>
  <div id="sources-content" style="margin-top:16px;"></div>
</div>

{leaflet_js_tag}
<script>
// Embedded data
const DATA = {embedded_json};
const CONFIG = {{
  center: [{geo['map_center_lat']}, {geo['map_center_lon']}],
  zoom: {geo['map_zoom']},
  org: "{org['name']}",
  gradeColors: {json.dumps(grade_colors)}
}};

let map = null;
let currentLayer = null;

// Tab switching
function showTab(tabId) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));

  const panelId = tabId === 'map' ? 'map-panel' : tabId === 'table' ? 'table-panel' : tabId;
  document.getElementById(panelId).classList.add('active');
  event.target.classList.add('active');

  if (tabId === 'map' && !map) initMap();
}}

// Overview stats
function initOverview() {{
  const scores = DATA.equity_scores;
  const tracts = scores.tracts || scores;
  const n = tracts.length;

  const grades = {{}};
  tracts.forEach(t => {{ grades[t.equity_grade] = (grades[t.equity_grade] || 0) + 1; }});

  const incomes = tracts.map(t => t.median_income).filter(v => v != null);
  const avgIncome = incomes.length ? Math.round(incomes.reduce((a, b) => a + b) / incomes.length) : 0;
  const totalPop = tracts.reduce((s, t) => s + (t.total_population || 0), 0);

  const grid = document.getElementById('stats-grid');
  grid.innerHTML = `
    <div class="stat-card"><div class="label">Census Tracts</div><div class="value">${{n}}</div></div>
    <div class="stat-card"><div class="label">Total Population</div><div class="value">${{totalPop.toLocaleString()}}</div></div>
    <div class="stat-card"><div class="label">Avg Median Income</div><div class="value">${{avgIncome.toLocaleString('en-US', {{style:'currency',currency:'USD',maximumFractionDigits:0}})}}</div></div>
    <div class="stat-card"><div class="label">High-Need Tracts (A/B)</div><div class="value">${{(grades['A']||0) + (grades['B']||0)}}</div></div>
  `;

  const legend = document.getElementById('grade-legend');
  legend.innerHTML = Object.entries(CONFIG.gradeColors).map(([g, c]) =>
    `<div class="legend-item"><div class="legend-color" style="background:${{c}}"></div>${{g}}: ${{grades[g]||0}} tracts</div>`
  ).join('');
}}

// Map
function initMap() {{
  map = L.map('map').setView(CONFIG.center, CONFIG.zoom);
  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}@2x.png', {{
    attribution: '&copy; OpenStreetMap, &copy; CARTO',
    maxZoom: 18
  }}).addTo(map);

  const scores = DATA.equity_scores;
  const tracts = scores.tracts || scores;
  const scoreIdx = {{}};
  tracts.forEach(t => {{ scoreIdx[t.geoid] = t; }});

  showChoropleth('equity_score', scoreIdx);
  setTimeout(() => map.invalidateSize(), 100);
}}

function showChoropleth(field, scoreIdx) {{
  if (currentLayer) map.removeLayer(currentLayer);

  currentLayer = L.geoJSON(DATA.tracts_geo, {{
    style: function(feature) {{
      const geoid = feature.properties.GEOID;
      const tract = scoreIdx[geoid];
      let color = '#ccc';
      if (tract) {{
        const grade = tract.equity_grade;
        color = CONFIG.gradeColors[grade] || '#ccc';
      }}
      return {{ fillColor: color, fillOpacity: 0.6, weight: 1, color: '#666', opacity: 0.5 }};
    }},
    onEachFeature: function(feature, layer) {{
      const geoid = feature.properties.GEOID;
      const tract = scoreIdx[geoid];
      if (tract) {{
        layer.bindPopup(`
          <strong>Tract ${{geoid}}</strong><br>
          Grade: <span class="grade grade-${{tract.equity_grade}}">${{tract.equity_grade}}</span><br>
          Income: $${{(tract.median_income||0).toLocaleString()}}<br>
          % Non-White: ${{(tract.pct_nonwhite||0).toFixed(1)}}%<br>
          % Cost Burdened: ${{(tract.pct_cost_burdened||0).toFixed(1)}}%<br>
          Transit Score: ${{(tract.transit_access_score||0).toFixed(1)}}/10
        `);
      }}
    }}
  }}).addTo(map);
}}

// Data table
function initTable() {{
  const scores = DATA.equity_scores;
  const tracts = scores.tracts || scores;

  let html = '<table id="data-table"><thead><tr>';
  html += '<th onclick="sortTable(0)">GEOID</th>';
  html += '<th onclick="sortTable(1)">Grade</th>';
  html += '<th onclick="sortTable(2)">Score</th>';
  html += '<th onclick="sortTable(3)">Income</th>';
  html += '<th onclick="sortTable(4)">% Non-White</th>';
  html += '<th onclick="sortTable(5)">% Cost Burdened</th>';
  html += '<th onclick="sortTable(6)">Transit</th>';
  html += '</tr></thead><tbody>';

  tracts.forEach(t => {{
    html += `<tr>
      <td>${{t.geoid}}</td>
      <td><span class="grade grade-${{t.equity_grade}}">${{t.equity_grade}}</span></td>
      <td>${{(t.equity_score||0).toFixed(3)}}</td>
      <td>$${{(t.median_income||0).toLocaleString()}}</td>
      <td>${{(t.pct_nonwhite||0).toFixed(1)}}%</td>
      <td>${{(t.pct_cost_burdened||0).toFixed(1)}}%</td>
      <td>${{(t.transit_access_score||0).toFixed(1)}}</td>
    </tr>`;
  }});
  html += '</tbody></table>';
  document.getElementById('table-container').innerHTML = html;
}}

let sortDir = 1;
function sortTable(col) {{
  const table = document.getElementById('data-table');
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  sortDir *= -1;
  rows.sort((a, b) => {{
    let va = a.cells[col].textContent.replace(/[$,%]/g, '');
    let vb = b.cells[col].textContent.replace(/[$,%]/g, '');
    const na = parseFloat(va), nb = parseFloat(vb);
    if (!isNaN(na) && !isNaN(nb)) return (na - nb) * sortDir;
    return va.localeCompare(vb) * sortDir;
  }});
  rows.forEach(r => tbody.appendChild(r));
}}

// Sources
function initSources() {{
  const manifest = DATA.fetch_manifest || {{}};
  let html = '<table><thead><tr><th>Dataset</th><th>Source</th><th>Records</th></tr></thead><tbody>';
  if (manifest.datasets) {{
    Object.entries(manifest.datasets).forEach(([name, info]) => {{
      html += `<tr><td>${{name}}</td><td>${{info.source || 'N/A'}}</td><td>${{info.count || 'N/A'}}</td></tr>`;
    }});
  }}
  html += '</tbody></table>';
  html += `<p style="margin-top:16px;font-size:13px;">Generated by Community Data Lab (TresPies) on ${{new Date().toLocaleDateString()}}.</p>`;
  document.getElementById('sources-content').innerHTML = html;
}}

// Initialize
initOverview();
initTable();
initSources();
</script>

<div class="footer">
  Built with <a href="https://github.com/trespies/community-data-lab" style="color:#1a237e;">Community Data Lab</a> | {org['name']} | {org['website']}
</div>

</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nStandalone viewer written to: {output_path}")
    print(f"File size: {size_mb:.1f} MB")
    print(f"Open in any browser — no server required.")
    print("Done.")


if __name__ == "__main__":
    main()


