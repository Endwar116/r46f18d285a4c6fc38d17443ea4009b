# KCG IT Daily Media Brief · Callable Technology Repository

這個 repository 保存可被模型載入、呼叫、比較、審查與延伸的 Daily Media Brief 輿情技術。

內部專案紀錄、人物／訪談內容、顧問討論、完整 PoC evidence 與專案狀態留在私人 `Endwar116/KS-goverment`。
本 repo 只保留 public-safe 技術、架構、設計演進與 handoff。

## Start Here｜目前讀取順序

1. [`CURRENT_TECHNOLOGY_MAP.md`](CURRENT_TECHNOLOGY_MAP.md) — 目前整套技術的單一地圖。
2. [`architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`](architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html) — 最新 Input／Process／Output、系統架構、關鍵字、TW100 與 Output Demo。
3. [`HANDOFF_CURRENT.md`](HANDOFF_CURRENT.md) — 下一棒工程與驗證狀態。
4. [`DESIGN_HISTORY/2026-08-31_ZERO_GAP_RECONCILIATION.md`](DESIGN_HISTORY/2026-08-31_ZERO_GAP_RECONCILIATION.md) — 本輪零斷層整理紀錄。

## Platform Lanes

### Claude

`claude/daily-media-brief/v0.6.0-rc1/`

目前 finalization target。
真實 fresh Claude runtime E2E 尚未確認通過。

### ChatGPT

`chatgpt/daily-media-brief/v0.6.0-rc1/`

目前 portability comparator。
保留 ChatGPT 專用操作／語言層。

兩個平台目錄彼此獨立。
不要讓其中一邊 runtime 直接引用另一邊的檔案。

## Current Design Candidates

以下是最新設計／校正狀態，但尚未默默取代 callable runtime authority：

- [`design/poc_search_profile_candidate_2026-08-31.yaml`](design/poc_search_profile_candidate_2026-08-31.yaml) — 13 組承辦 Primary Keywords、Alias、Semantic Expansion、Project Watchlist、負向條件候選。
- [`design/output_visual_contract_candidate_2026-08-31.md`](design/output_visual_contract_candidate_2026-08-31.md) — 視覺化 Daily Media Brief Output Layer 候選。

這個區隔是刻意的。
Overview／設計確認不等於 runtime 已 coding 或 E2E 已通過。

## Current Core

目前 v0.6.0-rc1 已包含的核心方向：

- 使用者可見 G0–G8。
- G1：日期＋目標新聞則數。
- Search Planner：關鍵字＋Semantic Expansion＋TW100 active source planning。
- G2：來源與證據。
- G3：具體事實與負向條件。
- G4：合標準／候選新聞／排除。
- G5：事件與跨日去重。
- G6：原始標題＋50～100 字摘要＋完整 URL。
- G7：拿 G1 目標做數量與交付完整度驗收；不足不硬湊。
- 今日總摘要：250 字以內。
- G8：人工確認。
- 發布邊界：人工通過不自動等於實際已發布。
- TW100：100-source coverage registry，不是排名。

## Status

目前仍屬 review / design candidate 階段。

`production_ready = false`

尚不可宣稱：

- Internal PoC 1 PASS。
- Internal PoC 2 PASS。
- fresh Claude E2E PASS。
- 完整 News Lifecycle Store 已完成。
- External PoC 已獲正式放行。

## Repository Boundary

技術成品、平台 adapter、public-safe 架構、design candidate 與 handoff 放這裡。

專案現場資料、需求訪談、人物討論、內部決策、治理紀錄、測試原始證據與 conversation trace 留在私人專案 repo。

詳見 [`REPO_BOUNDARY.md`](REPO_BOUNDARY.md)。
