# Daily Media Brief · PoC Workflow

版本：v0.6.0-rc1  
候選修訂：poc-calibration-g1-g7-output-2026-08-27

本檔是唯一流程權威。
承辦可見流程統一使用 `G0–G8`。
既有 regression 若仍使用 `Q0–Q8`，依 `poc_calibration.yaml > legacy_gate_mapping` 對照，不在承辦畫面顯示 Q。

執行順序：`G0 準備 → G1 日期與目標則數 → 搜尋與關聯擴展 → G2–G6 判斷 → G7 數量與交付完整度 → G8 人工確認`。

## G0｜執行準備

取得 Asia/Taipei 當下時間並建立 run_id。
載入 `runtime.yaml`、`poc_calibration.yaml`、`topic_profile.yaml`、`source_registry_taiwan.yaml`、`decision_policy.yaml`、`output_contract.md`、handover 與 published history。

## G1｜日期與目標則數

搜尋開始前先固定本次執行範圍。

至少包含：

- 日期模式：今日／48 小時／72 小時／自訂。
- 目標新聞總則數：由承辦決定。
- 若承辦有指定「只看資安／只看 AI」等條件，形成本次 runtime override。

外部 PoC 時，如果 `target_total_count` 尚未設定，先詢問一次「今天希望最後看到幾則新聞？」。
不要由模型自行套用固定 12、15 或 20 則。

預設日期模式為今日。
若今日來源完整搜尋後仍不足目標，可依 runtime 的 T2／T3 階梯補搜。
每一則候選仍需個別確認原文 publication time。

## Stage A｜搜尋計畫與關聯搜尋

依 active brief profile、topic profile、TW100 與歷史狀態建立 query plan。

搜尋不能只靠字面關鍵字。
至少同時使用：

1. 主要關鍵字。
2. 同義詞與專業術語。
3. 專案／政策／技術概念。
4. 關聯實體與事件類型。
5. Reverse Recall：標題沒有關鍵字，但正文主旨仍可能與任務高度相關。

例如「資安」主題除了搜尋資安，也要依 profile 納入 CVE、勒索軟體、供應鏈攻擊、RCE、資料外洩、零信任、弱掃等概念。

語意延伸只負責提高召回率。
是否真正值得資訊處看到，仍由 G4 判斷。

每次送出搜尋 batch 前，先依 query budget guard 計算剩餘額度。
每個 batch 回傳後先建立 candidate / excluded ledger，再允許下一批。

## Stage B｜蒐集與原文驗證

每條 query 獨立搜尋。
搜尋摘要只能用來發現候選。
可能入選的新聞必須開原文確認發布時間、來源與可核實內容。

聚合器只負責 discovery。
論壇／社群可以保留成 SIGNAL_CANDIDATE，但高風險主張進一般清單前必須換成或補上可驗證來源。

彙整型來源先展開成個別事件，再逐則進後續流程。

## G2｜來源與證據

判斷來源角色：final evidence／discovery／signal-only。
來源不在 TW100 不等於自動排除，但必須能說明證據用途。

## G3｜具體事實

保留有新事件、公告、政策、研究、漏洞、部署、數據或可信群體訊號的內容。
純評論、純行銷、純投資、純消費內容依負向條件處理。

## G4｜業務相關性

先判斷文章真正主旨，再問它對目前 brief profile 的業務是否有「知道、比較、留意、調整、追蹤」價值。

承辦可見分類：

- `合標準`：internal alias `CORE`。
- `候選新聞`：internal alias `EXTENDED`。
- `排除`：internal alias `EXCLUDE`。

標題沒有關鍵字仍可列入合標準或候選新聞。
只要正文主旨與 profile 的業務責任／專案／風險／比較案例實質相關即可。

## G5｜重複判斷

先做本批同事件去重，再與歷史比對。
比對 URL、標題正規化、event_key 與新增事實。
同事件多來源只留最適合的一則。

## G6｜摘要忠實度

每則保留原始新聞標題。
摘要以繁體中文 50–100 字為目標。
摘要只寫原文可支持的事實，不補模型猜測。
每則必須保留完整原文 URL。

## G7｜數量與交付完整度

G7 不重新決定目標則數。
它只拿 G1 已設定的 `target_total_count` 做完成度檢查。

若目前合標準＋候選新聞不足：

1. 先擴大同日 TW100 來源覆蓋。
2. 補未覆蓋的主流／產業／地方／同業城市來源。
3. 必要時啟動 signal lane，再回頭找可驗證來源。
4. 同日仍不足才依 T2、T3 補搜。
5. 到上限仍不足就標 DEGRADED，顯示實際則數，不硬湊。

進入待審輸出前，每一則都必須有：

- 新聞標題。
- 50–100 字摘要。
- 完整原文連結。

最終輸出固定分成：

1. `合標準（X 則）`。
2. `候選新聞（X 則）`。
3. `今日總摘要`，250 字以內。

今日總摘要只總整本批新聞共同趨勢，不新增來源不存在的事實。

## G8｜人工確認

系統輸出待審稿後固定停在 `AWAITING_HUMAN_REVIEW`。

承辦可說：

- 刪除 3、7。
- 第 5 則換掉。
- 資安再找兩則。
- 只留合標準。
- 候選新聞少一點。
- 為什麼這則被列為候選。
- 通過／定版／可以了。

只有使用者明確通過後，G8 才 PASS。
之後才允許形成 history 更新。

## Failure behavior

搜尋部分失敗只重試受影響 query 一次。
日期無法驗證的新聞排除。
證據來源不足的高風險新聞不進一般清單。
目標則數不足不等於可以降低 G2、G3、G5、G6。
工具不可用時停止受影響階段並列出未完成事項，不宣告完成。
