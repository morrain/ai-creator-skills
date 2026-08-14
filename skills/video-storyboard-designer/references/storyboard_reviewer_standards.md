# Storyboard & Unit Designer Reviewer Standards (视频单元与分镜动作链盲审标准)

本标准供 SubAgent 对 `video-storyboard-designer` 生成的视频单元配置文件（`unit_XX/BRIEF.md`）进行自动化质检。

---

## 1. 动态动作链连贯性 (Motion Chain Continuity)

- 必须包含完整的 3 幕动作演化描述（`Act 1: 引出问题` -> `Act 2: 核心动作` -> `Act 3: 交付结果`）。
- Act 2 的核心动作必须优先继承并延伸原正文插图文件（`illustration_*.md`）中确立的物理隐喻。
- IP Mascot 必须是动作的执行者，严禁沦为背景贴纸或无意义装饰。
- **二次分镜与元素清单硬卡点**: `BRIEF.md` 的 `## Intent` 正文必须明确包含全量画面元素清单（Scene Element Inventory）与带时间戳的镜头切片划分（Sub-shot Timeline Breakdown），特别是对 >20s 的长单元，严禁缺少基于口播文案的二次分镜切片！

---

## 2. 视觉 DNA 与生图 Prompt 规范 (Visual DNA & Prompt Gates)

- **构图与背景**: 强制 16:9 横版构图，纯白背景 (`#FFFFFF`)，黑色手绘线条质感 (Black minimalist hand-drawn line art)。
- **原生中文批注**: 英文 Prompt 中的文本批注须强制保留在引号内部的原生中文（如 `'数据流'`、`'56% OFF'`）。
- **图片与视频参数**: 英文 Prompt 末尾须附加 `--ar 16:9 --v 6.0` 或 i2v 生成控制参数。

---

## 3. 极简流派与低密度限制规程 (Minimalist & Low-Density Gates)

- **Style Preset 选型与全片一致性**: `BRIEF.md` 的 YAML Frontmatter 中必须包含从 [`references/style_presets.md`](style_presets.md) 自适应选定的有效 `style_preset`（如 `blue-professional`, `code-editorial`, `minimal`, `broadside`, `clean-editorial`, `swiss-graphic` 等），且全片所有视频单元（`unit_01` ~ `unit_N`）的 `style_preset` 必须绝对统一，严禁同一视频的不同单元风格游离！
- **One Statement Per Frame**: `## Customizations` 与 `## Notes` 中必须明确要求单屏仅表达 1 个核心结论，禁止堆砌多张卡片。
- **Cap Elements $\le 3$**: 单场景独立 UI 元素/卡片总量严格约束在 3 个以内。
- **Suppress Chrome**: 显式禁用背景网格点、装饰性线条、光晕/粒子等“视觉噪声”。

---

## 4. 首帧曝光与封面防白硬卡点 (First Frame Exposure Gate)

- 📸 **第 0 帧非空白**: `BRIEF.md` 的 `## Notes` 正文中必须显式写入 `First Frame Exposure & Anti-Blank Cover` 规程。
- 🎬 **`gsap.set` 初始态强制渲染**: 要求动画在 `t=0.0s` 时刻必须通过 `gsap.set` 保持主标题文字、背景卡片容器及 IP Mascot 姿势 `opacity: 1` 可见，禁止全白淡入导致小红书/视频号自动抽取封面一片空白！

---

## 5. 尾部 3s 点赞关注引导硬卡点 (Outro CTA Gate)

- ❤️ **尾部单元 CTA 契约**: 最终单元的 `BRIEF.md` 必须明确包含 3s 点赞关注引导分镜，显式绑定 `[Action Recipe: LIKE_AND_SUBSCRIBE]`。
- 🌟 **IP Mascot 互动表现**: 要求 IP Mascot 做欢快跳跃与举手向观众展示 `👍 点赞`、`⭐ 收藏`、`🔔 关注` 三连徽章。未包含尾部 Outro 单元契约者质检打回！
