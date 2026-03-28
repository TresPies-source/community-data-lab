# Prompt: Frame Spatial Equity Research Questions

## When to Use
At the start of a new city/community analysis, when you need to define what questions your data will answer.

## Context Block
```
I work for [organization name], a community development corporation in [city, state].

Our mission focuses on [housing / education / health / economic development].

We serve [neighborhoods/communities] where [describe the equity issue you observe — e.g., "families in our service area face long commutes on infrequent transit while school attendance drops"].

We need to produce data-driven analysis for [audience: city council / funders / coalition partners / internal planning].
```

## Instruction Block
```
Help me frame 5-8 testable spatial equity research questions for [city/county].

For each question:
1. State the question in the form "Does [independent variable] predict [dependent variable] after controlling for [control variable]?"
2. Identify the independent variable (the factor we think matters)
3. Identify the dependent variable (the outcome we care about)
4. Identify the control variable (usually household income or poverty rate)
5. List the data sources needed to answer it
6. Classify it: Tier 1 (answerable with public data now), Tier 2 (needs one additional data layer), or Tier 3 (needs a data partnership or MOU)

Organize the questions into domains: transit/mobility, housing, education, health, economic opportunity.

For context, here are the types of public data typically available:
- Census ACS: income, race, age, poverty, housing tenure, cost burden, uninsured rates (tract level)
- State education portals: school-level enrollment, attendance, chronic absence
- GTFS: transit stop locations, routes, frequency
- HRSA: health shortage areas, community health centers
- HUD: LIHTC properties, Section 8 project-based housing
- State licensing: childcare providers, capacity
```

## Constraints
- Questions must be answerable at the census tract level
- Each question must name a specific policy decision it could inform
- Control for income in every question — descriptive correlations between race and outcomes without income controls are not publishable
- Prioritize Tier 1 questions (answerable now) for the first round

## Example Output (from CWD Madison analysis)

**Domain: Transit and Mobility**
- RQ 2.1: Does transit access (% of residential tracts within 1/4-mile of a stop, peak service frequency) predict chronic school absence after controlling for median household income?
  - IV: Transit access (GTFS-derived)
  - DV: Chronic absence rate (WISEdash)
  - Control: Median household income (ACS)
  - Data: GTFS feed + Census ACS + State education portal
  - Tier: 1 (all public)
  - Policy use: BRT corridor investment decisions, transit equity arguments
