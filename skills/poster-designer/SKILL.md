---
name: poster-designer
description: 纯粹的单张手绘海报设计与 Prompt 生成原子技能。接收单点知识文本与指定版式要求，结合 IP Mascot 动态姿态（支持短路路由加载自定义 IP，默认小智）与 10 大经典海报版式库 (references/layouts.md)，输出包含了暖米白纸张 (#FAF6F0)、莫兰迪粉彩配色、3:4 比例、单引号原生中文与去乱码指令的单张海报 Markdown 配置文件。不依赖特定项目路径。
---

# Poster Designer Skill (`poster-designer`)

本技能为 **纯粹无状态的原子海报设计技能**。指导 AI Agent 接收输入的单点知识文本、指定版式类型（从 10 大经典版式中选一），组合 2-4 个莫兰迪手绘组件与 IP Mascot 动作，输出单张海报的中文确认版方案与 3:4 英文生图版 Prompt。

---

## 核心设计原则 (Core Principles)

1. **单点输入与无状态设计 (Stateless Single Poster Design)**：
   - 技能接收单点知识文本与版式要求。
   - 只专注为单张海报设计构图、手绘组件组合与双语 Prompt，零组图拆分逻辑与社媒文案依赖。
2. **防乱码指令与原生中文强留法则**：
   - Prompt 中必须写入去乱码指令：`strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes`。
   - 要求渲染在海报上的核心标题/文案必须在单引号 `'...'` 内部保留原生中文。
3. **美学与 3:4 比例**：
   - 暖米白羊膏纸背景（`#FAF6F0`）、莫兰迪粉彩配色（`#7B92A7`, `#E89C7D`, `#8FA89B`）、黑色细勾线，宽高比 `--ar 3:4`。

---

## 关联参考规范

在执行海报设计时，主动读取以下参考规范：
- [`references/layouts.md`](references/layouts.md)：10 大经典海报版式与 Prompt 模板。
- [`references/style_guide.md`](references/style_guide.md)：莫兰迪 3:4 手绘视觉风格指南。
- [`references/character_ip.md`](references/character_ip.md)：IP Mascot 规范（支持短路路由加载自定义 IP，默认小智）。
- [`references/poster_reviewer_standards.md`](references/poster_reviewer_standards.md)：海报审查 SubAgent 标准。

---

## 规范输出格式

生成单张海报的 Markdown 配置文件结构：

```markdown
# 海报 [编号]：[核心主题/版式名称]

## 卡片元数据
- **海报版式类型**：[10 大版式名称，如：四宫格干货版]
- **核心认知焦点**：[该海报承载的核心干货]

## 🔵 中文确认版 Prompt & 视觉卡片设计
- **卡片版式与手绘组件**：[3:4 比例，暖米白背景 `#FAF6F0`... 详细描述莫兰迪卡片组件与 IP Mascot 动作]
- **渲染文本**：`'标题文案'`、`'核心观点卡片'`

## 🟢 英文生图版 Prompt (Image Generation Prompt)
```text
Hand-drawn infographic poster, warm off-white cream paper texture (#FAF6F0), Morandi color palette... 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.
```
```
