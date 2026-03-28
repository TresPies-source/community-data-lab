# Prompt: Verify and Document Data Sources

## When to Use
After framing research questions, when you need to find and verify every data source required.

## Context Block
```
I'm building a spatial equity analysis for [city/county, state].

My research questions require data on: [list domains — e.g., demographics, school attendance, transit frequency, health access, housing affordability, childcare].

My geography is [county name] County, [state] — FIPS code [XX][YYY].

I need to find, verify, and document public data sources for each domain.
```

## Instruction Block
```
For each data domain listed above:

1. Identify the best publicly available data source for [state]
2. Verify the URL is accessible (fetch the page or API endpoint)
3. Document the source using this template:

   Source: [Name]
   URL: [Direct download or API endpoint]
   Geography: [Tract / school / point / county]
   Variables needed: [Specific field names]
   Vintage: [Year or date range of most recent data]
   Refresh schedule: [How often the source updates]
   Known limitations: [What it doesn't capture, suppression rules, etc.]
   Fetch method: [Census API / CSV download / manual export / web scrape]
   Registration required: [Yes/No — note if API key needed]

4. Flag any sources that:
   - Require registration or an MOU
   - Have data suppression rules (small cell sizes)
   - Are state-specific (not available in all states)
   - Have been discontinued or moved

5. For each domain, note if a national source exists (Census, HRSA, HUD) or if the source is state-specific

Write the complete manifest as a single reference document.
```

## Constraints
- Every URL must be verified as accessible
- Note the vintage — data from before 2020 should be flagged
- Document suppression rules (education data often suppresses cells < 10 students)
- Include the Census API table codes (e.g., S1901 for income, S2701 for uninsured)
- National sources preferred over state-specific when quality is comparable

## Example Output (from CWD data manifest)

```
Source: Census ACS 5-Year Estimates (Income)
URL: https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=tract:*&in=state:55+county:025
Geography: Census tract
Variables: B19013_001E (median household income)
Vintage: 2018-2022 (released December 2023)
Refresh: Annual (December)
Limitations: 5-year estimates smooth short-term changes; MOE can be large for small tracts
Fetch method: Census API (no key required for small queries)
Registration: No
```
