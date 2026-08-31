# Daily Media Brief｜Current Technology Map

Updated: 2026-08-31
Status: `HANDOFF_READY_WITH_OPEN_ITEMS`
Callable platform candidates: `v0.6.0-rc1`
Next retrieval candidate: **Dual Recall Architecture**
Production ready: **NO**

This file is the public-safe map of the current Daily Media Brief technology.
It exists so a new collaborator does not need to reconstruct the system from scattered YAML and Markdown files.

---

## 1. Product Goal

A staff member can ask naturally, for example:

`給我今日輿情 10 則`

The system should find enough same-day information, avoid obvious retrieval blind spots, verify sources/facts/date, evaluate business relevance, deduplicate events, create faithful summaries, and stop for human review.

The final output is a structured human-facing brief, not raw search results.

---

## 2. Current User Flow

`INPUT → RETRIEVAL → FORMAL PROCESS → OUTPUT → HUMAN REVIEW`

### Input

Examples:

- `給我今日輿情 X 則`
- `給我今天資安輿情 10 則`
- `今天只看資安`

G1 decides the requested date/time scope and final output target before retrieval begins.

### Formal process

User-facing process names remain:

- G0｜執行準備
- G1｜日期與目標則數
- Search Planner / Retrieval Layer
- G2｜來源與證據
- G3｜具體事實
- G4｜業務相關性
- G5｜重複判斷
- G6｜摘要忠實度
- G7｜數量與交付完整度
- G8｜人工確認

Legacy Q0–Q8 identifiers may remain only where required for regression traceability.

---

## 3. Retrieval Architecture｜Current Candidate Direction

2026-08-31 testing exposed a structural recall gap.

A simple date + keyword baseline found some same-day Kaohsiung / RDEC / iPASS material that the formal run did not surface, while the formal run found governed/security/AI-infrastructure items that were not prominent in the simple keyword baseline.

Therefore the retrieval layer is moving toward **two independent recall paths**.

```text
G1 date + output target
        │
        ├─────────────── RAW RECALL LANE
        │                direct Primary Keywords
        │                controlled related keywords
        │                broad daily sweep
        │                minimal raw filtering
        │
        └─────────────── FORMAL SKILL LANE
                         broad / source / precision / semantic recall
                         TW100 planning when available
                         project watchlist
        │
        ▼
MERGED CANDIDATE POOL
        │
        ▼
G2 → G3 → G4 → G5 → G6 → G7 → G8
```

Core principle:

> Raw decides what gets a chance to be seen.
> Formal gates decide what deserves to be shown.

Architecture candidate authority:

`design/dual_recall_architecture_candidate_2026-08-31.md`

This is **not runtime-validated authority yet**.

---

## 4. Raw Recall Lane｜Platform-Agnostic Safety Net

Shared candidate assets:

- `shared/RAW_RECALL_POWER_META_PROMPT.md`
- `shared/raw_recall_keyword_pack_kcg_v0.1.yaml`

Purpose:

- guarantee direct Primary Keyword search coverage;
- preserve a simple retrieval path that future models can execute;
- prevent semantic/governed retrieval from becoming the only way the system can see news;
- produce an inspectable `RAW_RECALL_PACKET` for later merge.

### Minimum environment requirement

The Raw Lane requires only ordinary web/search capability.

It must not require:

- TW100;
- YAML parsing;
- MCP;
- vector databases;
- a specific model vendor;
- a specific search API;
- G0–G8 knowledge.

If no web/search capability exists, it must fail explicitly instead of fabricating results.

### Raw stages

- R1｜Primary Keyword Direct Sweep
- R2｜Controlled Related Keyword Sweep
- R3｜Broad Daily Sweep
- R4｜Active Project Watchlist Sweep
- Minimal Raw Cleanup
- `RAW_RECALL_PACKET`

Every Primary Keyword should be represented by at least one direct query before Raw Recall is considered complete, unless a hard environment budget prevents it.

Raw Recall may remove only exact duplicates, verified off-date results, broken/empty results, and obvious spam.
It does **not** make final business-relevance decisions.

---

## 5. Formal Skill Lane｜Governed Retrieval and Decision

The Formal Lane retains responsibility for:

- broad recency retrieval;
- high-yield source sweep;
- profile precision queries;
- alias / semantic expansion;
- project watchlist recall;
- TW100 active-source planning where supported;
- source qualification;
- factuality;
- business relevance;
- event/cross-day deduplication;
- faithful summaries;
- delivery completeness;
- human review.

Recall-first patch candidate:

`design/recall_first_search_patch_candidate_2026-08-31.yaml`

The Raw Lane does not replace this patch.
The intended design is **complementary recall**, not winner-takes-all retrieval.

---

## 6. Parallel and Sequential Modes

### Preferred when supported: Parallel

Run Raw Recall and Formal Skill independently, then merge candidate pools before G2.

Benefits:

- independent blind spots;
- easier telemetry;
- no lane can prematurely suppress the other;
- faster in multi-tool environments.

### Universal fallback: Sequential

1. Raw Recall first.
2. Formal Skill receives `RAW_RECALL_PACKET`.
3. Formal Skill still performs its own required retrieval.
4. Merge before G2.

This allows constrained/local/single-agent environments to use the same semantic architecture.

---

## 7. Merge Contract

Merge before G2 using, in order:

1. canonical URL;
2. normalized URL;
3. normalized title;
4. later G5 event-level semantic deduplication.

Do not discard provenance when merging.

A merged item should preserve `recall_origins`, for example:

- `RAW_PRIMARY`
- `RAW_RELATED`
- `RAW_BROAD`
- `RAW_PROJECT`
- `FORMAL_BROAD`
- `FORMAL_SOURCE_SWEEP`
- `FORMAL_PRECISION`
- `FORMAL_SEMANTIC`

This makes Raw-only and Formal-only useful hits measurable.

---

## 8. G1 / Search Targets / G7

### G1

G1 decides:

- date/time scope;
- `output_target` / requested final news count.

The final output target must not be reused as the Raw or Formal discovery stop signal.

### Distinct retrieval quantities

Candidate concepts now include:

- `output_target`: final number requested by the officer;
- `raw_unique_target`: optional Raw Recall pool target;
- `formal_discovery_pool_target`: Formal Lane pre-G4 candidate target;
- `eligible_pool_target`: G4-after candidate pool available for replacement/diversity.

Current PoC candidates, not frozen rules:

- Raw: `max(output_target * 4, 40)`
- Formal discovery: `max(output_target * 3, 24)`
- Formal eligible: approximately `1.5x output_target` with a replacement buffer.

Coverage obligations matter more than hitting these candidate numbers.

### G7

G7 checks final delivery completeness against the G1 output target.
It must not use `output_target reached` alone as proof that retrieval was complete.

Same-day coverage should be expanded before T2/T3 time-window expansion.
If quality cannot meet target, report the shortage instead of padding.

---

## 9. Current KCG Keyword Design

Human-reviewed design candidate:

`design/poc_search_profile_candidate_2026-08-31.yaml`

Cross-model Raw candidate:

`shared/raw_recall_keyword_pack_kcg_v0.1.yaml`

Current Primary Keyword set contains 13 officer-provided terms:

- 高雄市
- 高雄市政府研究發展考核委員會
- 高雄市政府資訊處
- 智慧城市
- 物聯網
- 大數據資訊
- 資安
- AI
- 數位發展部
- 市民卡
- 一卡通
- MyData
- 智慧杆

The Raw pack also contains controlled aliases, related-keyword groups, and project-watchlist terms.

Important boundary:

These are design candidates pending final business calibration and runtime validation.

---

## 10. TW100 Coverage Registry

Authority file inside each platform lane:

`source_registry_taiwan.yaml`

Registry ID:

`TW100-COVERAGE-2026-08`

Meaning:

- curated 100-source Taiwan coverage pool;
- not a traffic ranking;
- not a trust ranking.

TW100 belongs primarily to the governed Formal Lane.
The Raw Lane intentionally does not depend on TW100 so it remains portable to other models/environments.

---

## 11. Formal Gate Responsibilities

After retrieval merge:

### G2｜來源與證據
Determine evidence role/admissibility.

### G3｜具體事實
Remove pure opinion, pure marketing, unsupported/non-event material, and apply configured negative conditions.

### G4｜業務相關性
Human-facing states:

- `合標準`
- `候選新聞`
- `排除`

### G5｜重複判斷
Batch and cross-day event deduplication.

### G6｜摘要忠實度
Each item requires original title, faithful 50–100 Traditional Chinese character summary, and full original URL.

### G7｜數量與交付完整度
Check G1 final target and output contract.

### G8｜人工確認
Hard human-review boundary.

---

## 12. Output Contract

Minimum structured output:

1. `合標準（X 則）`
2. `候選新聞（X 則）`
3. `今日總摘要`

Each item:

- original title;
- 50–100 Traditional Chinese character summary;
- full original URL.

Overall daily summary:

- <=250 Chinese characters.

Visual output design candidate:

`design/output_visual_contract_candidate_2026-08-31.md`

Human-facing Overview:

`architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`

---

## 13. Human and Publication Boundary

G8 is a hard human review boundary.

The system may prepare, explain, replace, and search more.

It must not treat a draft as published.

`approved != confirmed published`

Planned lifecycle:

`discovered_news → selected_news → published_news`

The complete lifecycle store remains **not implemented/validated**.

---

## 14. Cross-Model Technology Direction

Long-term architecture should separate:

### Shared universal core

- Raw Recall Power Meta Prompt;
- controlled keyword/profile contract;
- Raw Recall Packet schema;
- candidate merge contract;
- formal gate semantics;
- output semantics;
- cross-model regression set.

### Model/environment adapters

- ChatGPT search adapter;
- Claude search adapter;
- Gemini/browser adapter;
- local-agent adapter;
- optional future search/MCP adapters.

Target principle:

**Stable shared core + replaceable model adapters + replaceable business profiles.**

This is the preferred direction for future reuse beyond one model or one department.

---

## 15. Platform Lanes

### Claude

`claude/daily-media-brief/v0.6.0-rc1/`

Real fresh Claude E2E remains required before promotion.

### ChatGPT

`chatgpt/daily-media-brief/v0.6.0-rc1/`

ChatGPT is currently the first likely reference implementation for validating the new retrieval architecture.

Neither platform runtime has yet been declared upgraded to the Dual Recall candidate.

Do not make one platform lane import runtime files directly from the other.

---

## 16. Current Authority Layers

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

### Shared/design candidates

- `shared/RAW_RECALL_POWER_META_PROMPT.md`
- `shared/raw_recall_keyword_pack_kcg_v0.1.yaml`
- `design/dual_recall_architecture_candidate_2026-08-31.md`
- `design/recall_first_search_patch_candidate_2026-08-31.yaml`
- `design/poc_search_profile_candidate_2026-08-31.yaml`
- `design/output_visual_contract_candidate_2026-08-31.md`
- `architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`

Design candidates do not by themselves prove runtime implementation or validation.

---

## 17. Validation Boundary

Confirmed:

- current G0–G8 contract exists;
- TW100 exists;
- direct-keyword baseline exposed useful Raw-only hits;
- Recall-first test produced a full same-day ten-item brief;
- a platform-agnostic Raw Recall contract now exists;
- a Dual Recall architecture candidate now exists.

Not yet safe to claim:

- merged Dual Recall runtime PASS;
- formal A/B/C/D regression complete;
- ChatGPT rc2 frozen;
- fresh Claude E2E PASS;
- Internal PoC 1 PASS;
- Internal PoC 2 PASS;
- external PoC approved;
- production-ready.

---

## 18. Next Engineering Sequence

1. Execute fixed 2026-08-31 regression comparing:
   - Original Formal Skill;
   - Recall-first Formal Skill;
   - Direct Keyword Raw baseline;
   - Dual Recall merged candidate.
2. Measure Primary Keyword coverage, unique same-day recall, Raw-only useful hits, Formal-only useful hits, exclusion/noise ratio, eligible pool, and final usefulness.
3. Calibrate Raw and Formal pool targets.
4. If results hold, integrate ChatGPT as the first reference adapter.
5. Freeze the shared semantic contract.
6. Align Claude against the same shared contract.
7. Run Internal PoC and preserve evidence.

---

## 19. Handoff Reading Order

1. `README.md`
2. `CURRENT_TECHNOLOGY_MAP.md`
3. `design/dual_recall_architecture_candidate_2026-08-31.md`
4. `shared/RAW_RECALL_POWER_META_PROMPT.md`
5. `shared/raw_recall_keyword_pack_kcg_v0.1.yaml`
6. `architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`
7. `design/recall_first_search_patch_candidate_2026-08-31.yaml`
8. relevant platform lane files
9. `HANDOFF_CURRENT.md`

Internal project history, user/person feedback, PoC raw evidence, and governance logs remain in the private `Endwar116/KS-goverment` repository.
