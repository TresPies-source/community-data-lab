# Prompt: Write a Data-Grounded Policy Brief

## When to Use
When translating analysis results into a document for elected officials, funders, or coalition partners.

## Context Block
```
I need to write a policy brief on [topic — e.g., transit equity and school attendance] for [audience — e.g., city council, county board, funder].

My analysis found:
- [Key finding 1 — e.g., "Transit access predicts chronic absence after controlling for income (R²=0.34)"]
- [Key finding 2]
- [Key finding 3]

Organization: [name], a [description] serving [community]
Policy context: [what decision is upcoming — e.g., "BRT corridor funding vote in June"]
```

## Instruction Block
```
Write a 4-6 page policy brief in markdown format with the following structure:

1. **Title** — Action-oriented, specific to the policy context
   (e.g., "Transit Access and School Attendance: Evidence from [City]'s [Neighborhoods]")

2. **Executive Summary** (1 paragraph)
   - State the problem, the key finding, and the recommendation in 3-4 sentences

3. **The Challenge** (1 page)
   - Ground the problem in local data (use specific numbers from the analysis)
   - Name the affected population with demographic specificity
   - Connect to the upcoming policy decision

4. **What the Data Shows** (1-2 pages)
   - Present 2-3 key findings with data citations
   - Use plain language — no jargon, no regression coefficients
   - Translate statistical findings into human terms:
     BAD: "A one-unit increase in transit frequency is associated with a 2.3 percentage point decrease in chronic absence (p<0.05)"
     GOOD: "In neighborhoods where buses come every 15 minutes instead of every 30, chronic absence drops by about 2 percentage points — that's roughly 45 fewer students missing school regularly"
   - Include 1-2 data visualizations (reference the standalone viewer for interactive versions)

5. **Policy Implications** (1 page)
   - 3-5 specific, actionable recommendations
   - Each recommendation tied directly to a finding
   - Acknowledge what the data doesn't show (intellectual honesty builds credibility)

6. **About the Data** (half page)
   - List every data source with vintage
   - State the methodology in one sentence
   - Link to the standalone viewer for full interactive exploration
   - Note limitations transparently

7. **About [Organization]** (quarter page)
   - Brief credibility section
   - Contact information

Constraints:
- No jargon — write for an intelligent non-specialist
- Every claim must cite a specific data source
- Recommendations must be specific enough to act on (not "invest in transit" but "extend Route 15 service to 6am for neighborhoods west of [street]")
- Acknowledge limitations — briefs that oversell findings lose credibility
- Maximum 6 pages including all sections
```

## Templates Available
- `templates/brief_template_transit.md` — Transit and mobility
- `templates/brief_template_housing.md` — Housing affordability and displacement
- `templates/brief_template_education.md` — Education equity
- `templates/brief_template_zoning.md` — Zoning and land use
- `templates/brief_template_rapid_response.md` — Rapid turnaround for emerging issues
