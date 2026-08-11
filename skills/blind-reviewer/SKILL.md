---
name: blind-reviewer
description: 通用盲审引擎原子技能。完全无状态与业务解耦。接收审查目标资产 (target_file) 与工作流指定的审查标准文件 (standards_file)，直接单文件装载该标准文件执行冷酷苛刻质检，输出 [PASS] 或包含结构化重写指南的 [REJECT] 诊断报告。
---

# Universal Blind Reviewer Skill (`blind-reviewer`)

本技能为 **纯粹解耦、极速精准的通用盲审引擎原子技能**。不包含任何分支判定与业务硬编码，由上层工作流（Workflow）提前完成文件检测并传入明确的审查标准文件。

---

## 📥 输入参数规范 (Input Parameters)

盲审引擎被调度时接收以下 2 个核心参数：

| 参数名称 | 类型 | 说明 | 示例 |
| :--- | :--- | :--- | :--- |
| **`target_file`** | 字符串 (必填) | 待审查的目标资产文件路径 | `./my-article/mp_article.html` |
| **`standards_file`** | 字符串 (必填) | 工作流决定的单文件审查标准路径 | `./learnings/weixin.md` 或 `skills/wx-formatter/references/mp_reviewer_standards.md` |

---

## 🎯 极速质检流程 (Execution Protocol)

1. **单文件直接装载 (Single-File Direct Load)**：
   - 盲审 SubAgent 启动后，**直接且仅装载 `standards_file`** 指向的规则文件。
   - 零分支推理、零额外工具调用，实现理论上的极速推理与最高 Token 效率。
2. **冷酷苛刻与二元裁决 (Strict Binary Verdict)**：
   - 裁决结论仅为 **`[PASS]`**（通过）或 **`[REJECT]`**（打回）。
   - 判定 `[REJECT]` 时，必须输出具体到位置与行号的**结构化重写指南 (Actionable Revision Guide)**。

---

## 关联参考协议

- [`references/reviewer_engine_protocol.md`](references/reviewer_engine_protocol.md)：盲审引擎质检流程与诊断输出协议。
