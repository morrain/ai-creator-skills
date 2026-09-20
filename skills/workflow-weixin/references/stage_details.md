# 📱 微信公众号排版业务编排 - 阶段规程与细节

## 核心原则

1. **大标题剔除规则 (NO H1 Rule)**：正文中绝对不包含 H1 大标题。
2. **原文绝对零增删改 (Zero Text Alteration Rule)**：绝对禁止增删改原文字句。
3. **Markdown 表格 100% 彻底消解 (Table Deconstruction)**：表格一律重构为 HTML 卡片。

---

## 详细步骤

1. **定位工作区与读取资产**：读取 target `<article-slug>.md` 与 `assets/illustration_*.md`。
2. **调度原子技能 `wx-formatter`**：
   - 套用居中 H2 胶囊角标、左立边 H3、`💡 金句总结` 暖金虚线边框卡片及居中插图容器（嵌合 `images/illustration_N.<ext>`，动态适应后缀）。
   - 在最末尾嵌入 `🔥 结尾互动与引导关注卡片`（组件 7）。
3. **SubAgent 盲审闭环**：
   - 检查并读取 `./learnings/weixin.md`（若存在）或默认规程 `skills/wx-formatter/references/mp_reviewer_standards.md`。
   - 校验零表格、零增删改、草稿防擦除白名单属性。重构直至 `[PASS]`。
4. **存盘与交付**：
   - 写入 `./<article-slug>/mp_article.html`。
   - 呈报链接，提醒防限流注意事项并提示可使用 `/workflow-learn` 沉淀偏好。
