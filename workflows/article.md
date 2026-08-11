---
name: workflow-article
command: /写文章
description: 文章创作业务工作流。负责前置联网检索、主题工作区管理、调度 article-writer 拟定大纲与展开正文、两阶段人工卡点与 SubAgent 盲审闭环。
---

# 📝 文章创作业务工作流 (Article Business Workflow)

本工作流为 `ai-creator-skills` 项目的核心文章创作管道。负责接收选题（来自 `hot-topics` 的 `TopicItem` 或用户主题），执行强制互联网前置检索，管理主题工作区 `./<article-slug>/` 目录结构，调度底层原子技能 `article-writer`，以及运行多阶段 SubAgent 审稿闭环与人工批准卡点。

---

## 核心设计原则 (Core Principles)

0. **强制互联网前置检索 Protocol (Mandatory Web Search)**：
   - 在拟定任何大纲前，**必须优先显式调用 `search_web` 工具**检索最新技术事实、行业动态与 API 现状，严禁闭门造车。
1. **两阶段交互与人工卡点 (Two-Stage Human Gate)**：
   - **阶段一**：基于搜索事实由原子 Skill `article-writer` 拟定大纲草案，经 SubAgent 盲审后归档至 `./<article-slug>/outline.md`，呈现全量原文给用户，**显式暂停并卡点等待用户回复 `[通过/修改]`**。
   - **阶段二**：用户确认后，读取 `./<article-slug>/outline.md` 定稿，由原子 Skill `article-writer` 展开纯 Markdown 正文，经 SubAgent 盲审通过后存盘至 `./<article-slug>/<article-slug>.md`。
2. **主题工作区规范 (ADR-0001)**：
   - 提取 H1 标题对应的英文连字符 Slug（`<article-slug>`），全量资产落盘在项目根目录 `./<article-slug>/` 下。

---

## 详细工作流步骤

### 阶段一：前置检索、大纲拟定、SubAgent 盲审、落盘归档与人工卡点

1. **联网事实检索与输入解析**：
   - 解析输入的 `title` / `summary` 或关键词。
   - **显式调用 `search_web` 工具**对主题进行多角度实时检索，收集最新事实。
2. **调度原子技能 `article-writer` 智能识别文风并拟定大纲**：
   - 调度原子技能 `article-writer`（模式 `mode: outline`），基于检索到的事实与主题属性**自适应识别最佳文风**（干货指南/科技深度评论/社会观察/科普解说/故事叙事），生成 3 个备选 H1 标题（每个 ≤ 20 字）及带有 `【撰写指令】` 的大纲草案。
3. **SubAgent 大纲盲审闭环**：
   - 显式调用 `invoke_subagent` 发起 `article_reviewer` 子进程，读取并执行 `skills/article-writer/references/reviewer_standards.md`。
   - 若结论为 `[REJECT]`，针对性修正大纲草案直至 `[PASS]`（上限 8 次）。
4. **创建主题工作区与强制落盘归档**：
   - 大纲 `[PASS]` 后，在根目录下新建 `./<article-slug>/` 目录。
   - **前置归档**：将盲审通过的大纲全量原文存盘为固定的 `./<article-slug>/outline.md`。
5. **全量呈报原文与人工 Gate 卡点**：
   - **100% 完整呈报** `outline.md` 原文（附链接 [`./<article-slug>/outline.md`](./<article-slug>/outline.md)），禁止截断。
   - **暂停并等待**：明确提示用户可在编辑器中查看或修改，等待用户回复 `[通过/继续]` 或修改意见。

---

### 阶段二：定稿读取、正文展开、SubAgent 盲审与正文交付

1. **读取归档大纲定稿**：
   - 用户批准后，直接读取 `./<article-slug>/outline.md` 文件（以文件实际内容为准）。
2. **调度原子技能 `article-writer` 展开正文**：
   - 调度 `article-writer`（模式 `mode: full_article`），将 `【撰写指令】` 转化为行文推导与爆款金句，应用呼吸感排版（单段 2-4 行）与富 Markdown 组件（引用卡片、列表、加粗、对比表格）。
3. **SubAgent 正文盲审闭环**：
   - 显式调用 `invoke_subagent` 发起 `article_reviewer` 子进程，读取并执行 `skills/article-writer/references/reviewer_standards.md` 进行盲审（反 AI 味、干货度、代码注释、富排版、元指令隔离）。
   - 若打回，修正草稿直至 `[PASS]`（上限 8 次）。
4. **纯净 Markdown 落盘交付**：
   - 中英文排版自动加空格处理。
   - 最终正文存盘至 `./<article-slug>/<article-slug>.md`。
