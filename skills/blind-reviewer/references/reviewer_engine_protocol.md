# 通用盲审诊断协议与裁决输出规范 (Reviewer Engine Protocol)

本规范定义 `blind-reviewer` 通用盲审引擎在执行质检时的标准评估流程与输出格式。

---

## 1. 规则装载规范 (Domain Baseline + Project Learnings Loading)

上层工作流（Workflow）在发起盲审前，已提前完成 `./learnings/<phase_id>.md` 是否存在的逻辑判定，并向 `blind-reviewer` 显式透传参数：

- **若 `./learnings/<phase_id>.md` 存在** ➔ 工作流透传：
  - `default_standards: skills/<domain-skill>/references/*_reviewer_standards.md`
  - `learnings_file: ./learnings/<phase_id>.md`
  - *审稿人装载逻辑*：优先校验 `learnings_file` 中的项目专属偏好，同时加载 `default_standards` 及其同级引用的核心知识文件（`anti_patterns.md`、`golden_examples.md`、`style_definitions.md`）。
- **若 `./learnings/<phase_id>.md` 不存在** ➔ 工作流仅透传：
  - `default_standards: skills/<domain-skill>/references/*_reviewer_standards.md`
  - *审稿人装载逻辑*：仅装载技能默认标准及其引用的同级核心知识文件。

---

## 2. 盲审质检评估维度

盲审人 SubAgent 必须保持苛刻、客观、冷酷的审稿视角，逐项评估：
- **一票否决项 (Fatal Rejection Items)**：触发任意一票否决规则（如含有黑名单 AI 套话、语法标记残留、缺失必须组件等），直接判定为 `[REJECT]`。
- **排版与视觉体验 (UX & Readability)**：检查行文呼吸感、Emoji 密度、美学配色参数。
- **元指令与隐喻准确性**：检查是否遗留了元指令导语，或隐喻是否切题。

---

## 3. 标准裁决诊断输出格式

审稿人必须且仅能输出以下格式的结构化报告：

```markdown
### 🔍 盲审诊断报告 (Phase: <phase_id>)

**裁决结论**：[PASS / REJECT]
**综合品质得分**：XX / 100

#### 1. 扣分项与问题定位 (Only if REJECT)
- ❌ **[一票否决项 / 扣分维度]** (对应具体位置/句子)：具体原因说明。

#### 2. 结构化重写指导 (Actionable Revision Guide for Creator Agent)
1. **[修正指令 1]**：针对XX位置，删除/改写为...
2. **[修正指令 2]**：补充具体 Emoji / 转换卡片...
```
