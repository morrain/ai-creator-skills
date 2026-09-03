---
name: video-script-writer
description: 4 轨动画讲解视频剧本提炼技能。当需要将文章正文或知识主题拆解提炼为包含口播、画面与 IP 动作的 video_script.json 剧本时调用。
---

# Video Script Writer Skill (4 轨讲解剧本提炼技能)

本技能为 **纯粹无状态的原子剧本提炼技能**。指导 AI Agent 根据输入的长文章 Markdown（模式 1）或知识主题（模式 2），解耦并输出严格符合 4 轨规范的结构化 `video_script.json` 讲解剧本。

---

## 核心设计原则 (Core Principles)

1. **单点输入与无状态提炼 (Stateless Script Output)**：
   - 技能接收文章 Markdown 文本或知识主题名称，以及模式参数（`mode: article_derived` 或 `mode: standalone_topic`）。
   - 纯粹处理文本逻辑并返回标准的 4 轨 JSON 剧本，零主题工作区存盘与文件流转依赖。
2. **4 轨解耦结构 (Four-Track Script Schema)**：
   - 每个视频单元解耦为 4 个独立轨道：
     - `time_code` & `duration_seconds`: 单元编号与精准预估时长（单位：秒）。
     - `voiceover`: 极具知识博主/科普解说听感的逐字口播文案。
     - `visual_prompt & ip_action`: 画面背景描述与 IP Mascot（IP 角色）的具体物理动作指示。对于 **`duration_seconds > 20s`** 的较长单元，必须结合 `voiceover` 口播逐字逻辑进行详细的多阶段描绘（划分 `[0-10s] ➔ [10-20s] ➔ [20-30s]` 等连续演进切片），严禁写成单句概括！
     - `on_screen_elements` (极简克制原则与去字化铁律): 画面信息必须保持极低密度。画面标题花字 `title_card`（**默认必须设为 `null`！只有在全片开篇 Unit 01 或极其重大的知识点转折处才允许使用简短的 2~4 个字标题，绝对禁止在每个单元机械堆叠长标题**）、唱词高亮词 `highlight_keywords`（**非核心专有名词绝对禁止高亮，严禁满屏标注**）及视觉组件提示 `graphics_hint`（严禁写出文字列表或多重卡片）。所有核心信息由口播与画面 SVG 构件传递，绝不能依赖屏幕文字！
3. **双模式支持 (Dual-Mode Support)**：
   - **模式 1 (文章衍生 `article_derived`)**：分析长文的正文脉络与金句，保留文章插图中已确立的物理隐喻方向，将其重构为流畅的视频单元。
   - **模式 2 (独立主题 `standalone_topic`)**：直接根据输入的知识主题，自动规划引钩 (Hook)、原理解析与总结，生成 0 到 1 的讲解脚本。
4. **口播听感与短句呼吸感 (Natural Voiceover Pacing)**：
   - 必须使用口语化、接地气的听觉语言，杜绝“综上所述”、“显而易见”等书面套话。
   - 语速控制在 **4 ~ 5 字/秒**（例如 10 秒单元，口播在 35 ~ 45 字之间），单句控制在 25 字以内，具备自然呼吸停顿。
5. **单元间口播承上启下与叙事逻辑连贯性 (Inter-Unit Narration Continuity & Smooth Transitions)**：
   - **保留原文逻辑链与转折关联**：在拆解长文（`mode: article_derived`）或知识主题（`mode: standalone_topic`）为多单元时，绝对禁止将各单元切碎为孤立的摘要块。必须完整保留原文中的因果推演、逻辑钩子与转折关联（如“问题 ➔ 根因 ➔ 破局解法 ➔ 效果演进”）。
   - **严禁割裂与关键信息丢失 (Zero Logical Gap Rule)**：严禁在单元分割处删减原文关键的逻辑过渡词、因果推理和上下文锚点，避免导致上下单元口播脱节、逻辑断裂。
   - **口播台词语义完整性与单句闭环铁律 (Voiceover Semantic Completeness Mandate)**：
     - **🚫 严禁悬空半截话与未闭环主谓宾 (Zero Dangling Sentences & Incomplete Predicates)**：每句口播台词必须具备完整自洽的语义结构（主/谓/宾/补完整）。当台词中抛出动向或谓语（如“踩下刹车”、“做出调整”、“引发震荡”）时，**必须完整补充其核心宾语、限定词与事实解释**（例如“比尔·盖茨最近罕见踩下 AI 发展的刹车，呼吁暂停 GPT-5 级的超大模型训练”）。绝对禁止只保留动词而遗漏核心宾语/补语，导致话讲一半、信息丢失悬空（如绝不能写成“比尔·盖茨，最近罕见踩下刹车”然后直接切走）。
     - **精简台词不等于误删事实主干 (Preserve Essential Facts)**：精简口播文案的目的是“祛除冗余套话与无用修饰”，**绝非删减关键事实对象与逻辑闭环**。单元内抛出的任何重要论断或动作，必须在当前句或同单元内实现事实闭环。
6. **IP 角色动作核心化 (IP Action Centricity)**：
   - 剧本提炼阶段无须加载具体的 IP 形象规范。在 `ip_action` 与 `visual_prompt` 字段中，统一使用泛称 **`IP Mascot 角色`**，确保剧本绝对无状态与解耦。角色不是背景贴纸或卖萌吉祥物，而是正在拉扯线缆、推推闸门、盖章或操作机器的核心系统操作员。
7. **短单元拆分与精细动画保障 (Granular Short-Unit Splitting & Rich Animation Progression)**：
   - **优先拆分为 short, focused 单元（建议 5 ~ 12s）**：拆分视频单元时，应当尽量保持单元短小精悍。把复杂的知识脉络拆解为小步快跑的短单元，为下游分镜与动画组帧留出充裕的设计表达空间。
   - **动作密集处强制细分**：当涉及较多 IP Mascot 物理动作、画面形态转换（Metamorphosis）或构件演变时，**严禁将大量连续动作打包塞入一个的长单元（如 >15-20s）中**。长单元极其容易导致下游动画设计描述泛泛而谈、动效充实度不足。
   - **长单元（若确实存留在 15-20s）多阶段硬性描绘**：对极少数无法进一步切割的长单元，`visual_prompt` 与 `ip_action` 必须紧密结合 `voiceover` 划分为多阶段演进（如 `[0-5s] ➔ [5-10s] ➔ [10-15s]`），交代每一阶段的具体构件变迁与 IP Mascot 动作。
8. **尾部 5s 独立点赞关注引导单元 (Standalone Outro CTA Unit)**：
   - **必须作为单独一个独立单元**：剧本结尾 **必须单独划分出一个独立的 Outro 视频单元**（即全片最后一个 `unit_N`，`duration_seconds: 5s`），绝对禁止将其与前文总结或金句合并写在同一个单元内！
   - `voiceover`: 温暖简洁的互动引导语（如 "深度完整拆解，留言或者私信获取吧。如果对你有启发，记得点赞关注，我们下期见！"）。
   - `ip_action` 与 `visual_prompt`: 指示 `IP Mascot 角色` 动作，指定下游绑定 `[Action Recipe: LIKE_AND_SUBSCRIBE]`，做活泼弹跳与手持/举起点赞、关注、收藏三连花字徽章动作。
9. **内容驱动全局视觉主题与设计代币计算 (Content-Driven Visual Theme Allocation)**：
   - **必须在 metadata 中定义全局视觉主题 (`visual_theme`)**：在提炼剧本时，必须主动读取 [`references/theme_presets.json`](references/theme_presets.json)，**绝对禁止机械套用固定预设模板**。Agent 必须根据视频实际题材、情感基调与受众特征，**动态计算并设计一套具象的代币色值**（`canvas_bg`, `card_bg`, `primary_accent`, `secondary_accent`, `text_primary`, `subtitle_box_bg`, `subtitle_text_color` 等），作为贯穿下游所有分镜与网页渲染的单一事实源。
   - **⚠️ 字幕彻底消除背景框硬性约束**：全片所有调色主题中，`subtitle_box_bg` **必须强制设为 `"transparent"`**，`subtitle_box_border` 设为 `"none"`。**绝对禁止为唱词字幕添加任何深色/浅色背景矩形框或卡片**！浅色画布字幕文字设为深色 `#0f172a`，深色画布字幕文字设为亮色 `#ffffff`，确保通透无遮挡。
10. **内容驱动的高级感动效设计原则 (Content-Driven Premium Animation Design)**：
    - 剧本与脚本设计阶段是全片动画动效的源头！在设计各单元的 `visual_prompt` 与 `ip_action` 时，必须深度结合正文知识逻辑，从 5 个维度设计高级 2D 场景动效：
      1) **具象物理隐喻 (Concrete Metaphors)**：将抽象逻辑转化为带具名构件的机械/物理结构（如阀门、管道、电路引脚、齿轮、导轨、分流闸机）；
      2) **画面状态演进与形态转换 (Scene Evolution & Metamorphosis)**：场景构件随口播动态拆分、组合、蜕变、缩放（如拥挤办事大厅重组为智能闸机，单管道扩展为双向链表）；
      3) **动态数据与物理流向 (Dynamic Flow & Micro-Physics)**：光束导轨脉冲、水流充盈、仪表盘指针弹跳、能量扩散、刻度变化等动态流向；
      4) **微观物理交互 (Micro-Physics Interactions)**：IP Mascot 与实体构件产生拉手柄、踩槽位、盖印章、插拨塞子等物理机械力学响应；
      5) **层次感与空间位移动画 (Layer Depth & Spatial Kinetics)**：空间焦点转移、构件层次推拉与平滑过渡。
11. **拒绝文字卡片平移主导的反例硬禁令 (Anti-Text-Card Animation Mandate)**：
    - **🚫 绝对禁止在 `visual_prompt` 或 `graphics_hint` 中将“文字卡片平移/浮动/弹入”作为主画面动效**（例如“红色警示卡片从左滑入”、“三个文字框依次浮现”）。
    - 文字卡片与花字仅能充当辅助性文字注解，**画面视觉的核心焦点必须是具象 SVG 场景实体、场景状态变换与 IP Mascot 的物理动作链**！无具象物理场景演化的纯文字卡片浮动被判定为粗陋低质。
12. **上下文多音字拼音动态标记规范 (Dynamic Polyphone Pinyin Notation `{原字|带声调拼音}`)**：
    - **🚫 绝对禁止使用同音汉字替代**：撰写 `voiceover` 口播文案时，绝对禁止使用同音汉字替代多音字（避免替代字本身也是多音字而带来二次误读风险！）。必须且只能统一使用**标准带声调拼音**（如 `{重|chóng}`、`{还|huán}`、`{行|háng}`）。
    - **根据上下文语义动态识别（严禁机械穷举）**：Agent **必须根据段落的具体上下文含义与词性**，动态扫描并自动为台词中所有易误读的多音字添加拼音标记。不要依赖固定死板的列举清单，必须全面基于具体的解说语境做出准确判断。
    - **语法格式**：`"{屏幕显示原字|标准带声调拼音}"`（例如：`"报错可以零成本清空{重|chóng}跑"`、`"这在{行|háng}业内部"`、`"标注好单位和{量|liáng}程"`）。
    - **自动解耦机制**：下游 `voiceover-generator` 配音模块会自动将前半部分（原字）提取用于 `.srt`、`.ass` 及 `timestamps.json` 字幕渲染（保持 100% 正体汉字展示），将后半部分拼音提取给 TTS 引擎合成语音（100% 确保拼音发音精准且无额外误读风险）。




---

## 关联参考规范

在执行剧本提炼时，主动读取以下参考规范：
- [`references/theme_presets.json`](references/theme_presets.json)：内容驱动调色系统与字幕自适应规则指南。
- [`references/script_schema.json`](references/script_schema.json)：4 轨 JSON Schema 协议定义。
- [`references/script_examples.md`](references/script_examples.md)：标准 4 轨剧本 JSON 示范文件。
- [`references/script_reviewer_standards.md`](references/script_reviewer_standards.md)：脚本盲审与质检标准。

---

## 规范输出格式

调用本技能将直接输出符合 JSON Schema 的 `video_script.json` 内容：

```json
{
  "metadata": {
    "title": "视频大标题",
    "target_duration_seconds": 60,
    "genre": "科普解说",
    "mode": "article_derived",
    "source_article_path": "./path/to/article.md",
    "visual_theme": {
      "preset": "content_driven_custom",
      "style_description": "根据内容动态设计的清爽高对比浅色视觉主题",
      "tokens": {
        "canvas_bg": "linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)",
        "card_bg": "rgba(255, 255, 255, 0.94)",
        "card_border": "2px solid #cbd5e1",
        "primary_accent": "#2563eb",
        "secondary_accent": "#0284c7",
        "warning_accent": "#ef4444",
        "success_accent": "#10b981",
        "text_primary": "#0f172a",
        "subtitle_box_bg": "transparent",
        "subtitle_box_border": "none",
        "subtitle_text_color": "#0f172a"
      }
    }
  },
  "units": [
    {
      "unit_id": "Unit 01",
      "duration_seconds": 8,
      "voiceover": "逐字口播文案...",
      "visual_prompt": "16:9 干净留白背景，低密度视觉构图...",
      "ip_action": "IP Mascot 角色手持数据线缆...",
      "on_screen_elements": {
        "title_card": "单元标题",
        "highlight_keywords": ["关键词1", "关键词2"],
        "graphics_hint": "HyperFrames 视觉组件提示"
      }
    }
  ]
}
```
