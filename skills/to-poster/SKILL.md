---
name: to-poster
description: 将正文与插图转化为自媒体手绘图文海报与 200 字发布文案的 Skill。扫描主题工作区 (./<article-slug>/) 下的文章 Markdown 与插图配置，重构为 N 张手绘海报配置文件 (assets/poster_1.md ~ poster_N.md) 及纯文本社媒文案 (poster_post.md)，支持 5 大经典版式与莫兰迪 3:4 小红书风格，经多阶段 SubAgent 盲审通过后归档。默认仅生成配置文件（配置先行 / 按需延迟生图），仅在有明确生图指令时渲染图片。
---

# Multi-Image Poster Converter Skill (`to-poster`)

本技能指导 AI Agent 读取主题工作区（`./<article-slug>/`）内的干货长文（`./<article-slug>/<article-slug>.md`）与已归档的正文插图方案（`assets/illustration_*.md`），将长文干货与插图视觉隐喻相结合，重构成 N 张包含高密度干货、精细版式与小智 IP 形象的手绘图文海报说明文档（`assets/poster_1.md ~ poster_N.md`）与 200 字纯文本社媒发布文案（`poster_post.md`）。

引入 **海报审查 SubAgent (`poster_reviewer`)** 机制，采用 **多阶段与 N 个 SubAgent 并发审查模式**，打磨生成包含 🟢 **英文生图版 Prompt** 与 🔵 **中文确认版 Prompt** 的海报文档与纯文本发布文案并归档。

---

## 核心设计原则 (Core Principles)

1. **配置先行 / 按需延迟生图 (Lazy Generation)**：
   - 技能默认**仅生成海报 Markdown 配置文件**（`assets/poster_1.md` ~ `poster_N.md`）及社媒发布文案（`poster_post.md`）。
   - **默认绝不自动调用生图工具**，仅在主人明确发出生图指令时，才批量调用生图工具生成 `images/poster_1.png ~ poster_N.png`（3:4 比例）。
2. **社媒发布文案“绝对纯文本”硬性隔离 (Clean Plain Text Rule)**：
   - 发布文案 `poster_post.md` **必须绝对使用纯文本格式**，绝对严禁使用任何 Markdown 语法标记（如加粗 `**`、斜体 `*`、标题 `#`、列表 `- ` 或链接 `[text](url)`），防止用户复制粘贴到小红书、朋友圈、即刻等自媒体平台时残留源码符号。
   - 标题备选矩阵中，**第一备选项必须显式保留原文章大标题 H1**。
3. **原生中文保留与硬性防乱码指令 (Anti-Gibberish Protocol)**：
   - 🟢 英文生图版 Prompt 中，单引号 `'...'` 括起来要求渲染的核心标题与短语必须保持**原生中文**（严禁误翻译成英文）。
   - Prompt 结尾必须强制写入防杜撰/去乱码控制指令：`strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes`。
4. **视觉风格与莫兰迪美学 (Morandi Aesthetics & 3:4 Aspect Ratio)**：
   - 统一使用 Q 版软萌图文科普风格、暖米白羊膏纸质感背景（`#FAF6F0`）、莫兰迪配色体系与 3:4 小红书黄金比例。
5. **共享 IP 形象短路加载机制 (IP Mascot Short-Circuit Routing)**：
   - 默认复用共享主角 **小智 (Xiao Zhi)**（小方块头、点点眼、单天线、瘦长手脚、Deadpan 严肃呆萌气质）。
   - 按优先级**检查且仅读取 1 份** IP 规范：1) 主题级 `./<article-slug>/ip.md` -> 2) 全局级 `docs/domain/character_ip.md` -> 3) 技能默认 [`references/character_ip.md`](references/character_ip.md)。
6. **多阶段 SubAgent 审查闭环 (Multi-stage Reviewer Loop)**：
   - 包含阶段一（整体拆分蓝图审查）、阶段二（N 个并发 SubAgent 独立单张海报审查）以及阶段三（纯文本社媒发布文案审查），上限重写 8 次。

---

## 关联参考规范

在执行本技能时，Agent 必须主动读取并严格遵循以下文件：
- **共享 IP 形象规范**：[`references/character_ip.md`](references/character_ip.md)
- **手绘视觉风格指南**：[`references/style_guide.md`](references/style_guide.md)
- **海报 10 大经典版式与 Prompt 模板**：[`references/layouts.md`](references/layouts.md)
- **海报审查 SubAgent 裁决与审查标准手册**：[`references/poster_reviewer_standards.md`](references/poster_reviewer_standards.md)

---

## 详细执行步骤

### 步骤一：上下文扫描、插图隐喻继承与海报拆分蓝图提炼

1. **扫描主题工作区与资产**：
   - 确定主题 slug（`<article-slug>`）。读取 `./<article-slug>/<article-slug>.md` 长文内容。
2. **正文插图隐喻继承与小智动作延伸 (Illustration Metaphor Inheritance)**：
   - 读取 `./<article-slug>/assets/illustration_*.md` 方案文件，提取正文插图中已获批的 `核心认知锚点`、`低科技物件` 与 `小智动作`。
   - **视觉印记延伸规则**：海报在演绎对应章节的干货时，**必须优先继承并扩展正文插图中的核心隐喻与小智动作**（例如：若正文插图 `illustration_1.md` 设为“小智操作三棱镜”，海报在拆解该部分要点时应延伸为“小智手握三棱镜在卡片间分流红蓝要素”），形成跨媒介视觉连贯印记。
3. **划定 N 张海报拆分蓝图与版式映射 (Layout Mapping Matrix)**：
   - 对照内容属性，从 **10 大经典版式库**（`references/layouts.md`）中精准映射最契合的版式：
     - 组图封面 / 重磅观点 ➔ `1. Hero 破题冲击版`
     - 4-6 项并列要点 / 规则 / 矩阵 ➔ `2. 四宫格/六宫格干货版`
     - 新旧对比 / 痛点 vs 优势 / 正误对照 ➔ `3. 左右/上下双轨对比版`
     - 多阶段流水线 / 分步 Action Items ➔ `4. 纵向链路/管道流程版`
     - 单点核心概念展开 / 系统生态拆解 ➔ `5. 中心破局/脑图辐射版`
     - 组图封底总结 / 金句结语 / 唤起转发 ➔ `6. 极简金句闭环版`
     - 硬核技术测评 / 性能提升 / 基准参数 ➔ `7. 数据/指标面板版`
     - 常见误区澄清 / 实战避坑 / 红黑榜 ➔ `8. 避坑拆弹/红黑榜版`
     - 自问自答解密 / 热点疑问答疑 ➔ `9. Q&A 交互问答对话版`
     - 技术演进史 / 范式转移切片 ➔ `10. 时间线/演进史切片版`

---

### 步骤二：阶段一审查——全局海报 SubAgent 审查拆分蓝图

1. **发起全局审稿 SubAgent**：
   - 显式调用 `invoke_subagent` 工具发起 `poster_reviewer` 审稿子进程，读取并执行 `references/poster_reviewer_standards.md` 中【阶段一：海报整体拆分方案审查标准】。
2. **拆分蓝图判定**：
   - 若判定 **`[REJECT]`**：根据结构化意见重写拆分方案并重新送审（上限 8 次）。
   - 直至判定 **`[PASS]`**，方可进入阶段二。

---

### 步骤三：阶段二审查——并行启动 N 个 SubAgent 并发审查单张海报

针对获批的第 1 到 N 张海报，**同时/并行启动 N 个独立的海报审查 SubAgent**：

1. **撰写单张海报草稿**：
   - 依据映射矩阵从 `references/layouts.md` 选取最契合的版式，组合 2-4 个精细手绘视觉组件。
   - 注入继承自正文插图的小智动作延伸与画面隐喻。
   - 编写中文确认版 Prompt 与英文生图版 Prompt（包含单引号原生中文与去乱码控制指令）。
2. **并发 SubAgent 审稿与独立迭代**：
   - 分别发起 `poster_reviewer` 审稿子进程对第 i 张海报草稿（i = 1..N）进行审查。
   - 若判定 **`[REJECT]`**：仅针对第 i 张海报进行重写修正并重新送审（上限 8 次）。
   - 若判定 **`[PASS]`**：将定稿文档保存至 `./<article-slug>/assets/poster_i.md`。

---

### 步骤四：阶段三审查——200 字纯文本社媒发布文案审查与归档

1. **撰写纯文本发布文案**：
   - 提炼 200 字左右适合配合海报组图发帖的文案。
   - **绝对纯文本格式**：严禁出现 `**`、`#`、`[text](url)` 等 Markdown 语法。
   - **标题矩阵**：标题列表中，**第一条必须显式保留文章大标题 H1**。
2. **发布文案审查与存盘**：
   - 发起 `poster_reviewer` 审稿子进程审核文案，通过后保存至 `./<article-slug>/poster_post.md`。

---

### 步骤五：按需生图处理与结构化汇报

1. **按需生图判断**：
   - 默认跳过生图。仅当用户显式提出生图指令时，读取各 `assets/poster_i.md` 中的英文生图 Prompt，批量调用生图工具渲染图片，存入 `./<article-slug>/images/poster_i.png`。
2. **结构化汇报**：
   向控制台/对话框汇报：
   ```markdown
   💡 手绘图文海报配置文件与 200 字纯文本发布文案已完成审查并归档！
   - 海报配置文件：[./<article-slug>/assets/poster_1.md](./<article-slug>/assets/poster_1.md) ~ [poster_N.md](./<article-slug>/assets/poster_N.md)
   - 发布文案归档：[./<article-slug>/poster_post.md](./<article-slug>/poster_post.md)
   - 生图产物状态：已完成配置（等待生图指令）
   ```
