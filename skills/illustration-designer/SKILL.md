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
3. **画面精准表意与手写批注极简法则 (Visual Design Speaks & Minimal Annotation Rule)**：
   - 16:9 横版构图、纯白背景（`#FFFFFF`）、黑色手绘细线稿。画面构图、IP Mascot 物理动作与结构拓扑必须精准呈现原文核心逻辑与概念转折。
   - **尽量不使用手写批注/文字注释**：摒弃在画面节点/物件旁机械悬挂说明文字的做法，保持画面干净自解释；仅在视觉确实无法消除专业名词或数值歧义时，才允许保留 1-2 处极简字眼（英文 Prompt 中强制在双引号 `""` 或单引号 `'...'` 内部保留原生中文）。
4. **流程图/架构图代码块插画化法则 (Diagram Code Block Illustration Rule)**：
   - 当认知锚点包含 Markdown 代码块（```mermaid、```text、```ascii 等）描述的流程图、架构图或拓扑关系时，**强制将其转化为视觉手绘插画**。设计时必须将代码块中的节点层级、逻辑流转与核心实体解构为 IP Mascot 动作与具象手绘结构，用于后续替代代码块展示。
5. **深层本质机制理解与反字面直译法则 (Deep Essence & Anti-Literal Rule)**：
   - 必须深入解构输入锚点/段落背后的**本质物理机制、逻辑矛盾或认知转折**。若处于工作流且提供有全文上下文，需结合全文综合理解；若仅传入单一认知锚点或孤立段落，也必须透彻解构该概念背后的本质逻辑与底层机制，**严禁凭孤立词汇进行字面直译**（例如：看到“苹果”就画水果苹果、看到“防擦除”就画橡皮擦、看到“数据管道”就画水管）。插图视觉方案必须精准表达概念或全文语境下的真实底层机制。
6. **提示词视觉具象丰满法则 (Concrete Visual Detail & Rich Prompt Rule)**：
   - 严禁混淆“画面呈现极简手绘风格”与“提示词描述简单空洞”。英文生图提示词（`prompt_en`）必须具备极高的**视觉具象描写**。必须详尽描写：1) 明确的空间构图（左中右分布、空间视角）；2) 具体的低科技道具材质与结构细节（如“带手摇把的复古木箱、生锈的铁漏斗与纸片卡槽”，而非笼统写“机器”）；3) IP Mascot 的精确身体倾角、双手动作与 deadpan 面部表情；4) 箭头/线缆流动与物理交互的具体细节。严禁使用一两句抽象概括充数（如严禁仅写 "Xiao Zhi operates a machine"）。

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
# 插图：[插图标题/核心概念简述]

## 插图元数据
- **核心认知锚点**：[简述该插图表达的核心物理机制/逻辑转折]
- **深层本质机制说明**：[描述插图如何承载概念/全文的深层底层逻辑机制，而非机械直译字面词汇]

## 🔵 中文确认版 Prompt & 视觉方案设计
- **画面构图与核心视觉**：[16:9 横版，纯白背景，黑色手绘线条... 描绘精准呈现原文逻辑的构图、IP Mascot 动作与低科技物件]
- **手写中文批注**：[尽量不上字，默认为空；仅在图形无法消除歧义时保留 1-2 处极简字眼，如 `"v2.0"`]

## 🟢 英文生图版 Prompt (Image Generation Prompt)
```text
A 16:9 minimalist hand-drawn illustration on a clean pure white background with black line art...
```
```
