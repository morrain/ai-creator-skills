---
name: workflow-video
command: /讲解视频
description: 动画讲解视频生成业务工作流。负责提炼 4 轨脚本、结合正文插图推演 IP Mascot 3 幕动态动作链、生成 TTS 配音与字幕时间轴、调度 SubAgent 剧本盲审、3 阶段人工 Gate 确认卡点以及基于 HyperFrames 官方 Skills 与 FFmpeg 的无损视频合成导出。
---

# 🎬 动画讲解视频生成业务工作流 (Explainer Video Business Workflow)

本工作流为 `ai-creator-skills` 项目的动画讲解视频生成管道。负责接收输入（支持模式 1：已生成的长文路径 `./<article-slug>/<article-slug>.md`；或模式 2：独立知识主题），调度底层原子技能（`video-script-writer`、`voiceover-generator`、`video-storyboard-designer`、`video-renderer` 以及 HyperFrames 官方 Agent Skills 套件），并运行 SubAgent 剧本盲审与 3 阶段人工确认卡点闭环。

---

## 核心设计原则 (Core Principles)

1. **双模式自适应输入 (Dual-Mode Input Handling)**：
   - **模式 1 (文章转视频 `article_derived`)**：扫描 `./<article-slug>/` 目录，读取正文 Markdown 与 `./assets/illustration_*.md` 认知隐喻资产，继承并延伸 IP Mascot 的物理隐喻动作。
   - **模式 2 (独立知识主题创作 `standalone_topic`)**：基于输入的知识主题，自动规划从引钩到原理结语的 0 到 1 讲解剧本。
2. **四阶段交互与人工卡点 (Four-Stage Human Gate Protocol)**：
   - **阶段一 (剧本提炼与盲审卡点)**：生成 4 轨 `assets/video/video_script.json` 剧本草案，经 SubAgent 盲审打回修正通过后，全量呈现剧本文本，**显式暂停等待用户回复 `[通过/修改]`**。
   - **阶段二 (视频单元需求构建与试听预览卡点)**：调度 `video-storyboard-designer` 推演各视频单元 3 幕动作链，在 `./<article-slug>/assets/video/unit_XX/` 输出遵循 HyperFrames 官方 [`brief-format.md`](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-core/references/brief-format.md) 规范的 `BRIEF.md` 与矢量 IP `public/mascot.svg`；调度 `voiceover-generator` 生成完整试听音频 `assets/video/audio/voiceover.mp3` 与时间轴 `assets/video/audio_meta.json`，呈现预览信息，**等待用户显式发送“开始渲染视频”指令**。
   - **阶段三 (HyperFrames 官方 Skill SubAgent 独立单元串行制作与人工审核卡点)**：按顺序遍历每个视频单元目录，通过 `invoke_subagent` 派发独立 SubAgent 唤起 `/hyperframes` 主控入口技能，彻底隔离上下文干涉；每个 SubAgent 压制完成单元视频后，**显式暂停呈报单元预览，等待用户回复 `[通过]` 后方才启动下一个视频单元的 SubAgent 制作；若不符合要求，修改 `BRIEF.md` 后回复 `[重新生成 unit_XX]`**。
   - **阶段四 (FFmpeg 跨单元视频无损拼接与 Sidechain Audio Ducking)**：所有单元确认通过后，外层 `video-renderer` 遍历每个视频单元目录获取 HyperFrames 生成的视频片段，调用 FFmpeg 执行秒级无损拼接并应用 Sidechain Audio Ducking，导出最终 1920x1080 30fps 的 `video.mp4` 成果（根目录）。

3. **自进化规则闭环 (`/workflow-learn`)**：
   - 支持主编对剧本口播词、分镜 Prompt 进行人工修改后，回复 `/workflow-learn` 提炼偏好规则沉淀至 `./learnings/video_script.md`，实现盲审规程自进化。

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
     > 1. 剧本满意请回复 **`[通过]`** 或 **`[继续]`**，系统将生成视频单元需求与试听音频。
     > 2. 如对剧本字句进行了人工修饰，请回复 **`/workflow-learn video_script`** 提炼您对视频脚本的偏好规程！

---

### 阶段二：视频单元需求构建、TTS 音频生成与 HyperFrames 契约落盘

1. **读取剧本定稿与插图继承**：
   - 用户确认 `[通过]` 后，读取 `./<article-slug>/assets/video/video_script.json`。
2. **调度原子技能 `voiceover-generator` 生成全局音频与音频时间轴**：
   - 提取 `voiceover` 文案，调用 Edge-TTS (音色 `zh-CN-YunxiNeural`) 导出完整配音音频 `./<article-slug>/assets/video/audio/voiceover.mp3` 与官方标准字幕时间轴 `./<article-slug>/assets/video/audio_meta.json` 及 `SCRIPT.md`。计算各视频单元的精准口播时长 `target_duration`。
3. **调度原子技能 `video-storyboard-designer` 构建视频单元工作区与 HyperFrames BRIEF.md 契约**：
   - 扫描 `./<article-slug>/assets/illustration_*.md`（若存在），提取静态物理隐喻。
   - 将 `video_script.json` 拆解为 $N$ 个独立视频单元（`unit_01`, `unit_02`, ...），在 `./<article-slug>/assets/video/unit_XX/` 下建立独立工作区。
   - 针对每个视频单元，写入符合 HyperFrames 官方标准规范的 `./<article-slug>/assets/video/unit_XX/BRIEF.md`（包含单元核心 Message、单元内分镜设计与 3 幕动态动作链 Visual Prompt、口播时长卡点 `length: X.Xs`），并按 `mascot_svg_contract.md` 节点契约规范在各单元目录下同步落盘矢量 IP 资产 `./<article-slug>/assets/video/unit_XX/public/mascot.svg`。
4. **呈报预览与阶段二 Confirm 卡点提示**：
   - 在对话框呈现各视频单元 3 幕动作链摘要及试听音频生成信息。
   - **暂停并等待显式渲染指令**：
     > 💡 **视频单元预览与渲染确认提示**：
     > 1. 请预览视频单元动作链与音轨试听。确认满意请在对话框显式发送 **“开始渲染视频”**，系统将调度 HyperFrames 官方技能与 FFmpeg 执行单元制作与音频混流！
     > 2. 如需微调单元动作链或 Prompt，可在修改后回复 **`[更新单元]`**。

---

### 阶段三：HyperFrames 官方 Skill SubAgent 独立单元制作与串行人工审核卡点

1. **触发显式渲染指令**：
   - 收到用户回复 **“开始渲染视频”**。
2. **串行遍历并派发 SubAgent 制作各视频单元 MP4 片段**：
   - 顺序遍历 `./<article-slug>/assets/video/unit_XX/` 目录（当前处理单元 `unit_XX`）：
     - 主 Orchestrator 显式调用 `invoke_subagent` 启动独立的 `unit-worker` SubAgent，彻底隔离上下文与 DOM/GSAP 逻辑干扰。
     - SubAgent 在单元工程目录下装载 HyperFrames 官方主控入口 Skill (`/hyperframes`)。
     - `/hyperframes` 读取单元 `BRIEF.md` 与 `public/mascot.svg`，自主根据需求匹配并进入相应的工作流（如 `/faceless-explainer`），独立执行单元内分镜设计、GSAP HTML 编写（`compositions/frames/NN-*.html`）、`npx hyperframes check` 校验，并由 HyperFrames 内部自主压制导出该单元的 1080P 30fps H.264 视频片段。
3. **单元视频人工审核与串行卡点闭环 (Per-Unit Human Review & Sequential Gate)**：
   - SubAgent 运行完成返回后，主 Orchestrator 在对话框呈报该单元 HyperFrames 生成的视频片段预览信息。
   - **显式暂停并等待确认（未确认前禁止启动下一个单元的 SubAgent）**：
     > 💡 **单元视频人工审核提示 (串行阻塞卡点)**：
     > 1. 如单元 `unit_XX` 视频符合要求，请回复 **`[通过]`**，系统将启动下一个单元 (`unit_XX+1`) 的 SubAgent 制作；若为最后一个单元，将进入阶段四合并。
     > 2. 如该单元画面或动作不符合要求，请修改该单元 `./<article-slug>/assets/video/unit_XX/BRIEF.md` 后回复 **`[重新生成 unit_XX]`**，系统将再次派发 SubAgent 重新调起 `/hyperframes` 重新制作该单元！

---

### 阶段四：FFmpeg 跨单元无损合并与 Sidechain Audio Ducking

1. **遍历单元目录获取 HyperFrames 生成视频**：
   - 所有视频单元审核 `[通过]` 后，遍历各个 `./<article-slug>/assets/video/unit_XX/` 单元目录，获取 HyperFrames 在各单元内生成的视频文件。
2. **调度原子技能 `video-renderer` 执行 FFmpeg 无损合并与音频 Ducking**：
   - 运行 FFmpeg 快速无损拼接 (`-c:v copy`) 所有单元视频片段，混入全局配音 `audio/voiceover.mp3` 与背景音乐 `bgm.mp3`（自动开启 Sidechain Audio Ducking 动态闪避）。
3. **落盘 MP4 最终交付**：
   - 导出最终视频 `./<article-slug>/video.mp4` 与中间清单 `./<article-slug>/assets/video/render_manifest.json`。
4. **呈报成果与自进化提示**：
   - 呈报视频完成信息及本地播放链接（[`./<article-slug>/video.mp4`](./<article-slug>/video.mp4)）。

