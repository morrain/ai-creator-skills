# Storyboard & Unit Designer Reviewer Standards (视频单元与分镜动作链盲审标准)

本标准供 SubAgent 对 `video-storyboard-designer` 生成的视频单元配置文件（`unit_XX/BRIEF.md`）进行自动化质检。

---

## 1. 动态动作链连贯性 (Motion Chain Continuity)

- 必须包含完整的 3 幕动作演化描述（`Act 1: 引出问题` -> `Act 2: 核心动作` -> `Act 3: 交付结果`）。
- Act 2 的核心动作必须优先继承并延伸原正文插图文件（`illustration_*.md`）中确立的物理隐喻。
- IP Mascot 必须是动作的执行者，严禁沦为背景贴纸或无意义装饰。
- **二次分镜与元素清单硬卡点**: `BRIEF.md` 的 `## Intent` 正文必须明确包含全量画面元素清单（Scene Element Inventory）与带时间戳的镜头切片划分（Sub-shot Timeline Breakdown），特别是对 >20s 的长单元，严禁缺少基于口播文案的二次分镜切片！

---

## 2. 视觉 DNA 与生图 Prompt 规范 (Visual DNA & Prompt Gates)

- **构图与背景**: 强制 16:9 横版构图，纯白背景 (`#FFFFFF`)，黑色手绘线条质感 (Black minimalist hand-drawn line art)。
- **原生中文批注**: 英文 Prompt 中的文本批注须强制保留在引号内部的原生中文（如 `'数据流'`、`'56% OFF'`）。
- **图片与视频参数**: 英文 Prompt 末尾须附加 `--ar 16:9 --v 6.0` 或 i2v 生成控制参数。
