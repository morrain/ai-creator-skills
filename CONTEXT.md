# AI Creator Studio & Skills Suite

面向高级创作者与总编辑的 AI 全流程内容工程化套件，包含文章写作、认知隐喻插图设计、微信公众号离线 HTML 排版、海报设计与动画讲解视频生成。

## Language

**讲解脚本 (Explainer Script)**:
包含逐字口播文案（Voiceover）、画面视觉描述、时间轴划分及 IP 动作指示的结构化视频剧本。
_Avoid_: 视频文案, 剪辑脚本, 稿件

**音画时间轴 (Audio-Visual Timeline)**:
以 TTS 语音音频和字幕时间戳（SRT/JSON）为基准的时间对齐骨架，决定视频的总时长与画面切换切点。
_Avoid_: 时间线, 进度表

**视频单元关键帧 (Unit Keyframe)**:
根据脚本画面描述与 `character_ip.md` 规范在视频单元内部生成的视觉图片或动画片段，包含 IP 角色的具体动作场景。
_Avoid_: 视频画面, 插图, 配图

**合成渲染引擎 (Video Composite Engine)**:
基于代码（如 FFmpeg）将 TTS 配音、字幕花字、各视频单元素材无缝拼接渲染为标准 MP4 视频的渲染器。
_Avoid_: 视频剪辑软件, 导出器

**IP 动作延续性 (IP Motion Continuity)**:
在从已有长文+插图转化为视频讲解时，继承原正文插图中 IP Mascot（IP 角色，支持自定义路由加载）已经建立的物理隐喻和动作设定，使视频单元中的动作成为文章插图动作的自然延伸。
_Avoid_: 角色重置, 动态重复

**动态动作链 (Motion Chain)**:
将正文插图中的静态 IP 动作解耦并扩展为“引出问题 -> 动作核心 -> 交付结果”的三幕式动态链，作为视频单元内部分镜动作生成的基础。
_Avoid_: 逐帧动画, 随机动作

**4轨脚本规范 (Four-Track Script Schema)**:
将讲解脚本解耦为时间轴 (Time Code & Unit ID)、口播文案 (Voiceover)、画面与 IP 动作描述 (Visual & IP Action)、屏幕花字与视觉组件 (On-Screen Elements) 四个独立轨道的结构化协议。
_Avoid_: 纯文本剧本, 自由格式文本

**单视频单元独立渲染与双比例导出 (Per-Unit Independent Rendering & Dual-Aspect Export)**:
将长视频拆分为按知识结构划分的视频单元（`unit_XX`），由 HyperFrames 按单元依次独立渲染导出 `16:9` (`unit_XX_16x9.mp4`) 与 `9:16` (`unit_XX_9x16.mp4`) 片段。视频单元内部的分镜设计与 3 幕动作链落盘于该单元的 `BRIEF.md` 中，并在比例切换时归档源码快照（`BRIEF_16x9.md` / `BRIEF_9x16.md`）。
_Avoid_: 全量合成, 长视频一次性渲染, 单比例覆盖, 硬编码固定短分镜

**动态 GSAP 动作脚本 (Dynamic GSAP Motion Code)**:
根据视频单元 `BRIEF.md` 中的物理隐喻和 3 幕动作链，由 AI 智能生成具体的 GSAP 动画代码注入单元 HTML，而非依赖静态硬编码的动作宏。
_Avoid_: 静态动作宏, 硬编码动画

**音画强制强对齐 (Strict TTS-Timeline Syncing)**:
以 `voiceover-generator` 导出的实际语音时间轴 `audio_meta.json` 作为 HyperFrames 单视频单元渲染的绝对帧率与时长基准。
_Avoid_: 预估时长渲染, 变频合成

**BRIEF 契约 (BRIEF Contract)**:
遵照 HyperFrames 官方规范导出的 `BRIEF.md` 文件，包含全局 YAML Frontmatter（单元时长 `length`、核心 Message 等）以及单元内分镜设计（Visual Census 与带时间轴的 3 幕动作演化），作为阶段三 HyperFrames 官方技能消费的标准契约。
_Avoid_: 自由分镜文本, 非标 Markdown

**audio_meta 契约 (audio_meta Contract)**:
遵照 HyperFrames 官方规范导出的 `audio_meta.json` 文件，包含全量 TTS 配音路径、视频单元绝对时长以及逐句/逐字字幕时间戳，用于 HyperFrames 画布在动画演化中的精确寻帧对齐。
_Avoid_: 纯文本字幕, 忽略时间轴

**合成渲染引擎 (Video Composite Engine)**:
基于代码（如 FFmpeg `render_final_video.py --output-name "<article-title>" --fast-concat`）将已包含声音与字幕花字的各视频单元 MP4 片段执行纯视频 stream copy 缝合，导出成品 MP4 视频。因为字幕与音频已在单元视频渲染中固化，合成阶段不重新压制任何字幕与音轨（仅在有 `bgm.mp3` 时追加背景音乐混音）。
_Avoid_: 视频剪辑软件, 导出器, 自动二次压字幕, 重算语音时间轴

**全自动连续调度 (Full-Automation Orchestration Protocol)**:
在无 `--interactive` 或显式人工审核指令时，Agent 自动贯穿执行“1.生成脚本 -> 2.生成语音 -> 3.生成单元分镜 -> 4.渲染各单元16:9与9:16视频 -> 5.纯视频拼接”的全部 5 个步骤，无需中途暂停等待用户人工 Confirm。
_Avoid_: 机械卡点打断, 交互式卡死



