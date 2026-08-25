# Repository Boundary

## Callable technology repo

本 repo 可以放：

- 模型入口檔。
- runtime contract。
- topic / search profile。
- decision policy。
- workflow。
- output contract。
- platform adapter。
- 空白 state skeleton。
- 公開安全的架構圖與 review handoff。

## Internal project repo

`Endwar116/KS-goverment` 保留：

- 需求訪談與逐字來源。
- 人物與科別 Source of Truth。
- 顧問內部討論。
- 專案成員與主管的協作紀錄。
- 完整 regression / E2E 原始證據。
- SIC-JS governance log。
- project lifecycle state。

## Hard rule

這個 callable repo 是 public。
不得把內部專案資料因為「技術上有用」就順手複製進來。
若 runtime 規則來自內部需求，這裡只保留抽象後的可執行規則。
來源證據仍回內部 repo 查。
