# 任务归档：agreement-info-query

## 1. 基本信息
- 功能名称：agreement-info-query
- 功能类型：query
- 所属模块：transaction
- 完成时间：YYYY-MM-DD
- 任务状态：已完成 / 已归档

## 2. 本次最终采用文件
- spec：`./spec.md`
- design：`./design.md`
- tasks：`./tasks.md`

## 3. 本次最终实施结果
- 新增查询接口：...
- 新增 BO / DTO / VO / Entity：...
- 新增 / 修改 mapper / xml：...
- 新增 / 修改测试：...

## 4. 关键决策
- 为何放在 transaction 现有模块
- 为何不改资料表结构
- 为何不改既有 helper
- 为何沿用某个现有 query 模式
- 为何使用某个 converter / enum / helper

## 5. 实施结果摘要
- 变更文件清单：...
- 编译结果：通过 / 未通过
- 测试结果：通过 / 未通过
- 已知风险：...

## 6. 规范反哺
- 本次是否新增 / 修正 rules：是 / 否
- 涉及文件：...
- 本次是否更新 index：是 / 否
- 涉及文件：...

## 7. 下一次增强需求的引用建议
若后续需对本功能做 enhancement（增强）或重构，建议按以下顺序引用历史资产：

1. 先读本文件（`archive.md`），了解本次最终方案、关键决策、边界与风险
2. 再读 `spec.md`，理解原始目标、范围与验收标准
3. 再读 `design.md`，理解实现方式、分层设计与关键落位
4. 再扫描当前 Git 现状代码，确认历史资产与当前代码是否存在漂移
5. 如需复用实施顺序或检查清单，再读 `tasks.md`

注意：
- 若 `archive.md`、`spec.md`、`design.md` 与当前 Git 现状代码不一致，应以当前 Git 代码为实物基线，并在新一轮 spec 中明确标注差异。

## 8. 下一次提案需特别注意
- 与 Git 现状是否有漂移
- 是否仍需保持不改表 / 不改 helper
- 是否已有新设计文档覆盖当前 design