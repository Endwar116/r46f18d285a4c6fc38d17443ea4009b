# Daily Media Brief · Compact Workflow

版本：v0.6.0-rc2

本檔是唯一流程權威。
執行順序固定為：`Orchestrate → Budget Settlement → Collect → Filter → Dedup → Summarize → Verify → Draft → Human Review`。

## Stage 0 · Orchestrate

取得 Asia/Taipei 當下時間並建立 `KCG-BRIEF-YYYYMMDD-HHMM`。
載入 `runtime.yaml`、`topic_profile.yaml`、`decision_policy.yaml`、`output_contract.md`、handover 與 published history。
依 `runtime.yaml` 建立 T1 時間窗，週一套用 Monday rule。

建立 query plan 時，P0 一定跑、P1 正常跑。
P2 與 P3 只有在前段結果不足、分類空白或有直接可比較案例時才啟用。
同一主題的查詢可去重，但不得把不同主題塞成超長 query。

使用者本次說「今天只要資安」之類條件，只形成 runtime override。
只有使用者明確說「以後都這樣」才改永久 contract。

輸出 run manifest 與 query plan，狀態進入 `QUERY_PLANNED`。

## Stage 0b · Budget Settlement

這一階段必須在任何搜尋 dispatch **之前**完成。

1. 數出 query plan 中各優先層的實際條數。
2. 逐層比對 `topic_profile.yaml > query_planner.budget`。
3. 超支的優先層必須**先截斷再執行**，不是跑到一半才停。
4. 截斷依據依序為：直接專案命中優先、今日有新事實可能性優先、與已有 history 重疊度低者優先。
5. 輸出 `query_budget_settlement`，記錄各層規劃數、上限、實際執行數與被截斷的 query。

狀態進入 `BUDGET_SETTLED` 才可進 Stage 1。

未經結算就開始搜尋是 `never_do` 項目。
理由：budget 的目的是保證每一層都跑得完。跑到一半才發現超支，被牺牲的會是排在後面的 P1，而不是優先序最低的那幾條。

## Stage 1 · Collect

### 時間錨點（必要）

每條 query 都必須帶時間錨點。
搜尋引擎預設依權威度而非新鮮度排序，不帶錨點會回傳高排名的舊文，而不是今日新聞。
做法：在 query 尾端加上當日日期、「今天」「本週」等錨點，或使用搜尋工具的時間篩選參數。

錨點只影響召回，不影響判定。
回傳結果的發布時間仍一律依 `decision_policy.yaml > date_verification` 以原文為準。

### 批次紀律（必要）

搜尋以批次進行，一批建議 3–5 條 query。

**本批的 candidate ledger 與 excluded ledger 寫完，才能進下一批。**

ledger 不是最後一次補齊的文件，是每批的檢查點。
理由：長跑時前段候選若只活在上下文裡，一旦上下文壓縮就會靈點消失，而且沒有任何機制會發現它掉了。

每批寫入後回報累計：已執行 query 數、累計候選數、累計排除數。

### 搜尋與原文

每條 query 獨立搜尋，保存 query、priority、category、title、URL、search snippet、source hint 與可見時間。
搜尋摘要只負責召回候選，不能當最後事實來源。

可能入選、日期不明、標題不足以判斷、需要挑一手來源或需要寫摘要時，必須開原文。
發布時間依 `decision_policy.yaml > date_verification` 驗證。
無法確認 publication time 的候選標 `DATE_UNVERIFIED` 並排除。

### 列表頁與彙整容器

搜尋極常回傳列表頁（例如 `/tags/`、`/security`、分類首頁）。
列表頁既不是新聞也不是彙整容器，依 `decision_policy.yaml > digest_expansion.list_page` 處理：
取得個別文章連結後各自開原文，列表頁本身永不收錄。

彙整型容器（資安日報、週報等）先依 `digest_expansion` 展開事件，再讓每個事件獨立進後續流程。

## Stage 2 · Filter

順序固定：便宜雜訊規則 → 來源可驗證性 → 具體事實 → 語意主旨 → 資訊處相關性。

Q1、Q2、Q3、Q4 是入選前必要條件。
使用 `decision_policy.yaml` 的唯一 relevance score。
`score >= 5` 為 KEEP。
`score 3–4` 為 REVIEW。
`score <= 2` 為 EXCLUDE。

REVIEW 不會因為數量不足自動變 KEEP。
若 KEEP 數量已足，預設不把 REVIEW 塞進 LINE draft。

所有排除都留下標題、理由、score、negative signals、source tier 與 related project/duty。
這份 excluded ledger 是之後回答「為什麼沒收」的依據。

## Stage 3 · Dedup

先做本批同事件去重，再跟 `state/published_history.jsonl` 做跨日去重。
比對順序是 URL、標題正規化、event_key 語意比對。

同事件多來源時優先保留官方一手來源，其次完整度、來源層級與首發時間。
後續報導若有新增官方回應、數據或受害範圍，可以視為新事件進展。
只有重述與評論則排除。

history 為空時不中止執行。
Q5 必須標 DEGRADED，並告知跨日去重保護不完整。

## Stage 4 · Summarize

每則保留原標題，不改寫。
輸出來源、發布時間、完整原文 URL、分類、2–3 句繁體中文摘要與內部相關性理由。

摘要回答「發生什麼、涉及誰與規模、若有直接證據則補公部門意涵」。
所有事實都必須回到原文。
原文沒有的數字、時間與判斷不能自行補。

## Stage 5 · Verify

逐則執行 Q0–Q8。
Q1–Q6 任一 FAIL 的單篇不得進待審 LINE 草稿。
Q7 可為 DEGRADED，但不得補垃圾。
Q8 在人審前固定 WAIT。

T1 完成後若低於 target_min，依 `runtime.yaml` 擴到 T2，只補搜新時間區段。
T2 仍不足再跑 T3。
每次擴展都要回報，而且 Q3/Q4 門檻不變。

每次 run 都記錄 T1、T2、T3 的 yield telemetry。
累積五個工作日後才決定 24 小時窗是否合理。

## Stage 6 · Draft

依 `output_contract.md` 依序產出：run summary、審核表、LINE 草稿、excluded ledger 摘要、待確認設定。
Q0–Q8 結果放在稽核軌跡層，不放在承辦審核表首行。
此時狀態固定是 `AWAITING_HUMAN_REVIEW`。

承辦可以輸入：`刪除 3、7`、`第 5 則換掉`、`智慧城市多找兩則`、`只留今日的`、`為什麼沒收 X`。
系統只重跑受影響部分，不需要整批從零開始。

## Stage 7 · Human Review / Finalize

只有使用者明確說「通過／定版／可以了」，Q8 才 PASS。
之後才可以產生或寫回 `published_history.jsonl`。
週五定版時同步更新 `state/handover.md`。

若執行環境沒有檔案寫入能力，輸出待保存內容並明確標示尚未持久化。
不得把「已產生內容」寫成「已保存」。

## Failure behavior

搜尋部分失敗只重試受影響 query 一次。
原文抓取失敗且無替代可靠來源時移除該則。
核心來源互相衝突時標待查並移出 LINE draft。
工具不可用時停止受影響階段，列出未完成事項，不宣告完成。
