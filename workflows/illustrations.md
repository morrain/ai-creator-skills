---
name: workflow-illustrations
command: /正文插图
description: 正文认知隐喻插图设计工作流。当用户发送 /文章配图 指令、或需要为已生成的文章批量提炼隐喻插图与生成生图 Prompt 时唤起。
---

# 🎨 正文插图业务工作流 (Illustrations Business Workflow)

本工作流为 `ai-creator-skills` 项目的正文插图归档与延时渲染管道。负责扫描主题工作区 `./<article-slug>/`，提取正文认知锚点，短路加载 IP Mascot 规范，调度底层原子技能 `illustration-designer` 为每张插图生成 Markdown 配置文件与双语 Prompt，经 SubAgent 盲审通过后落盘至 `assets/illustration_N.md`，并在明确指令下懒加载渲染图片至 `images/illustration_N.png`。

---

## 核心设计原则 (Core Principles)

1. **配置文件先行与按需延时生图 (Strict Lazy Generation)**：
   - 默认**仅生成插图 Markdown 配置文件**（`assets/illustration_1.md` ~ `illustration_N.md`）。
   - **严禁自动调用 `generate_image` 工具**生图，除非用户明确给出“开始生图/生成图片”指令。
2. **IP 形象前置短路路由 (Short-Circuit IP Mascot Routing)**：
   - 按优先级显式检查且仅加载 1 份 IP 规范（统一文件名为 `character_ip.md`）：
     1. 主题级：`./<article-slug>/character_ip.md`
     2. 项目级：`./character_ip.md`
     3. 默认级：`skills/illustration-designer/references/character_ip.md`
   - 命中即止，拦截下位文件。
3. **磁盘文件最高事实源与正文前置读取 (Disk Source of Truth Protocol)**：
   - **设计插画前，强制阅读正文源文件**：Agent 在提炼认知锚点与设计插画前，**必须首先强制显式调用 `view_file` 重新读取磁盘上的正文源文件 `./<article-slug>/<article-slug>.md`**。

---

## 详细工作流步骤

### 阶段一：正文消化、插图配置生成、SubAgent 盲审与汇报

1. **定位工作区与扫描文章**：
   - 读取目标 `./<article-slug>/<article-slug>.md`。确认 `./<article-slug>/assets/` 目录存在。
2. **短路加载 IP 规范**：
   - 按 `主题级 ➔ 全局级 ➔ 原子技能默认级` 的顺序装载 1 份 IP 描述。
3. **提取认知锚点与调度原子 Skill**：
   - 提炼 4-8 个核心认知锚点。
   - 对每一张拟设计的插图（`N = 1, 2, ...`），调度原子技能 `illustration-designer` 生成单图画风构图与双语 Prompt。
4. **逐张落盘与 SubAgent 盲审**：
   - 将方案落盘为 `./<article-slug>/assets/illustration_N.md`。
   - 检查项目根目录是否存在项目进化规则 `./learnings/illustrations.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/illustration-designer/references/illustration_reviewer_standards.md` 与 `learnings_file: ./learnings/illustrations.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards: skills/illustration-designer/references/illustration_reviewer_standards.md`）。若裁决 `[REJECT]`，修正重写直至 `[PASS]`（上限 5 次）。
5. **结构化呈报结果与人工确认提示**：
   - 输出插图配置列表与可点击 Markdown 链接。
   - **统一人工确认提示**：
     > 💡 **主编审阅与自进化提示**：
     > 1. 预览配置文件（或在编辑器中修饰后），请在对话框回复 **“开始生图”** 以渲染图片。
     > 2. 如对插图提示词进行了人工修改，请在对话框回复 **`/workflow-learn`**，系统将自动归纳最近一轮意见供您勾选落盘！

---

### 阶段二：按需生图与 QA 审查交付 (Lazy Generation)

**当且仅当用户给出“开始生图”等显式指令时触发**：
1. 确认 `./<article-slug>/images/` 目录存在。
2. 遍历 `./<article-slug>/assets/illustration_1.md` ~ `illustration_N.md` 提取 `🟢 英文生图版 Prompt`。
3. 调用 `generate_image` 工具渲染 16:9 图片，保存至 `./<article-slug>/images/illustration_N.png`。
