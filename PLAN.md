# Strategic Execution Plan: Community Data Lab & CDC Research Accelerator

**Created:** 2026-03-29
**Owner:** Cruz Morales, TresPies
**Source Files:** 11 files across community-data-lab/ and CWD/research/
**Mode:** Context Ingestion — routed because: multiple file types (code, research, strategy docs) with a planning intent

---

## File Catalog

| # | File | Type | Key Content |
|---|------|------|-------------|
| 1 | `README.md` | Product positioning | Two-product framing (CDL open / CRA hired), competitive landscape, proof-of-concept |
| 2 | `CLAUDE.md` | Agent context | Key decisions locked: AI-agnostic, English-only, MIT license, stdlib only |
| 3 | `methodology/research-workflow.md` | IP backbone | 6-stage workflow (v1.0), four-layer gap thesis, analysis patterns, tech stack |
| 4 | `starter-kit/README.md` | Technical docs | 4-script pipeline (census, GTFS, scoring, viewer), setup instructions |
| 5 | `starter-kit/config_example.json` | Configuration | Parameterized for Cook County/Chicago — ready for TRP pilot |
| 6 | `research/community-data-lab-strategic-scout.md` | Strategy | Revenue model, phased rollout, competitive positioning, partner sequencing |
| 7 | `research/nonprofit-gis-landscape.md` | Market research | 14 sources, 6 findings — the four-layer gap is real and unoccupied |
| 8 | `research/trp-mercy-housing-partner-analysis.md` | Partner diligence | TRP: zero GIS, active advocacy need. Mercy: rich Salesforce, no spatial layer |
| 9 | `case-studies/trp-outreach-draft.md` | Outreach | Ready-to-send email to Raymundo/Johnson, free pilot framing |
| 10 | `templates/README.md` | Templates index | 4 brief templates + rapid response protocol, generalized from CWD |
| 11 | `prompt-library/README.md` | Prompt index | 6-stage prompt library, Claude Code recommended, AI-agnostic |

---

## Constraints (Extracted from Files)

1. **All code must be stdlib Python** — no pandas, numpy, or external dependencies (CLAUDE.md:39, research-workflow.md:145)
2. **All outputs must be self-contained** — single HTML files, no server requirements (CLAUDE.md:40)
3. **AI-agnostic methodology** with Claude Code as recommended tool (CLAUDE.md:18)
4. **English-only** for now; flag for Spanish when a bilingual engagement lands (CLAUDE.md:23)
5. **Open-source core (MIT)** with premium components in CDC Research Accelerator engagements only (CLAUDE.md:21)
6. **Research questions drive outputs** — every metric answers a specific equity question (CLAUDE.md:24)
7. **TRP first, Mercy within 12 months** — sequencing is locked (strategic-scout.md:104)
8. **MCF deadline: June 2026** — capacity building grant, funds curriculum development (strategic-scout.md:118)
9. **RWJF announcement: Fall 2026** — "Local Data for Equitable Communities" program (strategic-scout.md:127)
10. **Config already parameterized for Cook County** — state_fips 17, county_fips 031 (config_example.json:16-17)

---

## Contradictions

### Contradiction 1: TRP Engagement Pricing
- `strategic-scout.md:86` states "$8-12K consulting fee" for TRP engagement
- `trp-outreach-draft.md:14` offers the pilot "at no cost"
- **Resolution:** Free pilot is correct for Phase 1 validation. Paid engagement ($8-12K) is for the follow-on full data infrastructure build. The outreach draft should clarify this is a pro-bono pilot with a paid follow-on pathway.

### Contradiction 2: Curriculum Status
- `README.md:39-47` describes a 6-week curriculum as if it exists
- `curriculum/` directory is empty — no lesson plans, exercises, or assessments exist
- **Resolution:** The curriculum is designed (structure exists) but unwritten. Phase 2 must produce actual cohort materials. The README should note "curriculum (in development)" until materials exist.

### Contradiction 3: Scoring Weight for Youth
- `config_example.json:88` includes weight `pct_youth: 0.15`
- `03_composite_scoring.py` only processes `pct_nonwhite`, `poverty_rate`, `pct_cost_burdened`, `transit_access_inverse` — no `pct_youth` indicator
- **Resolution:** The scoring engine needs a youth population indicator added, or the config example should remove the weight.

---

## What Exists vs. What's Missing

### Built (Ready to Ship)

| Component | Status | Files |
|-----------|--------|-------|
| Methodology document (v1) | Complete | `methodology/research-workflow.md` |
| Prompt library (6 stages) | Complete (1 prompt per stage) | `prompt-library/01-06/` |
| Starter kit (4 scripts + 2 libs) | Complete | `starter-kit/*.py` |
| Config template (Cook County) | Complete | `starter-kit/config_example.json` |
| Policy brief templates (4 + protocol) | Complete | `templates/*.md` |
| Competitive landscape research | Complete | `CWD/research/nonprofit-gis-landscape.md` |
| Partner diligence (TRP + Mercy) | Complete | `CWD/research/trp-mercy-partner-analysis.md` |
| Strategic scout + revenue model | Complete | `CWD/research/community-data-lab-strategic-scout.md` |
| TRP outreach draft | Complete | `case-studies/trp-outreach-draft.md` |
| CLAUDE.md agent context | Complete | `CLAUDE.md` |

### Missing (Must Build)

| Component | Priority | Phase | Estimated Effort |
|-----------|----------|-------|-----------------|
| **CWD case study** (sanitized) | High | 1 | 8 hrs |
| **Chicago/Cook County config + test run** | High | 1 | 12 hrs |
| **TRP displacement vulnerability map** | High | 1 | 40-60 hrs |
| **Curriculum lesson plans** (6 weeks) | High | 2 | 60-80 hrs |
| **Curriculum exercises + assessments** | High | 2 | 30-40 hrs |
| **MCF LOI draft** | High | 1-2 | 12-16 hrs |
| **Additional prompt templates** (2-3 per stage) | Medium | 2 | 20 hrs |
| **Excel workbook builder script** | Medium | 2 | 8 hrs |
| **RQ analysis script templates** (parameterized) | Medium | 2 | 16 hrs |
| **Mercy Housing Lakefront config + pilot** | Medium | 2-3 | 60-80 hrs |
| **Contributing guide** (CONTRIBUTING.md) | Low | 2 | 4 hrs |
| **Video walkthroughs** (curriculum supplement) | Low | 3 | 20 hrs |
| **Spanish localization** (flag only) | Low | 3+ | TBD |

---

## The Plan

### Phase 1: Validate (April - August 2026)

**Goal:** Prove the methodology transfers from Madison to Chicago. Land TRP pilot, begin MCF LOI, push repo to GitHub.

#### Track A: TRP Pilot (April - June)

**Actions:**
1. Send TRP outreach email (`case-studies/trp-outreach-draft.md`) to Raul Raymundo and Mary Johnson — target send by April 7
2. Configure starter kit for Cook County — `config_example.json` already has Chicago/Cook FIPS codes (lines 16-17); run `01_fetch_census.py` against Cook County to validate Census API works at scale (1,318 tracts vs. Dane County's 125)
3. Source Chicago-specific data layers:
   - HMDA lending data (CFPB download, tract-level)
   - Cook County Assessor property values (public API)
   - CTA GTFS feed (transitchicago.com/downloads/sch_data/)
   - Illinois Report Card (school attendance, replaces WISEdash)
4. Build Pilsen displacement vulnerability analysis:
   - Define 3-5 displacement RQs with TRP leadership (1-hour scoping call)
   - Fetch and process data (adapt `01_fetch_census.py`, add HMDA fetcher)
   - Run composite displacement scoring (`03_composite_scoring.py` with displacement-specific weights)
   - Build standalone viewer (`04_build_viewer.py` configured for Pilsen/Little Village/Back of the Yards focus area)
5. Deliver pilot: standalone HTML viewer + 1 policy brief (displacement/anti-gentrification template)
6. Collect TRP feedback: Is the output usable for Pilsen Stay in Place? City council testimony? Funder presentations?

**Deliverables:**
- Working Cook County data pipeline (scripts running, data validated)
- Pilsen displacement vulnerability viewer (standalone HTML)
- 1 policy brief (displacement template)
- TRP feedback document (what worked, what didn't, what they'd pay for)

**Success Criteria:**
- [ ] All 4 starter kit scripts run successfully against Cook County data
- [ ] Viewer renders 1,318 Cook County tracts (or Pilsen-area subset) with displacement indicators
- [ ] TRP confirms the output is usable for at least one advocacy purpose
- [ ] TRP expresses interest in a paid follow-on engagement

#### Track B: Repo and IP (April - May)

**Actions:**
1. Write CWD case study (`case-studies/cwd-madison.md`):
   - Sanitize: remove internal contacts, personnel details, CWD-specific financial data
   - Keep: methodology narrative, data layer inventory, output descriptions, proof-of-concept metrics
   - Reference specific artifacts: 7 RQ analyses, 11-layer viewer, 19 data sources, 5 templates
2. Fix contradiction: add `pct_youth` indicator to `03_composite_scoring.py` or remove from `config_example.json`
3. Fix README: mark curriculum as "(in development)" until lesson plans exist
4. Create `.gitignore` (exclude `config.json`, `data/`, `output/`)
5. Create `LICENSE` (MIT)
6. Push to GitHub: `trespies/community-data-lab`
7. Write `CONTRIBUTING.md` with guidelines for city adapters, data source adapters, and curriculum contributions

**Deliverables:**
- Public GitHub repository with all current materials
- CWD case study (sanitized)
- Clean README with accurate status

**Success Criteria:**
- [ ] Repo is public on GitHub with MIT license
- [ ] CWD case study published with no sensitive data
- [ ] README accurately describes what exists vs. in-development

#### Track C: MCF LOI Preparation (May - June)

**Actions:**
1. Research MCF (McKnight Community Foundation or target capacity-building funder) LOI requirements and deadline details
2. Frame the ask: Community Data Lab as capacity building for Wisconsin CDCs, with TRP pilot as out-of-state validation
3. Draft LOI using CWD as proof-of-concept and TRP feedback as validation signal
4. Budget: $50-100K request, primarily funding:
   - Curriculum development (6-week cohort materials) — $25-40K
   - First Wisconsin CDC cohort delivery — $15-20K
   - Starter kit generalization and documentation — $10-15K
   - Cruz Morales time at research consultant rate — remainder
5. Get Justice Castaneda letter of support (CWD as proof-of-concept partner)

**Deliverables:**
- MCF LOI (4-6 pages)
- CWD support letter
- Budget narrative

**Success Criteria:**
- [ ] LOI submitted before June 2026 deadline
- [ ] Budget is specific and tied to named deliverables
- [ ] TRP pilot results (even preliminary) referenced as validation

---

### Phase 2: Package (September 2026 - February 2027)

**Goal:** Build the curriculum, run the first cohort, establish RWJF positioning.

#### Track D: Curriculum Development (September - November)

**Actions:**
1. Write 6 lesson plans (one per week), each containing:
   - Learning objectives (3-4 per lesson)
   - Live session outline (2 hours)
   - Async exercise specification
   - Assessment rubric
   - Required readings / data source URLs
2. Create participant exercises:
   - Week 1: Frame 5 research questions for your community
   - Week 2: Build a data manifest for your county (using verification protocol from `research-workflow.md:119-131`)
   - Week 3: Run the starter kit against your county's Census data
   - Week 4: Write and run one RQ analysis script with AI assistance
   - Week 5: Build a standalone viewer for your community
   - Week 6: Write a maintenance playbook and present findings
3. Build assessment system:
   - Formative: weekly exercise review
   - Summative: each participant exits with a working viewer + 1 policy brief
4. Write instructor guide for Cruz (or future cohort facilitators)

**Deliverables:**
- 6 lesson plans in `curriculum/`
- 6 exercise specifications with rubrics
- Instructor guide
- Participant onboarding checklist

**Success Criteria:**
- [ ] All 6 lesson plans written and reviewed
- [ ] At least 2 exercises tested by running them against a non-Madison, non-Chicago county
- [ ] Instructor guide covers facilitation, grading, and troubleshooting

#### Track E: First Cohort (January - February 2027)

**Actions:**
1. Recruit 8-12 participants from Wisconsin CDCs (MCF grant covers participation costs)
2. Run 6-week virtual cohort:
   - Week 1-6 live sessions (2 hrs each, Zoom or equivalent)
   - Async Slack/Discord channel for peer support
   - Cruz provides 1:1 office hours (30 min/week per participant)
3. Each participant produces:
   - Data manifest for their county
   - At least 1 RQ analysis
   - Working standalone viewer
   - 1 policy brief draft
4. Collect cohort feedback:
   - Post-cohort survey
   - 30-day follow-up: Are participants still using the tools?
   - Documented case studies from 2-3 strongest participants

**Deliverables:**
- 8-12 completed participant projects
- 2-3 participant case studies for `case-studies/`
- Cohort feedback report
- Curriculum v1.1 (revised based on feedback)

**Success Criteria:**
- [ ] At least 6 of 8-12 participants produce a working viewer
- [ ] At least 3 participants use outputs in a real advocacy or grant context within 60 days
- [ ] Net Promoter Score > 7/10 on post-cohort survey

#### Track F: RWJF Positioning (September - December 2026)

**Actions:**
1. Monitor RWJF "Local Data for Equitable Communities" announcement (expected Fall 2026)
2. Prepare pre-application materials:
   - TRP pilot results as evidence of methodology transfer
   - MCF LOI (submitted or awarded) as co-funder signal
   - GitHub repo with stars/forks as adoption signal
   - CWD + TRP case studies as proof-of-concept pair
3. Draft RWJF proposal framing:
   - $100-200K request
   - 2-year program: develop curriculum + run 4 cohorts + publish methodology paper
   - National partners: TRP (Chicago) + Mercy Housing Lakefront (IL/WI/IN) + 2 new CDCs
4. Identify RWJF program officer and warm introduction path

**Deliverables:**
- RWJF pre-application brief (2 pages)
- Evidence package (TRP results, CWD case study, GitHub metrics)

**Success Criteria:**
- [ ] Pre-application materials assembled within 30 days of RWJF announcement
- [ ] At least 1 warm introduction to RWJF program staff identified

#### Track G: Additional Prompt and Starter Kit Content (Ongoing)

**Actions:**
1. Add 2-3 additional prompt templates per stage (expanding from 1 to 3-4 per stage):
   - `01-research-questions/`: Displacement-specific RQs, health equity RQs
   - `02-data-sourcing/`: State-specific education data guide (IL, WI, CA as first three)
   - `03-data-processing/`: HMDA fetcher, eviction data parser, school data parser
   - `04-analysis/`: Displacement scoring, school outlier detection
   - `05-output-production/`: Excel workbook builder, funder narrative generator
   - `06-maintenance/`: Agent memory setup guide, CLAUDE.md template
2. Add RQ analysis script templates to starter kit:
   - `05_rq_analysis.py` — parameterized OLS regression runner
   - `06_displacement_scoring.py` — displacement-specific composite (for TRP-type engagements)
3. Add Excel workbook builder:
   - `07_build_workbook.py` — multi-sheet xlsx generation (stdlib + minimal dependency)

**Deliverables:**
- Expanded prompt library (18-24 templates, up from 6)
- 3 additional starter kit scripts
- State-specific data source guides for IL, WI, CA

**Success Criteria:**
- [ ] Prompt library covers all common CDC research scenarios
- [ ] Starter kit runs end-to-end for at least 3 US counties

---

### Phase 3: Scale (March 2027 - December 2027)

**Goal:** Recurring revenue from cohorts + consulting. Mercy Housing engagement. National visibility.

#### Track H: Mercy Housing Lakefront Engagement (March - June 2027)

**Actions:**
1. Secure warm introduction to Mark Angelini (Mercy Housing Lakefront president)
2. Scope engagement: Portfolio-level GIS context dashboard for 52 IL/WI/IN properties
   - Map all 52 properties against census tract demographics, health access, transit, displacement risk
   - Integrate Salesforce service data (if Mercy shares resident-level geocodable data)
   - Produce standalone viewer + portfolio brief
3. Price: $12-20K consulting fee (CDC Research Accelerator engagement)
4. Document as case study for national Mercy Housing audience

**Deliverables:**
- Mercy Lakefront portfolio viewer
- Portfolio-level equity brief
- Case study for `case-studies/mercy-lakefront.md`

**Success Criteria:**
- [ ] Viewer covers all 52 Lakefront properties with neighborhood context
- [ ] Mercy leadership uses viewer in at least 1 funder presentation or board report
- [ ] Case study published on GitHub and shared with national Mercy Housing team

#### Track I: Recurring Cohorts and Consulting (Ongoing 2027)

**Actions:**
1. Run 2 additional cohorts (Spring 2027, Fall 2027):
   - Target: 8-12 participants each
   - Price: $500-1,500/participant (sliding scale)
   - Marketing: GitHub repo, TRP/CWD case studies, MCF/RWJF network
2. Build consulting pipeline:
   - Target: 5-8 CDC Research Accelerator engagements in 2027
   - Source: cohort alumni referrals, funder introductions, conference presentations
3. Present at NACEDA (National Alliance of Community Economic Development Associations) or equivalent CDC conference

**Deliverables:**
- 2 completed cohorts (16-24 additional participants)
- 5-8 consulting deliverables
- 1 conference presentation

**Success Criteria:**
- [ ] Year 2 revenue reaches $100K+ (blended consulting + cohorts + grants)
- [ ] At least 3 CDCs independently maintaining their data infrastructure 6+ months post-cohort
- [ ] GitHub repo has 50+ stars and 5+ forks (adoption signal for funders)

---

## Grant Pipeline

| Funder | Program | Deadline | Ask | Status |
|--------|---------|----------|-----|--------|
| **MCF** | Capacity Building | **June 2026** | $50-100K | LOI in preparation |
| **RWJF** | Local Data for Equitable Communities | **Fall 2026** (announcement) | $100-200K | Pre-application prep |
| Arnold Ventures | Housing Supply Reform | Submitted March 2026 | $200-400K (CWD, not TresPies) | Awaiting response |
| Knight Foundation | Civic Tech | Rolling | $50-100K | Research stage |
| Otto Bremer Trust | Community Development | 3-12 months post-policy brief | $25-50K | Not yet approached |
| Section 4 via LISC | CDC Capacity Building | Annual | $10-25K | Not yet approached |

---

## Revenue Forecast

| Quarter | Consulting | Cohorts | Grants | Total |
|---------|-----------|---------|--------|-------|
| Q2 2026 | $0 (TRP pro-bono) | — | — | $0 |
| Q3 2026 | — | — | MCF LOI submitted | $0 |
| Q4 2026 | TRP follow-on ($8-12K) | — | MCF award ($50-100K) | $58-112K |
| Q1 2027 | 1-2 pilots ($10-20K) | Cohort 1 ($4-18K) | RWJF prep | $14-38K |
| Q2 2027 | Mercy ($12-20K) | — | RWJF submitted | $12-20K |
| Q3 2027 | 2-3 engagements ($16-36K) | Cohort 2 ($4-18K) | — | $20-54K |
| Q4 2027 | 2-3 engagements ($16-36K) | — | RWJF award ($100-200K) | $116-236K |
| **Year 1 Total** | | | | **$58-112K** |
| **Year 2 Total** | | | | **$162-348K** |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| TRP leadership doesn't respond to cold outreach | Medium | High | Seek warm introduction via MacArthur Foundation or Chicago CDC network |
| Cook County data pipeline breaks at scale (1,318 tracts) | Low | Medium | Test against Cook County before TRP scoping call; Census API handles large counties |
| MCF grant not awarded | Medium | High | Self-fund curriculum development from consulting revenue; apply to Knight as backup |
| RWJF program doesn't materialize in Fall 2026 | Medium | Medium | Pursue Otto Bremer Trust and LISC Section 4 as alternatives |
| Cohort participants can't complete exercises (too technical) | Medium | High | Build "Week 0" onboarding (Python setup, Claude Code basics); pair participants with different skill levels |
| Mercy Housing procurement process stalls engagement | High | Medium | Start at Lakefront regional level (Mark Angelini), not national HQ; frame as pilot not vendor relationship |
| Claude Code pricing changes make methodology unaffordable | Low | High | Methodology is AI-agnostic; document alternatives in prompt library |
| Someone else builds this first | Low | Low | CWD proof-of-concept and first-mover case studies are the moat; speed matters |

---

## Immediate Next Actions (This Week)

1. **Send TRP outreach email** — review and send `case-studies/trp-outreach-draft.md` by April 7
2. **Test Cook County pipeline** — run `01_fetch_census.py` against Cook County (state 17, county 031) and verify output
3. **Fix pct_youth contradiction** — add youth indicator to `03_composite_scoring.py` or remove weight from config
4. **Write CWD case study** — sanitize CWD artifacts into `case-studies/cwd-madison.md`
5. **Push to GitHub** — `trespies/community-data-lab`, MIT license, public repo

---

## Validation Checklist

- [x] All phases have deliverables and success criteria
- [x] All recommendations tied to specific files (README.md, config_example.json, etc.)
- [x] Plan is actionable without needing additional context
- [x] All constraints from files listed explicitly (10 constraints)
- [x] Contradictions flagged and addressed (3 found)
- [x] Revenue model grounded in strategic scout research
- [x] Partner sequencing grounded in partner diligence research
- [x] Grant pipeline tied to specific deadlines
