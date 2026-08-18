---
name: illustration-designer
description: 单图认知隐喻与生图 Prompt 设计技能。当需要将正文段落转化为结合 IP Mascot 的 16:9 手绘隐喻图 Prompt 与图注时调用。
---

# Illustration Designer Skill (纯粹插图视觉隐喻设计技能)

本技能为 **纯粹无状态的原子视觉设计技能**。指导 AI Agent 分析传入的“单个段落或认知锚点”，提炼物理动作与怪诞低科技物件，输出单张配图的说明、中文确认版 Prompt 与 16:9 英文生图版 Prompt。

---

## 核心设计原则 (Core Principles)

1. **单点输入与无状态设计 (Stateless Single-Illustration Output)**：
   - 技能接收单点认知锚点或段落说明。
   - 只专注为单张配图设计画质构图、IP Mascot 动作与双语 Prompt，零主题工作区存盘与文件目录依赖。
2. **IP 形象短路路由 (Short-Circuit IP Mascot Routing)**：
   - 按优先级检查并加载 1 份 IP 规范：1) 主题级 `./<article-slug>/character_ip.md` ➔ 2) 项目级 `./character_ip.md` ➔ 3) 默认技能级 [`references/character_ip.md`](references/character_ip.md)。
3. **怪诞手绘与原生中文批注法则**：
   - 16:9 横版构图、纯白背景（`#FFFFFF`）、黑色手绘细线稿。
   - 英文 Prompt 中手写批注词强制在双引号 `""` 或单引号 `'...'` 内部保留原生中文。
4. **流程图/架构图代码块插画化法则 (Diagram Code Block Illustration Rule)**：
   - 当认知锚点包含 Markdown 代码块（```mermaid、```text、```ascii 等）描述的流程图、架构图或拓扑关系时，**强制将其转化为视觉手绘插画**。设计时必须将代码块中的节点层级、逻辑流转与核心实体解构为 IP Mascot 动作与具象隐喻，用于后续替代代码块展示。

---

## 关联参考规范

在执行视觉设计时，主动读取以下参考规范：
- [`references/character_ip.md`](references/character_ip.md)：IP Mascot 视觉形象（支持短路路由加载自定义 IP，默认小智）定义、姿态与动作池。
- [`references/composition-patterns.md`](references/composition-patterns.md)：8 种构图模式与原创隐喻推演法。
- [`references/prompt-template.md`](references/prompt-template.md)：标准 16:9 英文生图 Prompt 模板。
- [`references/style-dna.md`](references/style-dna.md)：视觉 DNA 与绝对禁忌。
- [`references/illustration_reviewer_standards.md`](references/illustration_reviewer_standards.md)：审稿标准。

---

## 规范输出格式

生成单张插图的 Markdown 结构：

```markdown
# 插图：[插图标题/核心隐喻简述]

## 插图元数据
- **核心认知锚点**：[简述该插图表达的核心物理机制/逻辑转折]

## 🔵 中文确认版 Prompt & 视觉方案设计
- **画面构图与核心视觉**：[16:9 横版，纯白背景，黑色手绘线条... 描绘 IP Mascot 动作与低科技物件]
- **手写中文批注**：`"批注1"`、`"批注2"`、`"批注3"`

## 🟢 英文生图版 Prompt (Image Generation Prompt)
```text
A 16:9 minimalist hand-drawn illustration on a clean pure white background with black line art...
```
```
