---
name: workflow-video
command: /讲解视频
description: 动画讲解视频全流程生成工作流。当用户发送 /讲解视频 指令、或需要将文章/知识主题转化为带有配音、IP Mascot 动作链与视频渲染的 MP4 时唤起。
---

# 🎬 动画讲解视频生成业务工作流 (Explainer Video Business Workflow)

本工作流为 `ai-creator-skills` 项目的动画讲解视频生成管道。负责接收输入（支持模式 1：已生成的长文路径 `./<article-slug>/<article-slug>.md`；或模式 2：独立知识主题），调度底层原子技能（`video-script-writer`、`voiceover-generator`、`video-storyboard-designer`、`video-renderer` 以及 HyperFrames 官方 Agent Skills 套件），并运行 SubAgent 剧本盲审与 3 阶段人工确认卡点闭环。

---

## 核心设计原则 (Core Principles)

> ⚠️ **单一事实源 (Single Source of Truth) 执行约束**：
> 本板块仅对管道的核心架构与卡点原则进行高层定义。Agent 在实际执行工作流时，**必须且只能以下方【详细工作流步骤】中的具体规程、算法逻辑与 100% 固化的 SubAgent Prompt 模板作为唯一执行依据**，绝对禁止根据高层摘要直接提取指令或自由生成 SubAgent 提示词！

1. **双模式自适应输入 (Dual-Mode Input Handling)**：
   - 支持文章转视频 (`article_derived`) 与独立知识主题创作 (`standalone_topic`) 双模式自适应流。
2. **四阶段交互与人工卡点闭环 (Four-Stage Human Gate Protocol)**：
   - 管道分为 **阶段一 (剧本盲审卡点)** ➔ **阶段二 (TTS 时长反向锁定卡点)** ➔ **阶段三 (SubAgent 单元制作卡点)** ➔ **阶段四 (FFmpeg 硬件加速导出)** 4 个递进阶段。
3. **双轨自进化规则闭环 (`/workflow-learn`)**：
   - 支持主编通过 `/workflow-learn video_script` 与 `/workflow-learn video_storyboard` 沉淀动画与文案规程。

---

## 详细工作流步骤

### 阶段一：4 轨剧本提炼、SubAgent 盲审、落盘与人工 Confirm 卡点

1. **输入解析与短路模式识别**：
   - 解析命令行参数 `/讲解视频 [文章路径或主题]`。
   - 若传入已有主题目录或文章路径（如 `./<article-slug>/<article-slug>.md`），进入**模式 1 (文章转视频)**。
   - 若传入纯主题字符串（如 `Vue 3.5 响应式原理`），进入**模式 2 (独立主题创作)**。
2. **调度原子技能 `video-script-writer` 提炼 4 轨剧本**：
   - 调度 `video-script-writer`（传入模式与输入文本），生成包含 `time_code`、`voiceover`、`visual_prompt & ip_action` 及 `on_screen_elements` 4 轨结构的 `video_script.json` 草案。
3. **SubAgent 剧本盲审闭环**：
   - 检查项目根目录是否存在自进化规则 `./learnings/video_script.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/video-script-writer/references/script_reviewer_standards.md` 与 `learnings_file: ./learnings/video_script.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards: skills/video-script-writer/references/script_reviewer_standards.md`）。
   - 校验语速节奏（4-5字/秒）、短句呼吸感与 IP Mascot 动作定位。若结论为 `[REJECT]`，针对性修正直至 `[PASS]`。
4. **落盘剧本与呈现原文**：
   - 盲审 `[PASS]` 后，在主题工作区新建 `./<article-slug>/assets/video/` 子目录，将定稿存盘至 `./<article-slug>/assets/video/video_script.json`。
   - 在对话框中**全量呈报 4 轨剧本结构**（附链接 [`./<article-slug>/assets/video/video_script.json`](./<article-slug>/assets/video/video_script.json)）。
5. **阶段一人工 Confirm 卡点提示**：
   - **暂停并等待确认**：
     > 💡 **主编审阅与自进化提示**：
     > 1. 剧本满意请回复 **`[通过]`** 或 **`[继续]`**，系统将生成 TTS 配音与视频单元契约。
     > 2. 如对剧本字句进行了人工修饰，请回复 **`/workflow-learn video_script`** 提炼您对视频脚本的偏好规程！

---

### 阶段二：TTS 音频生成、时长反向契约锁定与 HyperFrames BRIEF.md 落盘

1. **读取剧本定稿与插图继承**：
   - 用户确认 `[通过]` 后，读取 `./<article-slug>/assets/video/video_script.json`。
2. **调度原子技能 `voiceover-generator` 生成 TTS 音频与精确时间轴（先生成）**：
   - 提取 `voiceover` 文案，调用 Edge-TTS (音色 `zh-CN-YunxiNeural`) 导出完整配音音频 `./<article-slug>/assets/video/audio/voiceover.mp3` 与字幕时间轴 `./<article-slug>/assets/video/audio/timestamps.json`。
   - 精确计算出各视频单元的**实际口播时长 $A_i$**。
3. **调度原子技能 `video-storyboard-designer` 反向注入口播时长并构建 BRIEF.md 契约**：
   - 扫描 `./<article-slug>/assets/illustration_*.md`（若存在），提取静态物理隐喻。
   - 将 `video_script.json` 拆解为 $N$ 个独立视频单元（`unit_01`, `unit_02`, ...），在 `./<article-slug>/assets/video/unit_XX/` 下建立独立工作区。
   - 针对每个视频单元，写入符合 HyperFrames 官方标准规范的 `./<article-slug>/assets/video/unit_XX/BRIEF.md`。
   - **关键时长契约注入**：显式将该单元的实际 TTS 时长注入契约中 `length: max(A_i + 0.3s, 4.0s)`，确保下一步 HyperFrames GSAP 动画构建时天然匹配口播长度。按契约落盘矢量 IP 资产 `./<article-slug>/assets/video/unit_XX/public/mascot.svg`。
4. **呈报预览与阶段二 Confirm 卡点提示**：
   - 在对话框呈现各视频单元 3 幕动作链摘要及试听音频生成信息。
   - **暂停并等待显式渲染指令**：
     > 💡 **视频单元预览与渲染确认提示**：
     > 1. 回复 **“开始渲染视频”**：开启【单单元逐个审核模式】（每单元渲染后暂停确认）。
     > 2. 回复 **“开始全自动渲染”**：开启【全自动批次渲染模式】（自动连续渲染全部单元后一次性呈报）。

---

### 阶段三：HyperFrames 官方 Skill SubAgent 独立单元制作与双模式渲染

1. **触发显式渲染指令**：
   - 收到用户回复 **“开始渲染视频”** 或 **“开始全自动渲染”**。
2. **派发 SubAgent 制作各视频单元 MP4 片段**：
   - 遍历 `./<article-slug>/assets/video/unit_XX/` 目录：
     - 显式调用 `invoke_subagent` 启动独立的 `unit-worker` SubAgent，隔离上下文与 DOM/GSAP 逻辑干扰。必须使用如下提示词模板，不能自己生成提示词。
     - **SubAgent 唤起提示词模板**：派发 SubAgent 时，必须 100% 格式化传入以下标准提示词：
       ```text
       你是一个精通 HyperFrames 动画引擎与 GSAP 物理特效的专家 SubAgent。
       你的任务是为当前视频单元构建完全符合 BRIEF.md 契约的高质量 1080P 矢量动画网页并导出为 MP4 片段。

       【工作目录与上下文】
       - 工作目录：./<article-slug>/assets/video/unit_<XX>/
       - 核心契约：必须读取并严格遵循本目录下的 `BRIEF.md`（包含精准时长 length、workflow: faceless-explainer、3幕动作轨迹与元素清单）。
       - 矢量 IP 资产：必须读取并引用 `./public/mascot.svg`（包含命名节点 #mascot-head, #mascot-arm-left, #mascot-arm-right, #mascot-leg-left, #mascot-leg-right, #mascot-body, #mascot-prop-slot, #mascot-stamp）。

       【HyperFrames 官方 Skill 规范与工程约束】
       1. 画幅与时长：固定 16:9 横版 1920x1080，HTML 画布与 timeline 严格卡点匹配 `BRIEF.md` 声明的 `length`（如 4.8s）。
       2. 矢量关节动画硬性规则 (GSAP svgOrigin Rule)：
          - 使用 GSAP 对 `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-leg-right`, `#mascot-head` 施加旋转/位移/缩放时，**必须且仅能使用 GSAP `svgOrigin: "X Y"` 锁定 300x400 viewBox 坐标**（如左肩 `svgOrigin: "90 205"`、右肩 `svgOrigin: "210 205"`、左髋 `svgOrigin: "120 300"`、右髋 `svgOrigin: "180 300"`、颈部 `svgOrigin: "150 160"`）。
          - **⚠️ 严禁使用 CSS `transformOrigin: "px px"`**，防止关节脱臼断裂。
       3. 物理隐喻动作绑定 (Action Recipe Execution)：
          - 必须严格执行 `BRIEF.md` 中指定的 Physical Action Recipe 模式（如 `[Action Recipe: PULL_DRAG]` 拖拽发力、`[Action Recipe: PUSH_PRESS]` 蓄力下压、`[Action Recipe: KICK_STEP]` 单腿踢飞、`[Action Recipe: OPERATE_LEVER]` 摇手柄/转阀门、`[Action Recipe: LIFT_DISPLAY]` 托举展示）。
          - **⚠️ 严禁生成仅对 `#mascot-head` 施加微弱旋转的偷懒代码！**
       4. 动效音与字幕隔离规程 (SFX & No-Subtitles Protocol)：
          - **🔊 允许添加动作动效音 (SFX 30% Volume Rule)**：允许在 HTML 中为 IP Mascot 核心动作（如按压、拉拽、踢飞、点击等）添加短促动效音，但**音量必须强制限制为 30% (`volume: 0.3` 或 HTML `<audio volume="0.3">`)** 作为背景音，严禁包含口播配音或盖过主配音。
          - **🚫 严禁读取字幕信息与添加字幕**：绝对禁止读取字幕数据（如 `timestamps.json` / `subtitles.ass`），绝对禁止在 HTML DOM 中创建 `#subtitle-bar` 或添加任何形式的口播字幕。所有字幕由阶段四 FFmpeg 统一在全局压制！

       【产物交付】
       完成渲染后，请仅回复 `[SUCCESS] 视频单元 unit_<XX> 制作完成，导出文件：./<article-slug>/assets/video/unit_<XX>/unit_<XX>.mp4`。
       ```
3. **根据模式执行审核或连续渲染**：
   - **逐单元审核模式**：单单元渲染完成后暂停，等待用户回复 `[通过]` 后启动下一个；
   - **全自动/批次渲染模式**：SubAgent 完成后自动开启下一个单元渲染，全部完成后统一提示进入阶段四合并。

---

### 阶段四：FFmpeg 硬件加速拼接、流规范化与 Sidechain Audio Ducking

1. **遍历单元目录获取 HyperFrames 生成视频**：
   - 所有视频单元制作完成（或审核通过）后，遍历各个 `./<article-slug>/assets/video/unit_XX/` 单元目录，获取 HyperFrames 生成的视频文件。
2. **调度原子技能 `video-renderer` 执行 FFmpeg 硬件加速合并与音频 Ducking**：
   - 运行 `video-renderer`（自动启用 macOS `h264_videotoolbox` 硬件加速编码，重采样规范化音视频流），混入全局配音与背景音乐（ Sidechain Audio Ducking），压制 `\an8\pos(960,960)` 顶基线硬锁定字幕。
3. **落盘 MP4 最终交付与自进化提示**：
   - 导出最终视频 `./<article-slug>/video.mp4`，呈报视频完成信息及本地播放链接（[`./<article-slug>/video.mp4`](./<article-slug>/video.mp4)）。
   - **视觉规程自进化提示**：如对某些单元的视觉呈现进行了人工修正，回复 **`/workflow-learn video_storyboard`** 沉淀动画视觉规程！

