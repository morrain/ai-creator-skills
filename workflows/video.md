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
   - 管道划分为 5 大递进步骤：**Step 1: 生成脚本** ➔ **Step 2: 生成语音** ➔ **Step 3: 设计单元分镜契约** ➔ **Step 4: 依次生成各单元 16:9 与 9:16 视频** ➔ **Step 5: 合成两种比例视频**。
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
   - 解析命令行参数 `/讲解视频 [文章路径或主题] [--style <preset>]`。
   - 若传入已有主题目录或文章路径（如 `./<article-slug>/<article-slug>.md`），进入**模式 1 (文章转视频)**。
   - 若传入纯主题字符串（如 `Vue 3.5 响应式原理`），进入**模式 2 (独立主题创作)**。
   - **显式风格选项支持**：若参数中指定了 `--style <preset>`（如 `--style blue-professional` 或 `--style code-editorial`），透传至 Step 3 锁定全局风格；若未指定，Step 3 自动根据主题领域自适应选型。
2. **调度原子技能 `video-script-writer` 提炼 4 轨剧本**：
   - 调度 `video-script-writer`（传入模式与输入文本），生成包含 `time_code`、`voiceover`、`visual_prompt & ip_action` 及 `on_screen_elements` 4 轨结构的 `video_script.json` 草案。
3. **SubAgent 剧本盲审闭环**：
   - 检查项目根目录是否存在自进化规则 `./learnings/video_script.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/video-script-writer/references/script_reviewer_standards.md` 与 `learnings_file: ./learnings/video_script.md`）；若不存在，启动 `blind-reviewer`（仅传入 `default_standards`）。
   - 校验语速节奏（4-5字/秒）、短句呼吸感、IP Mascot 动作定位及**尾部 3s 点赞关注 Outro 单元契约**。若结论为 `[REJECT]`，针对性修正直至 `[PASS]`。
4. **落盘剧本与 3s 独立 Outro 单元约束**：
   - 存盘至 `./<article-slug>/assets/video/video_script.json`。
   - **⚠️ 尾部 3s 独立单元强制规程**：剧本结尾 **必须单独划分为一个独立的视频单元**（即最后一个 `unit_N`，`duration_seconds: 3s`），专门用于互动引导（如 "如果对你有启发，记得点赞关注，我们下期见！"），绝对禁止将点赞关注引导口播与正文总结单元合并混写！
   - （仅当带有 `--interactive` 显式卡点选项时，暂停并等待回复 `[通过]` 后继续；默认无需人工审核，直接进入 Step 2）。

---

### Step 2: 生成语音 (Generate Voiceover & Lock Duration)

1. **读取剧本定稿**：
   - 读取 `./<article-slug>/assets/video/video_script.json`。
2. **调度原子技能 `voiceover-generator` 生成 TTS 音频与精确时间轴**：
   - 提取 `voiceover` 文案，调用 Edge-TTS (音色 `zh-CN-YunxiNeural`) 导出完整配音音频 `./<article-slug>/assets/video/audio/voiceover.mp3` 与字幕时间轴 `./<article-slug>/assets/video/audio/timestamps.json`。
   - 自动切分各个视频单元的音频文件 `./<article-slug>/assets/video/audio/unit_XX.mp3`。
   - 精确计算出各视频单元的**实际口播时长 $A_i$**，为 Step 3 注入 `BRIEF.md` 时长契约做前置准备。

---

### Step 3: 逐单元设计分镜契约与初始化工程 (Design Storyboard & Unit Workspaces)

1. **调度原子技能 `video-storyboard-designer` 提炼单元契约**：
   - 扫描正文插图描述（若存在），提取静态物理隐喻。
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
   - 写入 `./<article-slug>/assets/video/unit_XX/BRIEF.md`，显式注入口播时长 `length: max(A_i + 0.3s, 4.0s)`、风格预设 `style_preset`（优先使用显式指定的 `--style <preset>`，未指定则根据领域自适应选型）、3 幕动态动作链二次分镜切片、低密度限制规程、非 16:9 布局防裁剪规程、**首帧曝光与封面防白规程 (`t=0.0s` 即刻渲染高对比度封面与 IP 姿态)** 以及尾部单元专属 **`[Action Recipe: LIKE_AND_SUBSCRIBE]` 互动引导规程**。
4. **⚠️ Step 3 绝对禁令 (Strict Prohibition Rules)**：
   - **严禁编写初始化或 HTML 脚本**：Step 3 仅负责契约与脚手架逐单元初始化，**绝对禁止 Agent 编写任何批量初始化脚本（如 `setup_units.py`）或拼接 HTML/CSS/GSAP 代码的脚本（如 `build_unit_htmls.py`）**！
   - （仅当带有 `--interactive` 显式卡点选项时，暂停并等待回复 `[继续]` 后继续；默认无需人工审核，直接进入 Step 4）。

---

### Step 4: 逐单元唤起 SubAgent 生成 16:9 与 9:16 两种视频 (Render Unit Videos via HyperFrames SubAgents)

1. **⚠️ Step 4 核心调度原则 (SubAgent Invocation Mandate)**：
   - **严禁编写渲染脚本**：**绝对禁止 Agent 编写任何替代渲染的 Python 脚本（如 `render_all_units.py`）或在主进程中直接批量 Shell 渲染**！
   - **必须逐单元唤起 SubAgent**：主 Agent 必须通过 `invoke_subagent` **针对每一个 `unit_XX` 依次唤起独立的 HyperFrames 官方 SubAgent** 进驻 `./assets/video/unit_XX/` 目录，严格加载 HyperFrames 官方 Skill 执行 HTML 网页代码编写与 MP4 导出。
2. **按单元遍历并双比例连续渲染**：
   - 依次遍历 `./<article-slug>/assets/video/unit_01/` 到 `unit_N/`：
     - **第一阶段：渲染 16:9 宽屏版**：
       - 主 Agent 确保该单元的 `BRIEF.md` YAML Frontmatter 中 `aspect: 1920x1080`。
       - 显式调用 `invoke_subagent` 启动独立的 SubAgent，必须 100% 格式化传入以下固化的标准提示词模板：
         ```text
         1. 优先读取 HyperFrames 主控技能文件（`.agents/skills/hyperframes/SKILL.md`），严格按照其规程完成 HTML 组帧与渲染。
         2. 画幅与时长：卡点匹配 `BRIEF.md` 声明的 `aspect` 与 `length`。
         3. 矢量关节动画硬性规则 (GSAP svgOrigin Rule)：
            - 使用 GSAP 对 `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-leg-right`, `#mascot-head` 施加旋转/位移/缩放时，**必须且仅能使用 GSAP `svgOrigin: "X Y"` 锁定 300x400 viewBox 坐标**（如左肩 `svgOrigin: "90 205"`、右肩 `svgOrigin: "210 205"`、左髋 `svgOrigin: "120 300"`、右髋 `svgOrigin: "180 300"`、颈部 `svgOrigin: "150 160"`）。
            - **⚠️ 严禁使用 CSS `transformOrigin: "px px"`**，防止关节脱臼断裂。
         4. 物理隐喻动作绑定 (Action Recipe Execution)：
            - 必须严格执行 `BRIEF.md` 中指定的 Physical Action Recipe 模式（如 `[Action Recipe: PULL_DRAG]` 拖拽发力、`[Action Recipe: PUSH_PRESS]` 蓄力下压、`[Action Recipe: KICK_STEP]` 单腿踢飞、`[Action Recipe: OPERATE_LEVER]` 摇手柄/转阀门、`[Action Recipe: LIKE_AND_SUBSCRIBE]` 互动引导）。
         5. 音轨与字幕原生地固化：
            - 在 `index.html` 中挂载 `<audio id="unit-audio" class="clip" src="./public/audio.mp3"></audio>` 播放口播音频；
            - 读取 `public/timestamps.json` 建立 GSAP 字幕时间轴，在网页 DOM 中原生动态展示高对比度 HTML 唱词字幕。
         6. 首帧曝光与防白规程：
            - 在 `t=0.0s` 时，首帧必须通过 `gsap.set()` 渲染出主要标题、背景卡片与 IP Mascot 姿态，严禁首帧纯白空置。
         7. 执行渲染导出：
            - 运行命令 `npx hyperframes render "./<article-slug>/assets/video/unit_<XX>" --output="./<article-slug>/assets/video/unit_<XX>/unit_<XX>.mp4"`。

         【产物交付】
         完成渲染后，请仅回复 `[SUCCESS] 视频单元 unit_<XX> 制作完成，导出文件：./<article-slug>/assets/video/unit_<XX>/unit_<XX>.mp4`。
         ```
       - 渲染完成后，主 Agent 校验 `unit_<XX>.mp4` 存在且有效，将其归档备份为 `unit_<XX>_16x9.mp4`，并将源码备份存盘为 `BRIEF_16x9.md` 和 `index_16x9.html`。
     - **第二阶段：渲染 9:16 竖屏版**：
       - 主 Agent 将 `BRIEF.md` YAML Frontmatter 修改为 `aspect: 1080x1920`（同时写入非 16:9 防裁剪与竖屏流式布局规则）。
       - 再次唤起 HyperFrames 官方 SubAgent（传入提示词模板），执行 9:16 版本的代码调整与 MP4 导出。
       - 渲染完成后，主 Agent 校验 `unit_<XX>.mp4` 存在且有效，将其归档备份为 `unit_<XX>_9x16.mp4`，并将源码备份存盘为 `BRIEF_9x16.md` 和 `index_9x16.html`。

---

### Step 5: 合成两种比例视频 (Pure Video Stitching & Multi-Aspect Output)

1. **扫描多比例视频片段**：
   - 遍历扫描各个 `unit_XX` 目录下的 `unit_XX_16x9.mp4` 与 `unit_XX_9x16.mp4` 片段。
2. **调度原子技能 `video-renderer` 执行极速纯视频拼接**：
   - 运行 `video-renderer` 拼接脚本：
     ```bash
     python skills/video-renderer/scripts/render_final_video.py --project-dir ./<article-slug>/assets/video --fast-concat
     ```
   - **纯视频 Stitching 逻辑**：因为声音和字幕已经在 Step 3 & Step 4 中由 HyperFrames 网页画布原生集成并写入各个 `unit_XX` 视频片段，本步骤使用 `ffmpeg -f concat -c copy` 缝合，不重新压制字幕、不重新打字幕花字、不重算声音时间轴。若主题工作区存在 `bgm.mp3`，则追加音频背景音乐混音；若不存在，纯画面与语音音轨 100% 直通。
3. **交付最终成品 MP4**：
   - 输出两种比例的最终成品视频：
     - 横屏版：`./<article-slug>/video_16x9.mp4`（或软链 `./<article-slug>/video.mp4`）
     - 竖屏版：`./<article-slug>/video_9x16.mp4`
   - 在对话框呈报拼接完成信息与文件路径。
   - **自进化规则提示**：提示主编可使用 `/workflow-learn video_script` 或 `/workflow-learn video_storyboard` 沉淀自进化规程。
