# Daily Media Brief｜Universal Retrieval 2+1 Architecture Candidate

Date: 2026-09-01
Status: `DESIGN_CANDIDATE__NOT_RUNTIME_VALIDATED`
Purpose: Converge a cross-platform retrieval core that can run on ChatGPT, Claude, Gemini, browser agents, and local agents with ordinary web search, while allowing RSS/feed access as an optional accelerator rather than a hard dependency.

---

## 1. Design Goal

The shared Skill must remain usable when the environment only has ordinary web search.

The minimum portable architecture therefore contains two mandatory retrieval lanes and one optional accelerator lane.

```text
G1 date / timezone / output_target / brief_profile
        │
        ├─ Lane A｜RAW DIRECT SEARCH              [MANDATORY]
        ├─ Lane B｜FORMAL / SEMANTIC SEARCH       [MANDATORY]
        └─ Lane C｜RSS / FEED ACCELERATOR         [OPTIONAL]
        │
        ▼
NORMALIZED + MERGED CANDIDATE POOL
        │
        ▼
G2 → G3 → G4 → G5 → G6 → G7 → G8
```

Core principle:

- Raw protects recall.
- Formal protects usefulness and governance.
- RSS/feed reduces discovery/date-verification cost where the environment supports it.
- No single lane is allowed to become the only retrieval path.

---

## 2. Lane A｜Raw Direct Search

Mandatory cross-model safety net.

Minimum requirement: ordinary web search.

Responsibilities:

- direct query coverage for every Primary Keyword;
- controlled related-keyword search;
- broad same-day search;
- active project-watchlist search;
- minimal raw cleanup only.

Raw may remove only:

- exact duplicate URLs;
- verified off-date items;
- broken/empty results;
- obvious spam;
- duplicate mirrors when the canonical/original source is known.

Raw does not decide final business relevance.

Shared candidate assets:

- `shared/RAW_RECALL_POWER_META_PROMPT.md`
- `shared/raw_recall_keyword_pack_kcg_v0.1.yaml`

---

## 3. Lane B｜Formal / Semantic Search

Mandatory governed recall path.

Responsibilities:

- broad recency discovery;
- high-yield source sweep;
- profile precision queries;
- aliases and semantic expansion;
- project watchlist;
- TW100/source planning where supported;
- formal source/fact/relevance/dedup/output rules after merge.

Current candidate reference:

- `design/recall_first_search_patch_candidate_2026-08-31.yaml`

Formal search is not allowed to suppress Raw search because it has already found enough final-output candidates.

---

## 4. Lane C｜RSS / Feed Accelerator

Optional capability lane.

RSS/feed support is useful for:

- fast same-day discovery;
- structured publication time;
- predictable source polling;
- reducing repeated generic search queries for high-yield publishers.

But RSS must not be a universal hard dependency because:

- many important government/official sources have no usable feed;
- RSSHub routes can break when source sites change;
- some chat environments cannot fetch `application/rss+xml` directly;
- external feed readers/MCP/connectors may not exist in all model environments.

### Priority order

```text
Official publisher RSS
  > trusted feed adapter / reader
  > RSSHub-derived feed
  > normal web-search fallback
```

### Capability behavior

If feed access exists:

- execute RSS lane in parallel when possible;
- otherwise execute sequentially and merge before G2.

If feed access does not exist:

- return `RSS_CAPABILITY_UNAVAILABLE`;
- continue Raw + Formal normally;
- do not fail the Skill.

---

## 5. RSS Date Semantics

RSS does not skip G1.

G1 still defines:

- requested date/time scope;
- timezone;
- final output target.

RSS can reduce per-item date-discovery/verification cost.

Normalized candidates should distinguish evidence types.

```yaml
published_at: "2026-09-01T10:30:00+08:00"
date_evidence_type: "OFFICIAL_RSS|ARTICLE_PAGE|RSSHUB_DERIVED|SEARCH_SNIPPET|UNKNOWN"
date_confidence: "HIGH|MEDIUM|LOW|UNKNOWN"
```

Candidate confidence guidance:

- `OFFICIAL_RSS`: HIGH, subject to source metadata quality.
- `ARTICLE_PAGE`: HIGH when explicit article publication time is available.
- `RSSHUB_DERIVED`: MEDIUM by default unless the adapter demonstrably forwards source-native feed metadata unchanged.
- `SEARCH_SNIPPET`: LOW or MEDIUM; formally selected items should be verified when the date matters.

Do not treat an RSSHub parser-generated `pubDate` as automatically equivalent to an official publisher RSS timestamp.

---

## 6. Common Candidate Schema

All retrieval lanes normalize into a common schema before formal gates.

```yaml
candidate:
  candidate_id: "..."
  title: "..."
  canonical_url: "..."
  source_name: "..."
  source_class: "..."
  published_at: "..."
  date_evidence_type: "..."
  date_confidence: "..."
  snippet_or_feed_summary: "..."
  recall_origins:
    - RAW_PRIMARY
    - RAW_RELATED
    - RAW_BROAD
    - RAW_PROJECT
    - FORMAL_BROAD
    - FORMAL_SOURCE_SWEEP
    - FORMAL_PRECISION
    - FORMAL_SEMANTIC
    - RSS_OFFICIAL
    - RSSHUB
  matched_terms: []
  brief_profile_id: "..."
```

Merge must preserve `recall_origins`.

This enables measurement of:

- Raw-only useful hits;
- Formal-only useful hits;
- RSS-only useful hits;
- overlap;
- lane yield and noise.

---

## 7. Universal Core vs Business Profile

The Universal Skill core must not hard-code Kaohsiung, AI, cybersecurity, or any department-specific keyword set.

Shared profile contract candidate:

```yaml
brief_profile:
  id: "..."
  locale: "..."
  primary_keywords: []
  aliases: {}
  related_keywords: []
  semantic_expansion: []
  project_watchlist: []
  negative_conditions: []
  source_hints: []
  relevance_anchors: []
  output_preferences: {}
```

Example replaceable profiles:

- `kcg_it_ai_digital_governance`
- `cybersecurity`
- `smart_city`
- `healthcare_policy`
- `company_competitor_watch`
- `personal_ai_research`

One-run overrides modify the current execution only and must not silently mutate the permanent profile.

---

## 8. Cross-Platform Degradation Rules

The shared Skill must degrade gracefully.

### Environment has ordinary web search only

Run Lane A + Lane B.

### Environment also has RSS/feed fetch

Run Lane A + Lane B + Lane C.

### Environment has TW100/source registry loader

Use it as Formal Lane source-planning enhancement.

### Environment has no TW100 loader

Formal Lane still runs from the profile and ordinary web search.

### Environment cannot parse YAML

JSON or equivalent labeled Markdown packet is acceptable.

### Environment has no web/search capability

Return an explicit capability failure.
Do not fabricate current news from model memory.

---

## 9. Freeze Acceptance Tests

Use a fixed regression day before freeze.

Recommended reference date: `2026-08-31`.

Compare:

1. Original Formal Skill.
2. Recall-first Formal Skill.
3. Raw Direct baseline.
4. Dual Recall merged candidate.
5. 2+1 Retrieval candidate where RSS/feed capability exists.

Measure at minimum:

- Primary Keyword query coverage;
- same-day unique event recall;
- expected-hit recall;
- local/Kaohsiung recall;
- Raw-only useful hits;
- Formal-only useful hits;
- RSS-only useful hits;
- source diversity;
- exclusion/noise ratio;
- eligible pool size;
- final human usefulness.

Also test profile portability using at least two profiles:

- AI / digital governance;
- cybersecurity.

The same user command should produce a clear topic shift by changing the profile only, without editing the Universal Skill core.

---

## 10. Current Boundary

This file defines a design candidate.

It does not prove:

- ChatGPT runtime integration;
- Claude runtime integration;
- RSS adapter implementation;
- fixed regression PASS;
- Internal PoC PASS;
- production readiness.

The next step is cross-agent review and regression before promoting the shared contract.
