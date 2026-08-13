---
name: video-storyboard-designer
description: 视频单元分镜与 3 幕动态动作链需求构建技能。接收 4 轨讲解剧本 video_script.json 与正文插图隐喻，将长视频解耦为独立视频单元 (unit_XX)，推演 3 幕动态动作链 (Hook -> Core Action -> Delivery)，输出遵循 HyperFrames 官方 BRIEF 规范的 BRIEF.md 契约与 public/mascot.svg 矢量 IP 资产。
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
     - **Act 1 (引出问题 Hook)**：IP Mascot 面对混乱的数据/断点难题，神情冷静带冷幽默（Deadpan）。
     - **Act 2 (动作核心 Core Action)**：IP Mascot 亲自操作关键低科技道具（拉线缆、旋转阀门、调节杠杆、拧紧阀门），解决逻辑冲突。
     - **Act 3 (交付结果 Delivery)**：IP Mascot 完成步骤并在节点盖上 `[PASS]` 印章，线路恢复流畅运转。
4. **具象化视觉与动作描述原则 (Concrete Visual & Motion Detail Protocol)**：
   - 拒绝抽象泛化的概括句。Agent 编写 `BRIEF.md` 时，必须提供极高颗粒度的设计细节，确保下游 HyperFrames SubAgent 零歧义理解：
     - **画面元素清单 (Visual Element Census)**：显式列出单元场景内必须出现的所有 DOM/SVG 视觉构件（如标题花字框、发射器、解构卷轴、散射公式卡片、表情气泡等）。
     - **带时间轴的 3 幕动作轨迹 (Time-Coded 3-Act Trajectory)**：结合口播时长，将单元内 3 幕动作解耦为精准时间戳关键帧（如 `0.0s-2.5s Hook`、`2.5s-5.5s Core Action`、`5.5s-8.0s Delivery`），精确描述元素的入场方式、道具交互（手持放大镜、拉动下拉绳、指向蓝光波段）与表情演化（`❓` ➔ `💡` ➔ `✨`）。
     - **IP 节点与道具互动指引 (Mascot Joint & Prop Interaction)**：明确指出调用的 SVG 节点 ID（`#mascot-head`, `#mascot-arm-left`, `#mascot-arm-right`）及绑定的低科技道具。
5. **视频单元隔离与 HyperFrames 原生 BRIEF.md 契约**：
   - 每个视频单元为独立的构建空间 `./<article-slug>/assets/video/unit_XX/`。
   - 单元内 `BRIEF.md` 包含 YAML Frontmatter（声明 `workflow: faceless-explainer`、`message`、`length` 精准时长卡点、`aspect: 1920x1080`）及 Body 正文（`## Intent` 描述 3 幕动作链与视觉指导、`## Assets` 声明 `public/mascot.svg`）。
6. **16:9 纯白手绘美学与矢量 IP 节点**：
   - 美学基调：16:9 横版构图、纯白背景 (`#FFFFFF`)、黑色手绘线条风格。
   - 每个单元下落盘 `public/mascot.svg`，遵循 `mascot_svg_contract.md` 节点规范（如 `#mascot-head`, `#mascot-arm-left`, `#mascot-arm-right`），供下游 HyperFrames 内部分镜 GSAP 驱动。

---

## Agent 执行步骤协议 (Step-by-Step Protocol)

当 Agent 被调度执行分镜设计时，按以下步骤处理：

### 步骤一：路由解析 IP Mascot 形象规范
1. 检查是否存在 `./<slug>/character_ip.md`；若无，检查是否存在 `./character_ip.md`；若无，读取技能内置 [references/character_ip.md](references/character_ip.md)。
2. 提取文件中的 `Master Visual Prompt`（如 `Xiao Zhi robot, a minimalist hand-drawn mascot...`）作为全局 IP 描述。

### 步骤二：逐单元智能推演 3 幕动态动作链与计算时长
读取 `video_script.json` 中的 `units` 数组：
1. 遍历每个单元 `unit_id`，提取 `duration_seconds`、`voiceover`、`visual_prompt` 及 `ip_action`。
2. 将 `ip_action` 深度推演为具象的 3 幕动态动作链 (Act 1 ➔ Act 2 ➔ Act 3)，并梳理**画面元素清单**与**时间轴关键帧轨迹**。

### 步骤三：创建独立视频单元工作区并落盘 HyperFrames BRIEF.md
针对每个视频单元 `XX`（如 `01`, `02` ...）：
1. 创建目录 `./<article-slug>/assets/video/unit_XX/` 与 `./<article-slug>/assets/video/unit_XX/public/`。
2. 复制/生成矢量 IP 资产到 `./<article-slug>/assets/video/unit_XX/public/mascot.svg`。
3. 存盘写入 `./<article-slug>/assets/video/unit_XX/BRIEF.md`。在 `## Intent` 中必须详尽列出**画面元素清单**、**带时间戳的 3 幕动作轨迹**及 **IP 节点与道具互动细节**。Agent 在编写 `BRIEF.md` 时，必须直接参考并遵循 HyperFrames 官方最新的规范与契约链接：
   - 格式规范：https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-core/references/brief-format.md
   - 字段契约：https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-core/references/brief-contract.md
   - **强制写入 `## Notes` 规程**：为确保下游 HyperFrames 官方 SubAgent 读取 `BRIEF.md` 时遵循正确的矢量关节动画机制，`BRIEF.md` 的 `## Notes` 板块中必须包含以下说明：
     > `- SVG Mascot Joint Animation: When animating SVG mascot elements (#mascot-arm-left, #mascot-arm-right, #mascot-head) with GSAP, ALWAYS use GSAP svgOrigin: "X Y" based on viewBox coordinates (e.g. svgOrigin: "90 200"), NEVER use CSS transformOrigin: "px px", to prevent arm dislocation.`

---

## 交付产物

- `./<article-slug>/assets/video/unit_01/BRIEF.md` ~ `unit_N/BRIEF.md` (HyperFrames 官方标准 BRIEF 契约)
- `./<article-slug>/assets/video/unit_01/public/mascot.svg` ~ `unit_N/public/mascot.svg` (按节点契约规范生成的矢量 IP 资产)

---

## 关联参考规范

- [HyperFrames 官方 BRIEF 格式规范](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-core/references/brief-format.md)：`BRIEF.md` YAML Frontmatter 与 Body 结构定义。
- [HyperFrames 官方 BRIEF 字段契约](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-core/references/brief-contract.md)：`BRIEF.md` 字段枚举与模式派生定义。
- [`references/character_ip.md`](references/character_ip.md)：IP Mascot 视觉形象（支持短路路由加载自定义 IP，默认小智）规范说明。
- [`references/mascot_svg_contract.md`](references/mascot_svg_contract.md)：IP Mascot 矢量节点契约规范说明（指导生成下游 GSAP 可驱动的命名节点）。
- [`references/motion_chain_patterns.md`](references/motion_chain_patterns.md)：3 幕动态动作链设计范例与模式。
- [`references/storyboard_reviewer_standards.md`](references/storyboard_reviewer_standards.md)：分镜视觉与动作链盲审质检标准。
