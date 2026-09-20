---
name: video-storyboard-designer
description: 视频单元分镜与 HyperFrames BRIEF 构建技能。当需要将 video_script.json 转换为独立视频单元（unit_01 ~ unit_N）、初始化 HyperFrames 脚手架并落盘标准 BRIEF.md 契约文件时自动调用。
---

# Video Storyboard Designer 技能指南

`video-storyboard-designer` 是视频创作流水线中的**分镜与 BRIEF 创作核心技能**。其核心职责是将上游 `video-script-writer` 提炼的 `video_script.json` 解耦拆分为独立的视频单元 `unit_01` ~ `unit_N`，并在各单元下落盘 HyperFrames 官方标准的 `BRIEF.md` 契约与本地依赖资产（`mascot.svg`、`audio.mp3`、`timestamps.json`），为下游 HyperFrames SubAgent 提供精准的代码编写与渲染执行依据。

---

## 核心设计理念

1. **两层解耦与视频单元独立性 (Per-Unit Isolation)**：拒绝全量长视频一次性渲染，按结构将讲解剧本解耦为独立视频单元（`unit_01`, `unit_02`, ...），每个单元具备独立工作区，零跨单元上下文污染。

2. **物理隐喻动态生成 (Generative Physical Metaphor)**：根据视频主题，遵循 [references/physical_metaphor_schema.md](references/physical_metaphor_schema.md) 的 3 步推演法，动态将抽象逻辑解构为具象的 2D SVG 物理结构骨架（带具名 `id` 构件）与 GSAP 物理动作轨迹。

3. **3 幕动态动作链 (3-Act Motion Chain)**：将静态场景演化为 3 幕连续戏剧性动态，IP Mascot 必须与交互道具在同一 SVG 容器内同框，手臂/手掌末端锚点 100% 对齐道具物理接触中心。详细 Recipe 见 [`references/action_recipes.md`](references/action_recipes.md)。

4. **低密度视觉克制 (Low-Density Visual Restraint)**：全片不使用 HyperFrames 预设（不填 `style_preset`），遵循"一屏一结论、活跃构件 ≤ 5、禁止侧边栏堆叠、保持 70%+ 留白"的排版铁律。完整规程通过 `## Customizations` 与 `## Notes` 板块传递给下游（见步骤三第 5 点）。

5. **多比例自适应 (Multi-Aspect Responsive)**：默认 16:9（`1920x1080`），非 16:9 版本须在 `## Notes` 中写入防裁剪规程，防止 `overflow: hidden` 裁切左右元素（规程见步骤三第 5 点）。

6. **二次分镜拆解 (Secondary Storyboard Subdivision)**：深度结合 `voiceover`/`visual_prompt`/`ip_action`，在 `## Intent` 中输出带时间戳的分镜切片与 SVG 骨架草案，作为下游制作 SubAgent 的完整渲染依据（执行方法见步骤二）。

7. **Step 3 阶段绝对禁止编写 index.html 屏障 (Strict Separation of Storyboard & HTML Implementation)**：`video-storyboard-designer` 技能职责严格限定在分镜契约落盘与脚手架初始化，**绝对禁止在本阶段修改或编写任何 `index.html` 内容**。所有 HTML/CSS/GSAP 代码均留待下游 Step 4 渲染 SubAgent 独立进驻编写。

---

## Agent 执行步骤协议 (Step-by-Step Protocol)

### 步骤一：路由解析 IP Mascot 形象规范
1. 检查是否存在 `./<slug>/character_ip.md`；若无，检查 `./character_ip.md`；若无，读取技能内置 [references/character_ip.md](references/character_ip.md)。
2. 提取 `Master Visual Prompt`（如 `Xiao Zhi robot, a 2D minimalist hand-drawn mascot...`）作为全局 IP 描述。

### 步骤二：读取剧本、推演物理隐喻、执行二次分镜拆解
1. 读取 `video_script.json` 的 `units` 数组，提取每个单元的 `duration_seconds`、`voiceover`、`visual_prompt`、`ip_action`。
2. 参照 [references/physical_metaphor_schema.md](references/physical_metaphor_schema.md) 核心 3 步推演公式（按需检索特定行业案例，严禁全量装载冗长案例库），为每个单元的主题动态生成 SVG 物理骨架结构与节点 ID。
3. 结合口播台词与 `visual_prompt`/`ip_action`，对每个单元执行**二次分镜拆解**：梳理全量画面元素清单，划分为带时间戳的关键帧切片（如 `[Sub-shot 1]`、`[Sub-shot 2]`），显式绑定 **Physical Action Recipe**（如 `[Action Recipe: PULL_DRAG]`）。
4. 读取 `video_script.json` 中 `metadata.visual_theme` 提取全集统一视觉主题与 Palette Tokens，继承准备注入各单元 `BRIEF.md` 契约。

### 步骤三：创建单元工作区、初始化 HyperFrames 项目并落盘 BRIEF.md
针对每个视频单元 `XX`（如 `01`, `02` ...）：

1. 创建目录 `./<article-slug>/assets/video/unit_XX/`。

2. **初始化 HyperFrames 项目（必须先于写入 BRIEF.md 执行）**：
   ```bash
   HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init "./<article-slug>/assets/video/unit_XX" --non-interactive --example=blank
   ```
   > ⚠️ `init` 要求目标目录为空，必须在拷贝资产和写入 BRIEF.md **之前**执行。**严禁从其他单元复制脚手架文件**，以免破坏各 `unit_XX` 独立的 `package.json` / `meta.json` 元数据。

3. 准备本单元依赖资产到 `public/` 子目录：

   **`public/mascot.svg`（矢量 IP 角色资产）**：
   - **首个单元（unit_01）**：遵循 [`references/mascot_svg_contract.md`](references/mascot_svg_contract.md) 规范，根据步骤一解析的 IP 视觉描述**生成** `mascot.svg`（`viewBox="0 0 300 400"`，含全部标准命名节点 `#mascot-head`/`#mascot-arm-left` 等），写入 `unit_01/public/mascot.svg`，并同时备份至 `./<article-slug>/assets/mascot.svg`。
   - **后续单元（unit_02 ~ unit_N）**：直接从 `./<article-slug>/assets/mascot.svg` **复制**，无需重新生成。

   **`public/audio.mp3`**：从 `./<article-slug>/assets/audio/unit_XX.mp3` 复制本单元口播音频切片。

   **`public/timestamps.json`**：从 `./<article-slug>/assets/audio/timestamps.json` 提炼本单元逐句字幕时间戳。

4. **⚠️ 写入 BRIEF.md 前必须先读取**以下两份 HyperFrames 官方规范文件：
   - `.agents/skills/hyperframes-core/references/brief-format.md`（YAML Frontmatter 字段清单、Body 四板块结构、生命周期规则）
   - `.agents/skills/hyperframes-core/references/brief-contract.md`（`flow`/`storyboard`/`mode` 派生规则、`aspect`/`length` 等字段枚举值与语义）

5. 存盘写入 `./<article-slug>/assets/video/unit_XX/BRIEF.md`，各板块要求如下：

   **YAML Frontmatter**（必填字段，继承 `video_script.json` 中的 `visual_theme`）：
   ```yaml
   workflow: faceless-explainer
   flow: automation
   storyboard: no
   aspect: 1920x1080
   message: <单元核心结论>
   length: <duration_seconds>
   theme:
     canvas_bg: "linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 50%, #eff6ff 100%)"
     primary_accent: "#2563eb"
     secondary_accent: "#38bdf8"
     warning_accent: "#ef4444"
     success_accent: "#10b981"
   ```

   **`## Intent` 板块**须包含：
   - **3 层矢量物理骨架草案（必须直接输出完整 Raw SVG XML 代码块）**：遵循 `physical_metaphor_schema.md` 3 步推演与 3 层矢量精细化指南，必须在 `## Intent` 中按物理实体解耦输出独立的具名 `<g id="...">` XML 构件组（如 `<g id="dam-body">`、`<g id="water-gate">`、`<g id="farmland-target">`），**每个构件内部独立封装其自身的 Layer 1 底座 + Layer 2 纹理 + Layer 3 细节/指示灯**。自解释图形切勿强行加字！**🚫 绝对禁止按 Layer 1/2/3 建立全局大组包裹所有实体（如 `<g id="macro-system"><g id="textures">...</g></g>`）！绝对禁止仅输出高层文字描述或无纹理死板裸框！**
   - **画面元素清单**：按切片列出所有活跃构件（含 `#mascot`），每切片 ≤ 5 个。
   - **二次分镜切片**：带时间戳（如 `[Sub-shot 1: 00:00-00:10]`），明确各元素入场/退场动画与 IP Recipe 绑定。针对包含动作任务的切片，必须显式标注动作结束后的【空白归位坐标】与 `[Action Recipe: EXECUTE_THEN_RETREAT]` 指令（例如：`[Action Recipe: PUSH_PRESS] ➔ [Action Recipe: EXECUTE_THEN_RETREAT] (归位点: [140, 270])`），指导下游渲染代理生成精确的走动与回退动作。

   **`## Assets` 板块**（强制写入）：
   ```
   - public/mascot.svg
   - public/audio.mp3
   - public/timestamps.json
   ```

   **`## Customizations` 板块**（强制写入）：
   > `- 低密度与通透留白规程：一屏仅表达 1 个核心结论 (One Statement Per Frame)，任意时刻 t DOM 活跃构件总数绝对 <= 5 个 (Cap Elements <= 5)，切片交接时执行 opacity:0 淡出退场 (Visibility Timeline Matrix)，屏蔽背景网格点、装饰线条或粒子等视觉噪声 (Suppress Chrome)，保持 70%+ 通透留白。坚决移除死板的 Dashboard 文本卡片与长篇文字，核心信息直接以极少的大字号无框融入场景 (No Text Walls)。`

   **`## Notes` 板块**（超紧凑自包含渲染规程，作为传递给下游 Step 4 SubAgent 编写 index.html 时的渲染规范）：
   > `- Theme & Colors: 100% 继承 Frontmatter theme 声明的调色代币，浅色画布标题无框直用深色字，严禁突兀黑块。`
   > `- Mascot IP Protection & Engine: public/mascot.svg 原样复制写入 <g id="mascot"> 且置于主 SVG 容器末尾节点 (Painter's Model 置顶)；必须作为只读品牌资产，在 index.html 中绝对禁止改动其内部 path/fill 颜色，严禁擅自绘制帽子/眼镜/饰品，仅能对整体 <g id="mascot"> 控制 transform 缩放平移；挂载 Y 轴 2.2s 浮动呼吸 + 3.5s 眨眼常驻微动作与动作后走动平移归位。`
   > `- Low Density & Text Bounds: 单切片任意时刻活跃构件绝对 <= 3 个，通透留白 >= 70%。主标题 >= 80px，唱词字幕 >= 48px，标签 >= 36px，严禁任何 < 32px 小字，字多必须精简删字；SVG text 必须显式指定 font-family，第一行 <text> 必须显式指定 dominant-baseline="hanging" 或 y 坐标，标题组 translate.y 留足顶部安全距 (9:16 顶部 Y >= 240px)，进场动画严禁向上 negative Y 推顶，绝对防止字顶向上溢出端头裁切。`
   > `- Rotational Pivot (Needles/Gears): 仪表指针、齿轮、风车等旋转元素严禁 CSS transformOrigin，强制使用 GSAP svgOrigin: "cx cy" 锁死 viewBox 针座/旋转绝对轴心，杜绝偏心甩尾。`
   > `- Valve & Switch Joint: 阀门/开关必须按 3 层 DOM (阀体 -> 阀杆 -> 把手) 组织，把手旋转点精准挂载在阀杆销轴坐标，把手 rotation 必须同步驱动流体路径 shape 形变。`
   > `- Kinematic Scale Recipe: 天平必须解耦为支柱(不动)、横梁(绕中轴 cx cy 倾斜 θ)与左右托盘(挂于横梁端点)；横梁倾斜 θ 时，左右托盘必须同时执行 -θ 逆向旋转补偿 (Counter-Rotation)，保证托盘永远保持水平防脱落倾覆。`
   > `- Layout & UI Margins: 9:16 画布 Y: 0-200px 顶部与 Y: 1600-1920px 底部强制 100% 避让留白零构件；唱词字幕提升至 bottom: 320px。物理实体纵向 Top-to-Bottom 瀑布流排列。`
   > `- Subtitles: DOM #subtitles 强制 background: transparent; border: none; 浅色底深色字 #0f172a / 深色底纯白字 #ffffff，无任何卡片黑框。`
   > `- First Frame & Outro: t=0.0s 必须渲染标题背景与 IP 姿态防封面纯白；尾部单元绑定 [Action Recipe: LIKE_AND_SUBSCRIBE]。`
   > `- No Card Style: 场景构件强制使用 3 层 DOM 矢量结构 (Layer 1 基底 + Layer 2 纹理 + Layer 3 细节)，严禁纯色块占位或 <div class="card"> 矩形框。`

---

## 交付产物

- `./<article-slug>/assets/video/unit_01/` ~ `unit_N/`：各单元 HyperFrames 项目目录，含 `package.json`、`BRIEF.md`、`public/mascot.svg`、`public/audio.mp3`、`public/timestamps.json`。

---

## 关联参考规范

- `.agents/skills/hyperframes-core/references/brief-format.md`：BRIEF.md YAML Frontmatter 与 Body 结构定义（HyperFrames 官方源文件）。
- `.agents/skills/hyperframes-core/references/brief-contract.md`：BRIEF.md 字段枚举与模式派生定义（HyperFrames 官方源文件）。
- [`references/character_ip.md`](references/character_ip.md)：IP Mascot 视觉形象规范（支持自定义 IP 路由，默认小智）。
- [`references/mascot_svg_contract.md`](references/mascot_svg_contract.md)：IP Mascot 矢量节点契约（GSAP 可驱动的命名节点规范）。
- [`references/action_recipes.md`](references/action_recipes.md)：IP Mascot GSAP 物理动作范例库（推、拉、拖、踢、操作阀门等）。
- [`references/physical_metaphor_schema.md`](references/physical_metaphor_schema.md)：动态物理隐喻与 SVG 矢量生成思维指南（3 步推演法）。
- [`references/motion_chain_patterns.md`](references/motion_chain_patterns.md)：3 幕动态动作链设计范例与模式。
- [`references/storyboard_reviewer_standards.md`](references/storyboard_reviewer_standards.md)：分镜视觉与动作链盲审质检标准。
