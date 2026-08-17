---
name: workflow-poster
command: /海报
description: 知识总结与社媒海报生成工作流。当用户发送 /知识海报 指令、或需要将长文/知识点转化为多张手绘风格海报与社媒文案时唤起。
---

# 🖼️ 图文海报派生业务工作流 (Poster Business Workflow)

本工作流为 `ai-creator-skills` 项目的多图文海报与社媒文案派生管道。负责读取主题工作区 `./<article-slug>/` 目录中的文章与插图资产，提炼 N 张海报故事线蓝图，从 10 大版式库中匹配各张版式，并发调度底层原子技能 `poster-designer` 渲染单张海报设计，运行 3 阶段 SubAgent 审稿闭环，在 `assets/poster_N.md` 落盘海报配置，生成 100% 纯文本社媒文案 `poster_post.md`，并在指示下延时渲染图片至 `images/poster_N.png`。

---

## 核心设计原则 (Core Principles)

1. **配置文件先行与按需延时生图 (Strict Lazy Generation)**：
   - 默认仅生成海报 Markdown 配置文件 `assets/poster_1.md ~ poster_N.md` 与社媒文案 `poster_post.md`。
   - **严禁自动调用 `generate_image` 工具**生图，除非用户下达“开始生图”指令。
2. **社媒文案纯文本隔离 (Clean Plain Text Rule)**：
   - `poster_post.md` 绝对保持 100% 纯文本格式，严禁使用 `**`、`#`、`[text](url)` 等 Markdown 标记，防止复制粘贴时漏掉语法符号。
3. **内容属性 ➔ 10 大版式智能映射 (Layout Mapping Matrix)**：
   - 组图封面/重磅观点 ➔ `1. Hero 破题冲击版`
   - 并列要点 ➔ `2. 四宫格/六宫格干货版`
   - 对比分析 ➔ `3. 双轨对比版`
   - 步骤流程 ➔ `4. 纵向管道流程版`
   - 生态拆解 ➔ `5. 脑图辐射版`
   - 末页总结 ➔ `6. 金句闭环版`
   - 参数指标 ➔ `7. 数据面板版`
   - 避坑提醒 ➔ `8. 避坑拆弹版`
   - 问答解密 ➔ `9. Q&A 问答版`
   - 技术演进 ➔ `10. 时间线演进版`
4. **插图隐喻继承与 IP Mascot 动作延伸 (Illustration Metaphor Inheritance)**：
   - 海报在演绎对应章节的干货时，**必须优先继承并扩展正文插图配置 (`assets/illustration_*.md`) 中的核心隐喻与 IP Mascot 动作**。
5. **深度长文全渠道留言与私信引导 (Dual-Channel Messaging CTA Guidance)**：
   - **海报画面引导**：海报设计（特别是封底页及海报 Footer 区域）包含手绘胶囊/贴纸（如 `'💬 留言或私信获取完整拆解'`）。
   - **文案互动引导**：`poster_post.md` 社媒文案在正文末尾、话题标签前，强制加入纯文本格式的醒目引导句（如 `👇 想要解锁完整深度拆解？留言或者私信获取 💬`），避开平台外链限制并安全引导读者互动。

---

## 详细工作流步骤

### 阶段一：上下文扫描、长文拆分蓝图与阶段一审稿

1. **扫描主题工作区与干货**：
   - 读取 `./<article-slug>/<article-slug>.md` 与 `./<article-slug>/assets/illustration_*.md`。
2. **海报故事线蓝图提炼与版式映射**：
   - 规划 N 张海报（通常 3-6 张滑动组图），依据映射矩阵匹配各卡片版式，继承正文插图的 IP Mascot 动作。
3. **阶段一 SubAgent 全局蓝图审稿**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/poster_blueprint.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/poster-designer/references/poster_reviewer_standards.md` 与 `learnings_file: ./learnings/poster_blueprint.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards: skills/poster-designer/references/poster_reviewer_standards.md`）。审查整体拆分逻辑，修正直至 `[PASS]`（上限 8 次）。

---

### 阶段二：并发调度原子 Skill `poster-designer` 与阶段二审查

1. **并发调度原子技能 `poster-designer`**：
   - 针对获批的第 1~N 张海报，并发调用原子技能 `poster-designer` 生成各自的具体设计草稿。
2. **并发 SubAgent 单张审稿与独立迭代**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/poster_config.md`。若存在，启动 N 个 `blind-reviewer` SubAgent（传入 `default_standards: skills/poster-designer/references/poster_reviewer_standards.md` 与 `learnings_file: ./learnings/poster_config.md`）；若不存在，启动 N 个 `blind-reviewer` SubAgent（仅传入 `default_standards: skills/poster-designer/references/poster_reviewer_standards.md`）。审查单张海报（校验去乱码指令 `strictly NO fake subtext...`、单引号原生中文及莫兰迪 3:4 规范）。
   - 重试直至全部判定 `[PASS]`，落盘为 `./<article-slug>/assets/poster_1.md` ~ `poster_N.md`。

---

### 阶段三：社媒文案合成与阶段三审查

1. **社媒文案合成 (`poster_post.md`)**：
   - 📌 **标题顶部独立矩阵 (共 8 个备选标题：3 个 ≤ 20 字 + 1 个 ≤ 16 字)**：文案最顶部单独列出 8 个爆款备选标题。**第一备选标题必须严格为母版正文大标题 H1**（固定列举，无需标注字数）。8 个备选标题必须满足梯度字数结构：**包含 3 个不超过 20 字的标题、1 个不超过 16 字的短标题，其余 4 个字数不限制**。在满足字数限制的前提下，标题字数要尽可能多、尽可能完整表达原文意思。**除了第 1 个固定列举的文章大标题外，其它所有备选标题必须在标题末尾使用括号显式标注字数**（如 `示例爆款备选标题文本 (19字)`）。
   - 🎨 **高密度 Emoji 视觉排版与 100 字内极简**：正文控制在 100 字以内，**每一行/每个逻辑短句开头必须搭配与语义契合的 Emoji 表情符号**（如 🌤️, 💡, 🔴, 🔵, 👀, ✨, 👇, 🚀），采用小红书/即刻风格的极简短句换行结构，视觉层次丰富、生动吸睛，严禁大段无 Emoji 纯文字。
   - 💬 **深度长文留言与私信引导 (Messaging CTA)**：正文结尾、话题标签之前，**强制加入 1-2 行醒目的留言或私信引导提示句**（如 `👇 想要解锁完整深度拆解？留言或者私信获取 💬`），规避各平台外链限制并安全引导粉丝互动。
   - 🗣️ **评论区引爆讨论开放式提问 (Open-Ended Discussion Question)**：话题标签之后，专门设计一段由作者发布/置顶到评论区的开放式提问文案（如 `💡 大家在实际日常中，觉得哪一步最难落地？欢迎在评论区聊聊你的看法👇`），直击核心争议点或实践痛点，引爆评论区讨论热度。
   - 🏷️ **6-10 个热门话题标签**：文案最末尾**强制输出 6-10 个**以 `#` 开头的相关热门话题标签（如 `#科普 #物理学原理 #干货总结 #冷知识 #光学原理 #涨知识`）。
   - ⚠️ **纯文本硬性限制 (Clean Plain Text Only)**：发布文案 `poster_post.md` **必须绝对使用纯文本格式**，严禁使用任何 Markdown 语法标记（如加粗 `**`、斜体 `*`、标题 `##`、列表 `- ` 或链接 `[text](url)`），仅靠换行与 Emoji 符号进行视觉结构分割。
2. **阶段三 SubAgent 文案审稿与落盘**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/poster_post.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/poster-designer/references/poster_reviewer_standards.md` 与 `learnings_file: ./learnings/poster_post.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards: skills/poster-designer/references/poster_reviewer_standards.md`）。审查 `poster_post.md` 的顶部 8 个备选标题矩阵（含 1 个固定文章 H1 大标题、3 个 ≤ 20 字 + 1 个 ≤ 16 字短标题，满足字数限制下尽可能多且完整表达原文含义，且除第 1 个标题外其余标题末尾均显式带有 `(X字)` 括号字数标注）、高密度 Emoji 表情覆盖率、100 字限制、纯文本隔离度、留言/私信引导句与 6-10 个 `#话题标签` 完整性，修正直至 `[PASS]`，落盘至 `./<article-slug>/poster_post.md`。
3. **结构化汇报与人工确认提示**：
   - 呈报成果与可点击链接（[`./<article-slug>/poster_post.md`](./<article-slug>/poster_post.md) 及配置文件）。
   - **统一人工确认提示**：
     > 💡 **主编审阅与自进化提示**：
     > 1. 预览海报配置及社媒文案满意后，请在对话框回复 **“开始生图”** 以批量渲染海报图片。
     > 2. 如对海报配置文件、故事线拆分或社媒文案进行了人工修改，请在对话框回复 **`/workflow-learn`**，系统将自动提炼您的偏好规则并沉淀落盘，让后续盲审标准自动进化！
