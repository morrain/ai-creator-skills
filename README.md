<div align="center">

# 🎨 AI Content Creator Studio & Skills Suite

### 面向高级创作者与总编辑的 AI 全流程内容工程化套件

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Skills Platform](https://img.shields.io/badge/Skills-Atomic%20%26%20Decoupled-9932CC.svg)](#-底层纯粹原子技能库) [![Architecture](https://img.shields.io/badge/Architecture-Dual--Layer-success.svg)](#-双层架构设计) [![Blind Review Engine](https://img.shields.io/badge/Review-SubAgent%20Blind--Review-orange.svg)](#-通用盲审引擎-blind-reviewer) [![Self Evolution](https://img.shields.io/badge/Evolution-%2Fworkflow--learn-ff69b4.svg)](#-审稿规则自进化机制-workflow-learn)

<p align="center">
  <b>包含端到端爆款长文写作、认知隐喻插图设计、微信公众号防擦除 HTML 排版、3:4 莫兰迪图文海报与自进化审稿系统</b>
</p>

[✨ 核心亮点](#-为什么选择-ai-creator-studio) • [🏛️ 架构设计](#-双层架构设计-dual-layer-architecture) • [🚀 快速上手](#-安装与使用指引) • [🤖 业务工作流](#-端到端业务工作流-workflows)
[🧠 规则自进化](#-审稿规则自进化机制-workflow-learn) • [🛠️ 原子技能库](#-底层纯粹原子技能库) • [🎨 IP 角色体系](#-配图角色-ip-自定义指引) • [📁 目录结构](#-项目目录结构)

---

</div>

## 💡 为什么选择 AI Creator Studio？

> [!NOTE]
> 传统 AI 创作工具往往存在 **AI 味浓厚、格式挤压乱码、排版依赖微信后台被擦除、且“不长记性重复踩坑”** 等痛点。本套件通过 **双层解耦架构 + SubAgent 独立盲审 + 人工修改自进化闭环**，打造专业编辑级的内容产出工程。

* **⚡ 双层解耦架构设计**：底层原子技能 (`skills/`) 纯粹无状态、零依赖，可拆分单独安装；上层工作流 (`workflows/`) 串联检索、编排、盲审与人审卡点。
* **🔍 独立 SubAgent 盲审引擎 (`blind-reviewer`)**：打破“AI 既当作者又当裁判”的自夸误区，启动独立审稿子进程进行苛刻质检与诊断打回。
* **🧠 审稿规则自进化机制 (`/workflow-learn`)**：主编在编辑器中手工修饰一次，系统自动提取 Diff 并沉淀为项目级规则，实现“主编修改一次，AI 盲审永久记住”。
* **🎨 离线美学排版系统**：提供微信公众号离线 HTML 防擦除视觉系统、以及防乱码的 3:4 莫兰迪手绘社媒海报套件。

---

## 🏛️ 双层架构设计 (Dual-Layer Architecture)

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         上层业务工作流 (Workflows Layer)                         │
│    workflows/article.md  │  illustrations.md  │  weixin.md  │  poster.md         │
│    - 联网事实检索、文件夹自动创建、SubAgent 盲审调度、人工 Gate 确认卡点         │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ 调度技能 & 传递上下文
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      底层纯粹原子技能 (Atomic Skills Layer)                      │
│    skills/hot-topics  │  article-writer  │  illustration-designer  │ ...         │
│    - 零依赖单点能力，输入文本 -> 输出高品质文章 / HTML / Prompt 生图配置         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

| 架构层级 | 所在目录 | 核心定位 | 最佳使用场景 |
| :--- | :--- | :--- | :--- |
| **底层：纯粹原子技能** | `skills/` | 零依赖、纯粹的单点能力工具。只处理具体输入文本，生成高质量的内容或生图提示词。 | 可通过 `npx skills add` 独立安装到任意 Agent 运行环境中拆用。 |
| **上层：业务工作流** | `workflows/` | 多步骤场景编排。负责联网检索、建立主题目录、执行 AI 盲审与人工确认。 | 将工作流放入项目的 Agent 配置目录（如 `.agents/workflows/`）全自动运行。 |

---

## 🚀 安装与使用指引

### 1. 单独安装与拆用原子技能

如果您只需要在自己的 Agent 中单独使用某个写作或设计能力（例如仅需长文写作或海报设计）：

```bash
# 全量安装本仓库的所有原子技能
npx skills add morrain/ai-creator-skills

# 或仅安装指定的单个技能（例如：文章写作技能）
npx skills add morrain/ai-creator-skills --skill article-writer
```

> [!TIP]
> **对话调用示例**：
> - *"使用 `article-writer` 技能，帮我为主题 'Vue 3.5 响应式原理' 拟定一份大纲"*
> - *"使用 `illustration-designer` 技能，为 '探照灯聚焦夜空' 这个比喻设计 16:9 英文生图提示词"*

---

## 🤖 端到端业务工作流 (Workflows)

将本仓库的 `workflows/` 目录放入项目的 Agent 配置路径（如 `.agents/workflows/`）中，即可在对话框中直接通过命令触发：

| 触发命令 | 工作流文件 | 功能说明 | 交付产物 |
| :--- | :--- | :--- | :--- |
| **`/写文章 [主题]`** | [`workflows/article.md`](workflows/article.md) | 联网检索事实，拟定大纲待人工确认，生成呼吸感排版文章正文。 | `./<主题目录>/outline.md`<br>`./<主题目录>/<文章标题>.md` |
| **`/正文插图`** | [`workflows/illustrations.md`](workflows/illustrations.md) | 提取文章核心金句与概念，设计认知隐喻配图方案与英文 Prompt。 | `./<主题目录>/assets/illustration_*.md`<br>`./<主题目录>/images/illustration_*.png` (确认后生成) |
| **`/微信公众号`** | [`workflows/weixin.md`](workflows/weixin.md) | 排版为微信专用离线 HTML 网页，自动消解表格与注入防擦除 CSS。 | `./<主题目录>/mp_article.html` |
| **`/海报`** | [`workflows/poster.md`](workflows/poster.md) | 提取海报组图蓝图与版式，生成 3:4 生图配置与纯文本社媒文案。 | `./<主题目录>/assets/poster_*.md`<br>`./<主题目录>/poster_post.md`<br>`./<主题目录>/images/poster_*.png` (确认后生成) |
| **`/workflow-learn [环节]`** | [`workflows/learn.md`](workflows/learn.md) | 识别各创作环节的人工修改 Diff 或批注，沉淀至对应的审稿规则库。 | `./learnings/<phase>.md` (项目根目录) |

---

## 🛡️ 人机协同与防翻车机制

工作流内部设计了严格的防翻车机制与按需生成规则：

1. **大纲人工确认卡点**：
   - 执行 `/写文章` 时，完成联网检索和大纲审稿后，会自动存盘 `outline.md` 并**显式暂停对话**。
   - 必须等待你在对话框回复 `[通过]` 或提出修改意见后，才会继续撰写正文。
2. **提示词先行与按需生图**：
   - 执行 `/正文插图` 或 `/海报` 时，**默认只生成提示词配置文件**（`assets/*.md`），不直接消耗算力 / API 配额。
   - 当你预览配置文件满意后，回复 **“开始生图”** 显式指令，系统才会批量渲染图片。
3. **审稿规则自进化与反哺**：
   - 每次产物生成后，如果你在编辑器中对大纲、正文、提示词、HTML 或社媒文案进行了人工修改，只需在对话框回复 **`/workflow-learn`**。
   - 系统会自动比对 Diff 并将你的偏好沉淀落盘至根目录 `./learnings/<phase_id>.md`，让后续盲审越用越懂你！

---

## 🧠 审稿规则自进化机制 (`/workflow-learn`)

为了解决 AI 创作中“重复踩坑”、“不长记性”的痛点，套件内置了**分环节审稿规则自进化机制**，实现“主编修改一次，AI 盲审永久记住”的品质进化闭环：

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│  1. 盲审质检阶段 (SubAgent 盲审)                                                 │
│  - 工作流在各个关键节点自动启动 `blind-reviewer` 进行冷酷苛刻质检                │
│  - 自动装载【技能默认基线】+【项目专属进化规则 (`./learnings/<phase_id>.md`)】   │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ 生成初始产物 / 呈现给主编审阅
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│  2. 主编人工精修与反馈 (Human Review)                                            │
│  - 主编对生成的产物（大纲、正文、插图提示词、微信HTML、海报文案）进行修改批注    │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ 在对话框中回复 /workflow-learn
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│  3. 规则沉淀与自动进化 (Self-Evolving Learning)                                  │
│  - 系统自动比对人工修改 Diff，提炼出黑名单 (Anti-Patterns) 与金句例句 (Golden)   │
│  - 首次反哺自动按需建库，增量落盘至根目录 `./learnings/<phase_id>.md`            │
│  - 以后每次盲审该环节时，SubAgent 自动吸收主编的新偏好，实现免人工审查！         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### ⚙️ 分环节确定性路由表 (`phase_id`)

| 环节标识 (`phase_id`) | 覆盖的创作环节 | 审查资产文件 | 对应的项目进化规则路径 (项目根目录) |
| :--- | :--- | :--- | :--- |
| **`article_outline`** | 文章大纲阶段 | `./<slug>/outline.md` | `./learnings/article_outline.md` |
| **`article_content`** | 文章正文阶段 | `./<slug>/<slug>.md` | `./learnings/article_content.md` |
| **`illustrations`** | 正文插图阶段 | `./<slug>/assets/illustration_*.md` | `./learnings/illustrations.md` |
| **`weixin`** | 微信公众号排版 | `./<slug>/mp_article.html` | `./learnings/weixin.md` |
| **`poster_blueprint`** | 海报故事线蓝图 | 海报章节与版式拆分方案 | `./learnings/poster_blueprint.md` |
| **`poster_config`** | 单张海报 Prompt | `./<slug>/assets/poster_*.md` | `./learnings/poster_config.md` |
| **`poster_post`** | 海报社媒文案 | `./<slug>/poster_post.md` | `./learnings/poster_post.md` |
| **`<new_phase_id>`** | (未来扩展新环节) | (新场景产物) | `./learnings/<new_phase_id>.md` |

---

## 🛠️ 底层纯粹原子技能库

| 技能 ID | 技能定义说明 (`SKILL.md`) | 核心功能特性 |
| :--- | :--- | :--- |
| **`hot-topics`** | [`skills/hot-topics/SKILL.md`](skills/hot-topics/SKILL.md) | 自动抓取全网热榜 (今日热榜 https://tophub.today/)，去重聚合热点并提供科普创作切入建议。 |
| **`article-writer`** | [`skills/article-writer/SKILL.md`](skills/article-writer/SKILL.md) | 长文与大纲写作，支持干货指南、科技深度评论、社会观察、科普解说、故事叙事 5 种文风自适应识别。 |
| **`illustration-designer`** | [`skills/illustration-designer/SKILL.md`](skills/illustration-designer/SKILL.md) | 单图视觉隐喻设计，提炼认知概念与低科技物件，设计 16:9 纯白背景与原生中文批注提示词。 |
| **`wx-formatter`** | [`skills/wx-formatter/SKILL.md`](skills/wx-formatter/SKILL.md) | 微信公众号离线排版，套用防擦除视觉样式系统，自动消解表格为双色卡片，输出带视口的原生 HTML。 |
| **`poster-designer`** | [`skills/poster-designer/SKILL.md`](skills/poster-designer/SKILL.md) | 手绘图文海报设计，匹配 10 大经典版式与莫兰迪配色，输出防乱码的 3:4 生图配置与极简社媒文案。 |
| **`blind-reviewer`** | [`skills/blind-reviewer/SKILL.md`](skills/blind-reviewer/SKILL.md) | **通用自进化盲审引擎**，接收审查资产与规则路径，执行苛刻质检并输出二元裁决报告。 |

---

## 🎨 配图角色 IP 自定义指引

技能套件默认使用 **“小智”**（方块头、单天线、点点眼小机器人）作为配图与海报的主角形象。如果你希望使用自定义的角色 IP：

> [!IMPORTANT]
> **IP Mascot 校验优先级（统一文件名为 `character_ip.md`，只要找到一份即生效）**：
> 1. **主题目录级**：在具体的文章目录下新建 `./<主题目录>/character_ip.md`。
> 2. **项目根目录级（推荐）**：在项目根目录下新建 `./character_ip.md`。
> 3. **默认回退**：读取技能内置的默认 IP（小智）。

---

## 📁 项目目录结构

```text
ai-creator-skills/
├── GEMINI.md                               # 项目 Agent 规则与配置
├── LICENSE                                 # MIT 开源协议许可文件
├── README.md                               # 本文档
├── character_ip.md                         # (可选) 项目级自定义 IP 规范模板 (小智 Mascot 预置)
├── learnings/                              # (动态按需生成) 首次人审运行 /workflow-learn 后自动创建的分环节自进化审稿规则库
│   ├── article_outline.md                  # 文章大纲自进化规则
│   ├── article_content.md                  # 文章正文自进化规则
│   ├── illustrations.md                    # 正文插图自进化规则
│   ├── weixin.md                           # 微信排版自进化规则
│   ├── poster_blueprint.md                 # 海报蓝图自进化规则
│   ├── poster_config.md                    # 单张海报 Prompt 自进化规则
│   └── poster_post.md                      # 海报社媒文案自进化规则
├── docs/                                   # 项目设计文档与 ADR 决策记录
│   ├── adr/                                # 目录结构规范说明
│   └── agents/
├── skills/                                 # 底层纯粹原子技能 (可单独安装)
│   ├── hot-topics/                         # 1. 热门话题抓取
│   ├── article-writer/                     # 2. 文章与大纲写作
│   ├── illustration-designer/              # 3. 单图视觉隐喻设计
│   ├── wx-formatter/                       # 4. 微信公众号排版
│   ├── poster-designer/                    # 5. 手绘海报设计
│   └── blind-reviewer/                     # 6. 通用自进化盲审引擎
├── workflows/                              # 上层业务工作流 (自动化编排与审查)
│   ├── article.md                          # 写文章工作流 (/写文章)
│   ├── illustrations.md                    # 正文插图工作流 (/正文插图)
│   ├── weixin.md                           # 微信公众号排版工作流 (/微信公众号)
│   ├── poster.md                           # 图文海报工作流 (/海报)
│   └── learn.md                            # 规则自进化反哺工作流 (/workflow-learn)
└── <topic-slug>/                           # 实例：主题文件目录 (拟定大纲时自动新建)
    ├── outline.md                          # 文章大纲
    ├── <topic-slug>.md                     # 文章正文
    ├── character_ip.md                     # (可选) 主题级自定义 IP 规范
    ├── mp_article.html                     # 微信公众号离线网页
    ├── poster_post.md                      # 社媒纯文本文案
    ├── assets/                             # 生图提示词配置文件
    │   ├── illustration_1.md               # 插图 1 配置文件
    │   ├── poster_1.md                     # 海报 1 配置文件
    │   └── poster_2.md                     # 海报 2 配置文件
    └── images/                             # 图片渲染产物目录 (按需生成)
        ├── illustration_1.png ~ illustration_N.png
        └── poster_1.png ~ poster_N.png
```

---

## 📄 开源协议 (License)

本项目基于 [MIT License](LICENSE) 开源协议发布，您可以自由进行复制、修改、分发及商业化使用。详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ for AI Content Creators & Editors**

</div>