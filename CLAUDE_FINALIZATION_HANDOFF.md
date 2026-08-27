# Claude Finalization Handoff｜給德德

## 你會拿到兩個 repo

1. `Endwar116/KS-goverment`。
   內部專案 repo，用來查需求來源、PoC 計畫、測試證據、工程歷史與顧問決策。
2. `Endwar116/r46f18d285a4c6fc38d17443ea4009b`。
   Callable technology repo，只放模型要載入的技術與 public-safe handoff。

請維持這個邊界。

## 主要任務

以 `claude/daily-media-brief/v0.6.0-rc1/` 為 Claude finalization target。

`chatgpt/daily-media-brief/v0.6.0-rc1/` 只作 portability comparator。

## 2026-08-27 最新 PoC 裁定

Irene＋安安確認：

### G1｜日期與目標則數

搜尋前必須先固定：

- 日期／時間範圍。
- `target_total_count`。

目標新聞則數由承辦決定。
外部 PoC 若沒有 profile 預設值，詢問一次「今天希望最後看到幾則新聞？」。
模型不得自行默認固定 12／15／20 則。

### G7｜數量與交付完整度

G7 不重新決定目標。

它拿 G1 已鎖定的 target_total_count 檢查：

- 合標準數量。
- 候選新聞數量。
- 每則原標題。
- 每則 50～100 字摘要。
- 每則完整 URL。
- 今日總摘要 <= 250 字。

不足可 DEGRADED，不得為湊數降低 G2／G3／G5／G6。

### 使用者可見 Gate

PoC 對外統一顯示 G0–G8。

既有 regression／legacy contract 仍可能使用 Q0–Q8。
`poc_calibration.yaml` 有 mapping，請在沒有 regression evidence 前不要暴力刪除舊 Q alias。

### 分類顯示

- CORE → `合標準`。
- EXTENDED → `候選新聞`。
- EXCLUDE → 不進一般交付。

### 關聯搜尋

搜尋端必須先做 semantic expansion／reverse recall。
G4 只能判斷已被召回的文章，不能補救根本沒找到的新聞。

請確認：

`keywords → synonyms/pro terms → project concepts/event types/entities → query → article → G4`

## 新增／更新 callable files

- `poc_calibration.yaml`。
- `runtime.yaml`。
- `workflow.md`。
- `output_contract.md`。
- `SKILL.md`。
- `VERSION.yaml`。
- 最新 Solution Architecture Overview。

## Internal PoC Gate

8/28 前要先完成兩場 internal PoC。

詳見 KS-goverment：

`20_COLLABORATOR_協作者/Solutions_解決方案/Daily-Media-Brief_輿情情報蒐集/INTERNAL_POC_PLAN_v0.1_2026-08-27.md`

### PoC 1｜Fresh Run

確認 G1 → 搜尋 → G2–G7 → 結構化輸出 → G8 WAIT 的完整行為。

### PoC 2｜Stateful Rerun

確認重複新聞、人工操作與 discovered／selected／published 語義。
完整 News Lifecycle Store 尚未完成時，要明確標示人工／模擬 state，不能假裝自動持久化。

兩場 evidence 完成後，由 Irene 明確決定是否進 external PoC。

## 請你最後檢查

- Claude 真實 runtime 是否能載入新增 `poc_calibration.yaml`。
- G1 缺 target_total_count 時是否正確詢問一次。
- target_total_count 是否在後續全程保持，不被 G7 偷改。
- Semantic Expansion 是否真的增加非字面關鍵字召回。
- query budget 是否在 tool-dispatch 前被計數／截斷。
- 每一批搜尋是否先建立 candidate／excluded ledger。
- 日期驗證是否仍以原文 publication evidence 為權威。
- 合標準／候選新聞是否不混入 EXCLUDE。
- 每則是否確實 50～100 字摘要＋完整連結。
- 今日總摘要是否 <= 250 字且沒有模型補值。
- human review 前是否永遠停在 G8 WAIT。

## 完成條件

不要只因靜態檔案合理就宣告完成。

至少要有：

- compact contract static validation。
- existing regression corpus。
- Internal PoC 1 evidence。
- Internal PoC 2 evidence。
- 真實 Claude 新對話 E2E。
- 搜尋 budget crossing case。
- candidate / excluded ledger coverage case。
- G8 human review stop case。

通過後再決定是否由 rc 升版。
