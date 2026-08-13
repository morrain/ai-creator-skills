---
name: workflow-learn
command: /workflow-learn
description: 偏好提取与规则自进化反哺工作流。当用户发送 /workflow-learn 指令、或在审核通过/人工修饰后需要将主编偏好沉淀为长期规则时唤起。
---

# 🧠 分环节审稿标准与案例库反哺工作流 (Targeted Review Tuner Workflow)

本工作流为 `ai-creator-skills` 项目的**多环节精准自进化闭环管道**。

因为创作流中人工审核的环节不只一处，且不同环节的审查规则侧重不同，本工作流会自动识别用户针对的**具体创作环节 (Phase ID)**，将提炼出的人工偏好与规则，按需懒加载落盘至项目根目录 **`./learnings/<phase_id>.md`** 中。

本工作流遵循 **【领域基线】+【项目增量】解耦原则**：
- **`./learnings/<phase_id>.md` 仅存放主编通过 `/workflow-learn` 提炼出的项目专属增量偏好**（黑名单词、案例金句、硬指标）；
- 不机械重复拷贝几百行的技能静态默认规则，彻底避免同级相对路径 (`references/anti_patterns.md` 等) 断裂的问题！

---

## 🏛️ 确定性环节 ID 路由与增量目标映射表

| 环节 ID (`phase_id`) | 对应创作环节 | 审查目标资产 | 技能默认基线标准 (default_standards) | 项目级增量规则路径 (learnings_file) |
| :--- | :--- | :--- | :--- | :--- |
| **`article_outline`** | 文章大纲阶段 | `./<slug>/outline.md` | `skills/article-writer/references/reviewer_standards.md` | `./learnings/article_outline.md` |
| **`article_content`** | 文章正文阶段 | `./<slug>/<slug>.md` | `skills/article-writer/references/reviewer_standards.md` | `./learnings/article_content.md` |
| **`illustrations`** | 正文插图阶段 | `./<slug>/assets/illustration_*.md` | `skills/illustration-designer/references/illustration_reviewer_standards.md` | `./learnings/illustrations.md` |
| **`weixin`** | 微信公众号阶段 | `./<slug>/mp_article.html` | `skills/wx-formatter/references/mp_reviewer_standards.md` | `./learnings/weixin.md` |
| **`poster_blueprint`**| 海报故事线阶段 | 海报故事线草案 | `skills/poster-designer/references/poster_reviewer_standards.md` | `./learnings/poster_blueprint.md` |
| **`poster_config`** | 单张海报配置阶段 | `./<slug>/assets/poster_*.md` | `skills/poster-designer/references/poster_reviewer_standards.md` | `./learnings/poster_config.md` |
| **`poster_post`** | 海报社媒文案阶段 | `./<slug>/poster_post.md` | `skills/poster-designer/references/poster_reviewer_standards.md` | `./learnings/poster_post.md` |
| **`video_script`** | 讲解剧本阶段 | `./<slug>/assets/video/video_script.json` | `skills/video-script-writer/references/script_reviewer_standards.md` | `./learnings/video_script.md` |
| **`video_unit`**| 视频单元设计阶段 | `./<slug>/assets/video/unit_XX/BRIEF.md` | `skills/video-storyboard-designer/references/storyboard_reviewer_standards.md` | `./learnings/video_unit.md` |
| **`<new_phase_id>`** | (未来扩展新环节) | (新场景产物) | `skills/<new_skill>/references/<standards>.md` | `./learnings/<new_phase_id>.md` |

---

## 核心设计原则 (Core Principles)

1. **最近一轮审核意见精准搜集 (Recent Review Feedback Scope Only)**：
   - 当调用 `/workflow-learn` 时，**仅搜集与归纳最近一轮审核中提到的意见**（包含 SubAgent 最近一次盲审意见与主编最近一轮修饰批注/审查反馈）。
   - 严禁抓取全量历史修改或无关的早前轮次，保证搜集的规则针对性强。
2. **人工交互式规则筛选关卡 (User Selection Gate)**：
   - 归纳出候选意见清单后，**严禁自动全量落盘**。
   - 必须向用户呈现带编号的意见列表，**暂停对话并等待用户明确选择**（如回复编号“1”、“1, 3”或“全部”），**仅将用户选中的规则条目落盘至规范文件**。
3. **动态蒸馏去重与冲突覆盖 (Compaction & Conflict Overwrite)**：
   - 增量落盘时，Agent 必须自动将新选中的规则与现存旧规则进行语义比对：
     - **语义合并**：若语义重叠，归纳合并为 1 条精炼规则；
     - **冲突覆盖**：若新规则与旧规则有抵触矛盾，**强制以最新选择的规则为准覆盖/覆盖删除旧规则**。
4. **硬性容量上限与滑动淘汰 (Cap Limit & Eviction Policy)**：
   - 为 `./learnings/<phase_id>.md` 设定各分类条目硬性容量上限：
     - ❌ **反面黑名单**：上限 **10 条**
     - 🌟 **正面标杆**：上限 **5 条**
     - 📝 **审查硬指标**：上限 **5 条**
   - 当写入后条目超限时，自动依时间顺序 (FIFO) 淘汰最早的旧规则，保证文件体积恒定在轻量级（＜ 500 Tokens）。
5. **按需精准隔离与低 Token 污染 (Zero Context Cross-Contamination)**：
   - 规则按环节拆分归档。正文盲审只读 `article_content.md`，微信排版盲审只读 `weixin.md`，海报文案只读 `poster_post.md`。
6. **底层 Skill 纯洁零修改 (Skill Layer Purity)**：
   - 严禁修改 `skills/` 目录下的任何通用技能文件。所有演进规则集中在根目录 `./learnings/` 目录下。

---

## 详细工作流步骤

### 步骤一：识别环节 ID (`phase_id`) 与搜集最近一轮审核意见

1. **自动匹配 / 显式识别环节 ID**：
   - 根据被修改/审查资产的文件名自动推断（如 `mp_article.html` ➔ `phase_id: weixin`），或由用户直接传入参数。
2. **搜集最近一轮审核意见 (Collect Opinions from Latest Review Round)**：
   - 读取该资产在**最近一轮审核**（包括 SubAgent 最近一次盲审打回/通过记录，或主编最新一轮批注与意见）中提出的具体修正要求与问题定位。
   - 仅搜集该**最近一轮**的意见归纳，忽略早期历史轮次。

---

### 步骤二：结构化归纳候选规则清单

将最近一轮审核意见归类整理为待选规则项：
- ❌ **反面黑名单 (Anti-Patterns)**：审核指出的禁用词、违规格式或偏好禁忌。
- 🌟 **正面标杆 (Golden Examples)**：审核认可或精修的爆款范例、金句与表达。
- 📝 **审稿硬性指标 (Reviewer Additions)**：字数限制、Emoji 密度、特定组件卡片约束。

---

### 步骤三：呈报候选规则与人工选择关卡 (User Selection Gate)

1. **结构化呈报带编号的候选规则清单**：
   - 向用户呈现归纳出的意见编号列表。
2. **暂停并等待用户选择**：
   > 💡 **主编规则筛选与落盘提示**：
   > 以上为在**最近一轮审核**中提炼出的意见归纳：
   > 1. ❌ **[禁用词/反面模式]**：`...`
   > 2. 🌟 **[爆款范例/优质表达]**：`...`
   > 3. 📝 **[环节审查硬指标]**：`...`
   > 
   > 👉 请在对话框回复希望落到规范中的**规则编号**（例如：`1`、`1, 3` 或 `全部`），系统将**仅把您选中的条目**沉淀至 [`./learnings/<phase_id>.md`](./learnings/<phase_id>.md)！

---

### 步骤四：根据用户选择执行蒸馏、淘汰与落盘

1. **接收用户选择**：读取用户回复的编号（如 `1, 3`）。
2. **计算确定性目标路径**：`./learnings/<phase_id>.md`。
3. **按需检测与创建 (Delta Creation)**：
   - 检查项目根目录下是否存在 `./learnings/` 目录。若无，自动创建。
   - **检测 `./learnings/<phase_id>.md` 是否存在**：若不存在（首次建库），创建包含标题头的精纯增量规则库文件；若已存在，进入读取与蒸馏重构模式。
4. **蒸馏去重与冲突覆盖 (Compaction & Overwrite)**：
   - 将用户选中的规则条目与现存规则进行语义比对，合并重复规则，最新规则直接覆盖相矛盾的旧规则。
5. **硬性容量控制与淘汰 (Capacity Eviction Check)**：
   - 检查各大板块存量：若 `❌ 黑名单` > 10 条、`🌟 范例` > 5 条或 `📝 硬指标` > 5 条，优先按时间最早 (FIFO) 原则淘汰超出部分的旧规则。
6. **外科手术式落盘与呈报**：
   - 将整理后的精炼规则集写回 `./learnings/<phase_id>.md`，呈现落盘、覆盖与淘汰清理的最终沉淀报告。
