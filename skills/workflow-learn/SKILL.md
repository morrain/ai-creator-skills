---
name: workflow-learn
command: /workflow-learn
description: 偏好提取与规则自进化反哺工作流。当用户发送 /workflow-learn 指令、或在审核通过/人工修饰后需要将主编偏好沉淀为长期规则时唤起。
---

# 🧠 分环节审稿标准与案例库反哺 Skill (Targeted Review Tuner Skill)

本 Skill 为 `ai-creator-skills` 项目的多环节精准自进化闭环管道，负责自动识别创作环节 (`phase_id`)，搜集最近一轮审核修饰意见，呈报用户筛选，并将规则沉淀落盘至项目根目录 `./learnings/<phase_id>.md` 中。

---

## 核心设计原则

1. **最近一轮审核意见精准搜集**：仅抓取最近一轮盲审打回记录或主编批注。
2. **人工交互式规则筛选关卡 (User Selection Gate)**：呈现带编号候选列表，**暂停等待用户明确选择**，仅将选中的编号落盘。
3. **动态蒸馏去重与冲突覆盖**：最新选中的规则可覆盖旧冲突规则。
4. **硬性容量上限与滑动淘汰**：黑名单上限 10 条、范例上限 5 条、硬指标上限 5 条，超限 FIFO 淘汰。
5. **底层 Skill 零污染**：演进规则全量独立落盘在项目根目录 `./learnings/` 中。

---

## 阶段流程与 Reference 映射

详细步骤说明与 `phase_id` 路由表请参阅：
[references/stage_details.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-learn/references/stage_details.md)

1. **步骤一**：识别 `phase_id`，使用 `view_file` 重新读取磁盘文件，搜集最近一轮意见。
2. **步骤二**：结构化归纳候选规则清单。
3. **步骤三**：呈报清单，**暂停等待用户回复选择**。
4. **步骤四**：读取用户回复的选择编号，蒸馏去重并淘汰，落盘写入 `./learnings/<phase_id>.md`。
