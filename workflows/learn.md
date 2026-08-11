---
name: workflow-learn
command: /学习
description: 审稿标准与案例库增量反哺工作流。识别各创作环节的人工修改 Diff 或反馈批注，触发 review_tuner 机制。首次反哺时自动读取技能层默认审稿标准作为基线种子，全量写入并新建项目根目录 ./learnings/<phase_id>.md，随后增量追加新规则，使后续盲审实现单文件高效加载。
---

# 🧠 分环节审稿标准与案例库反哺工作流 (Targeted Review Tuner Workflow)

本工作流为 `ai-creator-skills` 项目的**多环节精准自进化闭环管道**。

因为创作流中人工审核的环节不只一处，且不同环节的审查规则侧重不同，本工作流会自动识别用户针对的**具体创作环节 (Phase ID)**，将提炼出的人工偏好与规则，按需懒加载落盘至项目根目录 **`./learnings/<phase_id>.md`** 中。

本工作流引入了 **基线种子播种机制 (Seeded Evolution)**：在某个环节**首次生成 `./learnings/<phase_id>.md` 时，会自动将底层 Skill 的默认基线标准全量写入**，随后追加人工修饰出的新规则。

这种设计使得 **`./learnings/<phase_id>.md` 成为一个全量自包含的完整审稿规则库**。在后续盲审中，通用盲审引擎 `blind-reviewer` **只需单文件装载 `./learnings/<phase_id>.md`**，无需再加载技能层的默认文件，达到极致的读取速度与零 Token 浪费！

---

## 🏛️ 确定性环节 ID 路由与基线种子映射表

| 环节 ID (`phase_id`) | 对应创作环节 | 审查目标资产 | 首次建库装载的基线种子标准 (Seed Source) | 项目级自包含规则路径 |
| :--- | :--- | :--- | :--- | :--- |
| **`article_outline`** | 文章大纲阶段 | `./<slug>/outline.md` | `skills/article-writer/references/reviewer_standards.md` | `./learnings/article_outline.md` |
| **`article_content`** | 文章正文阶段 | `./<slug>/<slug>.md` | `skills/article-writer/references/reviewer_standards.md` | `./learnings/article_content.md` |
| **`illustrations`** | 正文插图阶段 | `./<slug>/assets/illustration_*.md` | `skills/illustration-designer/references/illustration_reviewer_standards.md` | `./learnings/illustrations.md` |
| **`weixin`** | 微信公众号阶段 | `./<slug>/mp_article.html` | `skills/wx-formatter/references/mp_reviewer_standards.md` | `./learnings/weixin.md` |
| **`poster_blueprint`**| 海报故事线阶段 | 海报故事线草案 | `skills/poster-designer/references/poster_reviewer_standards.md` | `./learnings/poster_blueprint.md` |
| **`poster_config`** | 单张海报配置阶段 | `./<slug>/assets/poster_*.md` | `skills/poster-designer/references/poster_reviewer_standards.md` | `./learnings/poster_config.md` |
| **`poster_post`** | 海报社媒文案阶段 | `./<slug>/poster_post.md` | `skills/poster-designer/references/poster_reviewer_standards.md` | `./learnings/poster_post.md` |
| **`<new_phase_id>`** | (未来扩展新环节) | (新场景产物) | `skills/<new_skill>/references/<standards>.md` | `./learnings/<new_phase_id>.md` |

---

## 核心设计原则 (Core Principles)

1. **首次建库基线播种与单文件极速装载 (Seeded Initialization & Single-File Read)**：
   - 首次反哺新建 `./learnings/<phase_id>.md` 时，自动将 Skill 默认审查标准填入作为初始基线种子。
   - 使得该文件全量自包含，后续盲审**仅需单文件读取**。
2. **按需精准隔离与低 Token 污染 (Zero Context Cross-Contamination)**：
   - 规则按环节拆分归档。正文盲审只读 `article_content.md`，微信排版盲审只读 `weixin.md`，海报文案只读 `poster_post.md`。
3. **底层 Skill 纯洁零修改 (Skill Layer Purity)**：
   - 严禁修改 `skills/` 目录下的任何通用技能文件。所有演进规则集中在根目录 `./learnings/` 目录下。

---

## 详细工作流步骤

### 步骤一：识别环节 ID (`phase_id`) 与提取反馈 Diff

1. **自动匹配 / 显式识别环节 ID**：
   - 根据被修改资产的文件名自动推断（如修改 `mp_article.html` ➔ `phase_id: weixin`），或由用户直接传入参数。
2. **提取差异块 (Diff Extraction)**：
   - 比对 Agent 初始输出版本与主编人工修正后版本的字句、格式、标点及排版差异。

---

### 步骤二：触发 `review_tuner` 归纳演进

将修正动机归类为：
- ❌ **反面黑名单 (Anti-Patterns)**：用户删除的套话、违规格式或偏好禁忌。
- 🌟 **正面标杆 (Golden Examples)**：用户精修的爆款金句、高吸引力结构或精准隐喻。
- 📝 **审稿硬性指标 (Reviewer Additions)**：字数限制、Emoji 密度、特定组件卡片约束。

---

### 步骤三：基线播种与按需追加落盘

1. **计算确定性目标路径**：`./learnings/<phase_id>.md`。
2. **按需检测与基线播种 (Seeded Creation)**：
   - 检查项目根目录下是否存在 `./learnings/` 目录。若无，自动建目录。
   - **检测 `./learnings/<phase_id>.md` 是否存在**：
     - **若不存在（首次建库）** ➔ 读取该 `phase_id` 在降级表对应的 Skill 默认基线标准文件，写入 `./learnings/<phase_id>.md` 作为初始正文，建立全量自包含规则库！
     - **若已存在** ➔ 直接进入追加模式。
3. **外科手术式增量追加**：将本次提炼的新规则追加在末尾，标注来源主题与日期时间戳。

---

### 步骤四：呈报进化报告

呈报本次规则提炼与沉淀结果：

```markdown
### 🧠 分环节审稿规则自进化沉淀完成报告

**目标环节**：`[环节名称 & phase_id]`  
**目标落盘文件**：[`./learnings/<phase_id>.md`](../learnings/<phase_id>.md)

本次播种与提炼沉淀的规则：
1. 🌱 **基线种子播种**：已自动将领域默认审查标准全量包含至本项目规则库中。
2. ❌ **新增禁用词 / 反面模式**：`...`
3. 🌟 **新增爆款范例 / 降维比喻**：`...`
4. 📝 **环节审查增量硬指标**：`...`

> 💡 **生效提示**：下次执行该环节盲审时，`blind-reviewer` 将仅单文件装载 `./learnings/<phase_id>.md` 进行极速质检！
```
