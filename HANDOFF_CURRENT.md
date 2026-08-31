# Daily Media Brief｜Current Handoff

Updated: 2026-08-31
Status: `HANDOFF_READY_WITH_OPEN_ITEMS`

This file is the public-safe handoff entry point.

## Read first

1. `README.md`
2. `CURRENT_TECHNOLOGY_MAP.md`
3. `architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`
4. `DESIGN_HISTORY/2026-08-31_ZERO_GAP_RECONCILIATION.md`

## Current platform target

- Claude lane: `claude/daily-media-brief/v0.6.0-rc1/`
- ChatGPT lane: `chatgpt/daily-media-brief/v0.6.0-rc1/`

Claude remains the finalization target.
ChatGPT remains the portability comparator.

Do not make one platform lane import runtime files from the other.

## Current design candidates awaiting deliberate merge

### Search/profile candidate

`design/poc_search_profile_candidate_2026-08-31.yaml`

Contains the later officer-provided keyword set plus aliases, semantic expansion, project watchlist, and negative-condition candidates.

This file does not replace platform `topic_profile.yaml` yet.

### Visual output candidate

`design/output_visual_contract_candidate_2026-08-31.md`

Defines the current human-facing Daily Media Brief presentation concept.

It does not prove that a renderer is implemented.

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

## Latest human-facing process decisions

- G0–G8 are the user-facing Gate names.
- G1 decides date/time scope and target news count before search.
- Search Planner sits between G1 and G2.
- Search Planner includes literal keywords plus semantic expansion and TW100 active-source planning.
- G4 outputs 合標準／候選新聞／排除 in the human-facing layer.
- G6 requires original title, 50–100 character summary, and source URL.
- G7 checks the G1 target and delivery completeness; it does not invent a new target.
- Final overall summary is <=250 Traditional Chinese characters.
- G8 is a human review boundary.
- Approval is not automatically equal to confirmed publication.

## TW100

`source_registry_taiwan.yaml` is a 100-source coverage registry, not a traffic or trust ranking.

Do not sequentially crawl all 100 sources.
Select an active source set from profile/topic/source lane.

## Important implementation boundary

The current Overview and design candidates represent the latest discussion/calibration state.

They must not be presented as completed runtime implementation unless the approved design has actually been merged into the platform authority files and validated.

## Validation status

- Internal PoC 1: `NOT_CONFIRMED_PASS`
- Internal PoC 2: `NOT_CONFIRMED_PASS`
- fresh Claude E2E: `NOT_CONFIRMED_PASS`
- full discovered/selected/published lifecycle store: `NOT_COMPLETE`
- external PoC approval: `NOT_CONFIRMED`
- production ready: `FALSE`

## Next engineering action

1. Review/calibrate current Overview and design candidates.
2. Merge approved search/profile parameters into both platform lanes.
3. Map approved visual fields to runtime output schema if the visual design is accepted.
4. Run static validation and cross-lane diff.
5. Run Internal PoC 1.
6. Run Internal PoC 2.
7. Preserve evidence.
8. Update handoff/readiness only after evidence exists.

## Private project history

People-specific feedback, conversation history, internal decisions, governance logs, PoC evidence, and project-state trace live in the separate private project repository:

`Endwar116/KS-goverment`

Do not copy private internal records into this public callable repository.