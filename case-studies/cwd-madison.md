# Case Study: Commonwealth Development — Madison, WI

**Organization:** Commonwealth Development (CWD)
**Location:** Madison, Wisconsin
**Type:** Community Development Organization (CDO)
**Portfolio:** 165 affordable housing units, 43 business incubation spaces
**Engagement Period:** 2025-2026
**Partner:** TresPies (AI research consulting)

---

## The Challenge

Commonwealth Development needed spatial equity research to support advocacy, grant applications, and city council testimony. Like many community development organizations, CWD had access to neighborhood knowledge and program data but lacked the infrastructure to produce original, data-driven spatial equity analyses.

Specific needs:
- **Grant applications** requiring causal research designs (e.g., Arnold Ventures housing supply reform program)
- **City council testimony** grounded in tract-level data rather than anecdotal evidence
- **Funder presentations** with interactive visualizations showing neighborhood-level disparities
- **Institutional research memory** so that analyses could be updated and extended over time

CWD did not have GIS staff, a research department, or existing spatial analysis infrastructure.

## The Approach

TresPies applied the Community Data Lab methodology — an AI-assisted spatial equity research workflow using public data, stdlib Python, and self-contained HTML outputs.

### Research Question Framing

CWD leadership identified policy questions the organization needed to answer. Each question was structured to be:
- **Spatial** — answerable at the census tract level
- **Causal** — testable with regression controlling for income
- **Actionable** — connected to a specific policy decision or advocacy need

Example research questions:
- Does transit access predict chronic school absence after controlling for household income?
- Does housing cost burden predict health uninsurance rates at the tract level?
- Are childcare deserts spatially correlated with high-poverty tracts beyond what income alone predicts?

### Data Infrastructure

All data sourced from public, free APIs and downloads:

| Domain | Sources | Tracts Covered |
|--------|---------|----------------|
| Demographics | Census ACS 5-Year (income, poverty, race, age) | 125 |
| Housing | ACS cost burden, HUD AFFH, eviction records | 125 |
| Transit | Madison Metro GTFS feed (AM peak frequency) | 125 |
| Education | WISEdash (school attendance, chronic absence) | 54 schools mapped to tracts |
| Health | ACS uninsured rates, HRSA health professional shortage areas | 125 |
| Childcare | Wisconsin DCF licensed provider locations | Geocoded to tracts |

19 verified public data sources with documented refresh schedules.

### Analysis

Seven causal research question analyses, each using two-predictor OLS regression (stdlib Python, no external dependencies):

- **Predictor of interest** (e.g., transit access score)
- **Income control** (median household income)
- **Outcome** (e.g., chronic absence rate)

Each analysis produced: regression coefficients, R-squared decomposition showing what the predictor adds beyond income, t-statistics with approximate significance tests, and plain-language interpretation.

### Output Production

All outputs designed to be self-contained and portable:

- **Interactive equity data viewer** — Single HTML file (3.8 MB), 11 data layers, Leaflet.js map, PDF export, no server required. Shareable via email attachment.
- **Policy brief templates** — Transit, housing, education, zoning, and rapid response templates designed for city council and funder audiences.
- **Research question analysis reports** — Structured narratives with statistical findings, limitations, and policy implications.

## Results

| Metric | Count |
|--------|-------|
| Causal research question analyses | 7 |
| Interactive data layers in viewer | 11 |
| Verified public data sources | 19 |
| Quasi-experimental research designs (submitted to funders) | 2 |
| Policy brief templates produced | 5 |
| Census tracts analyzed | 125 |
| Schools mapped to tract-level data | 54 |

### What Worked

1. **Research questions as the organizing principle.** Every data fetch, every analysis, every visualization answered a specific question that CWD leadership cared about. This prevented the common failure mode of producing maps that illustrate rather than argue.

2. **Self-contained HTML outputs.** The standalone viewer could be emailed to city council members, attached to grant applications, and presented at community meetings without requiring any software installation or technical infrastructure.

3. **Stdlib Python, no dependencies.** The entire data pipeline runs on any machine with Python 3.8+. No conda environments, no package management, no version conflicts. This matters for organizations without IT staff.

4. **AI as research partner.** Claude Code was used not as a chatbot but as a research collaborator — designing regression specifications, writing data fetchers, building visualizations, and maintaining institutional memory across sessions. The methodology is AI-agnostic, but the AI acceleration reduced what would have been months of work to weeks.

5. **Institutional memory.** Agent memory architecture maintained research context, data source documentation, and methodological decisions across sessions. When CWD needed to update an analysis or extend a research question, the context was preserved.

### Lessons Learned

1. **Subject tables (S-prefix) in the Census API are less reliable at the tract level** than detailed tables (B-prefix). The pipeline includes fallback logic for this.

2. **GTFS feeds vary significantly between transit agencies.** The AM peak frequency calculation worked well for Madison Metro but may need adaptation for agencies with different service patterns or GTFS formatting.

3. **Composite scoring weights should be set by the organization, not the analyst.** CWD's leadership chose weights that reflected their advocacy priorities. The scoring engine is parameterized to support this.

4. **Policy briefs need to be opinionated.** Early drafts that presented data without interpretation were not useful for advocacy. The templates evolved to include recommended policy actions grounded in the data.

## Technical Stack

- **Language:** Python 3 (stdlib only)
- **Mapping:** Leaflet.js (embedded in HTML output)
- **Data sources:** Census ACS API, GTFS feeds, state education portals, HUD, HRSA
- **AI tool:** Claude Code (methodology is AI-agnostic)
- **Infrastructure:** Zero external infrastructure — all scripts run locally, all outputs are single HTML files

## Replication

The starter kit in this repository is parameterized for any US county. CWD's configuration targeted Dane County, WI (state FIPS 55, county FIPS 025). The same scripts, configured for a different county, will produce equivalent outputs.

See `starter-kit/README.md` for setup instructions and `config_example.json` for the configuration template.

---

*Built with Community Data Lab methodology by TresPies. For consulting engagements, contact cruz@trespies.com.*
