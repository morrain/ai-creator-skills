---
name: to-wx
description: 将正文与正文插图转化为微信公众号移动端排版文章的 Skill。扫描主题工作区 (./<article-slug>/) 下的文章 Markdown 与插图配置，套用微信草稿防擦除原生视觉设计系统 (references/mp_style_design_system.md)，消除 Markdown 表格并重构为对比/步骤卡片，进行精准行内适度高亮与插图图注嵌合，自动生成归档单文件 mp_article.html。
---

# WeChat Official Account Article Converter Skill (`to-wx`)

本技能指导 AI Agent 读取主题工作区（`./<article-slug>/`）内的干货长文（`./<article-slug>/<article-slug>.md`）与正文插图方案（`assets/illustration_*.md` / `images/illustration_*.png`），针对微信公众号移动端视口进行格式解构与固定风格的高颜值视觉重构。

彻底消解 Markdown 原生表格，统一套用 **微信草稿防擦除原生视觉排版设计系统 (`references/mp_style_design_system.md`)**，注入科技蓝品牌色、字距行高留白系统、H2 标题胶囊挂件、双色对比卡片、步骤卡片、爆款金句框与居中图注组件。

经 **微信长文审稿 SubAgent (`mp_article_reviewer`)** 审查通过后，**生成并归档单文件 `mp_article.html`**。

---

## 核心设计原则 (Core Principles)

1. **单 HTML 文件离线归档 (Single HTML Archive)**：
   - 微信长文输出**必须且仅生成单个 `<article-slug>/mp_article.html` 文件**。
   - 文件内置 `677px` 桌面端居中预览盒子。用户在浏览器中双击打开、全选 (Cmd+A) 复制 (Cmd+C)，粘贴至微信公众号后台保存草稿，所有样式 100% 完美保留不被擦除。
2. **大标题剔除规则 (NO H1 Rule)**：
   - 正文 HTML 内容中**绝对不包含 H1 大标题**（微信公众号后台在头部专门框中独立填写标题）。
3. **原文绝对零增删改原则 (Zero Text Alteration Rule)**：
   - **文本 100% 忠实**：转换微信文章时，**绝对严禁添加、删除或改写原文的任何字词与句子**，绝对禁止擅自新增 AI 提炼总结卡片、额外解析或新增段落！
   - **纯行内样式高亮**：重点强化**必须且仅能通过 `<span style="...">` 标签精准包裹原文已有的字词或句子**，严禁任何文字修改。
4. **适度点睛高亮 (Moderate Highlighting Standard)**：
   - 保持克制与清爽，杜绝密密麻麻过度高亮导致的视觉疲劳。
   - 每个二级标题小节高亮控制在 **2~3 处**（核心概念用荧光浅黄标记笔或极光蓝胶囊，关键结论用橙色下划线，避坑点用警示胶囊）。
5. **Markdown 表格 100% 彻底消解 (Table Deconstruction)**：
   - 原生 `| col1 | col2 |` 表格在移动端体验极差，必须转换为 `🔴 痛点 / 🟢 优势` 双色浅底边框对比卡片或 `🚀 步骤解析卡片`。
6. **审稿人 SubAgent 审查闭环 (Reviewer SubAgent Loop)**：
   - 转换过程中**必须发起 `mp_article_reviewer` 审稿子进程**，读取并严格执行 `references/mp_reviewer_standards.md`。
   - 若审稿裁决为 `[REJECT]`，主创 Agent 必须根据诊断意见重写修正（最多循环 8 次），直至裁决为 `[PASS]`。

---

## 关联参考规范

在执行本技能时，Agent 必须主动读取并严格遵循以下文件：
- **微信固定视觉 UI 设计系统**：[`references/mp_style_design_system.md`](references/mp_style_design_system.md)
- **微信长文审稿标准**：[`references/mp_reviewer_standards.md`](references/mp_reviewer_standards.md)

---

## 详细执行步骤

### 步骤一：上下文扫描与内容提取

1. **定位主题工作区与输入文件**：
   - 确定主题 slug（`<article-slug>`）。读取 `./<article-slug>/<article-slug>.md` 长文全量内容。
2. **插图与落位锚点扫描**：
   - 扫描 `./<article-slug>/assets/` 目录，识别已归档的正文插图方案 `illustration_1.md` ~ `illustration_N.md`。
   - 检查对应的渲染图片路径：优先使用 `./<article-slug>/images/illustration_1.png` ~ `illustration_N.png`（若图片尚未生成，仍需保留插图卡片容器与占位说明，以便后续替换）。
3. **结构解析**：
   - 解析长文结构，标记全文中所有的 **Markdown 原生表格 (`| ... |`)**、**代码块 (Code Blocks)**、**引用/金句段落** 以及 **插图对应落位锚点**。

---

### 步骤二：强制套用微信组件库与排版重构

读取并应用 [`references/mp_style_design_system.md`](references/mp_style_design_system.md) 中的草稿安全 HTML 组件：

1. **全局文字与呼吸感排版**：
   - 全文段落：字号 `15px`，行高 `1.75`，字间距 `0.5px`，正文字色 `#333333`，单段控制在 `2-4 行`。
   - **剔除正文 H1 标题**。
2. **内联 HTML 组件转换**：
   - **二级标题 (H2)**：转为 `H2 蓝条居中胶囊挂件`：
     ```html
     <section style="text-align: center; margin: 30px auto 20px auto; line-height: 1.4;">
       <section style="display: inline-block; background-color: #EBF7FF; color: #10AEFF; font-size: 12px; font-weight: bold; padding: 2px 10px; border-radius: 10px; letter-spacing: 1px; line-height: 1.2;">SECTION 01</section>
       <section style="margin-top: 4px; text-align: center;">
         <section style="display: inline-block; font-size: 18px; font-weight: bold; color: #111827; border-bottom: 2.5px solid #10AEFF; padding-bottom: 4px; letter-spacing: 0.5px; line-height: 1.4;">
           一、 标题内容
         </section>
       </section>
     </section>
     ```
   - **三级标题 (H3)**：转为左侧靠左对齐 + 极光蓝立边：
     ```html
     <section style="border-left: 3.5px solid #10AEFF; padding-left: 10px; font-size: 16px; font-weight: bold; color: #111827; margin: 26px 0 14px 0; line-height: 1.5; text-align: left; letter-spacing: 0.5px;">
       1.1 三级小节标题
     </section>
     ```
   - **消解 Markdown 对比表格**：重构为 `🔴 痛点 / 🟢 优势` 双色浅底卡片：
     ```html
     <section style="margin: 24px 0;">
       <section style="background-color: #FFF5F5; border-left: 4px solid #FA5151; border-radius: 6px; padding: 12px 16px; margin-bottom: 12px;">
         <strong style="color: #FA5151; font-size: 15px;">🔴 传统模式痛点</strong>
         <p style="margin: 6px 0 0 0; font-size: 14px; color: #555555; line-height: 1.7;">内容描述...</p>
       </section>
       <section style="background-color: #F0F9F4; border-left: 4px solid #07C160; border-radius: 6px; padding: 12px 16px;">
         <strong style="color: #07C160; font-size: 15px;">🟢 新架构优势</strong>
         <p style="margin: 6px 0 0 0; font-size: 14px; color: #555555; line-height: 1.7;">内容描述...</p>
       </section>
     </section>
     ```
   - **消解流程表格/列表**：重构为 `🚀 步骤/流程解析卡片`。
   - **爆款金句**：重构为 `💡 金句总结` 暖金虚线边框卡片：
     ```html
     <section style="background-color: #FFF9F0; border: 1px dashed #FA9D3B; border-radius: 8px; padding: 14px 16px; margin: 24px 0; font-size: 15px; color: #664600; line-height: 1.75;">
       💡 <strong>金句总结：</strong>金句内容...
     </section>
     ```
   - **正文插图嵌合**：在对应锚点插入居中插图容器，带有斜体中文图注：
     ```html
     <section style="text-align: center; margin: 22px 0;">
       <img src="images/illustration_1.png" style="max-width: 100%; border-radius: 8px; vertical-align: middle;" />
       <section style="font-size: 13px; color: #888888; margin-top: 8px; font-style: italic; text-align: center;">
         💡 图 1：说明文字
       </section>
     </section>
     ```
   - **适度点睛高亮**：100% 保持原文文字不变，仅用 `<span style="...">` 标签行内包裹（每个 H2 小节 2~3 处）。
   - **结尾引导关注卡片**：文章末尾添加 `🔥 结尾互动与引导关注卡片`。

---

### 步骤三：触发 SubAgent 审稿闭环 (`mp_article_reviewer`)

1. **唤醒微信审查 SubAgent**：
   - **必须显式调用 `invoke_subagent` 工具**发起 `mp_article_reviewer` 审稿子进程，读取并严格执行 [`references/mp_reviewer_standards.md`](references/mp_reviewer_standards.md)。
2. **审稿维度检验**：
   - **表格零残留检测**：文章中是否有残留的 Markdown 原生表格？（一票否决）
   - **固定 UI 规范复用度**：H2 标题挂件、双色对比块、金句框与关注引导卡片是否完备？
   - **插图与图注**：图片是否带有居中显示与斜体图注？
   - **母版忠实度与零增删改**：是否完整保留了原文核心干货且没有篡改字句/没有擅自加提炼总结卡片？
3. **裁决与修正闭环**：
   - 若判定 **`[REJECT]`**：主创 Agent 根据诊断重写 HTML 草稿并重新送审（上限 8 次）。
   - 若判定 **`[PASS]`**：进入定稿归档环节。

---

### 步骤四：HTML 单文件导出与汇报

审稿通过后，生成包含 `677px` 预览框架的网页文档 **`./<article-slug>/mp_article.html`**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>微信公众号预览 - Article</title>
</head>
<body style="background-color: #F2F2F2; margin: 0; padding: 20px 0; font-family: -apple-system-font, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial, sans-serif;">
  <div style="max-width: 677px; margin: 0 auto; background-color: #FFFFFF; padding: 24px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-radius: 8px;">
    <!-- 微信排版正文内容 (不含 H1 大标题) -->
    ...
  </div>
</body>
</html>
```

向主人汇报归档状态：
```markdown
💡 微信公众号专用长文已完成审稿并归档！
- 网页文件：[./<article-slug>/mp_article.html](./<article-slug>/mp_article.html)

提示：双击打开 mp_article.html，全选 (Cmd+A) 复制 (Cmd+C)，直接粘贴进微信公众号后台即可，保存草稿样式 100% 不丢失！
```
