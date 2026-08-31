# Daily Media Brief｜Current Handoff

Updated: 2026-08-31
Status: `HANDOFF_READY_WITH_OPEN_ITEMS`

This file is the public-safe handoff entry point.

## Read first

1. `README.md`
2. `CURRENT_TECHNOLOGY_MAP.md`
3. `design/dual_recall_architecture_candidate_2026-08-31.md`
4. `shared/RAW_RECALL_POWER_META_PROMPT.md`
5. `shared/raw_recall_keyword_pack_kcg_v0.1.yaml`
6. `architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`
7. `DESIGN_HISTORY/2026-08-31_ZERO_GAP_RECONCILIATION.md`

## Current platform target

- Claude lane: `claude/daily-media-brief/v0.6.0-rc1/`
- ChatGPT lane: `chatgpt/daily-media-brief/v0.6.0-rc1/`

The platform runtimes have **not yet been declared upgraded** to the new Dual Recall design.

Do not make one platform lane import runtime files from the other.

## Current retrieval decision

2026-08-31 testing showed that direct date + keyword search and the governed Formal Skill each find useful same-day items the other may miss.

The current design direction is therefore:

```text
RAW RECALL LANE ─┐
                 ├─> MERGED CANDIDATE POOL -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8
FORMAL SKILL LANE┘
```

### Raw Recall Lane

Purpose: maximize basic visibility and guarantee direct Primary Keyword coverage.

Shared candidate files:

- `shared/RAW_RECALL_POWER_META_PROMPT.md`
- `shared/raw_recall_keyword_pack_kcg_v0.1.yaml`

Raw Recall must remain cross-model and cross-environment.
It requires only ordinary search capability.
It performs minimal cleanup only and does not make final business-relevance decisions.

### Formal Skill Lane

Purpose: governed retrieval and formal decision quality.

Relevant current candidates:

- `design/recall_first_search_patch_candidate_2026-08-31.yaml`
- `design/poc_search_profile_candidate_2026-08-31.yaml`

The Formal Lane continues to own G2–G8, TW100 planning, source qualification, factuality, relevance, deduplication, faithful summaries, delivery completeness, and human review.

## Merge point

Merge Raw and Formal candidate pools **before G2**.

Preserve recall provenance such as:

- `RAW_PRIMARY`
- `RAW_RELATED`
- `RAW_BROAD`
- `RAW_PROJECT`
- `FORMAL_BROAD`
- `FORMAL_SOURCE_SWEEP`
- `FORMAL_PRECISION`
- `FORMAL_SEMANTIC`

Do not discard duplicate provenance when the same item is found by both lanes.

## Parallel / sequential execution

Preferred when supported:

- run Raw and Formal lanes independently in parallel;
- merge before G2.

Universal fallback:

1. Raw Recall first;
2. Formal Skill receives the Raw packet but still performs its own required retrieval;
3. merge before G2.

Sequential fallback exists so local or single-agent environments can still use the same architecture.

## Important target semantics

Do not use the officer's final requested count as the retrieval stop signal.

Separate:

- `output_target`
- optional `raw_unique_target`
- `formal_discovery_pool_target`
- `eligible_pool_target`

All current numeric formulas are PoC calibration candidates until regression evidence exists.

## Existing callable authority

Within each platform lane, treat the following as callable authority unless a newer explicit version is promoted:

- `SKILL.md`
- `runtime.yaml`
- `poc_calibration.yaml`
- `topic_profile.yaml`
- `source_registry_taiwan.yaml`
- `decision_policy.yaml`
- `workflow.md`
- `output_contract.md`
- `state/*`

Shared/design candidate files do not automatically replace platform runtime authority.

## Latest human-facing process decisions

- G0–G8 remain the formal user-facing Gate names.
- G1 decides date/time scope and final target count.
- Retrieval now has a Dual Recall candidate architecture before G2.
- G4 outputs `合標準 / 候選新聞 / 排除`.
- G6 requires original title, 50–100 character summary, and source URL.
- G7 checks final delivery completeness and must not treat `output target reached` as proof retrieval was complete.
- Daily overall summary is <=250 Traditional Chinese characters.
- G8 is a human review boundary.
- Approval is not automatically equal to confirmed publication.

## Validation evidence already observed

- Original/sparse retrieval exposed a recall problem.
- Recall-first Formal test produced ten same-day items without T2/T3.
- Direct Keyword baseline found some useful same-day local items not present in the formal ten-item result.
- Formal retrieval found some governed/security items not prominent in the simple keyword baseline.
- Therefore complementary recall is justified as a design hypothesis.

## Validation still required

Fixed regression day: `2026-08-31`.

Compare:

1. Original Formal Skill.
2. Recall-first Formal Skill.
3. Direct Keyword Raw baseline.
4. Dual Recall merged candidate.

Measure:

- Primary Keyword query coverage;
- unique same-day events;
- expected-hit recall;
- local/Kaohsiung recall;
- Raw-only useful hits;
- Formal-only useful hits;
- exclusion/noise ratio;
- source diversity;
- eligible pool size;
- final ten-item usefulness.

## Current validation status

- Dual Recall merged runtime: `NOT_RUN`
- formal A/B/C/D regression: `NOT_RUN`
- ChatGPT rc2 freeze: `NOT_DONE`
- Internal PoC 1: `NOT_CONFIRMED_PASS`
- Internal PoC 2: `NOT_CONFIRMED_PASS`
- fresh Claude E2E: `NOT_CONFIRMED_PASS`
- full lifecycle store: `NOT_COMPLETE`
- external PoC approval: `NOT_CONFIRMED`
- production ready: `FALSE`

## Next engineering action

1. Run the fixed Dual Recall regression.
2. Calibrate Raw/Formal pool targets.
3. If evidence supports the design, implement ChatGPT as the first reference adapter.
4. Freeze the shared semantic contract after reference validation.
5. Align Claude with the same shared contract.
6. Run Internal PoC.
7. Preserve evidence and update handoff/readiness.

## Private project history

People-specific feedback, conversation history, internal decisions, governance logs, PoC raw evidence, and project-state trace live in the separate private project repository:

`Endwar116/KS-goverment`

Do not copy private internal records into this public callable repository.
