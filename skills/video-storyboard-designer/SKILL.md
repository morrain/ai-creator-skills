---
name: video-storyboard-designer
description: 视频单元分镜与 HyperFrames BRIEF 构建技能。当需要将 4 轨剧本解耦为独立视频单元、推演 3 幕动作链并落盘 BRIEF.md 契约时调用。
---

# Video Storyboard & Unit Designer Skill (视频单元分镜与 3 幕动作链构建技能)

本技能为 **纯粹无状态的视频单元需求与分镜契约构建技能**。指导 AI Agent 读取 4 轨讲解剧本 (`video_script.json`)，结合 `character_ip.md` 规范与正文插图中的物理隐喻，将视频解耦拆分为 $N$ 个独立的视频单元工作区 (`./assets/video/unit_XX/`)，并为每个单元落盘 HyperFrames 官方标准 `BRIEF.md` 需求契约与矢量 IP 资产 `public/mascot.svg`。

---

## 核心设计原则 (Core Principles)

1. **两层解耦与视频单元独立性 (Per-Unit Isolation)**：
   - 拒绝全量长视频一次性渲染。按结构将讲解剧本解耦为独立视频单元（`unit_01`, `unit_02`, ...）。
   - 每个单元具备独立的生成空间 `./<article-slug>/assets/video/unit_XX/`，零跨单元上下文污染。
2. **物理隐喻继承 (Physical Metaphor Continuity)**：
   - 在 `mode: article_derived` 模式下，读取 `./<article-slug>/assets/illustration_*.md` 配图描述，提取正文中 IP Mascot 已建立的低科技道具（如数据线缆、齿轮阀门、止逆阀、钢印）。
3. **3 幕动态动作链深度推演 (3-Act Motion Chain)**：
   - 将静态场景解耦并演化为 3 幕连续的戏剧性动态描述：
       - **IP 节点与道具互动指引 (Mascot Joint & Prop Interaction)**：明确指出调用的 SVG 节点 ID（`#mascot-head`, `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-leg-right`, `#mascot-prop-slot`）及绑定的物理动作 Recipe 模式（引自 [`references/action_recipes.md`](references/action_recipes.md)，如 `[Action Recipe: PULL_DRAG]`, `[Action Recipe: PUSH_PRESS]`, `[Action Recipe: KICK_STEP]`, `[Action Recipe: OPERATE_LEVER]`）。严禁生成单纯“摇头晃脑”的无隐喻描述！
4. **视觉克制与呼吸感 (Visual Restraint & Layout Rhythm)**：
   - 分镜设计师拥有画面排版与视觉元素的最高决策权。并非每个单元都必须添加标题卡片或唱词高亮词。
   - **标题卡片裁剪原则**：通常仅在 Unit 01 开篇 Hook 或重大章节转换单元放置 `title_card`；中间原理解析单元一律省略标题卡片，保持 16:9 纯白画布干净连贯，避免每个单元机械悬挂标题导致的死板与重复感。
   - 保持画面留白，将视觉焦点集中于 IP Mascot 的物理动作与关键逻辑构件。
5. **视频单元隔离与 HyperFrames 原生 BRIEF.md 契约**：
   - 每个视频单元为独立的构建空间 `./<article-slug>/assets/video/unit_XX/`。
   - 单元内 `BRIEF.md` 包含 YAML Frontmatter（声明 `workflow: faceless-explainer`、`message`、`length` 精准时长卡点、`aspect: 1920x1080`）及 Body 正文（`## Intent` 描述 3 幕动作链与视觉指导、`## Assets` 声明 `public/mascot.svg`）。
6. **16:9 纯白手绘美学与矢量 IP 节点**：
   - 美学基调：16:9 横版构图、纯白背景 (`#FFFFFF`)、黑色手绘线条风格。
   - 每个单元下落盘 `public/mascot.svg`，遵循 `mascot_svg_contract.md` 节点规范（如 `#mascot-head`, `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-leg-right`），供下游 HyperFrames 内部分镜 GSAP 驱动。

---

## Agent 执行步骤协议 (Step-by-Step Protocol)

当 Agent 被调度执行分镜设计时，按以下步骤处理：

### 步骤一：路由解析 IP Mascot 形象规范
1. 检查是否存在 `./<slug>/character_ip.md`；若无，检查是否存在 `./character_ip.md`；若无，读取技能内置 [references/character_ip.md](references/character_ip.md)。
2. 提取文件中的 `Master Visual Prompt`（如 `Xiao Zhi robot, a 2D minimalist hand-drawn mascot...`）作为全局 IP 描述。

### 步骤二：逐单元智能推演 3 幕动态动作链与计算时长
读取 `video_script.json` 中的 `units` 数组：
1. 遍历每个单元 `unit_id`，提取 `duration_seconds`、`voiceover`、`visual_prompt` 及 `ip_action`。
2. 将 `ip_action` 深度推演为具象的 3 幕动态动作链 (Act 1 ➔ Act 2 ➔ Act 3)，并梳理**画面元素清单**与**时间轴关键帧轨迹**，显式绑定特定的 **Physical Action Recipe**（如 `[Action Recipe: PULL_DRAG]`）。

### 步骤三：创建独立视频单元工作区、初始化 HyperFrames 项目并落盘 BRIEF.md
针对每个视频单元 `XX`（如 `01`, `02` ...）：
1. 创建目录 `./<article-slug>/assets/video/unit_XX/`。
2. **初始化 HyperFrames 项目（必须在写入 BRIEF.md 之前执行）**：在 `unit_XX/` 目录下执行以下命令，生成 `hyperframes.json` 与 `package.json`，使其成为合法的 HyperFrames 项目：
   ```bash
   npx hyperframes init "./<article-slug>/assets/video/unit_XX" --non-interactive --example=blank
   ```
   > ⚠️ `init` 要求目标目录为空或不存在，因此必须在拷贝 `public/mascot.svg` 和写入 `BRIEF.md` **之前**执行。
3. 创建 `public/` 子目录并复制/生成矢量 IP 资产到 `./<article-slug>/assets/video/unit_XX/public/mascot.svg`。
4. **⚠️ 强制前置读取规范（写入 BRIEF.md 之前必须完成）**：使用 `view_file` 依次读取项目根目录下 HyperFrames 官方的以下两份规范文件，理解 BRIEF.md 的完整结构与字段语义后，方可开始编写：
   - 格式规范：`.agents/skills/hyperframes-core/references/brief-format.md`（定义 BRIEF.md 的 YAML Frontmatter 字段清单、Body 四板块结构 `## Intent` / `## Assets` / `## Customizations` / `## Notes`、生命周期规则）
   - 字段契约：`.agents/skills/hyperframes-core/references/brief-contract.md`（定义 `flow` / `storyboard` / `mode` 运行形态派生规则、`message` / `destination` / `aspect` / `length` / `angle` 等共享字段的枚举值与语义）
5. 存盘写入 `./<article-slug>/assets/video/unit_XX/BRIEF.md`。**严格按照上述两份规范**填写 YAML Frontmatter（必须包含 `workflow`、`flow`、`storyboard`、`message`、`length`、`aspect` 等字段）与 Body 正文。在 `## Intent` 中必须详尽列出**画面元素清单**、**带时间戳的 3 幕动作轨迹**及 **IP 节点与道具互动细节（含 GSAP Action Recipe 绑定）**。
   - **强制写入 `## Assets` 板块**：声明 `public/mascot.svg` 矢量 IP 资产。
   - **强制写入 `## Notes` 规程**：为确保下游 HyperFrames 官方 SubAgent 读取 `BRIEF.md` 时遵循正确的矢量关节动画机制，`BRIEF.md` 的 `## Notes` 板块中必须包含以下说明：
     > `- SVG Mascot Joint Animation: When animating SVG mascot elements (#mascot-arm-left, #mascot-arm-right, #mascot-leg-left, #mascot-leg-right, #mascot-head) with GSAP, ALWAYS use GSAP svgOrigin: "X Y" based on viewBox coordinates (e.g. svgOrigin: "90 205"), NEVER use CSS transformOrigin: "px px", to prevent arm dislocation.`

---

## 交付产物

- `./<article-slug>/assets/video/unit_01/hyperframes.json` ~ `unit_N/hyperframes.json` (HyperFrames 项目配置)
- `./<article-slug>/assets/video/unit_01/package.json` ~ `unit_N/package.json` (锁定 HyperFrames CLI 版本)
- `./<article-slug>/assets/video/unit_01/BRIEF.md` ~ `unit_N/BRIEF.md` (HyperFrames 官方标准 BRIEF 契约)
- `./<article-slug>/assets/video/unit_01/public/mascot.svg` ~ `unit_N/public/mascot.svg` (按节点契约规范生成的矢量 IP 资产)

---

## 关联参考规范

- `.agents/skills/hyperframes-core/references/brief-format.md`：`BRIEF.md` YAML Frontmatter 与 Body 结构定义（HyperFrames 官方源文件，动态读取以保持最新）。
- `.agents/skills/hyperframes-core/references/brief-contract.md`：`BRIEF.md` 字段枚举与模式派生定义（HyperFrames 官方源文件，动态读取以保持最新）。
- [`references/character_ip.md`](references/character_ip.md)：IP Mascot 视觉形象（支持短路路由加载自定义 IP，默认小智）规范说明。
- [`references/mascot_svg_contract.md`](references/mascot_svg_contract.md)：IP Mascot 矢量节点契约规范说明（指导生成下游 GSAP 可驱动的命名节点）。
- [`references/action_recipes.md`](references/action_recipes.md)：IP Mascot GSAP 物理动作范例库（提供推、拉、拖、踢、操作阀门的真实动作模式）。
- [`references/motion_chain_patterns.md`](references/motion_chain_patterns.md)：3 幕动态动作链设计范例与模式。
- [`references/storyboard_reviewer_standards.md`](references/storyboard_reviewer_standards.md)：分镜视觉与动作链盲审质检标准。
