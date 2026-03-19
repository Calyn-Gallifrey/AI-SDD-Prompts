# UAW AI 規範索引（how-to-index）

## 1. 文件定位

本索引用於 UAW 專案中 AI 規範文件的檢索與裝配，供人與 AI 在以下環節使用：

- 生成功能級 spec / proposal（提案 / 增量規格）
- 生成設計文檔 design
- 生成任務編排 tasks
- Builder / AI 實施代碼時選取對應規範
- 增強需求時回看既有規範與功能資產

注意：

1. 本索引不是功能 spec，也不是 todo。
2. 本索引不直接承載具體功能需求，只承載“該讀哪些規範”的路由信息。
3. 同一份規範可能在 spec、design、tasks 多個環節被重複引用。
4. 項目階段（需求 / 設計 / 開發 / 測試）僅作為檢索視角，不作為 how-to 主存儲結構。

---

## 2. 當前 how-to 目錄現狀

### 2.1 detailed-context
用於存放領域背景、字典、輔助性上下文、輸出模板等資料。

### 2.2 spec-context
用於存放可重複調用的工程規範、實作模式、對象規則、測試規範等文件。

注意：
雖然當前目錄名仍為 `spec-context`，但其中大部分內容本質上不是 spec，而是 rules / patterns / templates。

---

## 3. 按知識性質分類的主索引

> 說明：以下為“主分類”，優先作為 AI 與人檢索規範時的第一層路由。

### 3.1 領域上下文（Context）

#### 3.1.1 transactions 字典與命名上下文
- `detailed-context/2.transactions字典清单.md`
- 用途：
  - 查詢 transactionType、模塊歸屬、命名方式
  - 在 spec 階段理解功能所屬交易類型
  - 在 design / tasks 階段確定 transaction 類型、包路徑與相關依賴

#### 3.1.2 git commit 輸出模板
- `detailed-context/3.根据本次变更内容生成git_commit记录.md`
- 用途：
  - 在任務完成後生成提交信息
  - 不屬於功能規格，也不屬於開發規則
  - 屬於交付與收尾模板

#### 3.1.3 create table 腳本模板
- `detailed-context/1.create_table编写规范.md`
- 用途：
  - 根據本次變更輸出 SQL 建表 / 變更腳本
  - 偏模板，不是完整的資料表設計規則
  - 與“如何新增一個資料庫表”配合使用

---

### 3.2 後端工程規則（Backend Rules）

#### 3.2.1 資料表規則
- `spec-context/1.如何新增一个数据库表.md`
- 用途：
  - 新增表命名、審計欄位、索引、約束、腳本落位等規則
  - 適用於 spec / design / tasks 三個環節

#### 3.2.2 transaction 模塊包結構規則
- `spec-context/2.如何新增一个transaction业务功能包结构.md`
- 用途：
  - 明確 transaction 模塊的 base/common/core/support 分層方式
  - 在 spec 階段確定增量落位
  - 在 design / tasks 階段確定包路徑與類落位

#### 3.2.3 後端 API 規則
- `spec-context/3.如何开发一个后端API接口代码.md`
- 用途：
  - Controller / Service / DTO / VO / Helper / Converter 等生成規則
  - 為 design 與 tasks 階段的核心引用文件

#### 3.2.4 MyBatis ORM 規則
- `spec-context/4.如何开发mybatis的ORM代码.md`
- 用途：
  - Entity / Mapper / XML / namespace / <where> / <foreach> / 目錄落位等規則
  - 適用於 design / tasks / code review

#### 3.2.5 當前用戶規則
- `spec-context/5.如何获取当前用户.md`
- 用途：
  - 規定不同層如何獲取當前使用者
  - 適用於 design / tasks / 代碼檢查

#### 3.2.6 EPI 接口調用規則
- `spec-context/6.如何调用epi网关接口.md`
- 用途：
  - 外部接口調用、ACL（防腐層）實作、parser / helper 組裝等
  - 適用於 design / tasks

#### 3.2.7 MapStruct 轉換規則
- `spec-context/7.如何基于mapstruct进行值对象转换.md`
- 用途：
  - BO / DTO / VO / Entity 之間的轉換規則
  - 適用於 design / tasks / 代碼檢查

---

### 3.3 對象生成規則（Model Rules）

#### 3.3.1 BO 規則
- `spec-context/8.1-BO对象生成规范.md`

#### 3.3.2 VO 規則
- `spec-context/8.2-VO对象生成规范.md`

#### 3.3.3 DTO 規則
- `spec-context/8.3-DTO对象生成规范.md`

#### 3.3.4 Entity 規則
- `spec-context/8.4-Entity对象生成规范.md`

用途：
- 在 design 階段定義對象設計
- 在 tasks 階段生成與檢查具體模型類
- 不作為獨立功能 spec 使用

---

### 3.4 集成與兼容模式（Patterns）

#### 3.4.1 OM API 防腐層模式
- `spec-context/9.如何开发om api防腐代码.md`
- 用途：
  - 與 OM 對接時的 ACL / parser / helper / 調用模式
  - 適用於 design / tasks

#### 3.4.2 transaction 與 caseTracker 兼容模式
- `spec-context/11.新增transaction如何兼容caseTrakcer功能.md`
- 用途：
  - 新增 transaction 類型時如何兼容既有 caseTracker 能力
  - 適用於 spec / design / tasks
  - 屬於高風險場景必讀規範

---

### 3.5 測試規則（Testing Rules）

#### 3.5.1 通用方法單測
- `spec-context/10.如何生成方法的单元测试.md`

#### 3.5.2 Service 單測
- `spec-context/29-1如何service的单元测试.md`

#### 3.5.3 static 方法單測
- `spec-context/29-2如何生成静态static方法的单元测试.md`

#### 3.5.4 Controller 單測
- `spec-context/29-3如何编写controller单元测试规范.md`

#### 3.5.5 ServiceStrategy 單測
- `spec-context/29-4如何创建ServiceStrategy的单元测试.md`

用途：
- tasks 階段補充測試任務
- code review / 自動補測試時引用
- 不在 spec 階段大量引用，除非需求本身要求補齊測試範圍

---

## 4. 按項目階段的檢索索引（僅作檢索視角）

> 注意：此部分不是 how-to 主目錄，只是檢索入口。

### 4.1 spec / proposal 階段優先讀取

當目標是“生成功能提案、增量 spec、需求邊界說明”時，優先讀取：

- `detailed-context/2.transactions字典清单.md`
- `spec-context/2.如何新增一个transaction业务功能包结构.md`
- `spec-context/1.如何新增一个数据库表.md`（若涉及表變更）
- `spec-context/11.新增transaction如何兼容caseTrakcer功能.md`（若涉及 transaction 類型）
- `spec-context/6.如何调用epi网关接口.md`（若涉及外部 EPI）
- `spec-context/9.如何开发om api防腐代码.md`（若涉及 OM 對接）

spec 階段的目標不是直接生成代碼，而是回答：
- 本次功能屬於哪個模塊
- 建立在什麼存量之上
- 哪些地方是增量
- 哪些規則後續設計一定會引用
- 哪些高風險兼容點必須提前寫入 spec

---

### 4.2 design 階段優先讀取

當目標是“生成設計文檔、類設計、分層方案、數據流設計”時，優先讀取：

- `spec-context/3.如何开发一个后端API接口代码.md`
- `spec-context/4.如何开发mybatis的ORM代码.md`
- `spec-context/5.如何获取当前用户.md`
- `spec-context/7.如何基于mapstruct进行值对象转换.md`
- `spec-context/8.1-BO对象生成规范.md`
- `spec-context/8.2-VO对象生成规范.md`
- `spec-context/8.3-DTO对象生成规范.md`
- `spec-context/8.4-Entity对象生成规范.md`
- `spec-context/6.如何调用epi网关接口.md`（若涉及 EPI）
- `spec-context/9.如何开发om api防腐代码.md`（若涉及 OM）
- `spec-context/11.新增transaction如何兼容caseTrakcer功能.md`（若涉及 caseTracker）

design 階段的目標是回答：
- 類與包應該怎麼拆
- 對象怎麼建
- 查詢與持久化怎麼做
- 外部接口怎麼封裝
- 轉換與當前用戶邏輯怎麼放
- 哪些規則需要在 tasks 階段被顯式編排

---

### 4.3 tasks 階段優先讀取

當目標是“生成 Builder 任務編排文件、AI 執行順序、代碼生成與檢查清單”時，優先讀取：

- `spec-context/3.如何开发一个后端API接口代码.md`
- `spec-context/4.如何开发mybatis的ORM代码.md`
- `spec-context/5.如何获取当前用户.md`
- `spec-context/7.如何基于mapstruct进行值对象转换.md`
- `spec-context/8.1-BO对象生成规范.md`
- `spec-context/8.2-VO对象生成规范.md`
- `spec-context/8.3-DTO对象生成规范.md`
- `spec-context/8.4-Entity对象生成规范.md`
- `spec-context/10.如何生成方法的单元测试.md`
- `spec-context/29-1如何service的单元测试.md`
- `spec-context/29-2如何生成静态static方法的单元测试.md`
- `spec-context/29-3如何编写controller单元测试规范.md`
- `spec-context/29-4如何创建ServiceStrategy的单元测试.md`
- `detailed-context/3.根据本次变更内容生成git_commit记录.md`

tasks 階段的目標是回答：
- 先做哪些對象
- 再做哪些 service / controller / mapper / xml
- 哪些規則必須作為檢查項
- 最後要補哪些測試
- 收尾時如何生成 commit 記錄

---

## 5. 按常見任務場景的組合索引

### 5.1 場景：新增 transaction 查詢接口
必讀：
- `detailed-context/2.transactions字典清单.md`
- `spec-context/2.如何新增一个transaction业务功能包结构.md`
- `spec-context/3.如何开发一个后端API接口代码.md`
- `spec-context/4.如何开发mybatis的ORM代码.md`
- `spec-context/5.如何获取当前用户.md`
- `spec-context/7.如何基于mapstruct进行值对象转换.md`
- `spec-context/8.1-BO对象生成规范.md`
- `spec-context/8.2-VO对象生成规范.md`
- `spec-context/8.3-DTO对象生成规范.md`
- `spec-context/8.4-Entity对象生成规范.md`
- 測試規則（視範圍補充）

### 5.2 場景：新增 transaction 類型
必讀：
- `detailed-context/2.transactions字典清单.md`
- `spec-context/2.如何新增一个transaction业务功能包结构.md`
- `spec-context/11.新增transaction如何兼容caseTrakcer功能.md`
- 視情況補：
  - `spec-context/1.如何新增一个数据库表.md`
  - `spec-context/4.如何开发mybatis的ORM代码.md`
  - `spec-context/3.如何开发一个后端API接口代码.md`

### 5.3 場景：新增資料表並落地 CRUD / 查詢
必讀：
- `detailed-context/1.create_table编写规范.md`
- `spec-context/1.如何新增一个数据库表.md`
- `spec-context/4.如何开发mybatis的ORM代码.md`
- `spec-context/8.4-Entity对象生成规范.md`

### 5.4 場景：對接 EPI / OM 外部接口
必讀：
- `spec-context/6.如何调用epi网关接口.md`
- `spec-context/9.如何开发om api防腐代码.md`
- `spec-context/5.如何获取当前用户.md`
- 視情況補：
  - `spec-context/7.如何基于mapstruct进行值对象转换.md`
  - `spec-context/8.* 对象生成规范`

### 5.5 場景：補充或生成單元測試
必讀：
- `spec-context/10.如何生成方法的单元测试.md`
- `spec-context/29-1如何service的单元测试.md`
- `spec-context/29-2如何生成静态static方法的单元测试.md`
- `spec-context/29-3如何编写controller单元测试规范.md`
- `spec-context/29-4如何创建ServiceStrategy的单元测试.md`

---

## 6. spec / design / tasks 三個環節如何引用本索引

### 6.1 在 spec 階段
先讀本索引第 4.1 節與第 5 節，確定：
- 功能屬於哪個場景
- 應讀哪些 context / rules / patterns
- 哪些兼容點與存量風險應寫入 spec

輸出：
- 功能 spec / proposal / 增量需求說明

### 6.2 在 design 階段
先讀本索引第 4.2 節與第 5 節，確定：
- 類與包如何設計
- 使用哪些 model 規則
- ORM / ACL / converter / current user 應如何落位

輸出：
- 設計文檔 design

### 6.3 在 tasks 階段
先讀本索引第 4.3 節與第 5 節，將規範顯式轉成執行順序：
- 先生成哪些類
- 再生成哪些 API / ORM / converter
- 補哪些測試
- 最後如何輸出 commit

輸出：
- 任務編排文件 tasks / builder-tasks

---

## 7. 使用原則

1. 本索引不替代具體規範文件。
2. 每次任務不必讀完整個 how-to，只讀本索引路由出的必要文件。
3. spec 階段偏重 context + 高層規則。
4. design 階段偏重 rules + patterns。
5. tasks 階段偏重可執行順序與檢查清單。
6. 若任務完成後新增了新的通用規則，需回寫 how-to 文件，並同步更新本索引。
7. 若任務只是局部小修補，不必強行重走完整編排，但涉及通用經驗時仍需更新索引或對應規範。