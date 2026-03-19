# 功能提案入口

## 1. 業務任務信息
功能名稱：agreement-info-query
功能類型：query
所屬模塊：transaction
變更目標：新增 agreement information 查詢接口
技術面：API / ORM / mapstruct / current user / test
變更範圍：新增查詢接口、新增查詢入參與返回對象、新增 mapper 查詢
禁止變更：不改資料表結構、不改既有 API path、不改既有 helper

## 2. AI 知識底座路徑
AI知識底座根目錄：`.project-ai/`
索引文件：`.project-ai/context/index.md`
上下文目錄：`.project-ai/context/`
規則目錄：`.project-ai/rules/`
模板目錄：`.project-ai/templates/`

## 3. 現狀掃描範圍
代碼倉根目錄：`<repo-root>/`
優先掃描：
- `<repo-root>/src/main/java/.../transaction/`
- `<repo-root>/src/main/resources/mapper/transaction/`
- `<repo-root>/src/test/java/.../transaction/`

擴展掃描：
- `<repo-root>/src/main/java/.../agreement/`
- `<repo-root>/src/main/resources/mapper/agreement/`

需優先檢查的存量類型：
- Controller
- Service
- BO / DTO / VO / Entity
- Mapper / XML
- Helper / Converter
- Enum / 常量
- 單元測試

## 4. 設計文檔選擇規則
設計文檔根目錄：`.project-design-docs/`
如已知，直接指定設計文檔：
- `.project-design-docs/sprint5/xxx.md`

若未指定，按以下優先級選擇：
1. 與功能名稱最接近的設計文檔
2. 同模塊（transaction）下最近一次 query 類設計文檔
3. 同 sprint 下最相近功能文檔
4. 若無可參考文檔，標註“本次基於存量代碼與規則推導設計”

## 5. 本次功能資產輸出位置
功能資產根目錄：`.project-features/`
本次輸出目錄：`.project-features/sprint5/agreement-info-query/`

需生成文件：
- `spec.md`
- `design.md`
- `tasks.md`

## 6. 歸檔位置與歸檔標準
本次歸檔文件：`.project-features/sprint5/agreement-info-query/archive.md`

歸檔標準：
僅在以下條件全部滿足後才允許歸檔：
1. spec 已確認
2. design 已確認
3. tasks 已確認
4. 代碼實施已完成
5. 編譯 / 測試結果已輸出
6. 人工最終審核已通過

歸檔內容至少包括：
- 本次任務基本信息
- 最終採用的 spec / design / tasks 路徑
- 最終實施結果摘要
- 變更文件清單
- 關鍵決策與取捨
- 未解決問題 / 後續風險
- 是否新增 / 修正了 rules / index / templates
- 下一次增強需求應優先閱讀哪些文件

## 7. 歷史歸檔引用規則（供未來提案使用）
若本次功能後續有 enhancement（增強需求）或重構需求，下一次提案應優先引用：
1. `.project-features/sprint5/agreement-info-query/archive.md`
2. `.project-features/sprint5/agreement-info-query/spec.md`
3. `.project-features/sprint5/agreement-info-query/design.md`
4. `.project-features/sprint5/agreement-info-query/tasks.md`
5. 當前 Git 現狀代碼
6. 必要時再補讀 `.project-design-docs/` 對應文檔

引用原則：
- 先讀 `archive.md` 了解上次最終方案、決策、風險與推薦閱讀路徑
- 再讀 `spec.md` 理解原始目標、邊界與驗收標準
- 再讀 `design.md` 理解實現方式與分層設計
- `tasks.md` 僅在需要復用實施順序或檢查清單時閱讀
- 若 archive 與 Git 現狀代碼衝突，以 Git 現狀為實物基線，並在新 spec 中標明差異

## 8. 執行要求
1. 先讀索引文件，再按索引裝配 context / rules / templates
2. 再掃描指定代碼範圍
3. 再讀匹配的設計文檔
4. 先生成 `spec.md`
5. spec 確認後，再生成 `design.md`
6. design 確認後，再生成 `tasks.md`
7. tasks 確認後，按 `spec + design + tasks` 實施代碼
8. 人工審核通過後，再執行歸檔
9. 如本次產生通用規範增量，需同步更新 `.project-ai/context/index.md` 或對應 rules