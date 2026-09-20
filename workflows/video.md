---
name: workflow-video
command: /讲解视频
description: 动画讲解视频全流程生成工作流。当用户发送 /讲解视频 指令、或需要将文章/知识主题转化为带有配音、IP Mascot 动作链与视频渲染的 MP4 时唤起。
---

# 🎬 动画讲解视频生成业务工作流 (Explainer Video Business Workflow)

本工作流为 `ai-creator-skills` 项目的动画讲解视频生成管道。负责接收输入（支持模式 1：已生成的长文路径 `./<article-slug>/<article-slug>.md`；或模式 2：独立知识主题），调度底层原子技能（`video-script-writer`、`voiceover-generator`、`video-storyboard-designer`、`video-renderer`、`cover-designer` 以及 HyperFrames 官方 Agent Skills 套件），自动贯穿执行标准的递进步骤。

---

## 核心设计原则 (Core Principles)

> ⚠️ **单一事实源 (Single Source of Truth) 执行约束**：
> 本板块仅对管道的核心架构进行高层定义。Agent 在实际执行工作流时，**必须且只能以下方【详细工作流步骤】中的具体规程、算法逻辑与 100% 固化的 SubAgent Prompt 模板作为唯一执行依据**，绝对禁止根据高层摘要直接提取指令或自由生成 SubAgent 提示词！

1. **双模式自适应输入 (Dual-Mode Input Handling)**：
   - 支持文章转视频 (`article_derived`) 与独立知识主题创作 (`standalone_topic`) 双模式自适应流。
2. **双节点强制人工审核卡点 (Dual Mandatory Human Approval Gates)**：
   - 管道划分为 5 大递进步骤：**Step 1: 生成脚本与封面配置文件** ➔ **Step 2: 生成语音** ➔ **Step 3: 设计单元分镜契约** ➔ **Step 4: 逐单元渲染与逐单元人工审核** ➔ **Step 5: 合成成品视频**。
   - **默认仅生成 9:16 竖屏格式**：为了适配移动端主流媒体平台（小红书/微信视频号/抖音/Shorts），工作流默认仅渲染 9:16 竖屏视频（`1080x1920`）。仅当用户命令行或指令中显式包含生成宽屏版本的指令（如包含 `--widescreen` 选项或明确要求生成宽屏版本）时，才会在 9:16 渲染完成后，逐单元继续渲染生成 16:9 宽屏切片（`1920x1080`）。
   - **卡点 1：剧本方案强制人工确认 (Step 1 Gate)**：在 Step 1 剧本生成阶段，Agent 提炼并完成 SubAgent 盲审后，**必须先在对话框向人类主编输出剧本拆分方案**（包含拆分 unit 数量、拆分逻辑、各 unit 时长、口播台词及动画设计等），中途停顿等待主编给出修改意见。**只有在主编显式确认通过后，才正式落盘 `video_script.json`，随后开启 Step 2**。
   - **卡点 2：首单元独立审核确立风格 + 后续单元无打扰批量渲染 + 全量完成终审 (Step 4 Gate)**：
     1) **首单元样式审核与确认后规程继承**：`unit_01`（第一个单元）单独渲染并提交人类主编审核，用于确定全片视觉风格基调并暴露潜在视觉缺陷。若主编对 `unit_01` 提出修改意见，Agent 针对 `unit_01` 重新进驻修改。**只有当 `unit_01` 最终显式确认通过后，Agent 才集中分析此前针对 `unit_01` 提出的全部修改意见与定稿特征**，总结提炼出适用于后续单元的通用样式规则（如字号、配色、IP 缩放、动画节奏等），传递并应用到后续 `unit_02`..`unit_N` 的渲染环节中。
     2) **后续单元无打扰批量渲染**：`unit_02` 至 `unit_N` 注入继承的通用样式规则，按照 **3 ~ 4 个单元为一组进行 SubAgent 批量自动渲染**，中途**不再进行逐批次人工停顿审核**，高效连续完成渲染。
     3) **全量单元完成人工终审**：全部单元（`unit_01`..`unit_N`）均渲染完成后，主 Agent 统一呈报全量单元视频切片 MP4 超链接路径，中途停顿**进行全片第二次（最终）人工审核与修改确认**。主编确认通过后方可开启 Step 5 合成成品视频。
3. **音画字幕单元内固化与纯视频缝合 (Unit Self-Contained Audio & Subtitles)**：
   - 音频配音、时间戳与美化 HTML 字幕在 Step 3 & Step 4 渲染视频单元时已原生固化压制在单元 MP4 中。Step 5 仅做极速纯视频 `ffmpeg -c copy` 拼接，不重新压制字幕或重算声音。
4. **双轨自进化规则闭环 (`/workflow-learn`)**：
   - 支持主编通过 `/workflow-learn video_script` 与 `/workflow-learn video_storyboard` 沉淀动画与文案规程。
5. **单元间口播自然衔接与完整叙事连贯性 (Unit Narration Continuity & Logical Flow)**：
   - 拆解视频单元时，**严禁将各个单元切碎为孤立的内容摘要。** 口播台词要依据原文叙事逻辑包含自然平滑的过渡与衔接，确保全片音频口播浑然一体、逻辑通顺无割裂感。当然**严禁为了衔接而生硬的增加或改写内容，保证不要没用的废话。**
   - **台词单句语义闭环与严禁谓语/宾语悬空 (Zero Dangling Sentence Mandate)**：每句口播必须保持结构完整（主谓宾/补语齐全），**绝对禁止抛出谓语或动作而丢失核心宾语/事实闭环**（如绝不能出现“比尔·盖茨，最近罕见踩下刹车”后文直接缺失的不完整台词，必须写明“踩下 AI 发展的刹车，呼吁暂停大模型研发”）。精简台词是去无用套话，绝非删减关键事实。
   - **短单元拆分与精细动画保障 (Granular Short-Unit Mandate)**：拆分单元时应保持短小精悍（建议单单元 5 ~ 12 秒）。当涉及到较多 IP 物理动作或构件演变时，**必须拆分为多个短单元**，确保每一个单元都有充裕的空间完成充实、精细的动画设计，避免单元过长导致动画设计泛泛而谈。
6. **内容驱动的高级感动效设计与拒绝文字卡片平移硬禁令 (Content-Driven Premium Animation Design & Anti-Text-Card Mandate)**：
   - 在脚本与剧本设计阶段，动画动效必须深度根据文章内容与知识逻辑进行具象推演（包含具象物理隐喻、画面状态演进、数据/粒子流向脉冲、结构拆合与 IP 物理交互），**绝对禁止将“文字卡片平移/浮动/弹入”作为主画面动效**！文字与卡片仅能作为辅助性注解，绝对禁止缺乏具象场景动效的粗陋设计！
7. **台词多音字上下文拼音按需精准标记规程 (Context-Dependent Polyphone Pinyin Notation Mandate)**：
   - 撰写 `voiceover` 台词时，Agent 必须根据具体上下文语义与词性按需识别多音字，**遵循高频词组免注音避让原则**（如“央行”、“还要”、“刹车”、“为什么”、“银行”、“重要”等现代汉语高频固定词组，TTS 的 NLU 上下文识别率极高，**绝对禁止过度注音拆解**，避免打碎神经网络自然分词与发音韵律）。仅在上下文确实存在发音歧义的单字处标注无歧义的 `{原字|带声调拼音}`（如 `{重|chóng}`、`{还|huán}`；**绝对禁止使用同音汉字替代**，避免替代字也是多音字带来的二次误读；也无需机械枚举，必须根据语境动态识别）。确保下游 TTS 音频合成发音 100% 精准，且字幕剥离拼音后保持 100% 正体汉字展示。
8. **双层路径与 MP4 超链接呈报规程 (Dual-Layer Path & Video Hyperlink Mandate)**：
   - **静态规范层 (项目代码/规范文档)**：在 `.md` 规范文件、工作流定义与代码注释中，**绝对禁止硬编码个人机器的绝对路径**（如 `/Users/morrain/...`）。统一使用以 `./` 开头的相对路径或通用占位符（如 `./<article-slug>/assets/...`），确保 Git 仓库 100% 跨机器、跨平台可移植。
   - **运行时 Chat 呈报层 (IDE 对话框交互)**：Agent 在对话框中呈报切片或成品视频时，**统一呈报带 `file://` 协议头的绝对路径 MP4 超链接** `[unit_01.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/unit_01/unit_01.mp4)`（如 `[unit_01.mp4](file:///Users/morrain/Documents/codes/...)`），人类主编一键点击即可在 IDE 编辑器中实时播放视听。
   - **优势**：既保证了 Git 仓库内部静态文件不包含任何个人绝对路径（100% 可移植），又确保了对话框界面简洁干净、所有视频超链接 100% 可一键点击直接播放！

---

## 详细工作流步骤

### Step 1: 生成脚本 (Generate Script & Review)

1. **输入解析与短路模式识别**：
   - 解析命令行参数 `/讲解视频 [文章路径或主题]`。
   - 若传入已有主题目录或文章路径（如 `./<article-slug>/<article-slug>.md`），进入**模式 1 (文章转视频)**。
   - 若传入纯主题字符串（如 `Vue 3.5 响应式原理`），进入**模式 2 (独立主题创作)**。
   - **低密度视觉排版规程**：在 `BRIEF.md` 中不填写 `style_preset` 字段。视频排版严格遵循低密度呼吸感规程（70%+ 留白空间，一屏仅表达 1 个核心结论，单切片活跃元素 $\le 5$）。
2. **调度原子技能 `video-script-writer` 提炼 4 轨剧本**：
   - 调度 `video-script-writer`（传入模式与输入文本），生成包含 `metadata.visual_theme` 全局视觉主题代币、`time_code`、`voiceover`、`visual_prompt & ip_action` 及 `on_screen_elements` 4 轨结构的 `video_script.json` 草案。在撰写各单元 `voiceover` 时，必须融入原文过渡词句，确保单元间逻辑紧密挂钩；**必须根据上下文语义执行多音字按需精准识别**，遵循高频词组免注音避让原则，仅为存在发音歧义的单字标注 `{原字|带声调拼音}` 格式（**绝对禁止使用同音字替代**，**严禁对高频固定词组过度注音**）；在设计 `visual_prompt` 与 `ip_action` 时，**必须根据内容推演具象场景演进与高级动效，严禁以文字卡片平移/浮动作为主画面动效**。
3. **SubAgent 剧本盲审与前置自检闭环 (Pre-Flight Self-Audit & Blind Review)**：
   - **前置自检门控 (Pre-Flight Self-Check)**：在唤起 `blind-reviewer` SubAgent 之前，主 Agent 必须先进行一次剧本硬性指标自检（对照核验：1. 多音字 `{原字|带声调拼音}` 按需标记与高频词组免注音避让；2. 口播单句语义闭环与严禁谓语/宾语悬空；3. 优先 5-12s 短单元；4. `title_card` 极简克制；5. 尾部 5s 独立 Outro 单元）。自检无误后再唤起 `blind-reviewer`，确保盲审一次性 `[PASS]`，彻底避免打回重试循环。
   - 检查项目根目录是否存在自进化规则 `./learnings/video_script.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/video-script-writer/references/script_reviewer_standards.md` 与 `learnings_file: ./learnings/video_script.md`）；若不存在，启动 `blind-reviewer`（仅传入 `default_standards`）。
   - 校验语速节奏（4-5字/秒）、短句呼吸感、**单元拆分粒度与动画充分性（优先 5-12s 短单元，动作密集处切细；无复杂 IP 动作的叙事过渡段落允许合并为 15-20s 中型单元，控制总单元数）**、IP Mascot 动作定位、**单元间口播承上启下过渡词句与因果推理链完整性（严禁口播割裂或丢失原文逻辑钩子）**、**口播单句语义闭环与严禁悬空半截话/谓语宾语缺失卡点**、**多音字按需带声调拼音标记完整性（严禁同音字替代与高频词组过度注音）校验卡点**、**全局视觉主题 `visual_theme` 代币完整性**、**画面高级感动效设计与拒绝文字卡片平移硬卡点**、**`title_card` 极简克制门控**及**尾部 5s 点赞关注 Outro 单元契约**。若结论为 `[REJECT]`，针对性修正直至 `[PASS]`。
4. **剧本拆分方案输出与人工确认卡点 (Human Approval Gate - 强制停顿确认)**：
   - **⚠️ 暂不落盘文件**：盲审 `[PASS]` 后，Agent **严禁直接写入 `video_script.json`**，必须先在对话中将剧本方案结构化呈报给人类主编审阅。
   - **方案呈报格式要求**：呈报内容必须包含以下 5 大核心要素：
     1) 📌 **单元拆分总数、逻辑递进与承上启下衔接**：明确全片拆分为多少个 `unit_XX`（优先采用 5 ~ 12 秒短单元拆分策略，动作密集处切细，无复杂 IP 动作的叙事段落可合并为 15 ~ 20 秒），各单元对应的文章章节与知识脉络，并**显式标注单元间的承上启下过渡逻辑**；
     2) ⏱️ **单元预估时长**：逐单元标注预计口播时长（`duration_seconds`）；
     3) 🎙️ **逐字口播台词**：逐单元输出包含自然过渡句与完整主谓宾/事实闭环的 `voiceover` 完整解说文案（严禁谓语悬空、宾语缺失的半截话，多音字须按上下文语义按需标注 `{原字|带声调拼音}` 动态发音，高频词组遵循免注音避让原则）；
     4) 🎨 **画面视觉与高级动效/IP 动作设计**：逐单元输出 `visual_prompt` 具象物理场景演进与 `ip_action` 角色物理交互动作（长单元标注多阶段时间切片，必须指明具体的构件形变、流动、变幻等高级动效，严禁描述为“文字卡片平移展示”）；
     5) 🔤 **上屏元素与花字**：标注包含的 `on_screen_elements`（明确 `title_card` 克制规则：若非确实需要，默认设为 null，严禁在常规单元堆叠；唱词高亮词及图形提示）。
   - **⚠️ 尾部 5s 独立单元强制规程**：剧本结尾 **必须单独划分为一个独立的视频单元**（即最后一个 `unit_N`，`duration_seconds: 5s`），专门用于互动引导（如 "深度完整拆解，留言或者私信获取吧。如果对你有启发，记得点赞关注，我们下期见！"），绝对禁止将点赞关注引导口播与正文总结单元合并混写！
   - **交互修改与落盘门控 (Human Feedback Loop & File Save Mandate)**：
     - 向主编发问提示：“*以上为视频剧本拆分与分镜设计草案，请主编审阅并提出修改意见。确认通过后我将为您生成 `video_script.json` 并进入后续语音生成与视频渲染流程。*”
     - 若主编提出修改意见（如调整口播字数、增减视频单元、修改 IP Mascot 动作或画面隐喻），Agent 必须针对性修改剧本方案并重新呈报；
     - **只有当主编回复“确认”、“通过”或“同意”后**，Agent 方可将最终定稿落盘至 `./<article-slug>/assets/video/video_script.json`。

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
4. **⚠️ Step 3 绝对禁令与脚手架初始化 (Strict Prohibition Rules)**：
   - **严禁修改 `index.html` 或编写 HTML/GSAP 代码**：Step 3 仅负责契约与脚手架逐单元初始化（生成 `BRIEF.md`、拷贝 `public/` 资产与 `hyperframes init`）。**绝对禁止主 Agent 或本阶段技能在 Step 3 中修改、创建或编辑任何 `index.html` 文件**，严禁编写任何批量初始化脚本或拼接 HTML 代码的脚本！`index.html` 的编写与编辑必须且只能在 Step 4 由独立的 SubAgent 进驻执行。
5. **跨阶段上下文轻量化隔离规程 (Cross-Stage Context Pruning Mandate)**：
   - 完成全部单元脚手架初始化与 `BRIEF.md` 落盘后，**主 Agent 仅保留 `metadata` 视觉代币、`units` 映射表及当前 Batch 状态**，清理 Step 1 阶段解析原始大段文章的中间历史，以最极简状态切入 Step 4 逐单元批次渲染与人工审核。

---

### Step 4: 逐单元渲染 9:16 竖屏视频片段（及可选 16:9 宽屏片段） (Render 9:16 Portrait & Optional 16:9 Widescreen Per Unit)

1. **⚠️ Step 4 核心调度原则 (SubAgent Batch Dispatch Mandate)**：
   - **🔒 主 Agent 工具排他锁 (Main Agent Tool Lock Mandate)**：在 Step 4 渲染阶段，**主 Agent 自身的唯一许可工具动作是调用 `invoke_subagent`**！**绝对禁止主 Agent 亲自调用 `write_to_file`、`replace_file_content` 或 `multi_replace_file_content` 撰写、创建或编辑 `unit_XX/index.html` 文件**！主 Agent 必须严格扮演“调度指挥官”的角色，把所有 HTML 代码编写、GSAP 动画挂载与 MP4 渲染导出任务，封包移交给 `invoke_subagent` 唤起的 SubAgent 独立进程执行。
   - **首单元独立渲染与确认后意见分析继承 (Unit 01 Review & Post-Approval Inheritance Mandate)**：
     - **第一个单元 `unit_01` 必须单独渲染并率先提交人工审核**（Batch 0：仅包含 `unit_01`），在对话框呈报视频 MP4 超链接路径 `[unit_01.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/unit_01/unit_01.mp4)` 给人类主编。
     - **极速修改迭代**：若主编对 `unit_01` 提出修改意见，Agent 仅对 `unit_01` 进驻修改并重新呈报，直至主编满意。
     - **确认通过后的通用规则提炼**：**只有当 `unit_01` 最终获得主编显式“确认/通过”后，主 Agent 才可以集中分析此前针对 `unit_01` 提出的全部修改意见与定稿特征**。主 Agent 将其中适用于全片的通用规则（如调整全局花字字号、背景高光强度、IP Mascot 默认缩放/位置、动画平滑度或特定主题色）提炼汇总为 `[inherited_style_rules]` 契约，传递并应用到后续所有单元。
   - **后续单元免打扰批量连续渲染 (Uninterrupted Batch Rendering for Unit 02..N)**：
     - 主编确认 `unit_01` 并输出通用风格规则后，对于 `unit_02` 至 `unit_N`，主 Agent 将其划分为每 3 ~ 4 个单元为一个 Batch (如 Batch 1: `unit_02` ~ `unit_05`, Batch 2: `unit_06` ~ `unit_09`)。
     - **后续 Batch 渲染过程中绝对不进行人工停顿审核**！主 Agent 连续自动唤起 SubAgent，每个 Batch 渲染成功后直接自动开启下一 Batch，直至 `unit_N` 全部完成，最大化提升效率并封堵 Token 膨胀。
   - **⚠️ 全量单元完成统一人工终审卡点 (Final Full-Video Human Gate)**：
     - 当全量单元（`unit_01` 至 `unit_N`）渲染导出全部完成后，主 Agent **必须强制停顿**，在对话框结构化呈报全量单元视频切片 MP4 超链接路径 `[unit_XX.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/unit_XX/unit_XX.mp4)`，等待人类主编进行全片第二次（最终）审核。主编确认“确认”、“通过”或“同意”后，方可切入 Step 5 合成成品视频。若主编对特定单元提出修改意见，仅针对该单元重新渲染呈报。
   - **极简 SubAgent 交付协议 (Compact Tool Output Protocol)**：SubAgent 完成渲染后，**严禁将详细的代码、抓帧日志或排查过程返回给主 Agent**，只允许返回最简状态标记与产物路径，彻底封堵主 Agent 侧的对话历史膨胀。
   - **强制 SubAgent 写入权限 (SubAgent TypeName Mandate)**：唤起 SubAgent 时**必须显式设置 `TypeName: "self"`**，确保具备文件写入与代码编辑权限。
   - **严禁编写批量 Shell 脚本**：绝对禁止 Agent 编写替代渲染的 Python 脚本或在主进程中直接批量 Shell 渲染，必须逐批次唤起 SubAgent 执行。

2. **批次渲染与人工审核流程**：
   - **【阶段 1：Batch 0 (`unit_01`) 单独渲染、反复迭代与确认后提炼】**：
     - 唤起 SubAgent 渲染 `unit_01`，完成后在对话框呈报 MP4 超链接路径 `[unit_01.mp4](file://...)`，请求主编审核。
     - 若主编提出修改意见，Agent 针对 `unit_01` 进驻修改并重新呈报，直至主编显式回复“确认”、“通过”或“同意”。
     - **⚠️ 确认通过触发提炼**：在 `unit_01` 确认通过的时刻，主 Agent **集中分析 `unit_01` 审核修改全过程中的最终定稿特征与通用修改项**，汇总提炼生成 `[inherited_style_rules]` 通用规则契约，随后切入阶段 2。
   - **【阶段 2：Batch 1 ~ M (`unit_02` ~ `unit_N`) 连续批量渲染 (免中途打扰)】**：
     - 将 `unit_02` 到 `unit_N` 划分为 Batch 1, Batch 2...（每批 3~4 个单元），顺序唤起 SubAgent：
       - 主 Agent 调用 `invoke_subagent`（**必须设置 `TypeName: "self"`**），传入超紧凑提示词模板（包含 `[inherited_style_rules]` 通用继承规则）：
         ```text
         请处理批次单元目录：./assets/video/unit_XX 至 ./assets/video/unit_YY。
         【继承首单元通用样式规则】: [inherited_style_rules]

         针对批次内的每一个单元：
         1. 进驻单元目录，读取 BRIEF.md 及 HyperFrames 主控技能（.agents/skills/hyperframes/SKILL.md），并遵守 [inherited_style_rules]。
          2. 严格按 BRIEF.md 契约完成 index.html 代码编写。
          3. ⚠️ **静态原点代码审查**：渲染前核验 index.html，确认所有 SVG 旋转/缩放/倾斜动画构件均**强制使用 GSAP svgOrigin: "X Y" 锁死 viewBox 绝对轴心（绝对禁止使用 CSS transformOrigin，避免包围盒偏移导致脱臼甩尾）**，且禁止 CSS 与 GSAP 同时控制同一构件导致闪烁争用。
          4. 运行渲染命令：
             npx hyperframes render "./assets/video/unit_XX" --output="./assets/video/unit_XX/unit_XX.mp4" --resolution portrait
          5. ⚠️ **动态撕裂与脱离自检**：使用 ffmpeg 在 0.5s、mid、end 抽取 3 张自检截图存入 ./assets/video/unit_XX/frames/ 目录，执行视效硬检（核验无小字、无异常遮挡、原点无甩飞、阀门/指针等构件无脱离底座现象，以及 IP 手臂节点无闪烁跳变与撕裂）。
          6. 若需生成 16:9 宽屏版 (仅在用户显式指令时)，先将 9:16 产物与契约备份存盘（unit_XX.mp4 -> unit_XX_9x16.mp4、BRIEF.md -> BRIEF_9x16.md、index.html -> index_9x16.html），再将 BRIEF.md Frontmatter aspect 改为 1920x1080 并重新渲染导出 unit_XX_16x9.mp4。

         【极简交付契约】全部单元完成后，请严格仅回复以下最简格式（严禁包含代码或长日志）：
         `[BATCH SUCCESS] Batch unit_XX..unit_YY 制作完成。产物路径: ./assets/video/unit_XX/unit_XX.mp4 等。自检结论: 均通过。`
         ```
       - SubAgent 返回 `[BATCH SUCCESS]` 后，主 Agent 校验 `unit_XX.mp4` 存在且有效（默认 9:16 视频直接使用 `unit_XX.mp4`，不额外做冗余备份）。**中途不暂停，自动直接切入下一 Batch 渲染**。
   - **【阶段 3：全量单元渲染完成统一人工终审 (Final Full-Video Human Review Gate)】**：
     - 全部单元（`unit_01` 至 `unit_N`）渲染导出完毕后，**主 Agent 强制暂停**，在对话框汇总呈报全量单元视频切片 MP4 超链接路径，等待主编终审。
     - **只有当主编回复“通过”、“确认”或“同意”后**，主 Agent 方可进入 Step 5 缝合全片成品视频。

---

### Step 5: 合成成品视频 (Stitch Final Videos)

1. **前置门控 (Strict Execution Gate)**：
   - **全量单元渲染完成触发**：必须在所有单元（`unit_01` 至 `unit_N`）的 9:16 竖屏切片片段（`unit_XX.mp4`）全部渲染成功且归档完毕后，方可触发 Step 5 缝合！若用户要求生成宽屏版本，则需等待 16:9 切片片段（`unit_XX_16x9.mp4`）也归档完毕。
2. **提取文章标题与极速缝合导出成品视频**：
   - **提取文章标题名**：从 `./<article-slug>/<article-slug>.md` 的 H1 标题或 `video_script.json` 的 `metadata.title` 中提取文章标题名 `<article-title>`（如 `什么是猪周期`）；若无标题则退回到 `<article-slug>`。文件名必须统一使用文章标题名。
   - 调度原子技能 `video-renderer` 运行纯视频拼接脚本，指定输出文章标题名：
     ```bash
     python skills/video-renderer/scripts/render_final_video.py --project-dir ./<article-slug>/assets/video --output-name "<article-title>" --fast-concat
     ```
   - 脚本会自动扫描各个 `unit_XX` 目录下的切片，通过 `ffmpeg -c copy` 极速缝合导出以文章标题命名的成品视频。
3. **交付成品与全平台发布文案生成 (Deliver Video & Generate Publishing Post)**：
   - 校验并在对话框呈报最终在 `./<article-slug>/assets/video/` 目录下导出的成品视频文件路径 Markdown 超链接：
     - 竖屏成品版（默认）：`[<article-title>_9x16.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/<article-title>_9x16.mp4)`
     - 宽屏成品版（仅当显式要求生成宽屏时）：`[<article-title>_16x9.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/<article-title>_16x9.mp4)`
   - **全平台发布文案自动生成规程 (Mandatory Post Copywriting)**：
     - 视频合成成功后，Agent **必须在对话框中同步呈报一份结构化的全平台发布文案**，包含以下 3 大模块（支持主编直接一键复制发布）：
       1) 📌 **多平台差异化标题（严格按各平台字数限制与调性定制）**：
          - **小红书标题**（限制 $\le 20$ 字，带情绪/悬念与 Emoji 视觉点缀）
          - **微信视频号 / 公众号标题**（限制 $\le 16$ 字，偏深度干货/专业解读）
          - **抖音 / 快手标题**（限制 $\le 30$ 字，短平快/爆款痛点/热点引流）
          - **B站 / 横屏标题**（限制 20-30 字，偏硬核原理/科普/求知）
       2) 📝 **精炼内容简介（100 字左右）**：
          - 结合视频核心痛点与结论，撰写一段适合发布在各平台视频简介/正文区的精炼摘要（控制在 90 ~ 110 字），通顺有吸引力。
       3) 🏷️ **核心话题标签（6 ~ 8 个）**：
          - 提取 6 ~ 8 个与视频主题高度相关的热门 Tag，格式为 `#话题名称`（如 `#AI工具` `#硬核科普` 等），方便一键一键复制粘贴发布。
 4. **自进化规则提示**：提示主编可使用 `/workflow-learn video_script` 或 `/workflow-learn video_storyboard` 沉淀自进化规程。
