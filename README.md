# 🎨 ai-creator-skills

> **AI 内容创作技能套件与自动化工作流工坊**  
> 采用“底层纯粹原子技能”与“上层业务工作流”的双层架构设计：底层技能纯粹无状态，可独立安装拆用；上层工作流串联整套创作与审查流程，提供端到端的内容创作管道。

---

## 🏛️ 架构设计

| 架构层级 | 所在目录 | 核心定位 | 使用方式 |
| :--- | :--- | :--- | :--- |
| **底层：纯粹原子技能** | `skills/` | 零依赖、纯粹的单点能力工具。只处理具体输入文本，生成高质量的内容或生图提示词。 | 可通过 `npx skills add` 独立安装到任意 Agent 运行环境。 |
| **上层：业务工作流** | `workflows/` | 多步骤场景编排。负责联网检索、建立主题目录、执行 AI 盲审与人工确认。 | 将工作流文件放入项目的 Agent 配置目录（如 `.agents/workflows/`）中触发。 |

---

## 🚀 安装与使用指引

### 1. 单独安装与使用原子技能

如果您只需要在自己的 Agent 中单独使用某个写作或设计能力（例如只用长文写作或海报设计）：

```bash
# 全量安装本仓库的所有原子技能
npx skills add morrain/ai-creator-skills

# 或仅安装指定的单个技能（如文章写作技能）
npx skills add morrain/ai-creator-skills --skill article-writer
```

**对话调用示例**：
- *"使用 `article-writer` 技能，帮我为主题 'Vue 3.5 响应式原理' 拟定一份大纲"*
- *"使用 `illustration-designer` 技能，为 '探照灯聚焦夜空' 这个比喻设计 16:9 英文生图提示词"*

---

### 2. 使用端到端业务工作流

如果您希望拥有包含**联网检索、主题文件夹自动管理、AI 盲审打回、人工审核确认**的完整创作管道，将本仓库的 `workflows/` 目录放入项目的 Agent 配置路径（如 `.agents/workflows/`）即可：

#### 命令唤起工作流

在 IDE 的对话框中直接输入对应命令：

| 触发命令 | 工作流文件 | 功能说明 | 交付产物 |
| :--- | :--- | :--- | :--- |
| **`/写文章 [主题]`** | [`workflows/article.md`](workflows/article.md) | 联网检索最新事实，拟定大纲待人工确认，生成呼吸感文章正文。 | `./<主题目录>/outline.md`<br>`./<主题目录>/<文章标题>.md` |
| **`/正文插图`** | [`workflows/illustrations.md`](workflows/illustrations.md) | 提取文章核心金句与概念，设计配图方案与英文提示词。 | `./<主题目录>/assets/illustration_*.md`<br>`./<主题目录>/images/illustration_*.png` (确认后生成) |
| **`/微信公众号`** | [`workflows/weixin.md`](workflows/weixin.md) | 排版为微信专用的离线网页，自动消解表格与注入防擦除样式。 | `./<主题目录>/mp_article.html` |
| **`/海报`** | [`workflows/poster.md`](workflows/poster.md) | 提取海报蓝图与匹配经典版式，生成海报配置文件与纯文本社媒文案。 | `./<主题目录>/assets/poster_*.md`<br>`./<主题目录>/poster_post.md`<br>`./<主题目录>/images/poster_*.png` (确认后生成) |
| **`/workflow-learn [环节]`** | [`workflows/learn.md`](workflows/learn.md) | 识别各创作环节的人工修改 Diff 或批注，沉淀至对应的审稿规则库。 | `./learnings/<phase>.md` (项目根目录) |

---

## 💡 人机协同与防翻车机制

工作流内部设计了严格的防翻车机制与按需生成规则：

1. **大纲人工确认卡点**：
   - 执行 `/写文章` 时，完成联网检索和大纲审稿后，会自动存盘 `outline.md` 并**显式暂停**。
   - 必须等待你在对话框回复 `[通过]` 或提意见修改，才会开始写作完整正文。
2. **提示词先行与按需生图**：
   - 执行 `/正文插图` 或 `/海报` 时，**默认只生成提示词配置文件**（`assets/*.md`），不消耗配额渲染图片。
   - 当你预览配置文件满意后，回复 **“开始生图”** 显式指令，才会批量渲染保存渲染好的图片。

---

## 🛠️ 底层纯粹原子技能列表

1. **`hot-topics`** ([`skills/hot-topics/SKILL.md`](skills/hot-topics/SKILL.md))
   - **功能**：自动抓取全网热榜 (今日热榜 https://tophub.today/)，去重聚合热点并提供创作切入建议，供在当前会话中挑选选题。
2. **`article-writer`** ([`skills/article-writer/SKILL.md`](skills/article-writer/SKILL.md))
   - **功能**：长文与大纲写作，支持干货指南、科技深度评论、社会观察、科普解说、故事叙事 5 种文风自适应识别。
3. **`illustration-designer`** ([`skills/illustration-designer/SKILL.md`](skills/illustration-designer/SKILL.md))
   - **功能**：单图视觉隐喻设计，提炼概念与低科技物件，设计 16:9 纯白背景与原生中文批注提示词。
4. **`wx-formatter`** ([`skills/wx-formatter/SKILL.md`](skills/wx-formatter/SKILL.md))
   - **功能**：微信公众号离线排版，应用防擦除视觉样式系统，自动消解表格，输出带预览视口的原生 HTML。
5. **`poster-designer`** ([`skills/poster-designer/SKILL.md`](skills/poster-designer/SKILL.md))
   - **功能**：手绘图文海报设计，匹配 10 大经典版式与莫兰迪配色，输出防乱码的生图配置。
6. **`blind-reviewer`** ([`skills/blind-reviewer/SKILL.md`](skills/blind-reviewer/SKILL.md))
   - **功能**：通用自进化盲审引擎，自动装载项目进化规则 (`./learnings/<phase_id>.md`) 与领域标准，二元裁决质检，可直接用于任意现有与新创作环节。

---

## 🎨 配图角色 IP 自定义指引

技能套件默认使用 **“小智”**（方块头、单天线、点点眼小机器人）作为配图与海报的主角形象。如果你希望使用自定义的角色 IP：

- **读取优先级（统一文件名为 `character_ip.md`，只要找到一份即生效）**：
  1. **主题目录级**：在具体的文章目录下新建 `./<主题目录>/character_ip.md`。
  2. **项目根目录级（推荐）**：在项目根目录下新建 `./character_ip.md`。
  3. **默认回退**：读取技能内置的默认 IP（小智）。

---

## 📁 项目目录结构

```text
ai-creator-skills/
├── GEMINI.md                        # 项目 Agent 规则与配置
├── README.md                        # 本文档
├── character_ip.md                  # (可选) 项目级自定义 IP 规范模板
├── learnings/                       # (动态按需生成) 首次人审运行 /workflow-learn 后自动创建的分环节自进化审稿规则库
│   ├── article_outline.md           # 文章大纲自进化规则
│   ├── article_content.md           # 文章正文自进化规则
│   ├── illustrations.md             # 正文插图自进化规则
│   ├── weixin.md                    # 微信排版自进化规则
│   ├── poster_blueprint.md          # 海报蓝图自进化规则
│   ├── poster_config.md             # 单张海报 Prompt 自进化规则
│   └── poster_post.md               # 海报社媒文案自进化规则
├── docs/                            # 项目设计文档与 ADR 决策记录
│   ├── adr/                         # 目录结构规范说明
│   └── agents/
├── skills/                          # 底层纯粹原子技能 (可单独安装)
│   ├── hot-topics/                  # 1. 热门话题抓取
│   ├── article-writer/              # 2. 文章与大纲写作
│   ├── illustration-designer/       # 3. 单图视觉隐喻设计
│   ├── wx-formatter/                # 4. 微信公众号排版
│   ├── poster-designer/             # 5. 手绘海报设计
│   └── blind-reviewer/              # 6. 通用自进化盲审引擎
├── workflows/                       # 上层业务工作流 (自动化编排与审查)
│   ├── article.md                   # 写文章工作流 (/写文章)
│   ├── illustrations.md             # 正文插图工作流 (/正文插图)
│   ├── weixin.md                    # 微信公众号排版工作流 (/微信公众号)
│   ├── poster.md                    # 图文海报工作流 (/海报)
│   └── learn.md                     # 规则自进化反哺工作流 (/workflow-learn)
└── <主题英文名>/                    # 实例：主题文件目录 (拟定大纲时自动新建)
    ├── outline.md                   # 文章大纲
    ├── <主题英文名>.md              # 文章正文
    ├── character_ip.md              # (可选) 主题级自定义 IP 规范
    ├── mp_article.html              # 微信公众号离线网页
    ├── poster_post.md               # 社媒纯文本文案
    ├── assets/                      # 生图提示词配置文件
    │   ├── illustration_1.md        # 插图 1 配置文件
    │   ├── poster_1.md              # 海报 1 配置文件
    │   └── poster_2.md              # 海报 2 配置文件
    └── images/                      # 图片渲染产物目录 (按需生成)
        ├── illustration_1.png ~ illustration_N.png
        └── poster_1.png ~ poster_N.png
```