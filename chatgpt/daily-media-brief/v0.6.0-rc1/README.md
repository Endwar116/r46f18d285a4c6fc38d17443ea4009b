# ChatGPT Daily Media Brief v0.6.0-rc1

這是 portability candidate。
它的使用者介面來源是已跑過 live UX / language regression 的 ChatGPT v0.4.7-rc1。

舊 baseline 的 live run 有兩個重要 findings。

第一，discovery search 32 的 sub-cap 曾實際跑到 36。
第二，當次 live run 沒有把所有 surfaced result 完整 materialize 成逐列 candidate / excluded ledger。

v0.6.0-rc1 已把 pre-dispatch budget clipping 與 batch-by-batch ledger persistence 寫入 compact contract。
這兩項目前仍屬 contract-level correction。
尚未用獨立新 ChatGPT 對話重新 E2E，所以不能視為 production-ready。

這個平台版本主要供德德比較 shared behavior。
Claude finalization 仍以 `claude/` 為主。
