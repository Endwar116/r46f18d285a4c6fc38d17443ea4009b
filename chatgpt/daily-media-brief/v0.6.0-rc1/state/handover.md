# Handover State

目前為空白 callable state skeleton。

輪值交接時只保存執行所需的非機敏摘要。
若內容含內部敏感資訊，應由部署環境的受控 state store 保存，不應 commit 到 public repo。
