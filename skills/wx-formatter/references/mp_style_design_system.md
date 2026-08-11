# 微信公众号草稿防擦除原生视觉排版设计系统 (WeChat Draft-Safe UI System)

本文档为微信公众号离线排版 HTML 的**唯一固定视觉设计与排版规范**。
用户在 Safari/Chrome 浏览器中双击打开生成的离线 HTML 文件全选复制，即可 100% 完美粘贴进微信公众号编辑器，且点击“保存草稿”后所有样式不会被腾讯服务器擦除。

⚠️ **大标题剔除规则**：正文内容中**绝对不包含 H1 大标题**（在微信公众号后台头部专门框中独立填写标题）。

---

## 一、 品牌色彩体系 (Color System)

- **品牌主色 (Primary Accent)**：`#10AEFF` (科技蓝 / 极光蓝) —— 用于 H2 标题下划线、角标与重点高亮。
- **正文字色 (Body Text)**：`#333333` 或 `#3E3E3E` (柔和深灰) —— 严禁使用 `#000000` 纯黑。
- **背景与卡片 (Cards & Surface)**：
  - 常规卡片底色：`#F6F8FA` 或 `#F8F9FA`
  - 爆款金句底色：`#FFF9F0` (暖金浅底) + `#FA9D3B` 虚线边框
  - 优势卡片底色：`#F0F9F4` (浅绿底) + `#07C160` (绿色边框)
  - 痛点卡片底色：`#FFF5F5` (浅红底) + `#FA5151` (红色边框)

---

## 二、 微信草稿白名单防护规则 (Draft Sanitizer Whitelist)

1. **白名单允许属性**：`background-color`, `color`, `font-size`, `font-weight`, `letter-spacing`, `line-height`, `text-align`, `padding`, `margin`, `border-left`, `border-bottom`, `border`, `border-radius`, `max-width`。
2. **严禁使用会被腾讯后端过滤删除的属性**：
   - 禁用 `box-shadow` (保存草稿时服务器会自动擦除阴影样式)；
   - 禁用 `display: flex` / `float` / `position: absolute`；
   - 禁用原生 `<h1>~<h6>` 标题标签；
   - 禁用空内容的 `<span style="..."/>`。

---

## 三、 草稿安全 HTML 组件模板库 (Inline Component Library)

### 1. 🔷 居中二级标题 (H2 替代 - 紧凑胶囊角标 + 极光蓝居中下划线)
```html
<section style="text-align: center; margin: 30px auto 20px auto; line-height: 1.4;">
  <section style="display: inline-block; background-color: #EBF7FF; color: #10AEFF; font-size: 12px; font-weight: bold; padding: 2px 10px; border-radius: 10px; letter-spacing: 1px; line-height: 1.2;">SECTION 01</section>
  <section style="margin-top: 4px; text-align: center;">
    <section style="display: inline-block; font-size: 18px; font-weight: bold; color: #111827; border-bottom: 2.5px solid #10AEFF; padding-bottom: 4px; letter-spacing: 0.5px; line-height: 1.4;">
      一、 示例二级标题名称
    </section>
  </section>
</section>
```

### 2. 🔹 三级/小节标题 (H3 替代 - 左侧极光蓝立边，多行自适应排版)
```html
<section style="border-left: 3.5px solid #10AEFF; padding-left: 10px; font-size: 16px; font-weight: bold; color: #111827; margin: 26px 0 14px 0; line-height: 1.5; text-align: left; letter-spacing: 0.5px;">
  1.1 示例三级小节标题
</section>
```

### 3. 🔴🟢 双色痛点/优势对比卡片 (替代 Markdown 对比表格)
```html
<section style="margin: 24px 0;">
  <section style="background-color: #FFF5F5; border-left: 4px solid #FA5151; border-radius: 6px; padding: 12px 16px; margin-bottom: 12px;">
    <strong style="color: #FA5151; font-size: 15px;">🔴 传统模式痛点</strong>
    <p style="margin: 6px 0 0 0; font-size: 14px; color: #555555; line-height: 1.7;">痛点描述...</p>
  </section>
  <section style="background-color: #F0F9F4; border-left: 4px solid #07C160; border-radius: 6px; padding: 12px 16px;">
    <strong style="color: #07C160; font-size: 15px;">🟢 新模式优势</strong>
    <p style="margin: 6px 0 0 0; font-size: 14px; color: #555555; line-height: 1.7;">优势描述...</p>
  </section>
</section>
```

### 4. 🚀 步骤/流程解析卡片 (替代 Markdown 流程表格/列表)
```html
<section style="background-color: #F8F9FA; border: 1px solid #EAEAEA; border-radius: 8px; padding: 16px; margin: 20px 0;">
  <strong style="color: #10AEFF; font-size: 16px; display: block; margin-bottom: 12px;">🚀 阶段解耦流水线全景解构</strong>
  <section style="margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #EEEEEE;">
    <span style="background-color: #10AEFF; color: #FFFFFF; font-size: 12px; padding: 2px 8px; border-radius: 4px; font-weight: bold;">步骤 1</span>
    <strong style="color: #222222; font-size: 15px; margin-left: 6px;">步骤名称 (Step Name)</strong>
    <p style="margin: 4px 0 0 0; font-size: 14px; color: #555555;">说明文本...</p>
  </section>
</section>
```

### 5. 💡 爆款金句高亮引用框
```html
<section style="background-color: #FFF9F0; border: 1px dashed #FA9D3B; border-radius: 8px; padding: 14px 16px; margin: 24px 0; font-size: 15px; color: #664600; line-height: 1.75;">
  💡 <strong>金句总结：</strong>金句内容...
</section>
```

### 6. 🖼 正文插图与居中图注容器
```html
<section style="text-align: center; margin: 22px 0;">
  <img src="images/illustration_1.png" style="max-width: 100%; border-radius: 8px; vertical-align: middle;" />
  <section style="font-size: 13px; color: #888888; margin-top: 8px; font-style: italic; text-align: center;">
    💡 图 1：说明文字
  </section>
</section>
```

### 7. 🔥 结尾互动与引导关注卡片
```html
<section style="background-color: #F8F9FA; border-radius: 10px; padding: 20px; margin: 30px 0 10px 0; text-align: center; border: 1px solid #EAEAEA;">
  <p style="font-size: 15px; font-weight: bold; color: #1A1A1A; margin-bottom: 8px;">🚀 开源项目直达 & 免费体验</p>
  <p style="font-size: 14px; color: #10AEFF; margin-bottom: 12px;"><a href="https://github.com/morrain/ai-creator-skills" style="color: #10AEFF; text-decoration: underline;">https://github.com/morrain/ai-creator-skills</a></p>
  <p style="font-size: 13px; color: #777777; margin: 0;">🔥 喜欢本文？欢迎“点赞 + 在看 + 转发”支持！欢迎 Star & Fork 体验！</p>
</section>
```

### 8. 🖍️ 重点文字行内高亮与下划线
```html
<span style="background-color: #FFF2B2; color: #222222; font-weight: bold; padding: 2px 5px; border-radius: 3px; margin: 0 2px;">核心关键词或短语</span>
<span style="background-color: #EBF7FF; color: #10AEFF; font-weight: bold; padding: 2px 6px; border-radius: 4px; margin: 0 2px;">技术概念名称</span>
<span style="border-bottom: 2.5px solid #FA9D3B; color: #111827; font-weight: bold; padding-bottom: 1px; margin: 0 2px;">关键洞察与结论短句</span>
<span style="border-bottom: 2px dashed #10AEFF; color: #10AEFF; font-weight: bold; padding-bottom: 2px; margin: 0 2px;">底层工作逻辑与原理</span>
<span style="background-color: #FFF5F5; color: #E53E3E; font-weight: bold; padding: 2px 6px; border-radius: 4px; border: 1px solid #FEB2B2; margin: 0 2px;">⚠️ 避坑提醒：注意事项</span>
```
