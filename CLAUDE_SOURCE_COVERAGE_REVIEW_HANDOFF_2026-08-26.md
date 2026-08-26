# Claude Daily Media Brief｜Source Coverage Review Handoff

日期：2026-08-26
Target：`claude/daily-media-brief/v0.6.0-rc1/`
狀態：REVIEW CANDIDATE / NOT PRODUCTION READY
Reviewer：德德 / VS德

## 這次為什麼改

目前技術的 precision 控制很完整，但可能出現 recall 過低。

盤點後確認有三個主要瓶頸。

1. Q2 曾把 PTT／Dcard／Mobile01 等來源直接視為 excluded source，導致早期訊號在 discovery 階段就消失。
2. Q4 的 relevance score 原本只有 `>=5` 才 KEEP，而同業城市比較案例、具政府部署影響的重大 AI 技術通常只有 3 分，長期停在 REVIEW。
3. Q7 原本 T1 數量不足後主要靠 T2／T3 擴時間，沒有先系統化擴大同日來源覆蓋。

## 本次 candidate 改動

### A. TW100 Taiwan Source Coverage Registry

新增：
`source_registry_taiwan.yaml`

內容為 100-source coverage registry。
它不是流量排名或可信度排行榜。

來源分成：
- 官方／研究一手來源。
- 科技、資安與研究專業來源。
- 主流新聞與編輯媒體。
- 產業、商業、公民媒體與同業城市。
- 聚合器。
- 論壇／社群 signal lane。

執行時不能 100 站逐站硬查。
應依 topic tags、source class、source rotation 建 active source set。

### B. Q2：Source Role / Admissibility

Q2 現在先判斷來源角色：
- final evidence。
- discovery aggregator。
- signal-only。

PTT、Dcard、Mobile01、Threads 等不再因來源名稱於 discovery 階段直接排除。

若論壇／社群只是早期訊號，先標 `SIGNAL_CANDIDATE`。
進一般待審稿前，需要換成或補上可驗證來源。

涉及資安漏洞、個資外洩、犯罪指控、政府事故等高風險主張，不得只靠論壇／社群定案。

### C. Q4：CORE / EXTENDED

`score >= 5` → `CORE｜核心輿情`。

`score 3–4` 且 Q1／Q2／Q3／S3 actionability 通過 → `EXTENDED｜延伸觀測`。

`score <= 2` → `EXCLUDE`。

EXTENDED 可以進承辦待審清單，但必須明確標示「延伸觀測」。
泛 AI、純評論、純業配、投資、消費產品仍不可因缺量升級。

### D. Q7：Source Expansion Before Time Expansion

若 T1 的 CORE＋EXTENDED 低於 target_min：

1. 先擴大 TW100 同日來源覆蓋。
2. 補未覆蓋的主流／產業／地方／同業城市來源帶。
3. 必要時啟動 signal lane，再回頭找可驗證來源。
4. 同日仍不足才進 T2。
5. T2 仍不足才進 T3。

任何階段都不能把 EXCLUDE 升級。
Q1 日期、Q3 事實性、Q5 去重、Q6 摘要忠實度不放寬。

## 請德德優先測這些案例

1. **Peer-city comparator**
   - 具體其他城市 AI／智慧城市部署。
   - relevance score = 3。
   - 應成為 EXTENDED，而不是永久卡在 REVIEW。

2. **Forum early signal**
   - PTT／Dcard／Mobile01 出現大量一致的服務異常回報。
   - discovery 階段不可因 domain 自動刪除。
   - 應先成 SIGNAL_CANDIDATE，再找正式媒體／官方／其他可驗證證據。

3. **High-risk forum claim**
   - 論壇聲稱政府機關資料外洩。
   - 沒有可驗證來源時，不得進一般 LINE 草稿。

4. **Generic AI noise**
   - 只有 AI buzzword，沒有公部門 actionability。
   - 即使來源是高品質媒體，也應 Q4 FAIL / EXCLUDE。

5. **Same-day volume recovery**
   - 初輪只有 7–9 則 CORE。
   - 系統應先使用 EXTENDED 與 TW100 source expansion 補今日內容。
   - 不應立刻跳到 48／72 小時舊聞。

6. **No padding**
   - 所有來源擴張與 T1–T3 跑完仍不足 12 則。
   - 應誠實輸出實際數量與 Q7 DEGRADED。
   - 不得把 EXCLUDE 塞進來。

7. **Source registry contract**
   - 執行 `python tools/validate_source_coverage.py`。
   - 預期：100 sources、TW001–TW100、Claude/GPT registries identical、Q2/Q4/Q7 linkage PASS。

## 驗收建議

不要只看最終則數。
至少記錄：
- CORE count。
- EXTENDED count。
- source expansion incremental。
- signal candidates。
- T1/T2/T3 incremental yield。
- false positive rate。
- 人工刪除率。
- 誤殺回查案例。

目標是提升 recall，同時讓 precision 的硬底線留在 Q1／Q3／Q5／Q6 與高風險 source corroboration。

## 尚未證明

本次只是 contract-level candidate correction。
尚未完成真實 Claude fresh-conversation E2E。

請德德完成 E2E 與 regression 後，再決定是否調整 threshold、source classes、signal corroboration 或升版。
