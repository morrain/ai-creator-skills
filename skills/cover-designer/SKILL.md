---
name: cover-designer
description: 自媒体爆款封面设计与 Prompt 提炼技能。分析文章或视频剧本，生成具备高 CTR 点击率与多平台生图 Prompt 的 assets/cover.md 配置文件。
---

# Cover Designer Skill (自媒体爆款封面设计器)

本技能为 **纯粹无状态的自媒体爆款封面设计原子技能**。自动解析传入的内容文本（文章 Markdown、剧本 JSON 或主题说明），提炼高 CTR 点击率主标题、按需互动钩子与具象物理隐喻，生成 `assets/cover.md` 配置文件及多平台生图 Prompt。

---

## 核心设计原则 (Core Principles)

1. **单点无状态提炼 (Stateless Cover Output)**：
   - 接收文章/剧本内容文本及可选目标平台参数（`platform: xiaohongshu|weixin|video|all`，默认 `all`），自动提炼并输出标准 `assets/cover.md`。
2. **内容契合与条件评论钩子 (Content-Driven CTR & Conditional Comment Gate)**：
   - 封面 100% 忠实体现正文核心干货与认知隐喻。
   - **按需启用评论钩子**：仅当内容具备天然互动切口（争议选型/避坑多选/悬念猜想/痛点吐槽/认知差）时配置 `👉 评论区...` 引导标记；纯干货/教程设为 `null`，严禁硬塞机械套路。
3. **配置文件先行与延时生图 (Strict Lazy Generation)**：
   - 默认仅提炼落盘 `assets/cover.md` 配置文件。
   - 用户触发“开始生图”或“生成封面”指令后，才调用 `generate_image` 工具导出图片至 `./images/cover_<platform>.png`。
4. **IP 形象短路路由 (Short-Circuit IP Routing)**：
   - 优先装载 1 份 `character_ip.md`：1) 主题级 `./<article-slug>/character_ip.md` ➔ 2) 项目级 `./character_ip.md` ➔ 3) 默认技能级 [`references/character_ip.md`](references/character_ip.md)。

---

## 关联参考规范

- [`references/platform_traffic_rules.md`](references/platform_traffic_rules.md)：各自媒体平台流量机制、尺寸画幅（3:4 / 2.35:1 / 9:16）与排版规程。
- [`references/engagement_recipes.md`](references/engagement_recipes.md)：5 维爆款评论引力范式图谱与按需触发原则。
- [`references/cover_reviewer_standards.md`](references/cover_reviewer_standards.md)：盲审质检打回标准。
- [`references/character_ip.md`](references/character_ip.md)：IP Mascot 形象与姿态。

---

## 规范输出格式 (`assets/cover.md`)

```markdown
# 封面设计：[爆款痛点/悬念主标题]

## 封面元数据
- **核心主题**：[描述本封面表达的核心痛点或争议点]
- **生成模式**：全平台适配模式 (Multi-Platform Mode)

## 🔵 中文确认版 封面视觉与爆款排版设计
- **爆款主标题（10-14字）**：`[72px+ 痛点/悬念 Hook 标题]`
- **评论区引导标记**：`"👉 评论区留下你的观点"` (或 null)
- **视觉焦点与构图**：[IP Mascot 发问/探查姿态与具象物理隐喻]
- **手写中文批注**：`"批注1"`、`"批注2"`

---

## 🟢 英文生图版 Prompt (按平台区分)

### 1️⃣ 小红书版 Prompt (黄金画幅 3:4 / 1080x1440)
```text
A 3:4 minimalist hand-drawn cover illustration for Xiaohongshu...
```

### 2️⃣ 微信公众号版 Prompt (首图画幅 2.35:1 / 900x383)
```text
A 2.35:1 wide banner cover illustration for WeChat Official Account...
```

### 3️⃣ 视频号/抖音/B站版 Prompt (竖屏画幅 9:16 / 1080x1920)
```text
A 9:16 vertical video cover illustration...
```
```
