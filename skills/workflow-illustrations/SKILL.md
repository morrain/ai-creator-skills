---
name: workflow-illustrations
command: /正文插图
description: 正文认知隐喻插图设计工作流。当用户发送 /正文插图 指令、/文章配图 指令、或需要为已生成的文章批量提炼隐喻插图与生成生图 Prompt 时唤起。
---

# 🎨 正文插图业务编排 Skill (Illustrations Workflow Skill)

本 Skill 为 `ai-creator-skills` 项目的正文插图归档与延时渲染管道，负责扫描工作区 `./<article-slug>/`，提取正文认知锚点，短路加载 IP Mascot 规范，调度原子技能 `illustration-designer` 生成配置文件与 Prompt，盲审后落盘至 `assets/illustration_N.md`，并在指令下按需生图。

---

## 核心设计原则

1. **按需延时生图 (Strict Lazy Generation)**：默认仅生成 Markdown 配置文件，除非用户明确给出“开始生图”指令，否则严禁自动生图。
2. **IP 形象前置短路路由**：依次检索主题级 ➔ 项目级 ➔ 默认级 `character_ip.md`。
3. **代码块图表强制插画化**：Markdown 代码块图表（```mermaid、```text 等）强制转换为认知隐喻插画以供替换。
4. **全文上下文通读与深层机制提炼**：在提炼认知锚点与设计插图前，必须通读全文背景，透彻理解文章深层逻辑与核心矛盾，严禁仅凭孤立段落或单句字面意思设计插图。

---

## 阶段流程与 Reference 映射

详细规程与步骤细节请参阅：
[references/stage_details.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-illustrations/references/stage_details.md)

1. **阶段一（配置生成与盲审）**：读取文章与 IP 规范，提炼认知锚点，调度 `illustration-designer`，盲审落盘 `assets/illustration_N.md`，呈报列表。
2. **阶段二（按需生图）**：用户回复“开始生图”后，提取英文 Prompt 并调用 `generate_image` 保存图片至 `images/illustration_N.png`。
