# ⚠️ 此版本已停用｜DEPRECATED

**這個目錄不是現行版本，請勿載入。**

## 現行版本

```
claude/daily-media-brief/v0.6.0-rc1/
```

依 `CURRENT_TECHNOLOGY_MAP.md`：`Callable candidate: v0.6.0-rc1`。

## 為什麼 rc2 的版號比 rc1 大，卻不是現行版本

rc2 不是 rc1 的後續版本，兩者是**不同分支**。

rc1 才是納入 PoC 校正後的完整版本，內容比 rc2 多：

| 項目 | rc1（現行） | rc2（已停用） |
|---|---|---|
| 檔案數 | 11 | 8 |
| 對外閘門名稱 | **G0–G8** | Q0–Q8 |
| 目標則數 | G1 於搜尋前先確定 | 直接套 target_min／max |
| TW100 來源池 | 有（`source_registry_taiwan.yaml`） | 無 |
| PoC 校正面 | 有（`poc_calibration.yaml`） | 無 |
| 輕量來源索引 | 有（`source_lane_index.yaml`） | 無 |
| 合標準／候選新聞分層 | 有 | 無 |

rc2 內部規則（日期驗證、去重、彙整容器展開）與 rc1 邏輯相通，
差別在 rc1 把對外語彙改為 G0–G8，並補上 PoC 校正、來源池與數量決策層。

`poc_calibration.yaml > legacy_gate_mapping` 保有 Q→G 對照，供 regression 追溯。

## 保留原因

保留本目錄僅供版本演進追溯與 regression 比對。

**不得**：

- 在新對話中載入本目錄執行；
- 從本目錄複製 runtime 檔案到 rc1；
- 以本目錄內容作為現行行為依據。

## 歷史價值

rc2 期間的兩次實測（2026-08-25）確認了「未帶時間錨點時 T1 命中為 0」，
此發現已納入 rc1 的 `topic_profile.yaml > recency_anchoring` 與
`runtime.yaml > yield_telemetry.observed_runs`。

---

Marked deprecated: 2026-08-31
