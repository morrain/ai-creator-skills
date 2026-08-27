---
name: workflow-article
command: /写文章
description: 深入探讨类长文写作工作流。当用户发送 /长文 指令、要求基于知识主题或参考资料撰写深度文章、或进行长文创作时唤起。
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
2. **磁盘文件最高事实源与强制重新读取 (Disk Single Source of Truth Gate)**：
   - 在进入阶段二生成完整正文前，Agent **必须首先强制显式调用 `view_file` 重新读取磁盘上的大纲源文件 `./<article-slug>/outline.md`**。
   - **绝对禁止复用对话内存中的大纲旧缓存**，确保完整吸收主编在外部编辑器中对大纲进行的手工修饰与结构微调。
3. **主题工作区规范**：
   - 提取 H1 标题对应的英文连字符 Slug（`<article-slug>`），全量资产落盘在项目根目录 `./<article-slug>/` 下。

---

## 详细工作流步骤

### 阶段一：前置检索、大纲拟定、SubAgent 盲审、落盘归档与人工卡点

1. **联网事实检索与输入解析**：
   - 解析输入的 `title` / `summary` 或关键词。
   - **显式调用 `search_web` 工具**对主题进行多角度实时检索，收集最新事实。
2. **调度原子技能 `article-writer` 智能识别文风并拟定大纲**：
   - 调度原子技能 `article-writer`（模式 `mode: outline`），基于检索到的事实与主题属性**自适应识别最佳文风**（干货指南/科技深度评论/社会观察/科普解说/故事叙事），生成 3 个爆款备选 H1 标题及带有 `【撰写指令】` 的大纲草案。
3. **SubAgent 大纲盲审闭环**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/article_outline.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/article-writer/references/reviewer_standards.md` 与 `learnings_file: ./learnings/article_outline.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards: skills/article-writer/references/reviewer_standards.md`）。
   - 若结论为 `[REJECT]`，针对性修正大纲草案直至 `[PASS]`（上限 8 次）。
4. **创建主题工作区与强制落盘归档**：
   - 大纲 `[PASS]` 后，在根目录下新建 `./<article-slug>/` 目录。
   - **前置归档**：将盲审通过的大纲全量原文存盘为固定的 `./<article-slug>/outline.md`。
5. **全量呈报原文与人工 Gate 卡点**：
   - **100% 完整呈报** `outline.md` 原文（附链接 [`./<article-slug>/outline.md`](./<article-slug>/outline.md)），禁止截断。
   - **暂停并等待与统一人工确认提示**：
     > 💡 **主编审阅与自进化提示**：
     > 1. 大纲满意请回复 **`[通过]`** 或 **`[继续]`**，系统将自动开始写作完整正文。
     > 2. 如对大纲进行了人工修饰或提供了调整批注，请在对话框回复 **`/workflow-learn`**，系统将自动提炼您的大纲偏好规则并沉淀落盘，让后续大纲盲审标准自动进化！

---

### 阶段二：定稿读取、正文展开、SubAgent 盲审与正文交付

1. **强制重新读取大纲源文件 (Disk Pre-Read Gate)**：
   - 用户批准后，Agent **必须首先显式调用 `view_file` 重新读取磁盘上的 `./<article-slug>/outline.md` 文件**（以磁盘最新文件内容为唯一事实源，绝对禁止复用 Memory 里的旧大纲缓存，确保完整包含主编在编辑器中修改的大纲字句）。
2. **调度原子技能 `article-writer` 展开正文**：
   - 调度 `article-writer`（模式 `mode: full_article`），将 `【撰写指令】` 转化为行文推导与爆款金句，应用呼吸感排版（单段 2-4 行）与富 Markdown 组件（引用卡片、列表、加粗）。
3. **SubAgent 正文盲审闭环**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/article_content.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/article-writer/references/reviewer_standards.md` 与 `learnings_file: ./learnings/article_content.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards: skills/article-writer/references/reviewer_standards.md`）。
   - 若打回，修正草稿直至 `[PASS]`（上限 8 次）。
4. **纯净 Markdown 落盘交付与封面提炼**：
   - 中英文排版自动加空格处理。
   - 最终正文存盘至 `./<article-slug>/<article-slug>.md`。
   - **自动调度 `cover-designer` 提炼封面**：调度原子技能 `cover-designer`，从文章核心观点与金句中提炼带有 10-14字爆款痛点 Hook 标题、评论区引导标记与 2D 物理隐喻的封面方案，落盘至 `./<article-slug>/assets/cover.md`。
5. **呈报成果与人工审阅卡点提示**：
   - 呈报正文完成信息及本地查看链接（[`./<article-slug>/<article-slug>.md`](./<article-slug>/<article-slug>.md) 与 [`./<article-slug>/assets/cover.md`](./<article-slug>/assets/cover.md)）。
   - **统一人工确认提示**：
     > 💡 **主编审阅与自进化提示**：
     > 1. 您可在编辑器中查看并修饰正文内容。
     > 2. 如对本次生成的字句或排版进行了人工精修，请在对话框回复 **`/workflow-learn`**，系统将自动提炼您的偏好规则并沉淀落盘，让后续盲审标准自动进化！
