# 🎨 ai-creator-skills

> **AI 创作技能套件仓库**  
> 包含选题获取、文章生成、正文插画设计、手绘海报生成等一系列内容创作 Agent Skill。

---

## 🛠️ 核心技能套件 (Creative Skills Suite)

1. **`hot-topics`** ([`skills/hot-topics/SKILL.md`](skills/hot-topics/SKILL.md))
   - **功能**：自动抓取全网热榜 (今日热榜 https://tophub.today/)，去重评估爆款潜质，输出多端热度排名与包含结构化 `TopicItem` JSON 的选题报告。

2. **`articles`** ([`skills/articles/SKILL.md`](skills/articles/SKILL.md))
   - **功能**：接收热点话题，采用“大纲人工评审 + 确认后展开正文”的两阶段互动流程，支持科技评论、社会观察、科普解说、故事叙事、干货指南等多种文风，输出纯净 Markdown 文章。

3. **`illustrations`** ([`skills/illustrations/SKILL.md`](skills/illustrations/SKILL.md))
   - **功能**：参考 `article-illustrations` 规范，分析文章提炼认知锚点与怪诞隐喻，在 `./<article-slug>/assets/` 目录下生成独立插图配置文件；每张插图配置自动发起 SubAgent 盲审，默认仅生成配置文件（按需延迟生图），全部完成后进行结构化汇报。

4. **`to-wx`** ([`skills/to-wx/SKILL.md`](skills/to-wx/SKILL.md))
   - **功能**：参考 `mp_style_design_system` 规范，将文章正文与插图转换为微信公众号草稿安全的移动端排版长文；消除 Markdown 表格并重构为对比/步骤卡片，嵌合居中插图与斜体图注，进行适度点睛高亮，经 SubAgent 盲审后归档为单文件网页 `mp_article.html`。

5. **`to-poster`** ([`skills/to-poster/SKILL.md`](skills/to-poster/SKILL.md))
   - **功能**：参考 `layouts` 与 `style_guide` 规范，将正文干货与插图隐喻提炼重构为 N 张包含高密度干货的手绘图文海报配置文件 (`assets/poster_1.md ~ poster_N.md`) 及 200 字纯文本社媒发布文案 (`poster_post.md`)；支持 5 大经典版式与莫兰迪 3:4 小红书黄金比例，经多阶段 SubAgent 盲审通过后归档（配置先行 / 按需延迟生图）。

*(注：动画生成技能 `animation` 已记录于工程地图，暂作搁置待后续迭代支持。)*

---

## 🎨 视觉 IP 形象配置与自定义指引 (IP Mascot Customization)

技能套件默认使用 **“小智 (Xiao Zhi)”**（方块头、单天线、点点眼小机器人）作为文章插画与图文海报的共享视觉主角。

- **前置短路加载逻辑 (Short-circuit Routing)**：视觉技能在运行时，按优先级**检查且仅读取 1 份** IP 规范（命中即止，拦截后续默认文件）：
  1. **主题级自定义**：在具体主题工作区新建 `./<article-slug>/ip.md`。
  2. **全局级自定义（推荐）**：在项目根目录下新建 `docs/domain/character_ip.md`。
  3. **默认回退**：前两者均不存在时，读取 [`/references/character_ip.md`](/references/character_ip.md)（小智 IP）。

---

## 📁 目录结构与主题工作区 (Topic Workspace)

每次在 `articles` 技能大纲通过后，系统会在项目根目录下自动创建简短英文连字符命名的 **主题工作区目录**（`./<article-slug>/`），所有下游衍生产物均集中存放在该文件夹内：

```text
ai-creator-skills/
├── GEMINI.md                        # Agent 规则与配置文件
├── README.md                        # 本文档
├── CONTEXT.md                       # 统一领域模型 (Ubiquitous Language)
├── docs/                            # 领域规范与 ADR 决策记录
│   ├── adr/                         # 0001-root-topic-workspace-directory-structure.md
│   └── agents/
├── skills/                          # 创作 Agent 技能套件
│   ├── hot-topics/                  # 1. 热门话题搜集
│   ├── articles/                    # 2. 交互式大纲与文章写作
│   ├── illustrations/               # 3. 按需插画配置与位置映射
│   ├── to-wx/                       # 4. 微信公众号长文派生与视觉排版
│   └── to-poster/                   # 5. 图文海报派生与纯文本社媒文案
└── <article-slug>/                  # 实例：主题工作区 (拟定大纲阶段自动新建)
    ├── outline.md                   # 文章大纲 (固定文件名)
    ├── <article-slug>.md            # 纯净 Markdown 文章
    ├── mp_article.html              # 微信公众号派生网页 (可以直接复制粘贴进公众号后台)
    ├── poster_post.md               # 200 字纯文本社媒发布文案 (用于复制发布至小红书/即刻)
    ├── assets/                      # 衍生配置文件目录
    │   ├── illustration_1.md        # 插图 1 配置文件 (含元数据、双语 Prompt 与手写批注)
    │   ├── illustration_2.md        # 插图 2 配置文件
    │   ├── poster_1.md              # 海报 1 配置文件 (含版式、视觉组件与双语 Prompt)
    │   └── poster_2.md              # 海报 2 配置文件
    └── images/                      # 渲染图片素材目录 (按需生图产物)
        ├── illustration_1.png ~ illustration_N.png # 按需生成的插图图片
        └── poster_1.png ~ poster_N.png            # 按需生成的海报图片
```