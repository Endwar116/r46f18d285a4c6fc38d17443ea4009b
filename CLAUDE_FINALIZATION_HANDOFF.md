# Claude Finalization Handoff｜Current Entry for 德德

Updated: 2026-08-31
Status: `HANDOFF_READY_WITH_OPEN_ITEMS`

## 0. 先不要直接改 runtime

先讀：

1. `README.md`
2. `CURRENT_TECHNOLOGY_MAP.md`
3. `architecture/CURRENT_DAILY_MEDIA_BRIEF_OVERVIEW.html`
4. `HANDOFF_CURRENT.md`
5. `DESIGN_HISTORY/2026-08-31_ZERO_GAP_RECONCILIATION.md`
6. 再進 `claude/daily-media-brief/v0.6.0-rc1/`

原因：2026-08-27～31 的 Overview／搜尋參數／Output Visual Layer 已經比原本 compact runtime design 多了一輪人工校正。

這些最新設計已被整理成 design candidate，但尚未假裝完成 runtime merge。

## 1. 兩個 Repo 邊界

### Internal

`Endwar116/KS-goverment`

用途：需求來源、人物回饋、Conversation Trace、Calibration Matrix、Internal PoC Plan、完整工程／治理紀錄、PoC evidence。

### Public Callable

`Endwar116/r46f18d285a4c6fc38d17443ea4009b`

用途：public-safe callable technology、architecture、design candidates、handoff。

不要把 internal 人物／逐字／raw evidence 搬到 public repo。

## 2. Finalization Target

Claude：

`claude/daily-media-brief/v0.6.0-rc1/`

ChatGPT：

`chatgpt/daily-media-brief/v0.6.0-rc1/`

ChatGPT 是 portability comparator。

兩 lane 不得 runtime cross-import。

## 3. Existing Callable Core｜Repo Readback 已確認

目前 Claude compact candidate 已有：

- G0–G8 user-facing mapping。
- G1 日期＋目標則數。
- 搜尋／Semantic Expansion stage。
- TW100 source registry。
- G2 來源與證據。
- G3 具體事實／負向條件。
- G4 業務相關性。
- G5 去重。
- G6 原標題＋50～100 字摘要＋完整 URL。
- G7 使用 G1 target 做數量／完整度驗收。
- 250 字內今日總摘要。
- G8 人工確認。
- publish boundary：approved 不自動等於 confirmed published。

因此不要重新發明另一套 core。

## 4. 2026-08-31 最新設計差異｜需要先校正再 merge

### A. Search Profile Candidate

`design/poc_search_profile_candidate_2026-08-31.yaml`

狀態：

`DESIGN_CANDIDATE__NOT_RUNTIME_VALIDATED`

它整理了最新承辦提供的 13 組 Primary Keywords：

- 高雄市。
- 高雄市政府研究發展考核委員會。
- 高雄市政府資訊處。
- 智慧城市。
- 物聯網。
- 大數據資訊。
- 資安。
- AI。
- 數位發展部。
- 市民卡。
- 一卡通。
- MyData。
- 智慧杆。

另外包含 Alias／Normalization、Semantic Expansion、Project Watchlist、Negative Conditions candidates。

現有 platform `topic_profile.yaml` 是較早 compact set。

請不要直接假裝兩者已同步。

正確順序：

1. 用 Current Overview 完成業務校正。
2. approved candidate merge 到 Claude topic_profile。
3. 同步 ChatGPT lane 或清楚保留 platform-specific difference。
4. 做 diff／parse／contract validation。
5. 再進 Internal PoC。

### B. Search Planner 顯性化

位置：

`G1 → Search Planner → G2`

Search Planner 不是 Gate。

它負責：

- Primary Keywords。
- Alias／Normalization。
- Semantic Expansion。
- Project Watchlist。
- Query Plan。
- TW100 active source set。

搜尋不得只靠 literal keyword。

### C. Visual Output Candidate

`design/output_visual_contract_candidate_2026-08-31.md`

狀態：

`DESIGN_CANDIDATE__NOT_RUNTIME_VALIDATED`

它是 Presentation Layer，不取代現有文字最低 output contract。

Latest human-facing sequence：

- 今日重點。
- 合標準新聞。
- 候選新聞。
- 待查證與次要資訊。
- 今日總摘要。

O01 HOW TO READ 是說明。

O02 DEMO OUTPUT 起只放真正使用者看到的成品，不混 G4/G8/runtime/source role 等內部語言。

使用者狀態顯示：

`待人工確認`

如果視覺方案被確認，才把 fields 映射進 runtime output schema／renderer。

## 5. G1｜日期與目標則數

搜尋前固定：

- 日期／時間範圍。
- `target_total_count`。

目標則數由承辦或 explicit profile default 決定。

缺值時要有明確行為，不得 model 偷塞固定數字。

## 6. G7｜數量與交付完整度

G7 不重新決定 target。

它拿 G1 target 檢查：

- 合標準數量。
- 候選新聞數量。
- actual total。
- 每則原標題。
- 每則 50～100 字摘要。
- 每則完整 URL。
- 今日總摘要 <= 250 字。

不足順序：

1. 擴大 same-day source coverage。
2. 補未覆蓋 source lanes。
3. 必要時使用 signal 發現事件再回找可驗證來源。
4. 同日仍不足才進 48h／72h（若 calibration 允許）。
5. 還不足就 honest DEGRADED，不硬湊。

## 7. TW100

`source_registry_taiwan.yaml`

Registry：`TW100-COVERAGE-2026-08`

是 coverage registry，不是排名。

不要 100 站 sequential crawl。

依 topic/profile/source tags 選 active source set。

論壇／社群可作 signal，但高風險事實不能只靠 signal final。

Current Overview 已將 TW001–TW100 全部展開供人討論。

## 8. G8 / Publication Boundary

輸出後停人工 review。

承辦可以刪除、替換、補找、追問。

`approved != confirmed published`

若沒有真正 publish event／人工回寫，不得把 selected 當 published。

## 9. News Lifecycle Roadmap

預期：

`discovered_news → selected_news → published_news`

完整 store 尚未完成。

現有 published-history mechanism 不能宣稱等價完整 lifecycle。

## 10. Internal PoC Gate

Internal repo：

`20_COLLABORATOR_協作者/Solutions_解決方案/Daily-Media-Brief_輿情情報蒐集/INTERNAL_POC_PLAN_v0.1_2026-08-27.md`

### PoC 1｜Fresh Run

驗證 Input → G0 → G1 → Search Planner → G2–G7 → structured output → G8 human wait。

### PoC 2｜Stateful Rerun

驗證 duplicate/new-update、history、人工 feedback、selected/published 邊界。

兩場都要留 evidence。

## 11. Finalization Checks

至少確認：

- Claude 真的載入所有 authority files。
- G1 缺 target 時行為正確。
- Search Planner 真的能用 approved keyword + Semantic Expansion。
- TW100 active source planning 不變成 100-site brute force。
- query budget 在 dispatch 前 guard。
- candidate/excluded ledger 有 coverage。
- 日期以原文 publication evidence 為權威。
- 合標準／候選不混入 EXCLUDE。
- 摘要與 URL contract 成立。
- G7 target 不被偷改。
- G8 human stop 成立。
- selected / published 不混淆。

## 12. Completion Rule

沒有真實 evidence 不要寫完成。

至少需要：

- static/contract validation。
- existing regression corpus。
- approved search-profile merge evidence。
- Internal PoC 1 evidence。
- Internal PoC 2 evidence。
- fresh Claude E2E。
- query-budget crossing case。
- candidate/excluded ledger case。
- G8 human-review stop case。

在此之前：

`production_ready = false`

`external_poc_ready = false`，除非 internal evidence 完成且 internal repo 有明確 external-PoC approval evidence。
