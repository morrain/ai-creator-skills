---
name: workflow-article
command: /写文章
description: 深入探讨类长文写作工作流。当用户发送 /写文章 指令、/长文 指令、要求基于知识主题或参考资料撰写深度文章、或进行长文创作时唤起。
---

# 📝 文章创作业务编排 Skill (Article Workflow Skill)

本 Skill 为 `ai-creator-skills` 项目的核心文章创作管道，负责接收选题，执行强制联网检索，管理 `./<article-slug>/` 工作区，调度原子技能 `article-writer` 和 `cover-designer`，并运行多阶段 SubAgent 盲审闭环与人工批准卡点。

---

## 核心设计原则

1. **强制互联网前置检索 Protocol**：在拟定任何大纲前，必须优先显式调用 `search_web` 工具检索最新技术事实，严禁闭门造车。
2. **三阶段交互与人工卡点 (Three-Stage Human Gate)**：
   - 阶段一（大纲阶段）：拟定大纲草案 ➔ SubAgent 盲审 ➔ 落盘 `outline.md` ➔ **暂停等待用户确认 [通过/修改]**。
   - 阶段二（正文阶段）：重读 `outline.md` ➔ 展开正文 ➔ SubAgent 盲审 ➔ 落盘 `<article-slug>.md` ➔ **暂停等待用户确认 [通过/设计封面]**。
   - 阶段三（封面阶段）：重读正文定稿 ➔ 调度 `cover-designer` ➔ 落盘 `assets/cover.md` ➔ **按需触发 `generate_image` 生图**。
3. **磁盘文件最高事实源**：每次切入新阶段前，强制显式调用 `view_file` 重新读取磁盘上的源文件，绝不复用 Memory 缓存。

---

## 阶段流程与 Reference 映射

详细步骤说明、SubAgent 盲审规程与人工确认提示词请参阅：
[references/stage_details.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-article/references/stage_details.md)

1. **阶段一（大纲）**：调用 `search_web`，使用 `article-writer` (mode: outline) 拟定大纲，盲审通过后存盘 `./<article-slug>/outline.md`，呈现全量原文，**暂停等待确认**。
2. **阶段二（正文）**：使用 `view_file` 重新读取磁盘 `outline.md`，使用 `article-writer` (mode: full_article) 展开正文，盲审通过后存盘 `./<article-slug>/<article-slug>.md`，**暂停等待确认**。
3. **阶段三（封面）**：使用 `view_file` 重新读取磁盘 `<article-slug>.md`，调度 `cover-designer` 导出 `./<article-slug>/assets/cover.md`。当用户指示 `[渲染封面]` 时调用 `generate_image` 生图。
