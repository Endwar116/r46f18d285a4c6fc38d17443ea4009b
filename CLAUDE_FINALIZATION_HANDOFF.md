# Claude Finalization Handoff｜給德德

## 你會拿到兩個 repo

1. `Endwar116/KS-goverment`。
   這是內部專案 repo，用來查需求來源、測試證據、工程歷史與顧問決策。
2. `Endwar116/r46f18d285a4c6fc38d17443ea4009b`。
   這是 callable technology repo，只放模型要載入的技術與公開安全的 handoff。

請維持這個邊界。
不要把內部訪談、人名、治理 log 或原始測試紀錄搬進 callable repo。

## 你的主要任務

請以 `claude/daily-media-brief/v0.6.0-rc1/` 作為 Claude finalization target。

`chatgpt/daily-media-brief/v0.6.0-rc1/` 是 portability comparator。
它可以幫你檢查共同核心有沒有遺漏，但不應反過來主導 Claude 的平台行為。

## 老翔這輪做了什麼

Claude runtime 已由舊 33 個 runtime-visible fragment 收斂成 compact contracts。
核心權威現在集中為：

- `SKILL.md`。
- `runtime.yaml`。
- `topic_profile.yaml`。
- `decision_policy.yaml`。
- `workflow.md`。
- `output_contract.md`。
- `state/handover.md`。
- `state/published_history.jsonl`。

舊版重複的 relevance score 已合併。
Q0–Q8 保留為唯一 gate 命名。
F-3 標題日期陷阱、E1–E6 digest expansion、T1→T2→T3、event-level dedup、人審 Q8 都保留。

## 請你最後檢查

- Claude 真實 runtime 是否能穩定載入 compact contracts。
- query budget 是否在 tool-dispatch 前就會被計數與截斷。
- 每一批搜尋結果是否先寫 candidate / excluded ledger，再進下一批。
- 日期驗證是否仍以原文 publication evidence 為權威。
- digest container 是否會先展開，再讓條目各自走 Q1–Q6。
- T1 不足時擴 T2/T3 是否只擴時間，不會降低 Q3/Q4。
- human review 前是否永遠停在 WAIT。
- 承辦可見輸出是否維持白話，不外洩內部代號。

## 完成條件

請不要只因靜態檔案合理就宣告完成。
至少要有：

- compact contract static validation。
- existing regression corpus。
- 真實 Claude 新對話 E2E。
- 搜尋 budget crossing case。
- candidate / excluded ledger coverage case。
- human review stop case。

通過後再決定是否由 rc 升版。
