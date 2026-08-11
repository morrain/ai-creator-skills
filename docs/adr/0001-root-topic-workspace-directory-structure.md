# 1. 采用项目根目录主题工作区 (`./<article-slug>/`) 组织产物

- **状态**: 已接受 (Accepted)
- **日期**: 2026-08-11

## 上下文与问题陈述 (Context)

`ai-creator-skills` 包含文章写作、正文插画设计、手绘海报生成等多个跨媒介技能。一个主题在创作过程中会产生多种文件：
- 文章 Markdown 文件 (`<article-slug>.md`)
- 微信公众号离线网页 (`mp_article.html`)
- 插图配置文件 (`assets/illustration_1.md` ~ `illustration_N.md`)
- 海报配置文件与社媒文案 (`assets/poster_1.md` ~ `poster_N.md` / `poster_post.md`)
- 最终按需生成的图片素材 (`images/illustration_1.png`, `images/poster_1.png`)

我们需要决定如何在文件系统中组织这些跨技能的产物，以便于用户查阅、发布和迁移。

## 决策 (Decision)

我们决定：
1. 在 `articles` 技能的大纲阶段，自动提取/生成简短英文连字符命名的 `<article-slug>`（例如 `iphone-18-launch`）。
2. 在项目根目录下直接新建主题工作区文件夹 `./<article-slug>/`，并将大纲保存为固定的 `outline.md`。
3. 后续所有关联技能（`articles`、`illustrations`、`to-wx`、`to-poster`）的产物均统一存入该主题工作区中，不再采用深层嵌套的 `output/articles/<slug>` / `output/posters/<slug>` 分离目录。

示例目录结构：
```text
ai-creator-skills/
├── iphone-18-launch/                 # 主题工作区 (Topic Workspace)
│   ├── outline.md                    # 文章大纲 (固定文件名)
│   ├── iphone-18-launch.md           # 文章正文
│   ├── mp_article.html              # 微信公众号离线网页
│   ├── poster_post.md               # 200 字纯文本社媒发布文案
│   ├── assets/                       # 衍生配置文件目录
│   │   ├── illustration_1.md         # 插图 1 配置文件 (Markdown 模版)
│   │   ├── illustration_2.md         # 插图 2 配置文件
│   │   ├── poster_1.md              # 海报 1 配置文件
│   │   └── poster_2.md              # 海报 2 配置文件
│   └── images/                       # 渲染图片素材目录 (按需生图产物)
│       ├── illustration_1.png ~ illustration_N.png # 按需生成插图产物
│       └── poster_1.png ~ poster_N.png            # 按需生成海报产物
```

## 结果与权衡 (Consequences)

### 正面效果 (Positive)
- **极高的内聚性**：同一个主题的所有资产（文字、配图配置、海报、生成图片）归集在单一文件夹中，一目了然，方便用户一键打包、导出或发布。
- **消除了跨技能路径不一致**：下游视觉技能直接定位根目录下的主题工作区，无需拼装复杂的多层 `output/...` 相对路径。

### 负面效果/风险 (Negative)
- **根目录条目增加**：当主题变多时，项目根目录下会有多个 `<article-slug>` 文件夹（可通过 `.gitignore` 或归档文件夹处理历史主题）。
