---
name: articles
description: 将热点话题生成高质量文章的 Skill。在生成大纲前执行强制互联网前置检索 (search_web)，采用“大纲生成 + 审稿人 SubAgent 闭环审查 + 主人评审批准 + 正文展开”的流程，默认使用“干货指南”文风，结合 references/reviewer_standards.md 实施盲审，输出纯净 Markdown 文章。
---

# Articles Skill (热点话题文章创作)

本技能指导 AI Agent 根据选择的热点话题（如来自 `hot-topics` 的 `TopicItem` 或用户指定主题），在进行强制互联网前置检索后，经过大纲共创、审稿人 SubAgent 闭环审查、主人评审与正文反 AI 味质量盲审，生成高质量的纯 Markdown 排版文章。

---

## 核心设计原则 (Core Principles)

0. **强制互联网前置检索 (Mandatory Web Search Protocol)**：
   - 在进行任何大纲提炼与构建前，**必须优先显式调用 `search_web` 工具**对【知识主题】进行多角度检索（获取最新行业动态、最新技术架构、权威测评与最新 API 现状），严禁未经检索闭门造车或凭空臆造。
1. **两阶段互动流程 (Two-Stage Workflow)**：
   - 阶段一：基于互联网前置检索结果拟定大纲草案，经审稿人 SubAgent 盲审通过后，呈现给主人评审。**必须等待主人批准后方可生成正文**。
   - 阶段二：大纲批准后展开正文撰写，经审稿人 SubAgent 盲审通过后落盘。
2. **默认文风设定**：
   - **默认统一采用【干货指南】文风**（聚焦实战步骤、避坑指南、分步 Action Items 与工具推荐）。
   - 同时支持在阶段一由用户切换为其他备选文风。
3. **标题字数与全一致性硬约束**：
   - 文章大标题 (H1) **必须严格控制在 20 个字以内**（含标点），且富有吸引力。
   - 大纲确立标题后，正文及后续派生必须严格保持统一，严禁擅自修改。
4. **内容与撰写元指令强制隔离 (Meta-instructions Demarcation)**：
   - 在大纲中，使用 `【撰写指令】` 明确隔离“指导性元指令”（如卖点、Hook、金句规划）与“实际小节标题”。
   - 正文阶段**绝对禁止**将指令词（如 `【撰写指令】`、`总结与爆款金句`、`强冲突勾子`）作为小标题或正文输出。
5. **【科普名师文风】与反 AI 味审查**：
   - **痛点 Hook**：开篇明确告知读者能解决什么痛苦/提升什么能力。
   - **呼吸感排版**：单段严格控制在 2-4 行以内，拒绝超长文字墙。
   - **去同质化**：严禁出现 `references/anti_patterns.md` 中的 AI 套话黑名单。
6. **丰富 Markdown 排版系统 (Rich Markdown Layout System)**：
   - 绝不使用单一枯燥的纯文本陈述，必须灵活运用 Markdown 富排版语法：
     - **引用块卡片 (`>`)**：用于突出核心金句、避坑警告与提示（如 `> 💡 **核心提示**：...`）。
     - **无序/有序列表 (`-` / `1.`)**：列举并列卖点、操作步骤或参数时强制使用列表，替代长段落。
     - **精准局部加粗 (`**重点**`)**：对核心概念、结论词汇进行局部精准加粗，形成视觉阅读锚点。
     - **对比表格 (`| ... |`)**：在方案对比、技术对比或优劣分析时自动引入 Markdown 表格。
7. **审稿人 SubAgent 审查闭环 (Reviewer SubAgent Loop)**：
   - 在阶段一（大纲）与阶段二（正文）生成草稿后，**必须发起审稿子进程 (`article_reviewer`)**，读取并严格执行 `references/reviewer_standards.md`。
   - 若审稿裁决为 `[REJECT]`，主创 Agent 必须根据诊断意见重写草稿（上限迭代 8 次），直至审稿裁决判定为 `[PASS]`。

---

## 支持的文风风格与极客表达规范 (Genres & Style Definitions)

在大纲拟定阶段，Agent 默认应用**干货指南**文风，也可根据用户显式要求切换。**所有文风均须严格遵循“顶级科普名师兼产品演说家”角色定位，痛点卖点切入，单段严格限制在 2 ~ 4 行（治理文字大山），丰富运用引用卡片、并列列表、局部加粗与对比表格，拒绝枯燥说教与大段纯文字**。完整指导详见 [`references/style_definitions.md`](references/style_definitions.md)：

1. 🌟 **干货指南 (默认 - Practical Handbook)**：实战演练与解决方案发布会。痛点切入，分步骤 Action Items 卡片，单段 2-4 行，关键代码带中文行内注释与成果解构，末尾附避坑清单与爆款金句。
2. **科技深度评论 (Tech Deep Dive & Trends)**：产业洞察与变革技术发布会。新旧范式剧烈冲突 Hook，结合对比表格/Mermaid 展现优势，用数据与惊艳事实说话，剔除“重塑范式”等 AI 空话。
3. **社会观察 (Social Observation & Human Insights)**：现象级大众心理与群体情绪解构。大众情绪痛点场景 Hook，启发式互动问答体（“为什么会这样呢？”），单段 2-4 行共情短段，激发截图转发冲动。
4. **科普解说 (Popular Science Explainer)**：硬核原理的通俗降维演示课。常识/直观误区 Hook，**精准降维演示**（用生活的熟知场景/产品体验类比复杂机制），单段 2-4 行，术语首次出现用一句话通俗解释。
5. **故事叙事 (Narrative Storytelling)**：身临其境的人物/案例冲突戏剧。戏剧性转折/决策时刻 Hook，紧凑的起伏线索与短小精悍的场景描写，单段 2-4 行明快节奏，传递震撼灵魂的终局金句。

---

## 核心工作流程

### 阶段一：大纲拟定、SubAgent 盲审、前置归档与主人评审 (Outline, Archiving & Human Review)

1. **强制互联网前置检索与输入解析 (Mandatory Web Search & Input Parsing)**：
   - 读取输入的 `title`、`summary`、`key_aspects` 与 `suggested_angles`。
   - **硬性前置检索**：在提炼任何大纲前，**必须优先显式调用 `search_web` 工具**对【知识主题】进行多角度检索（获取最新行业动态、最新技术架构、权威测评与最新 API 现状），结合搜索到的最新实时事实与技术背景，严禁未经检索凭空臆造。
2. **拟定大纲草案与 Slug 提炼 (Drafting & Slug Extraction)**：
   - 拟定 3 个备选 H1 标题（**每个标题必须 ≤ 20 字**），并提炼简短英文连字符 Slug（`<article-slug>`）。
   - 规划文章结构，清晰标注撰写指令：
     ```markdown
     # H1 标题 (≤ 20字)
     
     > 💡 选中文风：干货指南 (默认)
     
     ## 二级标题 1
     - 【撰写指令】：阐述核心痛点，引入爆款金句。
     - 核心论点与逻辑递进说明...
     ```
3. **触发审稿人 SubAgent 大纲审查闭环 (SubAgent Outline Review Loop)**：
   - **发起审稿子进程**：发起 `article_reviewer` 审稿子进程，读取并严格执行 `references/reviewer_standards.md` 手册，对大纲草案进行【标题字数 ≤20字】、【元指令隔离 `【撰写指令】`】、【切入角度与去同质化】以及【结构连贯性】四大维度审查。
   - 若审稿裁决为 `[REJECT]`，主创 Agent 必须根据诊断意见重写大纲草案，重复审查修正循环（上限迭代 8 次），直至裁决判定为 `[PASS]`。
4. **创建主题工作区并立即落盘归档大纲 (Topic Workspace Init & Pre-Archiving Outline)**：
   - 当大纲通过审稿人 SubAgent 盲审后，**必须立即在项目根目录下新建 `./<article-slug>/` 目录**。
   - **强制前置归档**：将通过盲审的大纲**全量原文**保存为固定的 `./<article-slug>/outline.md` 文件。
5. **全量呈现大纲原文并等待主人批准 (Full Original Outline Presentation & Human Gate)**：
   - **100% 完整输出大纲原文**：在呈现给主人的信息中，**必须全量输出 `outline.md` 完整的 Markdown 原文**（绝对禁止打折、总结概括或截断），并附带落盘路径与相对可点击链接（如 [`./<article-slug>/outline.md`](./<article-slug>/outline.md)）。
   - **卡点等待**：明确提示主人可直接在编辑器中查看或修改该归档大纲，**停止并等待主人回复 [通过/继续] 或修改意见**。

---

### 阶段二：大纲批准后正文生成、SubAgent 盲审与归档 (Full Article Generation)

1. **读取已归档的大纲定稿 (Read Archived Outline)**：
   - 主人确认通过大纲后，直接读取主题工作区中 `./<article-slug>/outline.md` 文件的定稿大纲与 H1 标题（若主人在落盘大纲文件中进行了修改，以文件实际内容为准）。
2. **正文展开撰写与富 Markdown 排版 (Rich Layout Drafting)**：
   - 严格按照 `./<article-slug>/outline.md` 的结构与标题展开正文。
   - 将大纲中的 `【撰写指令】` 自然转化为正文的实际推导与爆款金句，剥离元指令文本。
   - **富 Markdown 排版**：单段控制在 2-4 行；灵活嵌入引用卡片 `> 💡` 突出金句与警告、列表 `-` / `1.` 排版并列要点、局部加粗 `**` 建立视觉焦点、表格 `|...|` 呈现方案对比，绝不出纯文字大山。
   - 代码块只保留主干逻辑，每一行关键代码附带接地气的中文行内注释与运行成果解构。
3. **触发审稿人 SubAgent 盲审闭环 (SubAgent Master Article Review Loop)**：
   - **发起审稿子进程**：发起 `article_reviewer` 审稿子进程，读取并严格执行 `references/reviewer_standards.md` 审查手册。
   - 由审稿人 SubAgent 对正文草稿进行【反 AI 味/去同质化】、【干货度与可验性】、【逻辑自洽与破题相关性】、【富排版品质】及【元指令隔离】五大维度盲审。
   - 若审稿裁决为 `[REJECT]`，主创 Agent 必须根据诊断意见逐条重写修正草稿，重复此审查修正循环（上限迭代 8 次），直至裁决判定为 `[PASS]`。
4. **纯净 Markdown 存盘与归档**：
   - 对照 `references/anti_patterns.md` 进行最终符号排版自检（中英文混排自动加空格如 `AI 时代`）。
   - 将通过审稿人 SubAgent 盲审的最终纯净 Markdown 文章保存至 `./<article-slug>/<article-slug>.md`。
