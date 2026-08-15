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

---

## Agent 执行步骤协议 (Step-by-Step Protocol)

### 步骤一：路由解析 IP Mascot 形象规范
1. 检查是否存在 `./<slug>/character_ip.md`；若无，检查 `./character_ip.md`；若无，读取技能内置 [references/character_ip.md](references/character_ip.md)。
2. 提取 `Master Visual Prompt`（如 `Xiao Zhi robot, a 2D minimalist hand-drawn mascot...`）作为全局 IP 描述。

### 步骤二：读取剧本、推演物理隐喻、执行二次分镜拆解
1. 读取 `video_script.json` 的 `units` 数组，提取每个单元的 `duration_seconds`、`voiceover`、`visual_prompt`、`ip_action`。
2. 读取 [references/physical_metaphor_schema.md](references/physical_metaphor_schema.md)，按其 3 步推演法为每个单元的主题动态生成 SVG 物理骨架结构与节点 ID。
3. 结合口播台词与 `visual_prompt`/`ip_action`，对每个单元执行**二次分镜拆解**：梳理全量画面元素清单，划分为带时间戳的关键帧切片（如 `[Sub-shot 1]`、`[Sub-shot 2]`），显式绑定 **Physical Action Recipe**（如 `[Action Recipe: PULL_DRAG]`）。

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

   **YAML Frontmatter**（必填字段，不填 `style_preset`）：
   ```yaml
   workflow: faceless-explainer
   flow: automation
   storyboard: no
   aspect: 1920x1080
   message: <单元核心结论>
   length: <duration_seconds>
   ```

   **`## Intent` 板块**须包含：
   - **3 层矢量物理骨架草案（必须直接输出完整 Raw SVG XML 代码块）**：遵循 `physical_metaphor_schema.md` 3 步推演与 3 层矢量精细化指南，必须在 `## Intent` 中按物理实体解耦输出独立的具名 `<g id="...">` XML 构件组（如 `<g id="dam-body">`、`<g id="water-gate">`、`<g id="farmland-target">`），**每个构件内部独立封装其自身的 Layer 1 底座 + Layer 2 纹理 + Layer 3 细节/指示灯**。自解释图形切勿强行加字！**🚫 绝对禁止按 Layer 1/2/3 建立全局大组包裹所有实体（如 `<g id="macro-system"><g id="textures">...</g></g>`）！绝对禁止仅输出高层文字描述或无纹理死板裸框！**
   - **画面元素清单**：按切片列出所有活跃构件（含 `#mascot`），每切片 ≤ 5 个。
   - **二次分镜切片**：带时间戳（如 `[Sub-shot 1: 00:00-00:10]`），明确各元素入场/退场动画与 IP Recipe 绑定。

   **`## Assets` 板块**（强制写入）：
   ```
   - public/mascot.svg
   - public/audio.mp3
   - public/timestamps.json
   ```

   **`## Customizations` 板块**（强制写入）：
   > `- 低密度与通透留白规程：一屏仅表达 1 个核心结论 (One Statement Per Frame)，任意时刻 t DOM 活跃构件总数绝对 <= 5 个 (Cap Elements <= 5)，切片交接时执行 opacity:0 淡出退场 (Visibility Timeline Matrix)，屏蔽背景网格点、装饰线条或粒子等视觉噪声 (Suppress Chrome)，保持 70%+ 通透留白，严禁侧边解说卡片 (No Side Panels)。`

   **`## Notes` 板块**（强制写入以下全部规程）：
   > `- SVG Mascot Joint Animation: When animating SVG mascot elements (#mascot-arm-left, #mascot-arm-right, #mascot-leg-left, #mascot-leg-right, #mascot-head) with GSAP, ALWAYS use GSAP svgOrigin: "X Y" based on viewBox coordinates (e.g. svgOrigin: "90 205"), NEVER use CSS transformOrigin: "px px", to prevent arm dislocation.`
   > `- IP 与道具空间耦合规程：IP 角色与物理道具交互时，必须将 <g id="mascot"> 直接嵌入主场景 SVG 容器，或通过 gsap.set("#mascot", { x, y }) 对齐绝对坐标，确保手掌/手臂接触点 100% 触碰道具锚点。严禁 IP 在独立底部 div 而道具在顶部 SVG 中。`
   > `- IP 角色常驻微呼吸与 5s 习惯性微动作规程：在 index.html 中必须建立常驻微动作引擎，挂载 Y 轴 2.2s 浮动呼吸 + 3.5s 眨眼循环，并每 4~5s 周期性触发习惯性微动作（点头微摇手、侧身摇头、手势点按脉冲），消除场景静止僵硬感，无需复杂的画面静止检测！`
   > `- IP 角色空间智能避让与留白停留规程：在场景主体进行核心演示/放大的停留状态时，IP Mascot 必须通过 GSAP 自动平移避让至画布两侧的通透留白槽 (Negative Space, 对角互补法则：主体居右则 IP 避让至左侧 X:250，主体居左则 IP 避让至右侧 X:1650)，并微调头尖/眼珠朝向主体，绝对禁止在静止停留状态时停留在中央遮挡主体内容！`
   > `- IP Mascot 矢量源码嵌入与最顶层渲染规程：在 index.html 中，必须将 public/mascot.svg 内部包含 #mascot-head, #mascot-arm-left, #mascot-arm-right, #mascot-leg-left, #mascot-leg-right, #mascot-body 的完整 <g> 矢量 DOM 节点直接原样内嵌写入主场景 <g id="mascot"> 内部。在 <svg> DOM XML 结构中，<g id="mascot"> 必须放置在所有场景背景与物理实体 (如 #dam, #farmland, #chip, #stream) 的最下排末尾节点。基于 SVG Painter's Model 画家法则，DOM 顺序靠后的节点必定覆盖前面的节点，由此 100% 保证 IP 形象渲染在最顶层，绝对不被场景遮挡！严禁使用跨文件 <use href="./public/mascot.svg#..."> 标签，绝对禁止手写或脑补生成 <rect fill="#fbbf24"> 等彩色块/粗线条占位图形替代 IP 形象！`
   > `- 音轨绑定规程：必须在 index.html 中挂载 <audio id="unit-audio" class="clip" src="./public/audio.mp3" data-start="0" data-duration="..." data-track-index="0"></audio>。`
   > `- 字幕同步规程：必须读取 public/timestamps.json 建立 GSAP 字幕时间轴，在 DOM 中动态展示高对比度唱词字幕。`
   > `- 非 16:9 物理实体纵向流与防缩小规程：针对 9:16 竖屏画幅，必须将 3 层物理骨架中解耦的独立 <g id="..."> 构件由横向排列重构成纵向 Top-to-Bottom 瀑布流 (上:源头实体 ➔ 中:控制阀门 ➔ 下:受水目标)，同时将构件尺寸放大 1.3x~1.5x (充盈 1080px 宽度)，管道 path 改为纵向 V 形式，绝对禁止将全场景打包在单一死板组中导致竖屏整体缩成一小条！`
   > `- 9:16 视频平台 (小红书/抖音/视频号) 底部 UI 避让留白规程：针对 9:16 竖屏，底部 Y: 1600px - 1920px (至少 320px+) 必须保留为纯净背景避让留白区，唱词字幕盒子必须向上提升放置在 bottom: 320px (Y: 1460px - 1580px) 处，绝对禁止在底部 320px 内放置任何实体构件或字幕，防止发布后被小红书/抖音的头像、作者文案与互动按钮覆盖遮挡！`
   > `- IP Mascot 全局最高 Z-Index 最顶层置顶规程：在 index.html 中，必须将 public/mascot.svg 的完整 <g> 矢量节点直接内嵌写入 <g id="mascot">，并将其放置在全局最高层级 (z-index: 100，高于 Title Card z-index: 50 与场景 z-index: 10)。无论 IP Mascot 巡视位移至画面任何区域（包含靠近顶部标题栏），均 100% 保持为绝对最顶层，彻底杜绝任何图层压头遮挡！严禁使用跨文件 <use> 标签或手写彩色方块占位。`
   > `- 首帧防空白封面规程：t=0.0s 时首帧绝对不能是纯白画布！必须通过 gsap.set() 在 t=0 渲染主要标题、背景卡片与 IP 姿态 (opacity: 1)，确保小红书/微信视频号自动抽取的封面丰富可读。`
   > `- 字号下限规程：主标题 ≥ 64px、副标题/卡片标题 ≥ 38px、正文/标签 ≥ 32px（绝对禁止 font-size < 30px）、数据大字 ≥ 56px、唱词字幕 ≥ 44px、SVG 图表文字 ≥ 30px。`
   > `- SVG 文本字体与顶部防裁切规程：SVG 内部所有 <text> 节点必须显式指定 font-family（或在全局 CSS 中设置 svg text { font-family: "Noto Sans SC", sans-serif; }）；主标题组 transform 必须留足顶部安全距（16:9 顶部 translate.y ≥ 160px，9:16 顶部 translate.y ≥ 240px），第一行 <text> 必须显式设置 y 坐标（如 y="50" 或 dominant-baseline="hanging"），且标题进场动画禁止使用向上推顶的 y 位移（如 y: -25），绝对防止字顶向上溢出顶端边缘裁切。`
   > `- 尾部 Outro 规程：全片最后 ~3s Outro 单元必须绑定 [Action Recipe: LIKE_AND_SUBSCRIBE]，驱动 IP 欢快跳跃并举起点赞、收藏、关注互动徽章。`
   > `- 禁止 Dashboard UI 卡片风格：物理实体（水库、闸门、阀门、齿轮等）必须使用 SVG 矢量线条绘制，严禁用 <div class="card"> 矩形框替代。`

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
