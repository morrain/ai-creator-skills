---
name: wx-formatter
description: 微信公众号原生 HTML 排版转换技能。当需要将 Markdown 文章转换为符合微信防擦除原生视觉 UI 规范的离线 HTML 时调用。
---

# WeChat Off-line HTML Formatter Skill (`wx-formatter`)

本技能为 **纯粹无状态的原子格式化排版技能**。指导 AI Agent 接收输入的文本或 Markdown 文件，解构原生 Markdown 表格，套用微信草稿防擦除原生视觉排版设计系统，输出内嵌 `677px` 预览视口的原生 HTML 网页。

---

## 核心设计原则 (Core Principles)

1. **纯粹无状态格式转换 (Stateless HTML Conversion)**：
   - 技能接收输入 Markdown 文本内容或具体目标文件。只专注执行格式排版与内联样式注入，返回排版好的 HTML 字符串或保存至参数指定的位置。
2. **大标题剔除规则 (NO H1 Rule)**：
   - 输出的正文 HTML 内容中**绝对不包含 H1 大标题**（公众号后台在头部专门框中独立填写标题）。
3. **原文绝对零增删改原则 (Zero Text Alteration Rule)**：
   - 绝对严禁添加、删除或改写原文正文的任何字词与句子，严禁擅自新增 AI 提炼总结卡片。高亮仅通过草稿安全的 `<span style="...">` 行内包裹原文已有词句（每个 H2 小节 2~3 处）。
4. **Markdown 表格 100% 彻底消解 (Table Deconstruction)**：
   - 原生 `| col1 | col2 |` 表格重构为 `🔴 痛点 / 🟢 优势` 双色卡片或 `🚀 步骤解析卡片`。
5. **金句总结卡片弹性适配法则 (Flexible Golden Quote Card Standard)**：
   - 当原文包含金句总结或结尾提炼时，使用设计系统组件 5（`#FFF9F0` 浅黄底 + `1px dashed #FA9D3B` 虚线边框）进行美化装扮；若原文未包含总结，严禁擅自造词硬塞。
6. **结尾互动与引导关注卡片无指纹法则 (No-AIGC-Fingerprint Engagement Card Standard)**：
   - 在正文最末尾嵌入设计系统 (`references/mp_style_design_system.md`) 组件 7（`🔥 结尾互动与引导关注卡片`）。
   - ❌ **硬性禁止**：卡片内部严禁出现“本文由 Agent 排版”、“ai-creator-skills 自动化工具生成”等明文 AIGC 指纹词汇或机械引流套话。文案必须自然结合文章主题进行互动发问（如：“对此你有何看法？欢迎在评论区留言交流...”），消除平台 AIGC 审查与同质化风险。
7. **插图文件名主干匹配与后缀自适应 (Dynamic Image Format Resolution)**：
   - 在为正文嵌入插画图片时，严禁写死固定的 `.png` 扩展名。应按主干文件名 `illustration_N` 匹配扫描 `./<article-slug>/images/` 目录下实际存在的图片文件，识别并适配实际后缀（如 `.png`、`.jpg`、`.jpeg`、`.webp` 等），填入 `<img src="images/illustration_N.<ext>" ... />`。

---

## 关联参考规范

在执行排版转换时，主动读取以下参考规范：
- **微信固定视觉 UI 设计系统**：[`references/mp_style_design_system.md`](references/mp_style_design_system.md)
- **微信长文审稿标准**：[`references/mp_reviewer_standards.md`](references/mp_reviewer_standards.md)

---

## 规范 HTML 输出结构

输出带 `677px` 桌面预览容器的原生离线 HTML：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>微信公众号预览</title>
</head>
<body style="background-color: #F2F2F2; margin: 0; padding: 20px 0; font-family: -apple-system-font, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial, sans-serif;">
  <div style="max-width: 677px; margin: 0 auto; background-color: #FFFFFF; padding: 24px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-radius: 8px;">
    <!-- 微信排版正文内容 (不含 H1 大标题) -->
    ...
  </div>
</body>
</html>
```
