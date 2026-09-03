---
name: cover-designer
description: 自媒体爆款封面设计与 Prompt 提炼技能。分析文章或视频剧本，生成具备高 CTR 点击率与多平台生图 Prompt 的 assets/cover.md 配置文件。
---

# Cover Designer Skill (自媒体爆款封面设计器)

本技能为 **纯粹无状态的自媒体爆款封面设计原子技能**。自动解析传入的内容文本（文章 Markdown、剧本 JSON 或主题说明），提炼高 CTR 点击率主标题、按需互动钩子与自适应视觉方案（按需选用具象物理隐喻或极简大字 Typography 版式），生成 `assets/cover.md` 配置文件及多平台生图 Prompt。

---

## 核心设计原则 (Core Principles)

1. **纯粹封面定位与海报隔离原则 (Cover vs. Poster Demarcation)**：
   - 封面的唯一使命是作为文章/视频的第一视觉缩略图（Thumbnail Card），在 Feed 瀑布流中呈现爆款 H1 标题并拉满点击率 (CTR)；
   - **绝对禁止将封面混淆为长文海报或私域导流单**：
     - ❌ **严禁包含“留言/私信领资料”、“关注公众号”、“加微信”等私域导流/广告 CTA 贴纸**；
     - ❌ **严禁堆叠“卡片 A：...”、“卡片 B：...”等多段总结卡片与要点清单**（知识总结海报由 `poster-designer` / `/海报` 工作流专门负责）；
   - 封面仅保留 **主标题（10-14字爆款 Hook，或由上游工作流指定的精准标题）+ 主视觉/IP Mascot 动作 + 必要的单句副标题**，保持高级清爽，严禁牛皮癣感。若上游明确指定了标题（如文章定稿的 H1），必须完全复用，绝不擅自缩减或改写，保证表里如一。
2. **文风自适应与多样化美学矩阵 (Content-Driven & Diverse Aesthetic Matrix)**：
   - **解封固定画风限制，杜绝模版化套路**：Agent 须根据文章/剧本文风与情绪，自适应匹配最佳美学画风，绝不搞千篇一律的模板：
     - 🌟 **干货指南 / 小红书清爽** ➔ **暖米白莫兰迪手绘风** (`#FAF6F0` 羊膏纸底色、雾霾蓝/焦糖橙、极简手绘线条)；
     - 🚀 **科技洞察 / 破局重构** ➔ **硬核高对比光影风** (暗色渐变背景、高亮斜向聚光、发光视界门洞)；
     - 💡 **社会观察 / 现象解构** ➔ **明亮杂志排版几何风** (包豪斯高饱和块面切割、鲜明高光标题)；
     - 🔬 **硬核科普 / 机制拆解** ➔ **网格蓝图草图解构风** (网格工程纸、白板手绘划线、流程透视图)；
     - 🎭 **故事叙事 / 人物转折** ➔ **戏剧场景插画风** (富含情绪与故事起伏的插画场景)；
   - **IP Mascot 小智动态协同**：让 IP Mascot 小智（方块头、天线机器人）作为动作主角参与场景（如持灯探查、登阶、看蓝图、悬浮探头），增强生动趣味性；
   - **强概念视觉隐喻 (Strong Conceptual Visual Metaphor)**：封面必须将文章的核心逻辑、痛点或解决方案转化为**极其具象且极具吸引力的视觉场景**，绝不能仅仅描述一个普通的背景或字面意思上的静物。例如，如果是关于“内存泄漏”，应描绘一个“发光容器破裂、数字液体流失”的强隐喻场景，而不是仅仅画一台电脑。视觉隐喻必须精准表达核心含义，做到既吸引人又有深度。
   - **构图铁律**：无论采用何种画风，画面均须**主次分明、中央焦点清晰、留足呼吸空间**，杜绝多场景拼盘与杂乱元素堆叠！
3. **文字排版清晰度与超大字号视觉冲击力 (Massive Typography & Anti-Clutter Protocol)**：
   - 封面文案必须**服务于核心主题与意思表达**，主次分明：突出醒目的爆款主标题，可按需配置 1 处强化痛点的副标题作为补充。若输入中明确指定了主标题内容，必须一字不差地复用。
   - **超大字号与高亮对比规程**：主标题字号必须极具视觉冲击力（$\ge 120px$ 极粗体），副标题绝不能是被忽视的小字（字号 $\ge 80px$），并且副标题必须带有**高对比度底色背景或粗黑包边**（high contrast background block or thick stroke），确保在手机端缩略图尺寸下依然清晰可读，绝不融合在背景中。
   - **顶部呼吸留白安全区（防贴边与防数字噪点）**：标题文字**绝对不能紧贴画布顶端边缘**，必须预留充足的垂直呼吸留白（`generous top margin padding away from top border`），保证视觉舒展；
   - ⚠️ **英文 Prompt 绝对防噪铁律**：**英文 Prompt 中绝对禁止出现任何百分比数字**（如 `15%`, `20%`, `70%`）！因为 AI 生图模型会将 Prompt 中的 `15%` 误判定为要打印出来的文字标签并渲染在画布上。一律使用纯定性英文描述：`generous top margin, spacious edge padding, centered upper safety zone`；
   - 英文生图 Prompt 需明确渲染的文字内容（用单引号包裹），并强调超大字号、高亮对比与清晰度：`massive and clear typography hierarchy, giant bold main title centered inside upper safety zone with generous margins, crisp massive secondary subtitle with high-contrast background block, strictly NO text touching canvas border, NO garbled text, NO random percentage numbers`。
4. **深度内容契合与条件评论钩子 (Deep Content-Driven CTR & Conditional Comment Gate)**：
   - **拒绝“望文生义”**：在设计封面视觉（画面构图、物理隐喻与角色动作）时，**必须深入研读内容的核心干货与逻辑，绝对不能仅仅根据标题的字面意思敷衍设计**。封面必须 100% 忠实且深度体现内容的核心内涵。
   - **按需启用评论钩子**：仅当内容具备天然互动切口时配置 `👉 评论区...` 引导标记（仅在中文排版说明中展现，生图 Prompt 中不写小字）；纯干货/教程设为 `null`。
5. **设计方案与图像渲染两阶段解耦 (Decoupled Design & Image Generation Protocol)**：
   - **阶段 1 (设计封面/提炼方案)**： Agent 调度 `cover-designer` 技能分析正文/剧本，提炼爆款主标题 Hook、视觉构图与多平台 Prompt，落盘为 `./assets/cover.md` 配置文件。呈报 `cover.md` 链接并提示用户可回复 `[渲染封面]` 或 `[开始生图]`。
   - **阶段 2 (渲染封面/生成图片)**：仅当用户发送 `[渲染封面]`、`[开始生图]` 或指定平台渲染指令（如 `[渲染小红书封面]`）时，Agent 方可调用 `generate_image` 生图工具，抓取 `cover.md` 中的英文 Prompt 渲染导出真实图片至 `./assets/cover.jpg` (或指定平台图片 `./images/cover_<platform>.png`)。
6. **IP 形象短路路由 (Short-Circuit IP Routing)**：
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
- **爆款主标题**：`[120px+ 极粗体主标题]` (若上游指定则完全复用；否则提炼 10-14 字痛点 Hook)
- **副标题/痛点切口**：`[80px+ 高对比底色，单句强化痛点副标题，或 null]`
- **评论区引导标记**：`"👉 评论区留下你的观点"` (或 null)
- **视觉焦点与构图**：[IP Mascot 发问/探查姿态与画面构图]

---

## 🟢 英文生图版 Prompt (按平台区分)

### 1️⃣ 小红书版 Prompt (黄金画幅 3:4 / 1080x1440)
```text
A 3:4 minimalist hand-drawn cover illustration for Xiaohongshu...
```

### 2️⃣ 微信公众号版 Prompt (受模型支持度采用 16:9 画幅，必须绝对垂直居中)
```text
A 16:9 wide cover illustration for WeChat Official Account. All text and core subjects MUST be strictly placed in the absolute vertical center safe zone...
```

### 3️⃣ 视频号/抖音/B站版 Prompt (竖屏画幅 9:16 / 1080x1920)
```text
A 9:16 vertical video cover illustration...
```
```
