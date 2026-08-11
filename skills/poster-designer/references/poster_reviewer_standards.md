# 手绘海报审查 SubAgent 裁决与审查标准手册 (Poster Reviewer Standards)

本文档为海报审查 SubAgent 在对单张海报方案进行盲审时的唯一诊断与裁决依据。

---

## 核心审查维度

### 1. 显式文案完整性与防杜撰/去乱码指令 (Explicit Text & Anti-Gibberish Audit) —— 核心硬指标
- **防杜撰/去乱码约束**：生图 Prompt 中必须**显式写入纯净文本控制指令**（`strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes`）。
- ❌ **原生中文文案保留**：检查 🟢 英文生图版 Prompt 中，单引号 `'...'` 括起来要求渲染在海报上的核心标题/文案是否保持了原生中文。

### 2. 版式契合度与视觉组件多样性 (Layout & Visual Component Audit)
- **版式匹配**：从 10 大经典版式库中选择的版式是否与该卡片知识结构高度契合？
- **组件弹性组合**：根据海报版式选择最契合的 2-4 个精细手绘视觉组件（如卡片框、莫兰迪胶囊标题、悬挂吊牌、气泡总结框、放大镜等），确保层次清晰且保持舒服的留白。

### 3. IP Mascot 姿态与正文插图隐喻继承 (IP Mascot & Metaphor Inheritance)
- **动作具象化与跨媒介继承**：IP Mascot（默认小智）姿态必须具备场景感，且**必须优先继承并延伸该章节在正文插图配置中的隐喻印记与 IP 动作**。

### 4. Prompt 饱满度与美学参数 (Morandi Style & Rich Prompt Audit)
- **生图 Prompt 规范**：必须具备丰富具体的画面构图、背景纹理（暖米白羊膏纸 `#FAF6F0`）、配色方案（莫兰迪粉彩）、手绘黑色勾线与 3:4 宽高比例。

### 5. 社媒配文与话题标签审查 (`poster_post.md` Audit)
- **标题矩阵字数与位置约束 (每个标题 ≤ 20 字，一票否决)**：检查标题备选矩阵是否单独列在最顶部，第一备选标题必须为母版正文大标题 H1，且**顶部每个拟定的备选标题字数必须严格控制在 20 个字以内**（含标点符号）。若拟定标题超过 20 字，直接裁决为 `[REJECT]`。
- **高密度 Emoji 与 100 字短句结构 (一票否决)**：正文必须精炼极简控制在 **100 字以内**，且**每一行/每个短句前必须带有契合语义的 Emoji 符号**（如 🌤️, 💡, 🔴, 🔵, 👀, ✨, 👇）。若出现连续两行无 Emoji 符号或文字大段平铺直叙，直接裁决打回 `[REJECT]`。
- **纯文本格式隔离 (Clean Plain Text Only)**：正文绝对使用纯文本格式，严禁包含任何 `**bold**` 加粗、`*italic*` 斜体、`## Heading` 标题、`- ` 列表符号或 `[text](url)` 超链接。
- **6-10 个话题标签完整度 (一票否决)**：文案最末尾**必须包含 6-10 个以 `#` 开头的相关热门话题标签**（如 `#科普 #物理原理 #冷知识 #光学巨献 #自媒体选题 #爆款指南`），少于 6 个或无标签则直接裁决打回 `[REJECT]`。
