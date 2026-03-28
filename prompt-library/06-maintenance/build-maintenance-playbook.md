# Prompt: Build a Maintenance Playbook

## When to Use
After completing the initial build, to ensure the research infrastructure stays current and organizationally embedded.

## Context Block
```
I've built a spatial equity analysis for [city/county] with:
- [N] data sources (list each with refresh frequency)
- [N] analysis scripts
- [N] output products (viewer, briefs, workbooks)

Organization: [name]
Staff who will maintain this: [name(s) and roles]
```

## Instruction Block
```
Write a maintenance playbook that covers:

1. **Data Refresh Schedule**
   For each data source, document:
   - Source name and what it provides
   - Refresh frequency (annual / quarterly / monthly / event-driven)
   - Specific month/date when new data becomes available
   - Script to run for refresh (path and command)
   - Manual steps required (if any — e.g., "download CSV from [portal]")
   - Person responsible
   - Estimated time per refresh

2. **Script Inventory**
   For each Python script:
   - What it does (1 sentence)
   - What it reads (input files)
   - What it produces (output files)
   - How to run it (command)
   - Dependencies on other scripts (run order)

3. **Coalition/Policy Calendar**
   Map data refresh timing to policy opportunities:
   - When do budget hearings happen?
   - When are grant deadlines?
   - When do school board meetings occur?
   - What rapid-response scenarios might arise?

4. **Annual Maintenance Timeline**
   Month-by-month calendar of refresh actions, with estimated hours:
   - January: [actions]
   - February: [actions]
   - ...

5. **Troubleshooting Guide**
   Common issues and fixes:
   - Census API returns empty data (vintage changed, table restructured)
   - GTFS feed URL changed (check transit agency website)
   - Education data suppressed (cell size too small — aggregate or request MOU)
   - Geocoding failures above 5% (check address format, update geocode_fixes.json)

6. **Institutional Memory Checklist**
   If the primary maintainer leaves:
   - [ ] CLAUDE.md file is current and complete
   - [ ] All scripts have header documentation
   - [ ] Data manifest is up to date
   - [ ] Refresh schedule is in a shared calendar
   - [ ] Login credentials (if any) are in a shared password manager
   - [ ] This playbook has been reviewed by a second person
```

## Constraints
- Be specific — "refresh data" is not actionable; "run `python3 data/fetch_new_census_layers.py` and verify output in data/income_by_tract.json" is actionable
- Estimate time for each task (helps organizations plan capacity)
- Include a "total annual maintenance burden" estimate in hours
- Flag any tasks that require technical skill vs. tasks anyone can do
