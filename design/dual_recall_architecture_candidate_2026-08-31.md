# Daily Media Brief｜Dual Recall Architecture Candidate

Date: 2026-08-31
Status: `DESIGN_CANDIDATE__NOT_RUNTIME_VALIDATED`
Purpose: Combine a platform-agnostic Raw Recall Lane with the governed Formal Skill Lane so the system is less likely to miss obvious same-day items while preserving strict final quality control.

---

## 1. Decision

The retrieval layer should no longer rely on only one search strategy.

Preferred architecture:

```text
                    ┌────────────────────────────┐
                    │  RAW RECALL LANE           │
                    │  direct keywords + broad  │
                    │  minimal filtering only   │
                    └─────────────┬──────────────┘
                                  │
G1 date + target ─────────────────┤
                                  │
                    ┌─────────────▼──────────────┐
                    │  FORMAL SKILL LANE         │
                    │  source planning           │
                    │  semantic/project recall   │
                    │  governed retrieval        │
                    └─────────────┬──────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │ MERGED CANDIDATE POOL      │
                    │ canonical URL/title/event  │
                    └─────────────┬──────────────┘
                                  │
                    G2 → G3 → G4 → G5 → G6 → G7 → G8
```

The two lanes have different jobs.

- Raw Recall Lane: maximize visibility and direct keyword coverage.
- Formal Skill Lane: maximize business usefulness, evidence quality, semantic coverage, deduplication, and controlled output.

Neither lane should be treated as complete by itself.

---

## 2. Why Two Lanes

Observed on 2026-08-31:

- simple date + keyword searches surfaced same-day Kaohsiung / RDEC / iPASS items that the formal run did not place in its ten-item result;
- the formal run surfaced governed/security/AI infrastructure items that were not prominent in the simple keyword baseline;
- therefore direct keyword recall and formal semantic/governed retrieval have different blind spots.

The design goal is not to choose one winner.
The design goal is to make the blind spots overlap less.

---

## 3. Lane A｜Raw Recall Lane

Authority candidate:

- `shared/RAW_RECALL_POWER_META_PROMPT.md`
- `shared/raw_recall_keyword_pack_kcg_v0.1.yaml`

Responsibilities:

1. verify run date when possible;
2. directly query every Primary Keyword at least once;
3. query controlled related-keyword groups;
4. run a small broad same-day sweep;
5. optionally query active project-watchlist items;
6. remove only exact duplicates, verified off-date items, broken pages, and obvious spam;
7. return `RAW_RECALL_PACKET`.

It must not perform final business relevance ranking.

### Cross-model requirement

This lane must remain executable by any environment with ordinary search capability.

No mandatory dependency on:

- TW100;
- MCP;
- platform-specific search syntax;
- vector databases;
- a specific model;
- a specific browser/search provider.

If an environment cannot search the web, it must fail explicitly rather than fabricate results.

---

## 4. Lane B｜Formal Skill Lane

The existing governed lane keeps responsibility for:

- source/evidence planning;
- TW100 active-source planning when available;
- broad/recency sweep;
- high-yield source sweep;
- semantic expansion;
- project watchlist recall;
- source qualification;
- factuality;
- business relevance;
- event deduplication;
- faithful summaries;
- delivery completeness;
- human-review boundary.

Current recall-first patch candidate remains relevant:

`design/recall_first_search_patch_candidate_2026-08-31.yaml`

The new Raw Recall Lane does **not** replace it.

---

## 5. Merge Point

The merge occurs **before G2**.

Both lanes should preserve enough provenance to identify where an item came from.

Minimum merged candidate fields:

```yaml
candidate:
  title: "..."
  url: "..."
  source: "..."
  published_at: "..."
  snippet: "..."
  recall_origins:
    - "RAW_PRIMARY"
    - "RAW_RELATED"
    - "RAW_BROAD"
    - "RAW_PROJECT"
    - "FORMAL_BROAD"
    - "FORMAL_SOURCE_SWEEP"
    - "FORMAL_PRECISION"
    - "FORMAL_SEMANTIC"
  matched_terms: []
```

Merge key order:

1. canonical URL when available;
2. normalized original URL;
3. normalized title;
4. later G5 event-level semantic dedup.

Do not discard a duplicate candidate's provenance when merging.
If Raw and Formal lanes both found the same item, keep both `recall_origins`.

---

## 6. Parallel vs Sequential

### Preferred default: parallel when supported

Run Raw Recall Lane and Formal Skill Lane independently.

Advantages:

- independent search blind spots;
- no lane can prematurely suppress the other;
- easier A/B/C telemetry;
- faster when the environment supports parallel search.

### Universal fallback: sequential

1. Raw Recall first.
2. Formal Skill receives the Raw packet.
3. Formal Skill still performs its own required retrieval.
4. Merge all candidates before G2.

Sequential mode is preferred on constrained/local/single-agent environments.

---

## 7. Stop Conditions

Final user output target must not be used as the Raw Recall stop condition.

Three distinct concepts remain:

- `output_target`: what the officer wants to receive;
- `raw_unique_target`: optional Raw Recall calibration target;
- `formal_discovery_pool_target` / `eligible_pool_target`: governed lane calibration targets.

Candidate Raw value for PoC testing:

`raw_unique_target = max(output_target * 4, 40)`

This value is not frozen until regression telemetry exists.

Even when this target is reached, every Primary Keyword still requires direct query coverage unless the environment's hard budget prevents completion.

---

## 8. What Raw Lane Is Allowed to Delete

Allowed:

- exact duplicate URL;
- verified off-date result;
- clearly broken result;
- obvious empty/SEO spam page;
- duplicate mirror when an original source is known.

Not allowed in Raw Lane:

- deleting a result because it seems low priority;
- deleting a result because it would probably fail G4;
- deleting a result because its source is only discovery/signal quality;
- replacing formal evidence validation.

The purpose is to create a large, inspectable candidate pool.

---

## 9. Formal Gate Responsibility After Merge

After the merge, existing formal responsibilities remain:

- G2: source and evidence admissibility;
- G3: concrete fact / negative conditions;
- G4: `合標準 / 候選新聞 / 排除`;
- G5: event and cross-day deduplication;
- G6: original title + faithful 50–100 character summary + URL;
- G7: target count and delivery completeness;
- G8: human confirmation.

This is the core separation:

> Raw decides what gets a chance to be seen.
> Formal gates decide what deserves to be shown.

---

## 10. Cross-Model Portability

The long-term reusable technology should separate:

### Shared universal layer

- Raw Recall Power Meta Prompt;
- controlled keyword pack;
- Raw Recall Packet schema;
- merge contract;
- cross-model test set.

### Platform adapters

- ChatGPT search adapter;
- Claude search adapter;
- Gemini/browser adapter;
- local-agent adapter;
- future search/MCP adapters.

Adapters may optimize tool usage but must preserve the shared semantic contract.

This prevents the technology from becoming tied to one model's search syntax or one vendor's tool stack.

---

## 11. Validation Plan Before Freeze

Use 2026-08-31 as a fixed regression day.

Compare:

1. Original Formal Skill.
2. Recall-first Formal Skill.
3. Direct Keyword Raw Baseline.
4. Dual Recall merged candidate.

Metrics:

- Primary Keyword query coverage;
- unique same-day discovered events;
- expected-hit recall;
- Kaohsiung/local expected-hit recall;
- formal eligible count;
- noise/exclusion ratio;
- source diversity;
- final ten-item usefulness;
- overlap between Raw and Formal lanes;
- Raw-only useful hits;
- Formal-only useful hits.

Do not freeze this architecture as runtime authority until the merged approach is actually executed and compared.

---

## 12. Release Direction

If validation confirms the design:

- promote the shared Raw Recall contract as platform-agnostic core;
- integrate ChatGPT as the first reference adapter;
- align Claude against the same shared contract;
- keep profile, keyword pack, negative conditions, source priorities, and presentation as replaceable configuration layers.

Target principle:

**Stable shared core + replaceable model adapters + replaceable business profiles.**
