# Daily Media Brief · Compact Workflow

版本：v0.6.0-rc1  
候選修訂：source-coverage-expansion-2026-08-26

本檔是唯一流程權威。
執行順序固定為：`Orchestrate → Collect → Filter → Dedup → Summarize → Verify → Draft → Human Review`。

## Stage 0 · Orchestrate

取得 Asia/Taipei 當下時間並建立 `KCG-BRIEF-YYYYMMDD-HHMM`。
載入 `runtime.yaml`、`topic_profile.yaml`、`source_registry_taiwan.yaml`、`decision_policy.yaml`、`output_contract.md`、handover 與 published history。
依 `runtime.yaml` 建立 T1 時間窗，週一套用 Monday rule。

建立 query plan 時，P0 一定跑、P1 正常跑。
同時依本次 topic tags 從 TW100 registry 建立 active source set。
不得把 100 個來源逐站硬查。
優先覆蓋官方／專業來源，再輪替主流／產業／地方／同業城市來源。
論壇、社群與聚合器先放 signal lane，只有在候選不足、分類空白、突發訊號或使用者指定時啟用。

每次送出搜尋 batch 前，先依 `runtime.yaml > query_budget_guard` 計算剩餘搜尋額度。
proposed batch 超過 remaining slots 時先截斷，再送工具。
工具若支援 domain filter，優先用來源組合進行 domain-aware search。
不支援時，只對本輪 priority sources 使用 site: 查詢。

使用者本次說「今天只要資安」之類條件，只形成 runtime override。
只有使用者明確說「以後都這樣」才改永久 contract。

輸出 run manifest、source coverage plan 與 query plan，狀態進入 `QUERY_PLANNED`。

## Stage 1 · Collect

每條 query 獨立搜尋。
保存 query、priority、category、title、URL、search snippet、source_id、source_class、source lane 與可見時間。
每個 batch 回傳後先完成 candidate / excluded ledger row persistence，再允許下一批搜尋。
ledger row coverage 未完成時，停止後續 batch 並標示 evidence incomplete。

搜尋摘要只負責召回候選，不能當最後事實來源。
可能入選、日期不明、標題不足以判斷、需要挑一手來源或需要寫摘要時，必須開原文。
發布時間依 `decision_policy.yaml > date_verification` 驗證。
無法確認 publication time 的候選標 `DATE_UNVERIFIED` 並排除。

C_AGGREGATOR 只用來發現原始新聞。
S_SIGNAL_ONLY 與 B_COMMUNITY_PRO 不在 discovery 階段直接刪除。
它們先標 `SIGNAL_CANDIDATE`。
若不是貼文本身就是事件，進一般待審清單前必須找到 A/B/C/D 類可驗證來源或符合 signal corroboration 規則。

彙整型來源先依 `digest_expansion` 展開事件，再讓每個事件獨立進後續流程。

## Stage 2 · Filter

順序固定：便宜雜訊規則 → Q2 來源角色／證據用途 → Q3 具體事實 → 語意主旨 → Q4 資訊處相關性。

Q2 不再把「論壇／社群」等同垃圾來源。
Q2 的工作是先分類來源角色：`final evidence / discovery / signal-only`。
高風險事實仍禁止以論壇／社群單獨定案。

使用 `decision_policy.yaml` 的唯一 relevance score 與 selection bands。
`score >= 5` 為 `CORE`。
`score 3–4` 且 Q1/Q2/Q3/S3 條件都通過時為 `EXTENDED`。
`score <= 2` 為 `EXCLUDE`。

CORE 是核心輿情。
EXTENDED 是延伸觀測，可進承辦待審清單，但必須明確標示，不假裝與 CORE 相同強度。

所有排除都留下標題、理由、score、negative signals、source_id、source_class、selection_band 與 related project/duty。
這份 excluded ledger 是之後回答「為什麼沒收」的依據。

## Stage 3 · Dedup

先做本批同事件去重，再跟 `state/published_history.jsonl` 做跨日去重。
比對順序是 URL、標題正規化、event_key 語意比對。

同事件多來源時優先保留官方一手來源，其次完整度、來源層級與首發時間。
論壇／社群若只是同事件轉貼，不增加則數。
若社群本身是事件的一部分，保留其訊號角色，但仍與可驗證來源綁定。

後續報導若有新增官方回應、數據或受害範圍，可以視為新事件進展。
只有重述與評論則排除。

history 為空時不中止執行。
Q5 必須標 DEGRADED，並告知跨日去重保護不完整。

## Stage 4 · Summarize

每則保留原標題，不改寫。
輸出來源、來源類別、selection band、發布時間、完整原文 URL、分類、2–3 句繁體中文摘要與內部相關性理由。

摘要回答「發生什麼、涉及誰與規模、若有直接證據則補公部門意涵」。
所有事實都必須回到原文。
原文沒有的數字、時間與判斷不能自行補。

EXTENDED 的內部理由要說清楚它是比較案例、前瞻技術、治理變化或需追蹤的訊號。
不能只寫「跟 AI 有關」。

## Stage 5 · Verify / Volume Recovery

逐則執行 Q0–Q8。
Q1、Q3、Q5、Q6 任一 FAIL 的單篇不得進待審 LINE 草稿。
Q2 signal-only 項目需完成換源或交叉驗證。
Q4 可為 CORE 或 EXTENDED。
Q8 在人審前固定 WAIT。

若 T1 的 CORE＋EXTENDED 低於 target_min，補量順序固定：

1. 先用 TW100 registry 擴大同日來源覆蓋。
2. 補足尚未覆蓋的主流／產業／地方／同業城市來源帶。
3. 必要時啟動 signal lane，將論壇／社群只作早期訊號，再回頭找證據來源。
4. 同日來源擴張仍不足，才擴到 T2。
5. T2 仍不足再跑 T3。

任何階段都不得把 EXCLUDE 升成 EXTENDED 或 CORE。
也不得降低日期驗證、事實性、去重或摘要忠實度。

每次 run 都記錄 CORE、EXTENDED、source expansion、signal candidate、T1、T2、T3 的 yield telemetry。
累積五個工作日後再判斷主要瓶頸是來源覆蓋、Q4 誤殺還是時間窗太窄。

## Stage 6 · Draft

依 `output_contract.md` 依序產出：run summary、source coverage summary、Q0–Q8、審核表、LINE 草稿、excluded ledger 摘要、待確認設定。
此時狀態固定是 `AWAITING_HUMAN_REVIEW`。

承辦審核表中，CORE 正常呈現。
EXTENDED 必須標 `延伸觀測`。
若有 SIGNAL_CANDIDATE 尚未完成交叉驗證，只能放「待查訊號」，不得混進可貼 LINE 草稿。

承辦可以輸入：`刪除 3、7`、`第 5 則換掉`、`智慧城市多找兩則`、`論壇訊號多看一下`、`只留核心輿情`、`只留今日的`、`為什麼沒收 X`。
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
搜尋 batch 超過剩餘額度時，在 dispatch 前截斷。
ledger row coverage 未完成時，停止下一批搜尋並保留 evidence incomplete 狀態。
來源 registry 某站失效時標 `SOURCE_UNAVAILABLE`，換同類來源，不中止整個 run。