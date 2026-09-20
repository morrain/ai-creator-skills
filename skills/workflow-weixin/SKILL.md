---
name: workflow-weixin
command: /微信排版
description: 微信公众号富文本排版工作流。当用户发送 /微信排版 指令、/公众号排版 指令、或需要将 Markdown 文章转换为符合微信原生渲染规范的离线 HTML 时唤起。
---

# 📱 微信公众号排版业务编排 Skill (WeChat Workflow Skill)

本 Skill 为 `ai-creator-skills` 项目的微信公众号离线 HTML 排版与交付管道，负责读取 `./<article-slug>/` 下的正文与插图资产，调度原子技能 `wx-formatter` 套用微信原生视觉 UI 系统，运行 SubAgent 盲审，生成内置 677px 预览视口的原生 HTML 网页 `./<article-slug>/mp_article.html`。

---

## 核心设计原则

1. **大标题剔除规则 (NO H1 Rule)**：排版 HTML 中绝对剔除 H1 标题。
2. **原文绝对零增删改 (Zero Text Alteration Rule)**：绝对禁止修改原文任何话术。
3. **Markdown 表格 100% 彻底消解 (Table Deconstruction)**：原表格重构为 HTML 卡片。

---

## 阶段流程与 Reference 映射

详细步骤说明与卡片样式说明请参阅：
[references/stage_details.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-weixin/references/stage_details.md)

1. 读取正文与插图，调度 `wx-formatter` 转换为离线 HTML。
2. 唤起 `blind-reviewer` 审查零表格、零文案修改与草稿防擦除白名单。
3. 存盘 `./<article-slug>/mp_article.html` 并呈报可点击链接。
