# Daily Media Brief｜Current Technology Map

Updated: 2026-08-31
Status: `HANDOFF_READY_WITH_OPEN_ITEMS`
Callable candidate: `v0.6.0-rc1`
Production ready: **NO**

This file is the public-safe map of the current Daily Media Brief technology. It exists so a new collaborator does not need to reconstruct the system from scattered YAML and Markdown files.

## 1. Product Goal

A staff member can ask for a daily media brief in natural language, for example:

`給我今日輿情 15 則`

The system plans search coverage, retrieves related information even when literal keywords are absent, verifies source/date/facts, evaluates business relevance, deduplicates events, produces faithful summaries, and stops for human review.

The final human-facing output is structured and visual rather than a raw list of search results.

## 2. Current User Flow

`INPUT → PROCESS → OUTPUT → HUMAN REVIEW`

### Input

Current intended input forms include:

- `給我今日輿情 X 則`
- `給我今天資安輿情 10 則`
- one-run overrides such as `今天只看資安`

The target number of news items is decided before search begins.

### Process

Current user-facing process names:

- G0｜執行準備
- G1｜日期與目標則數
- Search Planner｜搜尋規劃／關聯搜尋
- G2｜來源與證據
- G3｜具體事實
- G4｜業務相關性
- G5｜重複判斷
- G6｜摘要忠實度
- G7｜數量與交付完整度
- G8｜人工確認

Legacy Q0–Q8 identifiers can remain internally only where they are still required for regression traceability.

### Output

Minimum structured contract:

1. `合標準（X 則）`
2. `候選新聞（X 則）`
3. `今日總摘要`

Each news item requires:

- original title;
- 50–100 Traditional Chinese character summary;
- full original URL.

Daily overall summary: maximum 250 Chinese characters.

A visual output layer is currently a **design candidate**. See `design/output_visual_contract_candidate_2026-08-31.md` and `architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`.

## 3. G1 and G7 Current Decision

### G1

G1 decides the run scope before search:

- date/time window;
- `target_total_count`.

The target count belongs to the user/officer or an explicitly configured profile. The model must not silently invent 12/15/20 as a permanent default.

### G7

G7 does not choose the target.

It checks the G1 target and delivery completeness:

- qualified count;
- candidate count;
- actual total count;
- title present;
- summary length valid;
- original URL present;
- daily overall summary present and <=250 characters.

When same-day coverage is insufficient, source coverage expands before time-window expansion. If the target still cannot be met without lowering quality, the run must report the shortage instead of padding.

## 4. Search Planner

The Search Planner is explicitly located between G1 and G2:

`G1 → Search Planner → G2`

It is not currently treated as a Gate.

Its responsibilities are:

- Primary Keywords;
- aliases / normalization;
- Semantic Expansion;
- project watchlist;
- query plan;
- TW100 active source set.

Retrieval must not depend only on literal keyword matches.

Conceptual chain:

`primary_keyword → synonym → professional_term → related_concept → project_concept → event_type / related_entity → query_plan → candidate_news → G4 relevance`

Current officer-provided keyword candidate set and expansion candidates are recorded in:

`design/poc_search_profile_candidate_2026-08-31.yaml`

Important status boundary: this design candidate is **not yet declared runtime-validated authority**.

## 5. TW100 Coverage Registry

Authority file in each platform lane:

`source_registry_taiwan.yaml`

Registry ID:

`TW100-COVERAGE-2026-08`

Meaning:

- curated 100-source Taiwan coverage pool;
- not a traffic ranking;
- not a trust ranking;
- source class determines search/evidence role, not issue importance.

Daily runs do not query all 100 sources sequentially.

The active source set is chosen by topic/profile/source lane.

Expected source coverage includes:

- official / institutional / professional sources;
- mainstream / business / editorial sources;
- peer-city / local comparison sources;
- signal sources when useful.

Signal-only sources can help discover events but do not automatically become final evidence for high-risk factual claims.

## 6. Current Keyword Design Boundary

The public callable runtime currently contains an earlier compact topic profile.

A later human-reviewed design iteration contains 13 officer-provided Primary Keywords plus aliases and semantic/project expansion candidates.

To avoid pretending that design review equals completed coding, the newer set is stored separately as a design candidate until it is deliberately merged into both platform runtime authorities and validated.

This is an intentional boundary, not an omission.

## 7. Relevance Bands

User-facing labels:

- `合標準`
- `候選新聞`
- `排除`

Internal aliases may still exist for regression compatibility, but should not appear in officer/manager interfaces.

`候選新聞` is not a low-quality bucket. It is for comparison, forward-looking, follow-up, or contextual value that remains useful for human judgment.

## 8. Human Review Boundary

G8 is a hard human review boundary.

The system can prepare, replace, search more, or explain inclusion decisions.

It must not silently treat a generated draft as published.

Current principle:

`approved != confirmed published`

Actual publication requires a separate human feedback or external publish event.

## 9. News Lifecycle Roadmap

Planned lifecycle model:

`discovered_news → selected_news → published_news`

- discovered: the system has seen/evaluated it;
- selected: a human chose it for use/review;
- published: publication/share was actually confirmed.

The complete lifecycle store is **not implemented/validated yet**.

The existing published-history mechanism must not be described as equivalent to the full lifecycle design.

## 10. Phase 2 Generalization

Planned main switch:

`brief_profile_id`

The goal is one shared core with replaceable profiles, not separate rewritten Skills for every topic.

Candidate profiles:

- `cybersecurity`
- `ai_digital_governance`
- `smart_city`
- future custom profiles

A profile may define:

- primary keywords;
- Semantic Expansion;
- project watchlist;
- source priorities;
- negative conditions;
- G4 relevance anchors;
- default target count;
- presentation preferences.

One-run overrides must not automatically mutate a permanent profile.

## 11. Phase 3 Presentation Layer

The same selected data can later support different views:

- officer review list;
- visual Daily Media Brief;
- section-chief one-pager;
- director executive brief;
- weekly trend view.

Presentation changes must not silently change retrieval/decision logic.

## 12. Platform Lanes

### Claude

Path:

`claude/daily-media-brief/v0.6.0-rc1/`

Role: finalization target.

Real fresh Claude runtime E2E remains required before promotion.

### ChatGPT

Path:

`chatgpt/daily-media-brief/v0.6.0-rc1/`

Role: portability comparator with ChatGPT-specific operator layer.

A fresh independent v0.6 E2E remains required if this lane is promoted.

The two lanes must not directly import runtime files from each other.

## 13. Current Authority Layers

### Callable authority

Within each platform lane:

- `SKILL.md`
- `runtime.yaml`
- `poc_calibration.yaml`
- `topic_profile.yaml`
- `source_registry_taiwan.yaml`
- `decision_policy.yaml`
- `workflow.md`
- `output_contract.md`
- `state/*`

### Current design / discussion authority

- `CURRENT_TECHNOLOGY_MAP.md`
- `design/poc_search_profile_candidate_2026-08-31.yaml`
- `design/output_visual_contract_candidate_2026-08-31.md`
- `architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`

Design files describe the latest agreed/discussion state but do not themselves prove runtime implementation.

## 14. Current Validation Boundary

Confirmed at repository/document level:

- G1/G7 compact contract exists;
- G0–G8 user-facing mapping exists;
- TW100 registry exists in platform lanes;
- source expansion/relevance/dedup/output contracts exist;
- human-review stop is specified;
- latest design state is now consolidated in this map.

Not yet safe to claim:

- real fresh Claude E2E PASS;
- Internal PoC 1 PASS;
- Internal PoC 2 PASS;
- full news lifecycle store complete;
- external PoC approved;
- production-ready.

## 15. Next Engineering Sequence

1. Review and calibrate the current Overview and candidate search/output design.
2. Deliberately merge approved keyword/profile changes into both platform lanes.
3. Run static contract validation and lane diff.
4. Run Internal PoC 1 fresh run.
5. Run Internal PoC 2 stateful rerun.
6. Preserve evidence.
7. Obtain explicit external-PoC approval before changing readiness state.

## 16. Handoff Reading Order

1. `README.md`
2. `CURRENT_TECHNOLOGY_MAP.md`
3. `architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`
4. `design/poc_search_profile_candidate_2026-08-31.yaml`
5. `design/output_visual_contract_candidate_2026-08-31.md`
6. relevant platform lane files
7. `HANDOFF_CURRENT.md`

For internal project history, decisions, people-specific context, PoC evidence, and conversation trace, use the separate private project repository.