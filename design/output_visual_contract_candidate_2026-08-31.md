# Daily Media Brief｜Visual Output Contract Candidate

Date: 2026-08-31
Status: `DESIGN_CANDIDATE__NOT_RUNTIME_VALIDATED`

This file records the current visual-output design separately from the already-existing text output contract.

It must not be interpreted as evidence that a renderer or production interface is already implemented.

## 1. Why this layer exists

The retrieval/decision core can already prepare structured news results, but a usable officer/manager experience should not look like a raw search transcript.

The proposed presentation layer turns the same reviewed data into a clean Daily Media Brief view.

Core principle:

`same evidence + same decision result → different presentation surface`

Presentation must not silently change search, relevance, deduplication, or factuality decisions.

## 2. Two-layer output

### Layer A｜Conversation short view

The conversation can first return a compact status such as:

- today's target count;
- qualified count;
- candidate count;
- the top few items worth reading first;
- current state: `待人工確認`.

This view should be concise.

### Layer B｜Visual Daily Media Brief

The expanded visual view is intended for direct officer/manager reading.

Recommended order:

1. 今日重點
2. 合標準新聞
3. 候選新聞
4. 待查證與次要資訊
5. 今日總摘要

## 3. Human-facing header

Recommended header fields:

- 日期
- 目標則數
- 合標準則數
- 候選則數
- 參考來源數
- 狀態：`待人工確認`

Do not expose internal runtime state names in the normal user interface.

## 4. Today-at-a-glance

The first screen should help the reader answer:

- 今天最重要的是哪幾件事？
- 哪幾則是合標準？
- 哪幾則只是候選？
- 今天大致有哪些主題？

Possible summary tiles:

- 優先閱讀
- 合標準新聞
- 候選新聞
- 今日主要議題

These are presentation counters, not a new relevance/scoring engine.

## 5. News card

Each normal news card should remain readable without engineering knowledge.

Required visible content:

- original title;
- 50–100 character Traditional Chinese summary;
- status label: `合標準` or `候選`;
- original URL.

Optional human-facing content:

- topic tags;
- `為什麼值得看`;
- `可能影響` or `目前狀態`;
- `建議關注`;
- collapsible source/supplementary information.

Avoid normal-user labels such as:

- G4 / G8;
- runtime;
- source role;
- AWAITING_HUMAN_REVIEW;
- Output Contract;
- internal score names;
- regression aliases.

## 6. Candidate-news card

Candidate news should explain, in human terms:

- `為什麼列入候選`
- `承辦可以怎麼處理`

Candidate means contextual/comparative/forward-looking/follow-up value.
It does not mean low factual quality.

## 7. Unverified / signal area

Forum/social/other early signals must not visually blend into the verified normal-news list.

Human-facing language can simply state:

`待查證消息`

Recommended explanation:

> 如果論壇、社群或其他非正式來源出現值得注意的消息，會單獨放在這裡。尚未確認前，不會和正式新聞混在一起。

## 8. Daily overall summary

Final section:

`今日總摘要`

Maximum 250 Traditional Chinese characters.

It may summarize shared trends, major events, and areas worth attention from the current batch only.
It must not introduce unsupported facts.

## 9. Clean separation between explanation and demo

The current Overview uses two sections in the Output tab.

### O01 · HOW TO READ

This is explanation only.

It tells the project team:

- first look at today's highlights;
- then read the full news list;
- human decides what to use.

### O02 · DEMO OUTPUT

O02 starts after a strong visual break.

From this point onward the page should look like a finished user-facing Daily Media Brief, not a technical specification.

Do not insert engineering explanations inside the demo body.

## 10. Relation to the existing output contract

Existing callable contract remains authoritative for minimum structured content:

- `合標準（X 則）`
- `候選新聞（X 則）`
- `今日總摘要`
- original title
- 50–100 character summary
- full URL
- 250-character daily overall summary

This visual contract is a presentation-layer candidate above that contract.

## 11. Implementation boundary

Current status:

- design: documented;
- Overview demo: documented;
- production renderer: not claimed;
- real runtime binding: not validated;
- Internal PoC: not claimed passed.

Before implementation/promotion:

1. project team confirms the visual structure;
2. approved fields are mapped to the runtime output schema;
3. platform renderer/adaptor is implemented;
4. real runs are tested with long titles, missing sources, under-target counts, candidate-only cases, and mobile layout;
5. evidence is preserved.
