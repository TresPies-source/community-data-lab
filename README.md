# Community Data Lab

**AI-assisted spatial equity research for community development organizations.**

Community Data Lab is an open-source methodology, curriculum, and toolkit that teaches nonprofits to answer causal questions about their neighborhoods using AI-assisted workflows and public data.

Built by [TresPies](https://trespies.com). Proven at [Commonwealth Development](https://commonwealthdevelopment.org) in Madison, WI.

---

## The Problem

Community development corporations (CDCs) need spatial equity research to advocate effectively — but the existing tools solve the wrong problems:

| Tool | What it solves | What it doesn't |
|------|---------------|-----------------|
| Esri Nonprofit Program | Software access ($100/yr) | Research methodology |
| QGIS | Cost (free) | Data sourcing, analysis design |
| Urban Institute Spatial Equity Tool | Quick disparity snapshots | Custom research questions, causal analysis |
| PolicyMap | Ready-made neighborhood data | Original research, policy brief production |
| GIS consultants | Maps and analysis | Capacity building — they leave, the knowledge leaves |

**The gap:** Nobody teaches CDCs to design and execute original spatial equity research. CDCs with GIS licenses produce maps that illustrate rather than argue.

## What Community Data Lab Provides

### Methodology (AI-agnostic, Claude Code recommended)

A reproducible research workflow for nonprofits:

1. **Research Question Framing** — What makes a spatial equity question answerable with public data
2. **Data Sourcing** — Census API, GTFS, state education data, HRSA, HUD, Eviction Lab — all public, all free
3. **AI-Assisted Analysis** — Using AI as a research partner (not a chatbot) for regression, threshold detection, outlier identification
4. **Output Production** — Standalone HTML data viewers, policy briefs, funder-ready narratives
5. **Maintenance** — Refresh schedules, data quality monitoring, institutional memory

### Curriculum (6-week cohort)

A structured training program:

- **Week 1:** Spatial equity questions — framing what's answerable
- **Week 2:** Public data landscape — Census, transit, education, health, housing sources by state
- **Week 3:** AI as research partner — prompt engineering for spatial analysis
- **Week 4:** Analysis patterns — OLS regression, composite scoring, outlier detection (stdlib Python, no dependencies)
- **Week 5:** Output production — standalone viewers, policy briefs, Excel workbooks
- **Week 6:** Maintenance and sustainability — refresh cycles, coalition calendars, institutional memory

### Starter Kit

Parameterized Python scripts (stdlib only, no pandas/numpy) that can be configured for any US city:

- Census API data fetchers (demographics, income, housing cost burden, uninsured rates)
- GTFS transit frequency analyzer
- Composite equity scoring engine
- Standalone HTML viewer builder (Leaflet.js, embedded data, no server required)
- Policy brief templates (transit, housing, education, zoning, rapid response)

### Prompt Library

AI prompt templates for each stage of the research workflow. Designed for Claude Code, adaptable to other AI tools.

---

## Proof of Concept

Commonwealth Development (Madison, WI) — a 5-person CDC — used this methodology to produce:

- **7 causal research question analyses** answering "does X predict chronic school absence after controlling for income?" across transit, housing, health, and childcare domains
- **11-layer interactive equity data viewer** (3.8 MB standalone HTML, no server, PDF export)
- **19 verified public data sources** with automated refresh pipelines
- **2 quasi-experimental research designs** submitted to Arnold Ventures
- **5 policy brief templates** for city council and funder audiences
- **Agent memory architecture** maintaining institutional research knowledge across sessions

All built with Claude Code, stdlib Python, and zero external infrastructure.

---

## Repository Structure

```
community-data-lab/
  curriculum/          # 6-week cohort materials
  methodology/         # The TresPies research workflow documentation
  prompt-library/      # AI prompt templates for each research stage
  starter-kit/         # Parameterized Python scripts and HTML templates
  case-studies/        # Partner city analyses and lessons learned
  templates/           # Policy brief, viewer, and workbook templates
```

---

## For Hired Engagements

**CDC Research Accelerator** is TresPies' consulting practice built on Community Data Lab methodology. When you hire TresPies, you get:

- City-specific data infrastructure built and delivered
- Custom standalone viewers for your portfolio and service area
- Policy briefs grounded in your spatial equity data
- Staff training using Community Data Lab curriculum
- Ongoing research partnership

Contact: Cruz Morales, TresPies — [cruz@trespies.com](mailto:cruz@trespies.com)

---

## Contributing

Community Data Lab is open source. Contributions welcome:

- **New data source adapters** — State-specific education, health, or housing data parsers
- **City starter kits** — Pre-configured scripts for specific metro areas
- **Curriculum translations** — Bilingual materials for specific communities
- **Case studies** — Document your organization's experience with the methodology

---

## License

MIT License. Use it, fork it, teach with it.

Built by TresPies. Proven at Commonwealth Development.
