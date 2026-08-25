# KCG IT Daily Media Brief · Callable Technology Repository

這個 repository 只放可被模型載入、呼叫、比較與審查的輿情技術。

內部專案紀錄、訪談逐字、人物校正、顧問討論、治理事件與完整測試證據留在 `Endwar116/KS-goverment`。
這裡不複製那些內部材料。

目前分成兩條平台線。

- `claude/`：Claude compact candidate。
  這是目前要交給德德最後審查與完成的版本。
- `chatgpt/`：ChatGPT compact portability candidate。
  它保留 ChatGPT 的承辦介面與語言層，作為跨平台比較參考。

兩個平台目錄彼此獨立。
不要從其中一邊 runtime 直接引用另一邊的檔案。

## Status

兩邊目前都屬 review candidate。
尚未宣告 production-ready。

Claude candidate 已完成 compact contract 靜態檢查。
真實 Claude runtime E2E 仍需由德德執行。

ChatGPT candidate 由已實測的 v0.4.7-rc1 行為基線收斂而來。
舊基線曾出現 discovery sub-cap 超限與 live ledger 不完整，v0.6.0-rc1 已把兩項修正寫入 compact contract，但尚未以獨立新對話重新驗證。

## Repository boundary

技術成品與平台 adapter 放這裡。

專案現場資料、需求訪談、決策紀錄、測試原始證據與 handoff state 留在內部專案 repo。

詳見 `REPO_BOUNDARY.md`。
