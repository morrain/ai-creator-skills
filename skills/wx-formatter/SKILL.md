---
name: wx-formatter
description: 纯粹的微信公众号草稿安全 HTML 排版转换原子技能。接收任意纯文本或 Markdown 文章输入，应用草稿防擦除原生 UI 设计系统 (references/mp_style_design_system.md)，消解 Markdown 表格，注入居中 H2 胶囊、左边框 H3、金句框、行内高亮与插图图注，输出符合 677px 预览视口的原生离线 HTML。不包含长文写作或主题工作区目录搜寻逻辑。
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
5. **爆款金句统一组件法则 (Golden Quote Card Standard)**：
   - 文章末尾添加爆款金句总结：使用 **`💡 金句总结`** 暖金虚线边框卡片（设计系统组件 5，`#FFF9F0` 浅黄底 + `1px dashed #FA9D3B` 虚线边框）。
6. **结尾互动关注卡片必含法则 (End-of-Article Engagement Card)**：
   - 在正文最末尾必须嵌入设计系统 (`references/mp_style_design_system.md`) 组件 7（`🔥 结尾互动与引导关注卡片`），包含项目开源链接与“点赞 + 在看 + 转发”互动提示。

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
