---
name: illustrations
description: 根据文章内容设计正文配图与手绘插画的 Skill。参考 article-illustrations 规范与 assets 配置格式，提炼认知锚点与怪诞隐喻，为每张插图在 ./<article-slug>/assets/ 目录下生成独立的配置文档 (illustration_1.md ~ illustration_N.md)；每张插图配置生成后必须发起 SubAgent 盲审，校验提示词逻辑自洽性与 IP 形象动作设计；默认只生成配置文件不调用 generate_image 生图（按需延迟生图 Lazy Generation），全部完成后输出结构化汇报。适用于用户提出“文章配图”、“正文插图”、“插图配置”、“小智配图”、“手绘插画”、“配图建议”等任务。
---

# Illustrations Skill (文章怪诞正文配图与插画设计)

本技能指导 AI Agent 分析文章内容，提炼核心认知动作与视觉隐喻，在项目对应的主题工作区 `assets/` 目录下为每张插图生成独立的 Markdown 配置文件（`./<article-slug>/assets/illustration_1.md` ~ `illustration_N.md`），并通过 SubAgent 盲审把关逻辑与 IP 动作设计。**默认只生成配置文件，绝不自动调用生图工具**，仅在主人明确指示时延迟批量生成图片。

---

## 核心设计原则

1. **配置文件先行与按需生图 (Strict Lazy Generation)**：
   - 默认**仅生成插图 Markdown 配置文件**（`assets/illustration_1.md` ~ `illustration_N.md`）。
   - **严禁自动调用 `generate_image` 工具**生图，除非主人明确给出“开始生图/生成图片”指令。
2. **SubAgent 逐张插图盲审 (SubAgent Review Loop)**：
   - 每生成一张 `illustration_N.md` 配置文件，必须显式调用 SubAgent 发起盲审。
   - 参照 `references/illustration_reviewer_standards.md` 审核提示词是否精准表征原文逻辑、小智 IP 形象的动作与低科技物件设计是否符合内容需要、原生中文批注与 16:9 约束是否完备。若判定为 `[REJECT]`，针对性修正重写直至 `[PASS]`（重试上限 5 次）。
3. **主题工作区 `assets/` 与 `images/` 目录分工 (Directory Separation)**：
   - 遵照 `ADR-0001` 规范，所有插图配置文件存放在 `./<article-slug>/assets/` 目录下；按需生成的渲染图片统一存放在与 `assets` 同级的 `./<article-slug>/images/` 目录下。
4. **IP 形象前置短路路由 (Short-circuit IP Mascot Routing)**：
   - 在构建视觉方案前，Agent 按以下优先级**显式检查且仅加载 1 份** IP 规范（命中即止，短路终止）：
     1. 主题级：`./<article-slug>/ip.md` (或 `character_ip.md`)
     2. 全局级：`docs/domain/character_ip.md`
     3. 默认级：本技能 [`references/character_ip.md`](references/character_ip.md)
   - **干净隔离**：若命中主题级或全局级 IP 规范，绝对禁止继续读取 Skill 目录下的默认 IP 文件，彻底避免形象描述混合与上下文污染。
5. **怪诞手绘与原生中文批注**：
   - 纯白背景、黑线为主、少量红/橙/蓝批注、大面积留白。
   - **批注原生中文法则**：在英文 Prompt 中，手写批注词强制保留在双引号 `""` 或单引号 `'...'` 内部的原生中文，严禁机械翻译。

---

## 参考规范指引 (References)

在执行不同阶段的任务时，按需读取本技能 `references/` 下的子文档：

- [`references/illustration_reviewer_standards.md`](references/illustration_reviewer_standards.md)：插图配置与提示词 SubAgent 审稿手册（四大维度盲审与 `[PASS]` / `[REJECT]` 门禁）。
- [`references/style-dna.md`](references/style-dna.md)：视觉 DNA、色彩使用规范（黑主线/橙路径/红提醒/蓝补充）与绝对禁忌黑名单。
- [`references/character_ip.md`](references/character_ip.md)：小智 IP 形象定义、气场性格、动作池、视觉禁忌与二次开发扩展机制。
- [`references/composition-patterns.md`](references/composition-patterns.md)：8 种基础结构类型、原创隐喻 3 步推演法、低科技物件池。
- [`references/prompt-template.md`](references/prompt-template.md)：标准 16:9 横版英文生图 Prompt 模板与原生中文批注保留法则。
- [`references/qa-checklist.md`](references/qa-checklist.md)：生图阶段质量把关与修图/去标题提示词。

---

## 阶段工作流

### 阶段一：正文消化、插图配置生成、SubAgent 盲审与结果汇报

1. **定位目标主题工作区 (`<article-slug>`)**：
   - 若用户指定了 `<article-slug>`，定位至 `./<article-slug>/` 目录并读取文章。
   - 若未显式指定，自动扫描项目根目录下最近创建/修改的主题工作区文件夹（如 `./prevent-kidney-failure-guide/`）并向用户确认。
   - 确认 `./<article-slug>/assets/` 目录存在，若不存在则创建。

2. **前置短路加载 IP 形象规范 (Short-circuit IP Routing)**：
   - 按顺序依次检查：① `./<article-slug>/ip.md` (或 `character_ip.md`) ➔ ② `docs/domain/character_ip.md` ➔ ③ `skills/illustrations/references/character_ip.md`。
   - **命中即止**：仅读取第一份存在的 IP 文档作为本次任务的 IP Mascot 规范。若命中前两者，**切勿读取** Skill 目录下的默认 IP 文件，确保上下文干净隔离。

3. **消化文章与选择认知锚点**：
   - 提炼文章核心观点、认知转折点与适合视觉化的结构/流程/状态。
   - 参照 `composition-patterns.md`，使用“原创隐喻 3 步法”为每个锚点设计物理动作与低科技物件隐喻。
   - 控制插图数量在 4 ~ 8 张（短文 1-3 张，长文不超过 9 张）。

4. **逐张生成配置文件并触发 SubAgent 盲审**：
   对每一张拟设计的插图（`N = 1, 2, ...`）：

   **Step 3.1**：在 `./<article-slug>/assets/` 目录下生成 `illustration_N.md`，文件严格采用以下 Markdown 格式：

   ```markdown
   # 插图 N：[插图标题/核心隐喻简述]

   ## 插图元数据
   - **插图编号**：illustration_N
   - **对应章节**：[对应章节名称，如：第一章《...》]
   - **建议插入位置**：[具体段落或卡片引用之后]
   - **核心认知锚点**：[简述该插图表达的核心物理机制/逻辑转折]

   ## 🔵 中文确认版 Prompt & 视觉方案设计
   - **画面构图与核心视觉**：[16:9 横版，纯白背景，黑色手绘线条... 详细描绘小智动作、低科技物件、流向与视觉构图]
   - **手写中文批注**：`"批注1"`、`"批注2"`、`"批注3"`

   ## 🟢 英文生图版 Prompt (Image Generation Prompt)
   ```text
   A 16:9 minimalist hand-drawn illustration on a clean pure white background with black line art...
   ```
   ```

   **Step 3.2**：显式调用 SubAgent 盲审该 `illustration_N.md`：
   - 将 `illustration_N.md` 内容与对应章节原文提供给 SubAgent。
   - SubAgent 对照 `illustration_reviewer_standards.md` 进行盲审。
   - 若裁决为 `[REJECT]`，依据 SubAgent 的诊断报告修正 `illustration_N.md`，重新盲审，直至判定 `[PASS]`（上限 5 次）。

4. **全量完成结构化汇报**：
   当所有插图配置文件均落盘并打通 `[PASS]` 审核后，主 Agent 向主人输出结构化结果汇报，示例格式：

   ```markdown
   ### 🎨 插图配置文件生成与审稿完成汇报

   已在 `./<article-slug>/assets/` 目录下完成 **X 张**插图配置文件的生成与 SubAgent 盲审：

   | 插图编号 | 配置文件路径 | 对应章节 | 核心认知锚点 & 小智动作隐喻 | 盲审状态 |
   | :--- | :--- | :--- | :--- | :--- |
   | illustration_1 | [illustration_1.md](file:///path/to/assets/illustration_1.md) | 第一章《...》 | 小智操作三棱镜，分流红光大长腿与蓝光小碎步 | `[PASS]` |
   | illustration_2 | [illustration_2.md](file:///path/to/assets/illustration_2.md) | 第二章《...》 | 小智操控双光束发射器演示瑞利散射 | `[PASS]` |

   > 💡 **提示**：当前阶段仅生成 Markdown 配置文件（配置先行）。若需生成渲染图片，请回复指令 **“开始生图”**。
   ```

---

### 阶段二：按需生图与 QA 审核交付 (Lazy Generation Execution — 仅在主人明确指令时触发)

**当且仅当主人给出“开始生图”、“生成插图图片”等显式指令时**，方可进入本阶段：

1. **逐一解析配置文件并调用生图工具**：
   - 确认`./<article-slug>/images/` 目录存在，若不存在则创建。
   - 遍历 `./<article-slug>/assets/` 目录下的 `illustration_1.md` ~ `illustration_N.md`。
   - 提取每个文件中的 `🟢 英文生图版 Prompt`。
   - 调用 `generate_image` 工具生成 16:9 图片。
   - 图片存放在`./<article-slug>/images/` 目录下，命名为 `illustration_1.png` ~ `illustration_N.png`（或 `illu-01.png` ~ `illu-0N.png`）。

2. **质检与交付**：
   - 参照 `qa-checklist.md` 进行审查，若发现左上角标题等瑕疵，调用 `generate_image` 进行修正。
   - 向主人呈报生成结果与图片存盘路径（如 `./<article-slug>/images/illustration_1.png`）。
