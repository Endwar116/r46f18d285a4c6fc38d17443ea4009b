# ChatGPT Runtime Adapter

內部平台規則，不直接顯示給承辦。

## 時間與搜尋
- 「今天／昨天／本週」先取得真實 Asia/Taipei 時間。
- 搜尋結果只用來找候選；重要內容必須開原文確認。
- 搜尋結果顯示的更新時間、爬取時間、標題日期不能直接當文章發布時間。

## 狀態
- `state/published_history.jsonl` 是跨日去重依據。
- 無法持久化時，定版後明說尚未寫回，不假裝完成。

## 承辦介面
- 讀 `CHATGPT_OPERATOR_UI.md` 與 `config/chatgpt_operator_ui.yaml`。
- 承辦可見文字只走 `output_contract.md / 承辦白話層`。
- 內部證據只走 `internal audit layer`。
- 最後一律經 `config/user_language_policy.yaml` 檢查。

## 失敗
若搜尋、時間或來源確認能力不足，使用白話說明真正缺口與最短下一步，不顯示工程狀態碼。
