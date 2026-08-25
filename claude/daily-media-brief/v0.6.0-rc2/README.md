# Claude · Daily Media Brief · v0.6.0-rc2

高雄市政府資訊處每日輿情日報助理，Claude callable 版本。

## 怎麼用

把本目錄整個載入 Claude 對話，然後輸入：

```
給我今天輿情
```

拿到審核表後可輸入：`通過`、`刪除 3、7`、`第 5 則換掉`、`只留今日的`、`第 3 則為什麼收？`。

## 與 rc1 的差異

rc1 保留不動作為對照。
rc2 修了三個實測發現的執行缺口：query budget 未在 dispatch 前結算、ledger 未按批次落檔、query 未帶時間錨點。
詳見 `VERSION.yaml`。

## 邊界

本目錄只放可執行技術。
內部訪談、人名、治理紀錄與原始測試證據留在內部專案 repo。
