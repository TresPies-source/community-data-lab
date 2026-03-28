# Prompt: Build a Census API Data Fetcher

## When to Use
When you need to pull demographics, income, housing, or health insurance data from the Census ACS API.

## Context Block
```
I'm building a spatial equity data pipeline for [county name] County, [state].
State FIPS: [XX]
County FIPS: [YYY]

I need census tract-level data for [list variables — e.g., median income, race/ethnicity breakdown, housing cost burden, uninsured rate].
```

## Instruction Block
```
Write a Python script (stdlib only — no pandas, no requests library, use urllib) that:

1. Fetches the following ACS 5-year estimate variables from the Census API:
   - [Table codes — e.g., B19013_001E for median income, B03002 for race/ethnicity]

2. For every census tract in [state FIPS][county FIPS]

3. Outputs a JSON file keyed by tract GEOID (e.g., "55025000101") with fields:
   - geoid: full 11-digit FIPS
   - [variable_name]: [value]
   - (computed fields as needed — e.g., pct_nonwhite, pct_cost_burdened)

4. Includes a header comment documenting:
   - Source: Census ACS 5-Year Estimates
   - API endpoint used
   - Variables fetched
   - Vintage
   - Date script was last run

5. Handles API errors gracefully (retry once on timeout, skip tracts with missing data)

6. Writes output to data/[filename].json

Constraints:
- Python stdlib only (urllib.request for HTTP, json for parsing)
- Must be re-runnable (idempotent — running twice produces the same output)
- Census API does not require a key for small queries, but document where to add one if needed
- Compute percentages from raw counts where applicable (e.g., % below poverty = B17001_002E / B17001_001E)
```

## Example Output Structure
```json
{
  "55025000101": {
    "geoid": "55025000101",
    "median_income": 72500,
    "total_pop": 4231,
    "pct_nonwhite": 0.34,
    "pct_below_poverty": 0.12,
    "pct_cost_burdened": 0.38
  }
}
```
