# Video Script Reviewer Standards (讲解脚本盲审质检标准)

本标准供独立 SubAgent 盲审引擎 (`blind-reviewer`) 对 `video-script-writer` 导出的 `video_script.json` 进行严格质检打回。

---

## 1. 硬性格式合规性 (Hard Schema Gates)

- 必须通过 `references/script_schema.json` 规则验证：
  - `metadata` 包含 `title`, `target_duration_seconds`, `genre`, `mode`。
  - `units` 数组长度 >= 1。
  - 每一个视频单元严格包含 `unit_id`, `duration_seconds`, `voiceover`, `visual_prompt`, `ip_action`, `on_screen_elements` 4 轨完整数据。

---

## 2. 口播文案与节奏感 (Voiceover Pacing & Naturalness)

- 🚫 **严禁书面套话**：口播文案（`voiceover`）必须极具知识博主/科普解说的听感，禁绝“正如上文所述”、“综上所述”、“显而易见的是”等套话。
- ⏱️ **语速与时长匹配**：中文正常口播语速约为 4 ~ 5 字/秒。单个视频单元的 `voiceover` 字数必须与该单元的 `duration_seconds` 相契合（例如 10 秒单元，字数在 35 ~ 45 字之间）。
- ✂️ **短句呼吸感**：单句口播不超过 25 字，适度加入问句或戏剧性停顿。
- 🚫 **悬空半截话与语义断层硬卡点 (Zero Dangling Sentence Gate)**：
  - 口播台词必须具备完整的主谓宾/补语结构与事实闭环。
  - **红线打回判定**：若扫描到台词中存在谓语悬空、关键宾语/补语缺失、话讲一半或逻辑断层的句子（例如“比尔·盖茨最近罕见踩下刹车”未说明具体踩下什么刹车/后续动作；或“某大厂宣布重大调整”未说明调整内容直接切走），盲审引擎必须直接判定为 `[REJECT]` 打回重写，要求补全关键宾语与逻辑闭环！

---

## 3. IP 角色动作定位 (IP Character Action Fidelity)

- 🤖 **IP Mascot 不是背景贴纸**：`ip_action` 中的 IP Mascot 角色必须是**画面核心动作的执行者**（如拉线缆、推闸门、盖章、分拣数据块）。
- 🏷️ **统一使用泛称名称**：在 `visual_prompt` 与 `ip_action` 描述中，统一使用泛称 **`IP Mascot 角色`**（严禁硬编码具体形象名称如“小智”），保证剧本能够零成本解耦复用到任意自定义 IP 规范中。
- 🚫 **严禁卖萌或装饰**：IP Mascot 必须保持冷静认真与冷幽默（Deadpan），严禁描述为“微笑摇摆”、“可爱眨眼”。
- 🔗 **动作延续性**：在 `mode: article_derived` 模式下，视频单元动作必须与原正文插图中的隐喻道具和动作保持连贯逻辑。
- ⏱️ **短单元拆分与动画充分性硬卡点 (Granular Short-Unit & Full Animation Gate)**：
  - 提炼剧本时优先倡导 **5 ~ 12 秒短单元** 拆分策略。特别在动作密集、构件演变或状态转换多的段落，**必须拆解为多个短单元**，确保每个单元的动画设计与 IP Mascot 动作都能得到充分、精细表达。
  - 若单元时长 >15s 且内部动作繁复、但在 `visual_prompt` 与 `ip_action` 中描述模糊粗糙，盲审引擎必须判定为 `[REJECT]` 打回，要求拆分为更短的单元或补全多阶段详细动作切片！

---

## 4. 屏幕花字与视觉排版 (On-Screen Elements Quality)

- 📌 **`title_card` 极简克制规则**：若非确实需要（如仅在 Unit 01 Hook 开篇或重大章节转折），**默认一律设为 `null`**。绝对禁止在常规单元机械堆叠 `title_card` 标题花字，若滥用 `title_card` 质检直接打回！
- 🖍️ `highlight_keywords` 数组提取 1~3 个核心关键词，用于唱词高亮。
- 📊 `graphics_hint` 提供具体的视觉动画指导（如“柱状图对比”、“粒子流向动画”）。

---

## 5. 尾部 5s 独立点赞关注 Outro 单元硬卡点 (Standalone Outro CTA Gate)

- ❤️ **必须独立为单独一个单元**：`units` 数组末尾 **必须单独划分为一个独立的 Outro 视频单元**（即全片最后一个 `unit_N`，`duration_seconds: 5s`），绝对禁止将其与前文总结或金句合并写在同一个单元内！
- 🗣️ **口播与动作契约**：`voiceover` 须包含点赞关注引导词，`ip_action` 必须显式指示 `IP Mascot 角色` 绑定 `[Action Recipe: LIKE_AND_SUBSCRIBE]` 进行弹跳与举起三连徽章的引导动作。未包含尾部 5s 独立 Outro 单元者质检直接打回！

---

## 6. 画面高级感动效设计与拒绝文字卡片平移硬卡点 (Premium Animation & Anti-Text-Card Gate)

- 🚫 **严禁以文字卡片平移/浮动作为主画面动效**：`visual_prompt` 或 `graphics_hint` 中，**绝对禁止将“文字卡片平移/浮动/弹入/列表展示”作为主画面动效**（如“出现红色警示卡片”、“三条文字卡片依次滑入”）。如果画面缺乏具象场景构件，仅靠文字卡片在屏上平移或浮动，盲审引擎必须直接判定为粗陋低质 `[REJECT]` 并打回重写！
- 🎨 **必须具备内容驱动的 2D 具象场景演进动效**：每个单元的 `visual_prompt` 必须明确描述具体的 SVG 物理实体构件（如管道、齿轮、闸机、链表插头、仪表盘），并清晰注明构件在单元内的**动态形变、流动、分裂重组或物理交互过程**。对于大于 20s 的长单元，必须在多阶段演进中包含具体的场景形态转换（Metamorphosis）动效。

---

## 7. 多音字动态拼音标记质检硬卡点 (Polyphone Pinyin Review Gate)

- 🔤 **上下文多音字拼音标记校验**：盲审引擎必须审查 `voiceover` 口播台词中的多音字。凡是存在多音可能且易产生歧义的汉字，必须校验是否按上下文语义标注了 `{原字|带声调拼音}`。
- 🚫 **红线打回判定**：
  1) **严禁同音字替代**：若多音字使用了同音汉字替代（如 `{重|虫}`），直接判定为 `[REJECT]` 打回！（原因：替换的同音字本身也可能是多音字，存在二次误读风险，必须统一使用带声调拼音）；
  2) **严禁遗漏多音字**：若根据上下文推论存在易误读多音字但未标注拼音，直接判定为 `[REJECT]` 打回，要求补全 `{原字|带声调拼音}` 动态标记！
