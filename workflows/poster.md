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
   - 📌 **四大平台 (小红书/微信视频号/抖音/快手) 深度适配标题矩阵 (共 8 个备选标题)**：文案最顶部单独列出 8 个针对四大平台算法推荐机制、受众偏好及字数折叠限制深度适配的爆款备选标题。**第一备选标题必须严格为母版正文大标题 H1**（固定首位，无需标注字数）。其余 7 个备选标题必须根据以下四大平台规格精准定制（除了第 1 个 H1 标题外，其余所有标题末尾必须使用括号显式标注字数，如 `示例标题 (18字)`）：
     1) **小红书爆款规格 (≤ 20 字，黄金曝光 15 字内前置)**：适配小红书卡片折叠限制（前 15 字为首屏焦点区），融合 SEO 检索关键词、情绪共鸣与避坑/干货切入点（包含 **至少 2 个**）；
     2) **微信视频号/公众号规格 (≤ 16 字，无折叠单行精炼)**：适配微信卡片与朋友圈分享单行显示限制（防止长标题换行截断），突出专业深度、权威解读与知识点定性（包含 **至少 2 个**）；
     3) **抖音爆款规格 (≤ 30 字，前 12 字痛点/悬念钩子)**：适配抖音完播/互动算法，前 12 字前置痛点冲突、反常识悬念或高刺激情绪钩子，全标题 30 字内完整表达（包含 **至少 2 个**）；
     4) **快手落地实用规格 (≤ 25 字，前置接地气抓手)**：适配快手社区私域信任算法，强调保姆级实用技巧、避坑拆弹指北与通俗落地解说（包含 **至少 1 个**）。
   - 🎨 **高密度 Emoji 视觉排版与 100 字内极简干货 (适配小红书 CES 算法与快手极简流)**：正文控制在 100 字以内，**每一行/每个逻辑短句开头必须搭配与语义契合的 Emoji 表情符号**（如 🌤️, 💡, 🔴, 🔵, 👀, ✨, 👇, 🚀），采用小红书/即刻风格的极简短句换行结构，视觉层次丰富、生动吸睛，严禁大段无 Emoji 纯文字。
   - 💬 **深度长文留言与私信引导 (Messaging CTA，适配全平台外链避坑)**：正文结尾、话题标签之前，**强制加入 1-2 行醒目的留言或私信引导提示句**（如 `👇 想要解锁完整深度拆解？留言或者私信获取 💬`），规避各平台外链截流并安全引导粉丝互动留存。
   - 🗣️ **评论区引爆讨论开放式提问 (Open-Ended Question，适配微信/小红书互动算法)**：话题标签之后，专门设计一段由作者发布/置顶到评论区的开放式提问文案（如 `💡 大家在实际日常中，觉得哪一步最难落地？欢迎在评论区聊聊你的看法👇`），直击核心争议点或实践痛点，提高互动比率。
   - 🏷️ **6-10 个热度降序话题标签 (Topic Tags，适配小红书/抖音 SEO 检索算法)**：文案最末尾**强制输出 6-10 个**以 `#` 开头的相关话题标签。拟定标签时**必须深入结合本文核心主题以及当前各社交平台的相关话题热度**，且**必须严格按照热度与覆盖范围从高到低衰减进行降序排列**（排列顺序：全网/全行业高热大词 ➔ 垂直领域热门标签 ➔ 本文核心概念细分标签，如 `#AI大模型 #人工智能 #LLM原理 #Agent架构 #状态机`）。
   - ⚠️ **纯文本硬性限制 (Clean Plain Text Only)**：发布文案 `poster_post.md` **必须绝对使用纯文本格式**，严禁使用任何 Markdown 语法标记（如加粗 `**`、斜体 `*`、标题 `##`、列表 `- ` 或链接 `[text](url)`），仅靠换行与 Emoji 符号进行视觉结构分割。
2. **阶段三 SubAgent 文案审稿与落盘**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/poster_post.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/poster-designer/references/poster_reviewer_standards.md` 与 `learnings_file: ./learnings/poster_post.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards: skills/poster-designer/references/poster_reviewer_standards.md`）。审查 `poster_post.md` 的顶部 8 个备选标题矩阵（含 1 个固定文章 H1 大标题，以及针对小红书 ≤20字、微信视频号 ≤16字、抖音 ≤30字、快手 ≤25字四大平台算法/折叠深度适配的标题，除第 1 个标题外其余标题末尾均显式带有 `(X字)` 括号字数标注）、高密度 Emoji 表情覆盖率、100 字限制、纯文本隔离度、留言/私信引导句与 6-10 个 `#话题标签` 完整性，修正直至 `[PASS]`，落盘至 `./<article-slug>/poster_post.md`。
3. **结构化汇报与人工确认提示**：
   - 呈报成果与可点击链接（[`./<article-slug>/poster_post.md`](./<article-slug>/poster_post.md) 及配置文件）。
   - **统一人工确认提示**：
     > 💡 **主编审阅与自进化提示**：
     > 1. 预览海报配置及社媒文案满意后，请在对话框回复 **“开始生图”** 以批量渲染海报图片。
     > 2. 如对海报配置文件、故事线拆分或社媒文案进行了人工修改，请在对话框回复 **`/workflow-learn`**，系统将自动提炼您的偏好规则并沉淀落盘，让后续盲审标准自动进化！
