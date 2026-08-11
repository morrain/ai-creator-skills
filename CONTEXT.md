# CONTEXT.md — ai-creator-skills 统一领域模型 (Ubiquitous Language)

本文档定义 `ai-creator-skills` 创作技能套件的核心领域术语与通用语言，所有技能说明（`SKILL.md`）、架构设计及 Agent 交互均须严格遵守本文档所固化的命名与规则。

---

## 核心领域概念与词汇表 (Domain Terms)

### 1. 选题与输入 (Topic Acquisition)
- **`TopicItem`（话题项）**：`hot-topics` 技能聚合全网热榜后生成的标准化结构化数据单元，包含标题、热度评级、多平台排名及创作切入角度建议。

### 2. 文章创作与质量把关 (Article Writing & Quality Control)
- **`Mandatory Web Search Protocol`（强制互联网前置检索）**：大纲生成阶段的硬性前置动作。在提炼大纲草案前，必须优先显式调用 `search_web` 工具对知识主题进行多角度检索（获取最新行业动态、最新技术架构、权威测评与最新 API 现状），严禁未经检索闭门造车或凭空臆造。
- **`Two-Stage Review`（两阶段大纲评审）**：`articles` 技能特有的强制交互流程。阶段一经 SubAgent 盲审后，必须先自动新建主题工作区（`./<article-slug>/`）并将大纲落盘归档至固定的 `outline.md`，同时向主人呈现 100% 完整的 Markdown 大纲原文与存盘链接；必须等待主人明确回复 [通过/修改] 后，方可进入阶段二展开正文。
- **`Reviewer SubAgent Loop`（审稿人 SubAgent 审查闭环）**：在阶段一（大纲）与阶段二（正文）草稿生成后，必须显式发起 `article_reviewer` 审稿子进程，对照 `references/reviewer_standards.md` 执行四大维度盲审，若裁决为 `[REJECT]` 则针对性重写修正（最多循环 8 次），直至判定 `[PASS]`。
- **`Meta-instruction Demarcation`（元指令隔离）**：在大纲中使用 `【撰写指令】` 明确隔离创作指导（如 Hook、金句规划、痛点切入）与实际标题。正文展开时**绝对禁止**将元指令文本作为小标题或正文输出。
- **`Anti-AI Style`（反 AI 味审查）**：参照禁用词黑名单与【科普名师文风】标准（痛点 Hook、2-4 行短段呼吸感排版、去同质化套话），对正文进行质量约束。

### 3. 视觉衍生与生成 (Visual Arts & Asset Generation)
- **`IP Mascot`（共享视觉 IP 形象）**：`illustrations` 等视觉技能的视角主角形象——**小智 (Xiao Zhi)**（方块头、单天线、点点眼小机器人），确保配图视觉统一。
- **`Illustration Reviewer SubAgent Loop`（插图配置 SubAgent 盲审闭环）**：每生成一张插图 Markdown 配置文件（`assets/illustration_N.md`），必须显式发起 SubAgent 对照 `illustration_reviewer_standards.md` 进行盲审，确保提示词精准还原原文逻辑、小智 IP 动作设计符合内容需要。
- **`Illustration Config Files`（插图配置文件）**：在主题工作区 `./<article-slug>/assets/` 目录下为每张插图独立生成的 Markdown 配置文件（`illustration_1.md` ~ `illustration_N.md`），包含插图元数据、中文确认版 Prompt & 视觉方案设计以及英文生图版 Prompt。
- **`Lazy Generation`（配置先行 / 按需延迟生图）**：视觉技能的核心原则。优先生成全量文本配置与双语 Prompt Specs（中文预览版 / 英文生图版），默认绝不自动调用 `generate_image` 工具，仅在主人明确发出生图指令时，才批量调用图片生成工具。

### 4. 微信公众号派生与排版 (WeChat MP Article Derivation & Formatting)
- **`to-wx Skill`（微信文章派生技能）**：读取主题工作区的正文 Markdown 与插图配置，套用固定草稿安全 UI 设计系统，生成 `mp_article.html` 离线网页文件。
- **`WeChat Draft-Safe UI System`（微信草稿防擦除原生视觉排版设计系统）**：定义在 `references/mp_style_design_system.md` 中，基于微信后台 CSS 白名单构建的内联组件库（居中 H2 胶囊角标、左边框 H3、双色对比卡片、步骤卡片、金句引用框、居中插图容器与行内适度高亮），确保全选复制粘贴进微信后台保存草稿样式不被擦除。
- **`Zero Text Alteration Rule`（原文绝对零增删改原则）**：在派生微信长文时，绝对禁止修改、增删原文句子或新增 AI 提炼总结卡片，高亮标记仅能通过行内 `<span style="...">` 包裹原文已有词句。
- **`WeChat Reviewer SubAgent Loop`（微信长文审稿人盲审闭环）**：在生成 `mp_article.html` 过程中，必须发起 `mp_article_reviewer` 审稿子进程，对照 `references/mp_reviewer_standards.md` 执行表格零残留、组件完备度、图注嵌合与原文忠实度四大维度盲审。

### 5. 图文海报与社媒卡片派生 (Multi-Image Poster & Social Card Derivation)
- **`to-poster Skill`（图文海报派生技能）**：读取主题工作区的正文 Markdown 与插图配置，重构为 N 张包含高密度干货、莫兰迪 3:4 手绘美学与小智 IP 的海报配置文件（`assets/poster_1.md ~ poster_N.md`）及 200 字纯文本社媒发布文案（`poster_post.md`）。
- **`Poster Layouts`（海报 10 大经典版式）**：定义在 `references/layouts.md` 中（Hero 破题版、四宫格/六宫格干货版、左右/上下双轨对比版、纵向链路流程版、中心破局脑图版、极简金句闭环版、数据/指标面板版、避坑拆弹红黑榜版、Q&A 问答对话版、时间线演进史切片版）。
- **`Clean Plain Text Social Post Rule`（社媒文案纯文本防标记规则）**：`poster_post.md` **绝对禁止使用任何 Markdown 语法标记**（如加粗 `**`、标题 `#`、链接 `[text](url)`），防止复制粘贴至小红书/朋友圈/即刻等自媒体平台时残存源码符号；第一备选标题必须保留原文章大标题 H1。
- **`Anti-Gibberish Protocol`（生图 Prompt 原生中文与防乱码协议）**：🟢 英文生图版 Prompt 中要求渲染的短语保留单引号原生中文 `'...'`，且结尾必须强制写入显式去乱码控制指令（`strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish`）。

### 6. 产物管理与归档 (Artifact Management)
- **`Topic Workspace`（主题工作区目录）**：文章大纲阶段自动基于主题生成简短英文连字符 Slug（`<article-slug>`），并在项目根目录下新建 `./<article-slug>/` 独立文件夹。大纲保存为固定的 `outline.md`。该主题的所有后续衍生产物（文章 Markdown、微信公众号离线网页 `mp_article.html`、`assets/illustration_N.md` 插图配置、海报配置 `assets/poster_N.md`、纯文本社媒文案 `poster_post.md`、`images/` 目录下按需生成的图片）均集中存放在该文件夹及子文件夹内。
