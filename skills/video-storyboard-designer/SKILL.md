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
       - **IP 节点与道具互动指引 (Mascot Joint & Prop Interaction)**：明确指出调用的 SVG 节点 ID（`#mascot-head`, `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-leg-right`, `#mascot-prop-slot`）及绑定的物理动作 Recipe 模式（引自 [`references/action_recipes.md`](references/action_recipes.md)，如 `[Action Recipe: PULL_DRAG]`, `[Action Recipe: PUSH_PRESS]`, `[Action Recipe: KICK_STEP]`, `[Action Recipe: OPERATE_LEVER]`）。必须确保 IP Mascot 与交互道具在同一个主 SVG 容器内同框，且 IP 的手臂/手掌末端锚点与道具的物理接触中心 100% 坐标对齐重合！严禁生成单纯“摇头晃脑”或与道具空间割裂的假动作！
4. **显式指定优先与自适应风格选型 (Explicit Priority & Content-Adaptive Style Presets)**：
   - **显式指定优先**：若用户或上游工作流在调用时显式指定了 `--style <preset>` 参数（如 `--style blue-professional`），Agent 必须直接使用该指定的 `style_preset`。
   - **内容自适应保底**：若未显式指定 `--style` 参数，必须结合 `video_script.json` 的主题领域与文案基调，读取 [`references/style_presets.md`](references/style_presets.md) 指南评估并锁定最匹配的单一 `style_preset`（如 `blue-professional`, `code-editorial`, `minimal`, `broadside`, `clean-editorial` 等）。
   - **全片所有单元绝对统一**：选定的 `style_preset` 作为项目全局视觉基因，**必须且只能在第 01 单元设计前锁定一次**，全片所有视频单元（`unit_01` ~ `unit_N`）的 `BRIEF.md` YAML Frontmatter 必须继承该相同的 `style_preset`，严禁同一视频的不同单元风格游离！
   - **在设计契约中强制写入以下低密度限制规则 (Low Density Rules)**：
     - **One Statement Per Frame**：一屏只表达一个核心结论，禁止堆砌多张卡片；
     - **Cap Elements $\le 3$**：单个场景内出现的独立元素/卡片数量绝对不超过 3 个；
     - **Suppress Chrome**：屏蔽背景网格点、装饰性线条、炫酷但无意义的光晕/粒子等“视觉噪声”，保持高对比度与纯净呼吸感。
   - **标题卡片裁剪原则**：通常仅在 Unit 01 开篇 Hook 或重大章节转换单元放置 `title_card`；中间原理解析单元一律省略标题卡片，保持纯净画布干净连贯，避免每个单元机械悬挂标题导致的死板与重复感。
5. **视频单元隔离与 HyperFrames 原生 BRIEF.md 契约**：
   - 单元内 `BRIEF.md` 包含 YAML Frontmatter（**强制锁定** `workflow: faceless-explainer`、`flow: automation`、`storyboard: no`、`style_preset` (自适应选定)、`aspect: 1920x1080`、`message` 及 `length` 精准时长卡点）及 Body 正文（`## Intent` 描述 3 幕动作链与视觉指导、`## Assets` 声明 `public/mascot.svg`）。
6. **多比例自适应布局与 SVG 防裁剪规程 (Multi-Aspect Responsive Rules)**：
   - 默认 16:9 横屏美化 (`1920x1080`)：纯白背景 (`#FFFFFF`)、手绘线条风格。
   - **在生成 `BRIEF.md` 时，必须将非 16:9 防裁剪规程显式写入 `BRIEF.md` 的 `## Notes` 板块中，向下游 SubAgent 传递**：
     - **严禁**硬编码 1920 宽度的横向绝对坐标致使 `#root` (`overflow: hidden`) 裁剪左右元素；
     - 若沿用 1920 全景 SVG 坐标，SVG 容器必须声明 `preserveAspectRatio="xMidYMid meet"`（如 `<svg width="1080" height="1080" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid meet">`），使画面按比例整体收拢于视口居中安全区；
     - 若重构竖屏/正方形排版，需将原本左右并排的组件改为上下堆叠或收窄至 `0~1080px` 视口范围内，确保 IP Mascot、图表及 UI 元素 100% 完整显现。
7. **融合口播与画面描述的二次分镜拆解 (Secondary Storyboard Subdivision)**：
   - 在生成 `BRIEF.md` 时，必须深度结合当前单元的 `voiceover` 口播逐字稿、`visual_prompt` 场景视觉与 `ip_action` 的多阶段描述，在 `BRIEF.md` 的 `## Intent` 中对动画细节和画面元素进行**二次分镜拆解 (Secondary Storyboard Subdivision)**。
   - 拆解必须包含：
     - **画面元素与构件全量清单 (Scene Element & Asset Inventory)**：精细列出所有背景、物理道具、UI 卡片、数据流向及 IP Mascot 构件。
     - **带精准时间轴的二次分镜切片 (Sub-shot Timeline Breakdown)**：结合口播节奏划分为具体镜头切片（如 `[Sub-shot 1: 00:00-00:10]`、`[Sub-shot 2: 00:10-00:25]`），详细指明各元素的显隐入场/退场动画、IP 关节 Recipe 动作与 UI 图表弹显规则，确保下游 HyperFrames 制作 SubAgent 生成代码时具备完整、连续且丰富的动态渲染依据。

---

## Agent 执行步骤协议 (Step-by-Step Protocol)

当 Agent 被调度执行分镜设计时，按以下步骤处理：

### 步骤一：路由解析 IP Mascot 形象规范
1. 检查是否存在 `./<slug>/character_ip.md`；若无，检查是否存在 `./character_ip.md`；若无，读取技能内置 [references/character_ip.md](references/character_ip.md)。
2. 提取文件中的 `Master Visual Prompt`（如 `Xiao Zhi robot, a 2D minimalist hand-drawn mascot...`）作为全局 IP 描述。

### 步骤二：结合口播与剧本描述自适应锁定 style_preset、执行二次分镜拆解与 3 幕动态推演
读取 `video_script.json` 中的 `units` 数组及 TTS 时长：
1. **全局风格自适应选型（仅在第 01 单元前执行一次）**：结合剧本全局主题与调性，读取 [`references/style_presets.md`](references/style_presets.md) 锁定制选全片的单一 `style_preset`（如 `blue-professional`, `code-editorial`, `minimal`, `broadside` 等），并贯穿应用于所有单元。
2. 遍历每个单元 `unit_id`，提取 `duration_seconds`、`voiceover`、`visual_prompt` 及 `ip_action`。
3. 深度结合口播台词与 `visual_prompt` / `ip_action` 的阶段描述，执行**二次分镜拆解**：梳理全量**画面元素清单**，并按时间轴/切片划分为带时间戳的关键帧轨迹与分分镜切片（如 `[Sub-shot 1]`、`[Sub-shot 2]`），显式绑定特定的 **Physical Action Recipe**（如 `[Action Recipe: PULL_DRAG]`）。

### 步骤三：创建独立视频单元工作区、初始化 HyperFrames 项目并落盘 BRIEF.md
针对每个视频单元 `XX`（如 `01`, `02` ...）：
1. 创建目录 `./<article-slug>/assets/video/unit_XX/`。
2. **初始化 HyperFrames 项目（必须在写入 BRIEF.md 之前执行）**：
   - 执行以下命令初始化 HyperFrames 独立项目。**必须显式加上 `HYPERFRAMES_SKIP_SKILLS=1` 环境变量**，跳过远程 GitHub 技能包克隆（实现毫秒级纯本地脚手架生成），确保各单元精确生成包含对应 `unit_XX` 标识的 `package.json` 和 `meta.json`：
     ```bash
     HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init "./<article-slug>/assets/video/unit_XX" --non-interactive --example=blank
     ```
   > ⚠️ `init` 要求目标目录为空或不存在，因此必须在拷贝 `public/mascot.svg` 和写入 `BRIEF.md` **之前**执行。**严禁从其他单元直接复制脚手架文件**，避免破坏 `package.json` / `meta.json` 中属于各个 `unit_XX` 的独立项目名称与元数据。
3. 创建 `public/` 子目录，**前置将本单元所需的依赖资产复制落盘**：
   - `./<article-slug>/assets/video/unit_XX/public/mascot.svg`（矢量 IP 角色资产）
   - `./<article-slug>/assets/video/unit_XX/public/audio.mp3`（从 `../audio/unit_XX.mp3` 复制本单元口播音频切片）
   - `./<article-slug>/assets/video/unit_XX/public/timestamps.json`（从 `../audio/timestamps.json` 提炼本单元逐句字幕时间戳契约）
4. **⚠️ 强制前置读取规范（写入 BRIEF.md 之前必须完成）**：使用 `view_file` 依次读取项目根目录下 HyperFrames 官方的以下两份规范文件，理解 BRIEF.md 的完整结构与字段语义后，方可开始编写：
   - 格式规范：`.agents/skills/hyperframes-core/references/brief-format.md`（定义 BRIEF.md 的 YAML Frontmatter 字段清单、Body 四板块结构 `## Intent` / `## Assets` / `## Customizations` / `## Notes`、生命周期规则）
   - 字段契约：`.agents/skills/hyperframes-core/references/brief-contract.md`（定义 `flow` / `storyboard` / `mode` 运行形态派生规则、`message` / `destination` / `aspect` / `length` / `angle` 等共享字段的枚举值与语义）
5. 存盘写入 `./<article-slug>/assets/video/unit_XX/BRIEF.md`。**严格按照上述两份规范**填写 YAML Frontmatter（必须包含 `workflow`、`flow`、`storyboard`、`message`、`length`、`aspect` 及步骤二自适应选定的 `style_preset` 等字段）与 Body 正文。在 `## Intent` 中必须详尽列出**画面元素清单**、**结合口播时间轴的二次分镜切片与 3 幕动作轨迹**及 **IP 节点与道具互动细节（含 GSAP Action Recipe 绑定）**。
   - **强制写入 `## Customizations` 板块**：必须显式声明所选风格与低密度视觉要求：
     > `- Style Aesthetic: <style_preset> (Refer to style_presets.md design language definition).`
     > `- Low Density Rules: One Statement Per Frame (only 1 key conclusion per screen), Cap Elements <= 3 (max 3 independent cards/elements per scene), Suppress Chrome (disable background grid dots, decorative lines, or glowing particles).`
   - **强制写入 `## Assets` 板块**：声明 `public/mascot.svg`、`public/audio.mp3` 以及 `public/timestamps.json`。
   - **强制写入 `## Notes` 规程**：为确保下游 HyperFrames 官方 SubAgent 读取 `BRIEF.md` 时遵循正确的极简低密度排版、矢量关节动画、音频轨挂载与非 16:9 视口防裁剪机制，`BRIEF.md` 的 `## Notes` 板块中必须包含以下说明：
     > `- SVG Mascot Joint Animation: When animating SVG mascot elements (#mascot-arm-left, #mascot-arm-right, #mascot-leg-left, #mascot-leg-right, #mascot-head) with GSAP, ALWAYS use GSAP svgOrigin: "X Y" based on viewBox coordinates (e.g. svgOrigin: "90 205"), NEVER use CSS transformOrigin: "px px", to prevent arm dislocation.`
     > `- Mascot & Prop Spatial Coupling: When the IP mascot interacts with props (#target-valve-wheel, #target-button, #target-lever, cables), ALWAYS embed the IP SVG group (<g id="mascot">) directly inside the main scene SVG container or align its absolute position via GSAP gsap.set("#mascot", { x, y }) so that the mascot's hand/arm contact point 100% touches the prop anchor. NEVER place the mascot in a detached bottom div (e.g. top: 940px) while interactive props are inside a top/middle SVG.`
     > `- Audio Track Binding: ALWAYS include <audio id="unit-audio" class="clip" src="./public/audio.mp3" data-start="0" data-duration="..." data-track-index="0"></audio> inside index.html to bind the unit voiceover audio asset.`
     > `- Subtitle Animation Sync: ALWAYS read public/timestamps.json to build GSAP subtitle timeline using exact start/end seconds from subtitles array.`
     > `- Low Density Constraint: Obey "One Statement Per Frame" (1 core message/frame), "Cap Elements <= 3" (at most 3 visible UI cards/elements at any time), and "Suppress Chrome" (no background grid dots, decorative lines, or glowing particles).`
     > `- Non-16:9 Responsive Viewport: For non-16:9 aspect ratios (e.g. 1080x1080 or 1080x1920), ALWAYS set SVG preserveAspectRatio="xMidYMid meet" on full-stage SVG elements or stack layout vertically, to prevent left/right element clipping caused by overflow: hidden.`
     > `- First Frame Exposure & Anti-Blank Cover: At t=0.0s, the first frame MUST NOT be pure white blank canvas! ALWAYS use gsap.set() at t=0 to render main title text, background card container, and IP Mascot initial pose at opacity: 1 or visible state, ensuring auto-extracted cover images on social platforms (Xiaohongshu, WeChat) are visually rich and readable.`
     > `- Outro Call-To-Action (Tail Unit): For the final ~3s outro unit, ALWAYS bind [Action Recipe: LIKE_AND_SUBSCRIBE] to drive IP mascot cheerful bouncing animation and raise interactive badges (Like, Save, Follow).`

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
- [`references/style_presets.md`](references/style_presets.md)：HyperFrames 风格预设库与主题自适应选型指南。
- [`references/motion_chain_patterns.md`](references/motion_chain_patterns.md)：3 幕动态动作链设计范例与模式。
- [`references/storyboard_reviewer_standards.md`](references/storyboard_reviewer_standards.md)：分镜视觉与动作链盲审质检标准。
