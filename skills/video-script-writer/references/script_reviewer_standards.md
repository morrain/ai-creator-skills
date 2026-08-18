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

---

## 3. IP 角色动作定位 (IP Character Action Fidelity)

- 🤖 **IP Mascot 不是背景贴纸**：`ip_action` 中的 IP Mascot 角色必须是**画面核心动作的执行者**（如拉线缆、推闸门、盖章、分拣数据块）。
- 🏷️ **统一使用泛称名称**：在 `visual_prompt` 与 `ip_action` 描述中，统一使用泛称 **`IP Mascot 角色`**（严禁硬编码具体形象名称如“小智”），保证剧本能够零成本解耦复用到任意自定义 IP 规范中。
- 🚫 **严禁卖萌或装饰**：IP Mascot 必须保持冷静认真与冷幽默（Deadpan），严禁描述为“微笑摇摆”、“可爱眨眼”。
- 🔗 **动作延续性**：在 `mode: article_derived` 模式下，视频单元动作必须与原正文插图中的隐喻道具和动作保持连贯逻辑。
- ⏱️ **长单元（>20s）多阶段动作描述硬卡点**：对 `duration_seconds > 20s` 的单元，`visual_prompt` 与 `ip_action` 严禁使用单句模糊概括。必须结合 `voiceover` 口播逐字逻辑，划分为多阶段演进（如 `[0-10s] ➔ [10-20s] ➔ [20-30s]`）详细描绘画面变迁与 IP Mascot 连续动作，否则质检必须打回打重写！

---

## 4. 屏幕花字与视觉排版 (On-Screen Elements Quality)

- 📌 `title_card` 须精炼点明当前视频单元主题（不超过 10 字）。
- 🖍️ `highlight_keywords` 数组提取 1~3 个核心关键词，用于唱词高亮。
- 📊 `graphics_hint` 提供具体的视觉动画指导（如“柱状图对比”、“粒子流向动画”）。

---

## 5. 尾部 5s 独立点赞关注 Outro 单元硬卡点 (Standalone Outro CTA Gate)

- ❤️ **必须独立为单独一个单元**：`units` 数组末尾 **必须单独划分为一个独立的 Outro 视频单元**（即全片最后一个 `unit_N`，`duration_seconds: 5s`），绝对禁止将其与前文总结或金句合并写在同一个单元内！
- 🗣️ **口播与动作契约**：`voiceover` 须包含点赞关注引导词，`ip_action` 必须显式指示 `IP Mascot 角色` 绑定 `[Action Recipe: LIKE_AND_SUBSCRIBE]` 进行弹跳与举起三连徽章的引导动作。未包含尾部 5s 独立 Outro 单元者质检直接打回！
