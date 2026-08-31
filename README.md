# KCG IT Daily Media Brief · Callable Technology Repository

這個 repository 保存可被模型載入、呼叫、比較、審查與延伸的 Daily Media Brief 輿情技術。

內部專案紀錄、人物／訪談內容、顧問討論、完整 PoC evidence 與專案狀態留在私人 `Endwar116/KS-goverment`。
本 repo 只保留 public-safe 技術、架構、設計演進與 handoff。

## Start Here｜目前讀取順序

1. [`CURRENT_TECHNOLOGY_MAP.md`](CURRENT_TECHNOLOGY_MAP.md) — 目前整套技術的單一地圖。
2. [`design/dual_recall_architecture_candidate_2026-08-31.md`](design/dual_recall_architecture_candidate_2026-08-31.md) — 最新雙路召回架構候選。
3. [`shared/RAW_RECALL_POWER_META_PROMPT.md`](shared/RAW_RECALL_POWER_META_PROMPT.md) — 所有具一般網路搜尋能力模型都能執行的 Raw Recall 層。
4. [`shared/raw_recall_keyword_pack_kcg_v0.1.yaml`](shared/raw_recall_keyword_pack_kcg_v0.1.yaml) — 13 組 Primary Keywords、Alias、關聯字與 Project Watchlist 的跨模型受控字典。
5. [`architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`](architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html) — Input／Process／Output、系統架構、關鍵字、TW100 與 Output Demo。
6. [`HANDOFF_CURRENT.md`](HANDOFF_CURRENT.md) — 下一棒工程與驗證狀態。
7. [`DESIGN_HISTORY/2026-08-31_ZERO_GAP_RECONCILIATION.md`](DESIGN_HISTORY/2026-08-31_ZERO_GAP_RECONCILIATION.md) — 零斷層整理紀錄。

## Current Retrieval Direction｜Dual Recall

2026-08-31 的實測顯示，單一正式搜尋程序與單純日期＋關鍵字搜尋各有盲點。

目前設計方向改為兩條召回路徑互補：

```text
RAW RECALL LANE ─┐
                 ├─> MERGED CANDIDATE POOL -> G2 -> G3 -> G4 -> G5 -> G6 -> G7 -> G8
FORMAL SKILL LANE┘
```

### Raw Recall Lane

責任：不要漏掉。

- 每個 Primary Keyword 至少直接搜尋一次。
- 使用受控相關詞。
- 跑少量當日 broad search。
- 只做最小去重、日期與壞頁清理。
- 不做最終業務相關性判斷。
- 必須保持跨模型、跨搜尋環境可執行。

### Formal Skill Lane

責任：不要亂給。

- Governed retrieval。
- TW100 active-source planning。
- broad / high-yield / precision / semantic recall。
- G2–G8 正式來源、事實、相關性、去重、摘要、交付與人工審核。

兩條路徑的候選在 **G2 前合併**。

目前這仍是 `DESIGN_CANDIDATE__NOT_RUNTIME_VALIDATED`。

## Shared Cross-Model Layer

長期技術方向不是把 Skill 綁死在 ChatGPT 或 Claude。

Shared layer 目前先包含：

- Raw Recall Power Meta Prompt。
- Raw Recall keyword pack。
- `RAW_RECALL_PACKET` semantic schema。
- Candidate merge contract。
- Formal Gate semantics。
- Cross-model regression concept。

不同平台再各自做 adapter。

目標：

**Stable shared core + replaceable model adapters + replaceable business profiles.**

## Platform Lanes

### Claude

`claude/daily-media-brief/v0.6.0-rc1/`

目前 finalization target。
真實 fresh Claude runtime E2E 尚未確認通過。

### ChatGPT

`chatgpt/daily-media-brief/v0.6.0-rc1/`

目前第一個適合驗證 Dual Recall 的 reference candidate。

兩個平台目錄彼此獨立。
不要讓其中一邊 runtime 直接引用另一邊的檔案。

## Current Design Candidates

- [`design/dual_recall_architecture_candidate_2026-08-31.md`](design/dual_recall_architecture_candidate_2026-08-31.md) — Raw + Formal 雙路召回與 merge contract。
- [`design/recall_first_search_patch_candidate_2026-08-31.yaml`](design/recall_first_search_patch_candidate_2026-08-31.yaml) — 正式 Lane 的 Recall-first 修正候選。
- [`design/poc_search_profile_candidate_2026-08-31.yaml`](design/poc_search_profile_candidate_2026-08-31.yaml) — 13 組承辦 Primary Keywords、Alias、Semantic Expansion、Project Watchlist、負向條件候選。
- [`design/output_visual_contract_candidate_2026-08-31.md`](design/output_visual_contract_candidate_2026-08-31.md) — 視覺化 Daily Media Brief Output Layer 候選。

Design candidate 不等於 runtime 已 coding 或 E2E 已通過。

## Current Formal Core

目前 v0.6.0-rc1 仍保留：

- G0–G8。
- G1：日期＋最後交付目標則數。
- Search Planner。
- G2：來源與證據。
- G3：具體事實與負向條件。
- G4：合標準／候選新聞／排除。
- G5：事件與跨日去重。
- G6：原始標題＋50～100 字摘要＋完整 URL。
- G7：拿 G1 目標做數量與交付完整度驗收。
- 今日總摘要：250 字以內。
- G8：人工確認。
- `approved != confirmed published`。
- TW100：100-source coverage registry，不是排名。

## Validation Status

已確認：

- Direct Keyword baseline 找到 Formal run 漏掉的當日高雄／研考／一卡通相關結果。
- Recall-first Formal run 能在同日取得 10 則。
- Raw Recall shared contract 已建立。
- Dual Recall architecture candidate 已建立。

尚不可宣稱：

- Dual Recall merged runtime PASS。
- 正式 A/B/C/D regression 已完成。
- ChatGPT rc2 已封版。
- Internal PoC 1 PASS。
- Internal PoC 2 PASS。
- fresh Claude E2E PASS。
- External PoC 已正式放行。
- production-ready。

## Next Validation

以 2026-08-31 作固定回歸日，比較：

1. Original Formal Skill。
2. Recall-first Formal Skill。
3. Direct Keyword Raw baseline。
4. Dual Recall merged candidate。

至少量測：

- Primary Keyword coverage。
- unique same-day events。
- expected-hit recall。
- 高雄 local recall。
- Raw-only useful hits。
- Formal-only useful hits。
- exclusion/noise ratio。
- 最終 10 則實用度。

## Repository Boundary

技術成品、平台 adapter、public-safe 架構、shared contract、design candidate 與 handoff 放這裡。

專案現場資料、需求訪談、人物討論、內部決策、治理紀錄、測試原始證據與 conversation trace 留在私人專案 repo。

詳見 [`REPO_BOUNDARY.md`](REPO_BOUNDARY.md)。
