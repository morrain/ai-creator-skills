---
name: blind-reviewer
description: 通用自进化盲审引擎原子技能。完全无状态与业务解耦。接收审查目标资产 (target_file)、技能默认基线标准 (default_standards) 及可选的项目进化增量文件 (learnings_file)。若 learnings_file 存在则优先校验项目增量偏好并结合技能基线标准与关联同级文件 (如 anti_patterns.md) 进行综合质检，输出 [PASS] 或包含结构化重写指南的 [REJECT] 诊断报告。
---

# Universal Blind Reviewer Skill (`blind-reviewer`)

本技能为 **纯粹解耦、支持【领域基线】+【项目增量】双层精准组合的通用盲审引擎原子技能**。不包含任何业务硬编码，由上层工作流（Workflow）提前完成文件判定并精准透传参数。

---

## 📥 输入参数规范 (Input Parameters)

盲审引擎被调度时接收以下参数：

| 参数名称 | 类型 | 说明 | 示例 |
| :--- | :--- | :--- | :--- |
| **`target_file`** | 字符串 (必填) | 待审查的目标资产文件路径 | `./my-article/mp_article.html` |
| **`default_standards`** | 字符串 (必填) | 技能默认基线标准路径（保持与其同级 relative 引用链接完好） | `skills/wx-formatter/references/mp_reviewer_standards.md` |
| **`learnings_file`** | 字符串 (可选) | 项目级自进化增量偏好规则文件路径（若存在则传入） | `./learnings/weixin.md` |

---

## 🎯 规则装载与质检逻辑 (Execution Protocol)

1. **双层规则精准校验 (Dual-Layer Verification)**：
   - **当 `learnings_file` 存在并传入时**：
     - 审稿人 **优先校验 `learnings_file`** 中的主编专属黑名单、金句偏好与追加硬指标；
     - **同时装载 `default_standards`** 及其引用的领域核心词库（如 `references/anti_patterns.md`、`references/golden_examples.md`、`references/style_definitions.md`）。
   - **当 `learnings_file` 未传入时**：
     - 审稿人仅装载 `default_standards` 及其关联的同级领域词库执行基线质检。
2. **冷酷苛刻与二元裁决 (Strict Binary Verdict)**：
   - 裁决结论仅为 **`[PASS]`**（通过）或 **`[REJECT]`**（打回）。
   - 判定 `[REJECT]` 时，必须输出具体到位置与行号的**结构化重写指南 (Actionable Revision Guide)**。

---

## 关联参考协议

- [`references/reviewer_engine_protocol.md`](references/reviewer_engine_protocol.md)：盲审引擎质检流程与诊断输出协议。
