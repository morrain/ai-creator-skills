---
name: workflow-video
command: /讲解视频
description: 动画讲解视频全流程生成工作流。当用户发送 /讲解视频 指令、或需要将文章/知识主题转化为带有配音、IP Mascot 动作链与视频渲染的 MP4 时唤起。
---

# 🎬 动画讲解视频生成业务工作流 (Explainer Video Business Workflow)

本工作流为 `ai-creator-skills` 项目的动画讲解视频生成管道。负责接收输入（支持模式 1：已生成的长文路径 `./<article-slug>/<article-slug>.md`；或模式 2：独立知识主题），调度底层原子技能（`video-script-writer`、`voiceover-generator`、`video-storyboard-designer`、`video-renderer` 以及 HyperFrames 官方 Agent Skills 套件），自动贯穿执行 5 个标准的连续步骤。

---

## 核心设计原则 (Core Principles)

> ⚠️ **单一事实源 (Single Source of Truth) 执行约束**：
> 本板块仅对管道的核心架构进行高层定义。Agent 在实际执行工作流时，**必须且只能以下方【详细工作流步骤】中的具体规程、算法逻辑与 100% 固化的 SubAgent Prompt 模板作为唯一执行依据**，绝对禁止根据高层摘要直接提取指令或自由生成 SubAgent 提示词！

1. **双模式自适应输入 (Dual-Mode Input Handling)**：
   - 支持文章转视频 (`article_derived`) 与独立知识主题创作 (`standalone_topic`) 双模式自适应流。
2. **默认免人工审核原则 (Default Non-Interactive Execution)**：
   - 管道划分为 5 大递进步骤：**Step 1: 生成脚本** ➔ **Step 2: 生成语音** ➔ **Step 3: 设计单元分镜契约** ➔ **Step 4: 逐单元渲染 9:16 竖屏切片（及可选 16:9 宽屏切片）** ➔ **Step 5: 合成成品视频**。
   - **默认仅生成 9:16 竖屏格式**：为了适配移动端主流媒体平台（小红书/微信视频号/抖音/Shorts），工作流默认仅渲染 9:16 竖屏视频（`1080x1920`）。仅当用户命令行或指令中显式包含生成宽屏版本的指令（如包含 `--widescreen` 选项或明确要求生成宽屏版本）时，才会在 9:16 渲染完成后，逐单元继续渲染生成 16:9 宽屏切片（`1920x1080`）。
   - **默认无需人工审核**：管道默认在各步骤间自主衔接运行。在 Step 4 中，主 Agent 在后台逐个单元唤起 HyperFrames SubAgent 进行 HTML 制作与视频渲染，子 Agent 交付后自主切入下一个单元，全程无需人类用户手动 Confirm。
   - 仅当用户命令行指令中显式包含 `--interactive` 选项时，才会在 Step 1 与 Step 3 停顿等待人工 Confirmation。
3. **音画字幕单元内固化与纯视频缝合 (Unit Self-Contained Audio & Subtitles)**：
   - 音频配音、时间戳与美化 HTML 字幕在 Step 3 & Step 4 渲染视频单元时已原生固化压制在单元 MP4 中。Step 5 仅做极速纯视频 `ffmpeg -c copy` 拼接，不重新压制字幕或重算声音。
4. **双轨自进化规则闭环 (`/workflow-learn`)**：
   - 支持主编通过 `/workflow-learn video_script` 与 `/workflow-learn video_storyboard` 沉淀动画与文案规程。

---

## 详细工作流步骤

### Step 1: 生成脚本 (Generate Script & Review)

1. **输入解析与短路模式识别**：
   - 解析命令行参数 `/讲解视频 [文章路径或主题]`。
   - 若传入已有主题目录或文章路径（如 `./<article-slug>/<article-slug>.md`），进入**模式 1 (文章转视频)**。
   - 若传入纯主题字符串（如 `Vue 3.5 响应式原理`），进入**模式 2 (独立主题创作)**。
   - **低密度视觉排版规程**：在 `BRIEF.md` 中不填写 `style_preset` 字段。视频排版严格遵循低密度呼吸感规程（70%+ 留白空间，一屏仅表达 1 个核心结论，单切片活跃元素 $\le 5$）。
2. **调度原子技能 `video-script-writer` 提炼 4 轨剧本**：
   - 调度 `video-script-writer`（传入模式与输入文本），生成包含 `metadata.visual_theme` 全局视觉主题代币、`time_code`、`voiceover`、`visual_prompt & ip_action` 及 `on_screen_elements` 4 轨结构的 `video_script.json` 草案。
3. **SubAgent 剧本盲审闭环**：
   - 检查项目根目录是否存在自进化规则 `./learnings/video_script.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/video-script-writer/references/script_reviewer_standards.md` 与 `learnings_file: ./learnings/video_script.md`）；若不存在，启动 `blind-reviewer`（仅传入 `default_standards`）。
   - 校验语速节奏（4-5字/秒）、短句呼吸感、IP Mascot 动作定位、**全局视觉主题 `visual_theme` 代币完整性**及**尾部 3s 点赞关注 Outro 单元契约**。若结论为 `[REJECT]`，针对性修正直至 `[PASS]`。
4. **落盘剧本与 3s 独立 Outro 单元约束**：
   - 存盘至 `./<article-slug>/assets/video/video_script.json`。
   - **⚠️ 尾部 3s 独立单元强制规程**：剧本结尾 **必须单独划分为一个独立的视频单元**（即最后一个 `unit_N`，`duration_seconds: 3s`），专门用于互动引导（如 "如果对你有启发，记得点赞关注，我们下期见！"），绝对禁止将点赞关注引导口播与正文总结单元合并混写！
   - （仅当带有 `--interactive` 显式卡点选项时，暂停并等待回复 `[通过]` 后继续；默认无需人工审核，直接进入 Step 2）。

---

### Step 2: 生成语音 (Generate Voiceover & Lock Duration)

1. **读取剧本定稿**：
   - 读取 `./<article-slug>/assets/video/video_script.json`。
2. **调度原子技能 `voiceover-generator` 生成 TTS 音频与精确时间轴**：
   - 提取 `voiceover` 文案，调用 Edge-TTS (音色 `zh-CN-YunxiNeural`) 导出完整配音音频 `./<article-slug>/assets/video/audio/voiceover.mp3` 与字幕时间轴 `./<article-slug>/assets/video/audio/timestamps.json`（同时在 `metadata` 中透传 `visual_theme` 声明）。
   - 自动切分各个视频单元的音频文件 `./<article-slug>/assets/video/audio/unit_XX.mp3`。
   - 精确计算出各视频单元的**实际口播时长 $A_i$**，为 Step 3 注入 `BRIEF.md` 时长契约做前置准备。

---

### Step 3: 逐单元设计分镜契约与初始化工程 (Design Storyboard & Unit Workspaces)

1. **调度原子技能 `video-storyboard-designer` 提炼单元契约**：
   - 扫描正文插图描述（若存在），提取静态物理隐喻。
   - 读取 `video_script.json` 中的 `metadata.visual_theme` 提取全集统一视觉配色代币。
   - 将 `video_script.json` 拆解为 $N$ 个独立视频单元（`unit_01`, `unit_02`, ...），在 `./<article-slug>/assets/video/` 下逐单元建立独立工作区。
2. **逐单元独立运行 HyperFrames 初始化命令 (Per-Unit Sequential Init)**：
   - **主 Agent 必须对每一个 `unit_XX` 依次串行执行**初始化命令（**绝对禁止编写 `setup_units.py` 等 Python 脚本进行批量处理**）：
     ```bash
     HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init "./<article-slug>/assets/video/unit_XX" --non-interactive --example=blank
     ```
3. **前置资源与关键契约注入**：
   - 将本单元所需的前置依赖资产逐个拷贝落盘至 `./<article-slug>/assets/video/unit_XX/public/`：
     - `public/mascot.svg`（矢量 IP 角色资产）
     - `public/audio.mp3`（复制自 `../audio/unit_XX.mp3` 本单元配音切片）
     - `public/timestamps.json`（复制自 `../audio/timestamps.json` 本单元字幕时间戳契约）
   - 写入 `./<article-slug>/assets/video/unit_XX/BRIEF.md`，显式注入口播时长 `length: max(A_i + 0.3s, 4.0s)`（在 Frontmatter 注入 `theme` 代币）、3 幕动态动作链二次分镜切片、低密度限制规程、非 16:9 布局防裁剪规程、**全局视觉主题 Token 继承铁律**、**首帧曝光与封面防白规程 (`t=0.0s` 即刻渲染高对比度封面与 IP 姿态)** 以及尾部单元专属 **`[Action Recipe: LIKE_AND_SUBSCRIBE]` 互动引导规程**。
4. **⚠️ Step 3 绝对禁令 (Strict Prohibition Rules)**：
   - **严禁编写初始化或 HTML 脚本**：Step 3 仅负责契约与脚手架逐单元初始化，**绝对禁止 Agent 编写任何批量初始化脚本（如 `setup_units.py`）或拼接 HTML/CSS/GSAP 代码的脚本（如 `build_unit_htmls.py`）**！
   - （仅当带有 `--interactive` 显式卡点选项时，暂停并等待回复 `[继续]` 后继续；默认无需人工审核，直接进入 Step 4）。

---

### Step 4: 逐单元渲染 9:16 竖屏视频片段（及可选 16:9 宽屏片段） (Render 9:16 Portrait & Optional 16:9 Widescreen Per Unit)

1. **⚠️ Step 4 核心调度原则 (SubAgent Invocation Mandate)**：
   - **单Turn逐单元单比例串行调度 (Strict Sequential Execution Mandate)**：**主 Agent 在单个推理 Turn 中绝对禁止并发唤起多个 SubAgent！** 针对每一个 `unit_XX`，默认首先串行唤起 SubAgent 完成 9:16 竖屏版本的制作与渲染归档。仅当用户有明确指令要生成宽屏版本（如包含 `--widescreen` 或要求生成宽屏）时，收到 9:16 响应后再串行唤起 SubAgent 完成 16:9 宽屏版本的制作与渲染归档。当前单元所需比例渲染完成后，主 Agent 方可切入下一个单元 `unit_YY`。
   - **强制 SubAgent 写入权限 (SubAgent TypeName Mandate)**：主 Agent 在通过 `invoke_subagent` 唤起 SubAgent 时，**必须显式将其 `TypeName` 参数设置为具有文件写入与代码编辑权限的全功能型代理 `self`**，**绝对禁止错误地设置为只读的 `research`（研究型子代理）**！否则 SubAgent 将因缺乏写入权限而无法写入 `index.html` 或导出 MP4 视频。
   - **严禁编写渲染脚本**：**绝对禁止 Agent 编写任何替代渲染的 Python 脚本（如 `render_all_units.py`）或在主进程中直接批量 Shell 渲染**！
   - **必须逐单元依次串行唤起 SubAgent**：主 Agent 必须通过 `invoke_subagent` 依次逐个进驻 `./assets/video/unit_XX/` 目录，严格加载 HyperFrames 官方 Skill 执行 HTML 网页代码编写与 MP4 导出。
2. **逐单元渲染流程**：
   - 依次遍历 `./<article-slug>/assets/video/unit_01/` 到 `unit_N/`：
     - **【阶段 A：默认渲染 9:16 竖屏版 (Default Aspect: 1080x1920)】**：
       - 主 Agent 确保该单元的 `BRIEF.md` YAML Frontmatter 中 `aspect: 1080x1920`（同时在 `## Notes` 中写入物理实体纵向 Top-to-Bottom 瀑布流排列、构件 1.3x~1.5x 放大与管道 Path V-path 转换规则，防止画面缩成一小条）。
       - 显式调用 `invoke_subagent` 启动独立的 SubAgent（**必须设置 `TypeName: "self"`**），必须 100% 格式化传入以下精简的标准提示词模板：
         ```text
         1. 优先读取 HyperFrames 主控技能文件（`.agents/skills/hyperframes/SKILL.md`），严格按照其规程完成 HTML 组帧与渲染。
         2. 画幅、时长与全局视觉主题：卡点匹配 `BRIEF.md` 声明的 `aspect` (`1080x1920`) 与 `length`，且必须 100% 继承 BRIEF.md Frontmatter 中声明的 `theme` 配色代币（背景 Canvas BG、主色 Primary Accent 等），全局统一使用相同调色盘，绝对禁止单独更换纯黑或无关底色。
         3. 矢量精细化与 3 层结构规程（物理实体硬性铁律）：
            - **强制 3 层 DOM 结构**：所有物理实体（如农田、水库大坝、水闸阀门、渠道水流、芯片、数据库等）必须封装在 `<g id="...">` 组内，且必须完整包含 3 层 DOM 元素：
              1) Layer 1 实体基底：带有 fill 充盈色与 stroke 轮廓的底座/基础图形；
              2) Layer 2 具象特征纹理：必须包含至少 2 条以上表达物理特征的 `<path>` 路径（如农田田垄与幼苗 `<path>`、水库/大坝刻度与波纹 `<path>`、芯片电路/引脚 `<path>`、阀门轮辐/螺纹 `<path>`）；
              3) Layer 3 微观细节与可选标示：螺帽/铆钉点位、LED 发光指示灯、刻度指针、高光/阴影切线等微观质感细节，或必要时的精简中文 `<text>`（图样自解释的实体切勿强行加文字破坏拟物美感）。
            - **🚫 反例硬禁令**：针对物理实体，**绝对禁止在 index.html 中仅用单个 `<rect>`、`<circle>` 或 `<polygon>` 标签占位充当实体**！若检测到仅用单个无纹理裸框/几何块作为物理实体，渲染质检将直接判定失败打回。同时保留全部指定的 `id` 供 GSAP 驱动。
         4. IP Mascot 矢量源码嵌入与关节动画硬性规则：
             - **DOM 节点强制内联与最顶层渲染**：必须直接将 `public/mascot.svg` 内部包含 `#mascot-head`, `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-leg-right`, `#mascot-body` 的完整 `<g>` 矢量 DOM 节点原样复制内嵌写入 `index.html` 的 `<g id="mascot">` 内部。在 `<svg>` 主画布中，**`<g id="mascot">` 必须放在所有物理场景构件（水坝、管道、芯片、水流等）的最后方（末位 DOM 节点）**。基于 SVG Painter's Model 绘制规则，后置节点必定置顶，100% 保证 IP 形象在最上一层不被场景遮挡！**严禁使用 `<use href="./public/mascot.svg#...">`**，**绝对禁止手写或脑补生成 `<rect fill="#fbbf24">` 等彩色块/粗线条占位图形**！
             - **GSAP svgOrigin 关节锁死与常驻 5s 微动作引擎**：使用 GSAP 对 `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-leg-right`, `#mascot-head` 施加旋转/位移/缩放时，**必须且仅能使用 GSAP `svgOrigin: "X Y"` 锁定 300x400 viewBox 坐标**（如左肩 `svgOrigin: "90 205"`、右肩 `svgOrigin: "210 205"`、左髋 `svgOrigin: "120 300"`、右髋 `svgOrigin: "180 300"`、颈部 `svgOrigin: "150 160"`）。同时**必须建立常驻双层微动作引擎**（2.2s 浮动呼吸 + 3.5s 眨眼 + 每 4~5s 习惯性微动作循环如点头晃手臂），彻底杜绝镜头长达 5~6s 的静止死板。
             - **⚠️ IP Mascot 关节旋转防脱臼正反示例**：
                - ❌ **错误写法（绝对禁止！使用 CSS transformOrigin 会以包围盒左上角二次偏移，导致关节脱臼断裂）**：
                  `gsap.set("#mascot-arm-left", { transformOrigin: "90px 210px" });`
                - ✅ **正确写法（必须严格遵循！锁定 SVG viewBox 全局画布坐标）**：
                  `gsap.set("#mascot-arm-left", { svgOrigin: "90 205" });`
                  `gsap.set("#mascot-arm-right", { svgOrigin: "210 205" });`
                  `gsap.set("#mascot-leg-left", { svgOrigin: "120 300" });`
                  `gsap.set("#mascot-leg-right", { svgOrigin: "180 300" });`
                  `gsap.set("#mascot-head", { svgOrigin: "150 160" });`
              - **⚠️ 物理构件自转防甩飞规则（阀门/手轮/齿轮）**：手轮圆盘与内部轮辐线条必须统一封装在同一个 `<g id="xxx-wheel">` 矢量组内。使用 GSAP 驱动其旋转时，**必须强制使用 `svgOrigin: "X Y"` 传入其 viewBox 中心坐标**，绝对禁止误用 CSS `transformOrigin: "px px"`（因为 CSS transformOrigin 会以元素包围盒左上角二次偏移计算，导致手轮偏离原点做巨型圆周公转并甩飞出画面）。
              - **⚠️ IP Mascot 动作完成走动归位与空白待命注视规程**：IP Mascot 在物理构件处完成指定动作任务（拉手柄/搬箱子/按按钮）后，若无后续动作，必须通过 GSAP 触发双腿交替摆动（yoyo 摆腿 rotation ±25°）平移归位回退至空白待命区（Home Anchor），并微倾头部与视角（rotation: ±8°）持续注视当前核心构件，绝对禁止动作完成后长期滞留在物理实体上遮挡画面！
         5. 画布三区安全隔离与平台 UI 底部留白规程：
             - **画布三区隔离**：画面划分为 **顶部标题区**（Y: 60-200px）、**中间主舞台视觉区**（9:16 Y: 240-1550px）、**唱词字幕区**（9:16 bottom: 320px，即 Y: 1460-1580px）。
             - **9:16 视频平台 (小红书/抖音) 底部 UI 避让留白**：9:16 竖屏底部 **Y: 1600px - 1920px (至少 320px+)** 必须保留为纯净背景避让留白区（Zero Elements），唱词字幕盒子向上提升至 `bottom: 320px` 处，绝对禁止在底部 320px 放置任何实体或字幕，防止发布后被小红书/抖音的作者头像、文案与互动按钮遮挡！
            - **SVG 文本防覆盖**：所有 `<text>` 标签必须放置在实体边框、管道水流或阀门外侧（保留 15px+ 间距）或显式使用 `dominant-baseline="hanging"`/`middle`，绝对禁止文本基线与实体线条重合叠加。
          6. 物理隐喻动作绑定 (Action Recipe Execution)：
             - 必须严格执行 `BRIEF.md` 中指定的 Physical Action Recipe 模式（如 `[Action Recipe: PULL_DRAG]`、`[Action Recipe: PUSH_PRESS]`、`[Action Recipe: OPERATE_LEVER]`、`[Action Recipe: LIKE_AND_SUBSCRIBE]`），**且在每次物理动作任务完成后，必须强制挂载 `references/action_recipes.md` 中的 `[Action Recipe: EXECUTE_THEN_RETREAT]` 动作组，驱动 IP 双腿交替摆动走动平移回退至 BRIEF.md 约定的空白待命点**。
         7. 音轨与字幕原生地固化：
            - 在 `index.html` 中挂载 `<audio id="unit-audio" class="clip" src="./public/audio.mp3"></audio>` 播放口播音频；
            - 读取 `public/timestamps.json` 建立 GSAP 字幕时间轴，在网页 DOM 中原生动态展示高对比度 HTML 唱词字幕。
         8. 首帧曝光与防白规程：
            - 在 `t=0.0s` 时，首帧必须通过 `gsap.set()` 渲染出主要标题、背景卡片与 IP Mascot 姿态，严禁首帧纯白空置。
         9. 执行 9:16 竖屏渲染导出：
            - 运行命令 `npx hyperframes render "./<article-slug>/assets/video/unit_<XX>" --output="./<article-slug>/assets/video/unit_<XX>/unit_<XX>.mp4" --resolution portrait`。

         【产物交付】
         完成渲染后，请仅回复 `[SUCCESS] 视频单元 unit_<XX> 制作完成，导出文件：./<article-slug>/assets/video/unit_<XX>/unit_<XX>.mp4`。
         ```
       - 渲染完成后，主 Agent 校验 `unit_<XX>.mp4` 存在且有效，将其归档备份为 `unit_<XX>_9x16.mp4`，并将源码备份存盘为 `BRIEF_9x16.md` 和 `index_9x16.html`。
     - **【阶段 B：可选渲染 16:9 宽屏版 (Optional Aspect: 1920x1080 - 仅在用户明确指令时触发)】**：
       - **仅当用户有明确指令要生成宽屏版本时**（如命令行中包含 `--widescreen` 或显式要求生成宽屏）：
       - 主 Agent 将该单元 `BRIEF.md` YAML Frontmatter 修改为 `aspect: 1920x1080`。
       - 再次显式调用 `invoke_subagent` 启动 SubAgent（**必须设置 `TypeName: "self"`**），执行 16:9 宽屏版本的代码调整与 MP4 导出：`npx hyperframes render "./<article-slug>/assets/video/unit_<XX>" --output="./<article-slug>/assets/video/unit_<XX>/unit_<XX>.mp4"`。
       - 渲染完成后，主 Agent 校验 `unit_<XX>.mp4` 存在且有效，将其归档备份为 `unit_<XX>_16x9.mp4`，并将源码备份存盘为 `BRIEF_16x9.md` 和 `index_16x9.html`。
     - 该单元当前所需比例渲染归档完成后，主 Agent 自主切入下一个单元 `unit_YY`。

---

### Step 5: 合成成品视频 (Stitch Final Videos)

1. **前置门控 (Strict Execution Gate)**：
   - **全量单元渲染完成触发**：必须在所有单元（`unit_01` 至 `unit_N`）的 9:16 竖屏切片片段（`unit_XX_9x16.mp4` 或 `unit_XX.mp4`）全部渲染成功且归档完毕后，方可触发 Step 5 缝合！若用户要求生成宽屏版本，则需等待 16:9 切片片段（`unit_XX_16x9.mp4`）也归档完毕。
2. **极速缝合导出成品视频**：
   - 调度原子技能 `video-renderer` 运行纯视频拼接脚本：
     ```bash
     python skills/video-renderer/scripts/render_final_video.py --project-dir ./<article-slug>/assets/video --fast-concat
     ```
   - 脚本会自动扫描各个 `unit_XX` 目录下的切片，通过 `ffmpeg -c copy` 极速缝合导出成品视频。
3. **交付成品与自进化闭环**：
   - 校验并在对话框呈报最终成品视频文件路径：
     - 竖屏成品版（默认）：`./<article-slug>/video_9x16.mp4`（或软链/复制 `./<article-slug>/video.mp4`）
     - 宽屏成品版（仅当显式要求生成宽屏时）：`./<article-slug>/video_16x9.mp4`
   - **自进化规则提示**：提示主编可使用 `/workflow-learn video_script` 或 `/workflow-learn video_storyboard` 沉淀自进化规程。
