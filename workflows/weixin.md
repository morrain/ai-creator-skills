---
name: workflow-weixin
command: /微信公众号
description: 微信公众号富文本排版工作流。当用户发送 /公众号排版 指令、或需要将 Markdown 文章转换为符合微信原生渲染规范的离线 HTML 时唤起。
---

# 📱 微信公众号排版业务工作流 (WeChat Business Workflow)

本工作流为 `ai-creator-skills` 项目的微信公众号离线 HTML 排版与交付管道。负责扫描主题工作区 `./<article-slug>/`，读取正文 Markdown 与插图资产，调度底层原子技能 `wx-formatter` 套用微信草稿防擦除原生视觉 UI 系统（`references/mp_style_design_system.md`），运行 SubAgent 审稿闭环，并在 `./<article-slug>/mp_article.html` 生成内置 677px 预览视口的原生网页。

---

## 核心设计原则 (Core Principles)

1. **大标题剔除规则 (NO H1 Rule)**：正文中绝对不包含 H1 大标题。
2. **原文绝对零增删改 (Zero Text Alteration Rule)**：绝对禁止增加、删除或修改原文的任何话术与字句，严禁擅自插入 AI 总结卡片。
3. **Markdown 表格 100% 彻底消解 (Table Deconstruction)**：原表格语法一律重构为双色 HTML 边框卡片或步骤解析卡片。

---

## 详细工作流步骤

1. **定位工作区与读取资产**：
   - 读取目标 `./<article-slug>/<article-slug>.md` 原文及 `./<article-slug>/assets/illustration_*.md` 方案文件。
2. **调度原子技能 `wx-formatter` 格式化重构**：
   - 检查 `./<article-slug>/assets/cover.md` 是否存在。若不存在或需更新，自动调度原子技能 `name: cover-designer`（`platform: weixin`），提炼微信公众号 2.35:1 爆款头图封面方案，落盘至统一资产文件 `./<article-slug>/assets/cover.md`。
   - 调度原子技能 `wx-formatter`，将正文消解表格后套用居中 H2 胶囊角标、左立边 H3、**`💡 金句总结` 暖金虚线边框卡片**及居中插图容器（按 `illustration_N` 主干匹配识别 `./<article-slug>/images/` 下实际存在的图片，嵌合 `images/illustration_N.<ext>`，动态自适应 `.png` / `.jpg` / `.jpeg` / `.webp` 等后缀），并在文章最末尾嵌入 `🔥 结尾互动与引导关注卡片`（组件 7）。
3. **SubAgent 盲审闭环**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/weixin.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/wx-formatter/references/mp_reviewer_standards.md` 与 `learnings_file: ./learnings/weixin.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards: skills/wx-formatter/references/mp_reviewer_standards.md`）。苛刻校验零表格残留、零字句改动、草稿防擦除白名单属性与结尾互动卡片。
   - 若判定 `[REJECT]`，针对性重构至 `[PASS]`（上限 8 次）。
4. **离线 HTML 存盘交付与人工确认提示**：
   - 将通过盲审的完整 HTML 代码写入固定文件 `./<article-slug>/mp_article.html`。
   - 呈报完成信息与本地点击查看链接（如 [`./<article-slug>/mp_article.html`](./<article-slug>/mp_article.html)）。
   - **统一人工确认提示**：
     > 💡 **主编审阅与自进化提示**：
     > 1. 您可在浏览器或编辑器中预览并微调 HTML 网页排版。
     > 2. 🚨 **防限流提醒**：发文前请确认正文中已融入独家信息增量（如实测体验/反直觉洞察/降维比喻，避免纯 AI 通稿摘要导致平台判定为低创作度内容并限流）。
     > 3. 如对本次生成的 CSS 样式或卡片元素进行了人工修正，请在对话框回复 **`/workflow-learn`**，系统将自动提炼您的微信排版偏好并沉淀落盘，让后续盲审标准自动进化！
