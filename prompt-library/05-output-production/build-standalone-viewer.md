# Prompt: Build a Standalone Equity Data Viewer

## When to Use
After completing data processing and analysis, when you need to produce a portable, interactive visualization for stakeholders.

## Context Block
```
I've completed a spatial equity analysis for [city/county, state] with:
- [N] census tracts with demographic and economic data
- [N] [schools/sites/facilities] with outcome data
- [N] research question analyses
- Tract-level GeoJSON for map rendering

All data is in the /data/ directory as JSON files.
```

## Instruction Block
```
Build a standalone HTML file (single file, no external dependencies, no server required) that includes:

1. An interactive Leaflet.js map with:
   - Census tract choropleth layers (switchable):
     [List specific layers — e.g., median income, % nonwhite, chronic absence rate, equity score]
   - Point overlays (toggleable):
     [List specific points — e.g., schools, transit stops, health centers, affordable housing]
   - Legend that updates when layer changes
   - Tract popup on click showing key metrics

2. Data tables (sortable) for:
   - [Entity type — e.g., schools, sites, tracts] with key metrics
   - Color-coded by performance tier (A-F or quintile)

3. Cross-tabulation tool (if applicable):
   - Select two demographic dimensions
   - View outcome metrics for each combination

4. Navigation:
   - Tab-based interface (Overview, Map, [domain tabs], Cross Tabs)
   - Overview tab with 3-5 key equity visualizations

5. Export:
   - PDF export button (window.print() with print-optimized CSS)
   - Title and date stamp on exports

Technical requirements:
- Single HTML file with all CSS, JavaScript, and data embedded
- Leaflet.js loaded from CDN (only external dependency)
- All GeoJSON and data JSON embedded as JavaScript variables
- Responsive design (works on laptop and tablet screens)
- File size target: under 5 MB

Embed the following data files as JavaScript variables:
- [list each JSON file to embed]
- [GeoJSON tract file]
```

## Constraints
- Single file — everything embedded, distributable via email or USB
- No server-side code, no database, no API calls at runtime
- Leaflet.js from CDN is the only external load (graceful degradation message if offline)
- Color scheme must be colorblind-accessible (use viridis or similar sequential palette)
- Mobile-responsive is a bonus but laptop/desktop is the primary target
- Include a "Data Sources" section in the viewer documenting every source

## Example
The CWD MMSD YABIR Data Viewer is a 3.8 MB standalone HTML with:
- 11 tract-level choropleth layers
- 3 school-level overlays
- 54-school sortable table
- Cross-tabulation by race x economic status
- PDF export
- Embedded in a single file, no installation required
