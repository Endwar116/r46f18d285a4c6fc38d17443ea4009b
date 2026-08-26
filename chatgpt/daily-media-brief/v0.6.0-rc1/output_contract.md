# Daily Media Brief · Output Contract

版本：v0.6.0-rc1  
候選修訂：source-coverage-expansion-2026-08-26

本檔統一三種輸出：承辦審核表、LINE 可貼草稿、內部稽核軌跡。
三者來自同一批 selected items，禁止各自重做判斷。

## 1. 承辦審核表

目標是快速掃讀與一句話修改。
每則至少顯示：連續編號、selection band、原標題、時間階層、來源、來源類別、時間、第一句摘要、內部「為什麼要看」、原文連結。
編號跨分類連續，避免「刪除 3、7」產生歧義。

selection band：
- `CORE｜核心輿情`：直接業務、政策、重大資安或既有專案相關。
- `EXTENDED｜延伸觀測`：具有明確比較、前瞻、技術變化或可追蹤價值，且 Q1/Q2/Q3/S3 已通過。
- `SIGNAL_CANDIDATE｜待查訊號`：只在審核附區顯示，不得混入 LINE 可貼草稿，直到完成交叉驗證。

時間階層使用 `[今日]`、`[48h]`、`[72h]`。
若有來源擴張或時間擴展，審核表最上方必須列：CORE、EXTENDED、來源擴張新增數、signal candidates、T1/T2/T3 各自入選數。

「為什麼要看」是 Q4 的可視化結果。
若只能寫「與 AI／資安／智慧城市有關」，代表 Q4 沒有真正通過。

範例：
```text
輿情日報審核表｜YYYY/MM/DD
Q0 PASS · Q1 PASS · Q2 PASS · Q3 PASS · Q4 PASS · Q5 PASS · Q6 PASS · Q7 PASS · Q8 WAIT
來源覆蓋：官方/專業 ✓｜主流/產業 ✓｜地方/同業城市 ✓｜signal lane 2 則待查
入選：CORE 9｜EXTENDED 4｜今日 11｜48h 補 2｜72h 0

1 ▸ [CORE][今日] 原始新聞標題
   iThome｜B_PROFESSIONAL｜08/25 09:15
   為什麼要看：直接影響地方政府資訊安全責任，涉及＿＿＿＿。
   摘要：第一句摘要……
   https://example.com/article

2 ▸ [EXTENDED][今日] 原始新聞標題
   某主流媒體｜C_MAINSTREAM｜08/25 08:20
   為什麼要看：可作同業城市＿＿能力比較，資訊處可追蹤＿＿。
   摘要：第一句摘要……
   https://example.com/article

回覆：通過｜刪除 2、7｜5 換一則｜智慧城市多找兩則｜只留核心輿情｜論壇訊號多看一下｜3 為什麼收？
```

## 2. LINE 可貼草稿

LINE 是純文字環境。
一則一段，段間空一行。
標題獨立成行。
完整 URL 放最後。
不用 Markdown 表格、粗體語法或縮網址。

CORE 與 EXTENDED 可同時進待審 LINE 草稿。
若有 EXTENDED，分類標頭或該則前綴需讓承辦看得出是「延伸觀測」。
SIGNAL_CANDIDATE 不可直接進 LINE 草稿。

每則格式：
```text
1. 原始新聞標題
來源｜MM/DD HH:MM
2–3 句繁體中文摘要。
https://example.com/article
```

若為 EXTENDED：
```text
延伸觀測
2. 原始新聞標題
來源｜MM/DD HH:MM
2–3 句繁體中文摘要。
https://example.com/article
```

超過 12 則時，依分類拆成多段訊息，避免一次變成文字牆。
若全部是 T1，不需在每則標時間階層。
若含 T2/T3，分類標頭必須說明「今日 N 則，其餘為 48／72 小時內補充」。
週一標頭需明寫涵蓋上週五 00:00 起至今。

某分類零則也保留分類，寫明已搜尋但目前沒有符合條件內容。
不能直接省略，避免讓人誤以為漏跑。

## 3. 來源覆蓋摘要

這層讓承辦與顧問知道「今天有沒有只困在少數網站」。
至少列：
- active source set 數量。
- 官方／專業來源命中數。
- 主流／產業來源命中數。
- 地方／同業城市來源命中數。
- signal lane surfaced 數量與已完成交叉驗證數。
- 本次未能存取的重要來源。

不需要把 100 個來源逐一印出。
完整來源表留在 `source_registry_taiwan.yaml`。

## 4. 稽核軌跡

這層給承辦、顧問與維護者調參，不直接貼 LINE。
每個 run 至少留下：
- run_id、執行時間、時間階層、source coverage plan 與 query plan。
- 候選總數、CORE、EXTENDED、SIGNAL_CANDIDATE、排除數。
- 每則 source_id、source_class、selection_band。
- 每則語意排除的標題與理由。
- Q0–Q8 結果。
- 本批與歷史去重數。
- 反向召回命中數。
- 各主題的雜訊比例與零結果 query。
- digest expansion 容器與展開數。
- source expansion 與 T1/T2/T3 yield telemetry。
- 人工刪除、換稿、補搜與最終通過事件。

被排除的新聞必須能回答「被哪個規則擋掉、當時用什麼來源、是否可能是誤殺」。
這樣後續調參才有實際依據。

## 5. 人工命令

`刪除 3、7`：移除並連續重新編號。
`第 5 則換掉`：只補搜相同 topic/category。
`智慧城市多找兩則`：建立本次 runtime override，不改永久 topic profile。
`論壇訊號多看一下`：啟動或加強 signal lane，只把完成交叉驗證者升到一般候選。
`只留核心輿情`：移除 EXTENDED，接受則數下降。
`只留今日的`：移除 T2/T3，接受則數下降。
`某則為什麼沒收`：查 excluded ledger 回答。
`通過／定版／可以了`：Q8 PASS，才允許形成歷史更新。

## 6. 發布邊界

本輸出只是可貼文字。
目前 Skill 不自行操作 LINE 群組，也不自行排程。
實際自動發送若未來要做，屬外部整合層，需要另外設計權限、排程、身份與稽核。