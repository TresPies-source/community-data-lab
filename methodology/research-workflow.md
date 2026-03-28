# The TresPies Research Workflow

**A reproducible methodology for AI-assisted spatial equity research at community development organizations.**

Version 1.0 | March 2026 | Cruz Morales, TresPies

---

## Overview

This document describes a 6-stage research workflow that enables small nonprofits to produce publication-quality spatial equity analysis using AI assistance, public data, and zero external infrastructure. The methodology is AI-agnostic — any capable AI coding assistant works — with Claude Code as the recommended tool.

The workflow was developed and validated at Commonwealth Development (Madison, WI), a 5-person CDC that used it to produce 7 causal research analyses, an 11-layer interactive equity data viewer, and 2 quasi-experimental research designs for Arnold Ventures.

---

## The Four-Layer Gap This Workflow Addresses

Most nonprofit GIS capacity-building fails because it targets the wrong layer:

| Layer | Question | Typical Solution | Why It Fails |
|-------|----------|-----------------|--------------|
| **Software** | "What tool do I use?" | Esri license, QGIS training | Having a tool doesn't mean knowing what to do with it |
| **Data** | "Where do I find data?" | Census data workshops | Having data doesn't mean knowing which data answers your question |
| **Analysis** | "How do I analyze it?" | Statistics training | Knowing regression doesn't mean knowing when to use it |
| **Research Design** | "What question am I answering?" | **This workflow** | Everything above follows from having the right question |

This workflow starts at the research design layer and works downward. The question shapes the data selection, which shapes the analysis, which shapes the tool choice.

---

## Stage 1: Research Question Framing

### Purpose
Define specific, answerable equity questions grounded in your organization's mission and the communities you serve.

### Process

1. **Start with the policy decision.** What is your organization trying to influence? A zoning vote, a budget allocation, a funder proposal, a coalition argument?

2. **Identify the equity claim.** What do you believe is true about your community that, if demonstrated with data, would strengthen your position? Examples:
   - "Transit-dependent families in our service area have worse school attendance"
   - "Affordable housing proximity reduces chronic absence"
   - "Our neighborhood has fewer childcare providers per child than the county average"

3. **Convert to a testable question.** Add a control variable (usually income) to make the question causal rather than descriptive:
   - "Does transit access predict chronic absence **after controlling for household income**?"
   - "Does proximity to affordable housing reduce absence **beyond what income alone predicts**?"

4. **Classify the question by data requirements:**
   - **Tier 1 — Answerable now:** All data sources are public and accessible
   - **Tier 2 — Needs one additional data layer:** Requires one new data source (e.g., childcare licensing database)
   - **Tier 3 — Needs a data partnership:** Requires an MOU with a school district, health department, or other agency

### Quality Check
A good research question:
- Names a specific independent variable (transit access, housing proximity, health access)
- Names a specific dependent variable (chronic absence rate, economic mobility indicator)
- Names a control variable (household income, poverty rate)
- Can be answered at the census tract level using public data
- Would change a decision if answered

### Output
A numbered list of research questions (RQs), classified by tier, with the policy context for each.

---

## Stage 2: Data Sourcing

### Purpose
Identify, verify, and document every data source needed to answer your research questions.

### The Public Data Landscape (US-specific)

**Demographics and Economics:**
- Census ACS (5-year estimates) — income, race, age, poverty, housing tenure, cost burden, uninsured rates
- Access: Census API with vintage control (free, no registration required)
- Geography: Census tract level (finest grain available for most variables)
- Refresh: Annual (December release for previous year)

**Education:**
- State education data portals — school-level enrollment, attendance, chronic absence, demographics
- Examples: WISEdash (WI), Illinois Report Card (IL), CDE DataQuest (CA)
- Geography: School-level (can be geocoded to census tracts)
- Refresh: Annual (fall for previous school year)
- Note: Disaggregated data (race x economic status) often requires a data sharing agreement

**Transit:**
- GTFS (General Transit Feed Specification) — stop locations, route geometries, schedules, frequency
- Access: Transit agency websites (most US agencies publish GTFS feeds)
- Geography: Stop-level (can be aggregated to census tracts via buffer analysis)
- Refresh: Varies (quarterly to annually)

**Health:**
- HRSA (Health Resources and Services Administration) — Health Professional Shortage Area designations, FQHC locations
- Access: HRSA data portal (free download)
- Geography: Census tract / county level
- Refresh: Quarterly

**Housing:**
- HUD LIHTC database — Low-Income Housing Tax Credit properties
- Eviction Lab — tract-level eviction rates (historical)
- State housing finance agencies — Section 8 project-based, affordable housing inventories
- ACS — housing cost burden, tenure, rent-to-income ratios
- Geography: Property-level (geocodable) and tract-level

**Childcare:**
- State childcare licensing databases — provider locations, licensed capacity
- HIFLD (Homeland Infrastructure Foundation-Level Data) — facility locations
- Geography: Point-level (provider addresses)

**Infrastructure:**
- Park and recreation data — municipal open data portals
- Library locations — state library systems
- Street lighting, bike infrastructure — municipal GIS portals

### Verification Protocol

For every data source, document:

```
Source: [Name]
URL: [Direct download or API endpoint]
Geography: [Tract / school / point]
Variables: [List of fields used]
Vintage: [Year or date range]
Refresh schedule: [How often updated]
Known limitations: [What it doesn't capture]
Fetch method: [API / CSV download / manual export]
Script: [Path to fetcher script, if automated]
```

### Output
A data manifest listing every source, verified by URL, with refresh schedule and known limitations.

---

## Stage 3: AI-Assisted Data Processing

### Purpose
Use AI as a research partner to write, test, and run data processing scripts that transform raw public data into analysis-ready datasets.

### Principles

1. **Stdlib only.** All scripts use Python standard library (json, csv, math, urllib, os). No pandas, numpy, or scikit-learn. This ensures portability — any machine with Python 3 can run the pipeline.

2. **Parameterized geography.** Scripts accept a state FIPS code, county FIPS code, or metro area name as input. Hardcoded geography prevents reuse.

3. **Embedded documentation.** Every script includes a header comment explaining what it does, what data it reads, what it produces, and how to refresh it.

4. **Idempotent execution.** Running a script twice produces the same output. Scripts read from `/data/raw/` and write to `/data/processed/`.

### Prompt Pattern for Data Processing

When asking AI to write a data processing script:

```
Context: I'm building a spatial equity analysis for [city/county].
Data source: [Name, format, location]
Research question: [The specific RQ this data serves]
Output format: JSON with census tract GEOID as key
Constraints: Python stdlib only (no pandas/numpy), must be re-runnable

Write a script that:
1. Reads [input file/API]
2. Processes [specific transformation]
3. Outputs [tract-level JSON with specific fields]
4. Includes a header comment documenting sources and refresh schedule
```

### Geocoding

Address-based data (school locations, provider addresses, facility sites) requires geocoding to latitude/longitude for spatial analysis.

- Use Census Geocoder API (free, no key required) for batch geocoding
- Maintain a `geocode_fixes.json` for manual corrections
- Document geocode failure rates — above 5% indicates data quality issues

### Output
A `/data/` directory with raw inputs and processed JSON files, keyed by census tract GEOID, with a fetch manifest documenting every source and its freshness.

---

## Stage 4: Analysis

### Purpose
Answer each research question using appropriate statistical methods, all implemented in stdlib Python.

### Analysis Patterns

**Pattern 1: Two-Predictor OLS Regression**
- Use: "Does X predict Y after controlling for income?"
- Implementation: Ordinary least squares with two independent variables (X and household income) predicting Y
- Output: Coefficients, R-squared, interpretation of whether X has independent explanatory power

**Pattern 2: Segmented/Threshold Analysis**
- Use: "Is there a nonlinear breakpoint in the income-outcome relationship?"
- Implementation: Split data at candidate breakpoints, compute fit for each segment
- Output: Identified threshold(s) where the relationship changes character

**Pattern 3: Residual-Based Outlier Detection**
- Use: "Which locations beat (or underperform) their neighborhood's prediction?"
- Implementation: Fit tract-level model, compute school/site-level residuals
- Output: Ranked list of positive and negative deviants with residual magnitudes

**Pattern 4: Correlation Matrix**
- Use: Initial scoping to identify which variables are worth regressing
- Implementation: Pearson r for all variable pairs
- Output: Correlation table with strength classifications

**Pattern 5: Composite Scoring**
- Use: "Which sites/tracts have the greatest combined need?"
- Implementation: Normalize indicators (0-1 scale), weight and sum, convert to A-F grades
- Output: Scored and ranked sites with transparent methodology

### Prompt Pattern for Analysis

```
Context: I'm answering RQ [number]: "[research question]"
Data available: [list of processed JSON files with field names]
Controlling for: household income (median_income field)
Method: [OLS regression / correlation / outlier detection]
Constraints: Python stdlib only (math module for calculations)

Write a script that:
1. Loads [data files]
2. Joins on census tract GEOID
3. Runs [analysis method]
4. Outputs results as JSON with interpretation
5. Includes effect size and sample size in output
```

### Output
A `/data/rq_*.json` file for each research question, containing results, interpretation, and methodology documentation.

---

## Stage 5: Output Production

### Purpose
Transform analysis results into decision-ready outputs for three audiences: community stakeholders, elected officials, and funders.

### Output Types

**1. Standalone HTML Data Viewer**

A single self-contained HTML file (typically 2-5 MB) that embeds:
- Leaflet.js interactive map with multiple choropleth layers
- Sortable data tables for tracts, schools, or sites
- Cross-tabulation tools for demographic breakdowns
- PDF export for offline distribution

No server required. Distributable via email, USB, or web hosting.

Build pattern: A Python script (`build_standalone.py`) that reads all processed JSON files, embeds them as JavaScript variables in an HTML template with Leaflet.js, and writes a single `.html` file.

**2. Policy Briefs**

4-6 page markdown documents structured for elected official and funder audiences:
- Problem statement grounded in local data
- Key findings (2-3 data visualizations referenced)
- Policy implications (specific, actionable recommendations)
- Data sources and methodology (transparency section)
- About the organization (credibility section)

Templates provided for: transit/mobility, housing affordability, education equity, zoning/land use, rapid response.

**3. Excel Workbooks**

Multi-sheet analysis workbooks for stakeholder discovery sessions:
- Sheet 1: Summary dashboard (key metrics, rankings)
- Sheet 2+: Domain-specific data (demographics, education, transit, health)
- Final sheet: Methodology and source documentation

### Prompt Pattern for Output Production

```
Context: I have completed analysis for [RQs] and need to produce [output type]
Audience: [community stakeholders / elected officials / funders]
Key findings: [2-3 headline results]
Data files: [list of analysis output JSONs]

Build a [standalone viewer / policy brief / workbook] that:
1. Presents findings for [audience] consumption
2. Includes [specific visualizations or sections]
3. Is self-contained and portable
4. Documents data sources and methodology transparently
```

### Output
Deliverable files ready for distribution to the target audience.

---

## Stage 6: Maintenance and Institutional Memory

### Purpose
Ensure the research infrastructure remains accurate, current, and organizationally embedded beyond any single person.

### Maintenance Schedule

| Frequency | Action | Example |
|-----------|--------|---------|
| **Annual** (December) | Census ACS refresh, re-run all RQ scripts | New 5-year estimates release |
| **Quarterly** | Health access data refresh (HRSA) | HPSA designation updates |
| **As available** | GTFS feed update, education data refresh | New school year data |
| **Event-driven** | Rapid response analysis | Zoning vote, budget hearing |

### Institutional Memory

The research workflow produces knowledge that must persist across staff transitions and session boundaries.

**CLAUDE.md file:** A project-level instruction file that tells AI assistants the project context, key decisions, file organization, and coding conventions. This file ensures any new session starts with full context.

**Agent memory architecture:** For Claude Code specifically, the `.claude/agent-memory/` directory stores:
- Research findings and their implications
- Data source documentation and known issues
- Strategic decisions and their rationale
- Partner relationships and engagement history

**Maintenance playbook:** A living document listing:
- Every data source with its refresh schedule and responsible party
- Manual actions required (data exports, API registrations)
- Policy/coalition calendar integration (when briefs are needed)
- Grant pipeline tracking (deadlines, contacts, status)

### Output
A maintenance playbook, CLAUDE.md file, and agent memory structure that ensures the research infrastructure is self-documenting and transferable.

---

## Appendix: Technology Stack

| Component | Tool | Why |
|-----------|------|-----|
| Data processing | Python 3 (stdlib) | Universal, portable, no dependency management |
| AI assistance | Claude Code (recommended) | Agent mode, file system access, memory architecture |
| Interactive maps | Leaflet.js | Open source, lightweight, embeddable |
| Map generation | Folium (Python) | Python wrapper for Leaflet, good for batch generation |
| Documents | Markdown | Universal, convertible to PDF/HTML/DOCX |
| Word docs | docx.js | Programmatic Word generation when needed |
| PDF export | Puppeteer | HTML-to-PDF for browser-rendered outputs |
| Data format | GeoJSON + JSON | Human-readable, web-native, no database required |
| Transit data | GTFS standard | Industry standard, published by most US transit agencies |
| Spatial reference | Census TIGER/Line | Official census tract geometries |

---

## Appendix: What This Methodology Produces vs. Alternatives

| Capability | Community Data Lab | Esri + Training | GIS Consultant | Urban Institute Tool |
|-----------|-------------------|-----------------|----------------|---------------------|
| Custom research questions | Yes | Possible with training | Yes (but leaves with them) | No (preset metrics) |
| Causal analysis (controlling for income) | Yes (OLS, thresholds) | Requires stats background | Depends on consultant | No |
| Standalone portable outputs | Yes (single HTML) | No (requires ArcGIS Online) | Varies | Web-only |
| Institutional memory | Yes (CLAUDE.md, agent memory) | No | No | No |
| Reproducible pipeline | Yes (re-runnable scripts) | Manual workflows | Varies | N/A |
| Staff capacity building | Yes (curriculum included) | Yes (but software-focused) | No | No |
| Cost for ongoing use | AI subscription ($20/mo) | $100-5000/yr | $5-15K/engagement | Free (limited) |
| Time to first output | 2-4 weeks | 3-6 months | 4-8 weeks | 1 day (preset only) |
