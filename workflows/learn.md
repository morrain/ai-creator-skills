---
name: workflow-learn
command: /学习
description: 审稿标准与案例库增量反哺工作流。识别各创作环节的人工修改 Diff 或反馈批注，触发 review_tuner 机制。按需懒加载创建精纯的项目规则增量文件 ./learnings/<phase_id>.md 并外科手术式追加落盘，保持底层 skills 零修改。
---

# 🧠 分环节审稿标准与案例库反哺工作流 (Targeted Review Tuner Workflow)

本工作流为 `ai-creator-skills` 项目的**多环节精准自进化闭环管道**。

因为创作流中人工审核的环节不只一处，且不同环节的审查规则侧重不同，本工作流会自动识别用户针对的**具体创作环节 (Phase ID)**，将提炼出的人工偏好与规则，按需懒加载落盘至项目根目录 **`./learnings/<phase_id>.md`** 中。

本工作流遵循 **【领域基线】+【项目增量】解耦原则**：
- **`./learnings/<phase_id>.md` 仅存放主编通过 `/学习` 提炼出的项目专属增量偏好**（黑名单词、案例金句、硬指标）；
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
| **`<new_phase_id>`** | (未来扩展新环节) | (新场景产物) | `skills/<new_skill>/references/<standards>.md` | `./learnings/<new_phase_id>.md` |

---

## 核心设计原则 (Core Principles)

1. **增量精纯存储 (Concise Delta Storage)**：
   - 首次反哺新建 `./learnings/<phase_id>.md` 时，仅创建标准的三向结构（黑名单、标杆例句、增量硬指标）标题头。
   - 避免机械大文件拷贝，解决技能默认标准依赖同级相对文件 (`anti_patterns.md`, `golden_examples.md`, `style_definitions.md`) 的寻址断裂问题。
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

### 步骤三：按需懒加载创建与增量追加落盘

1. **计算确定性目标路径**：`./learnings/<phase_id>.md`。
2. **按需检测与创建 (Delta Creation)**：
   - 检查项目根目录下是否存在 `./learnings/` 目录。若无，自动建目录。
   - **检测 `./learnings/<phase_id>.md` 是否存在**：
     - **若不存在（首次建库）** ➔ 创建包含标题头的精纯增量规则库文件！
     - **若已存在** ➔ 直接进入追加模式。
3. **外科手术式增量追加**：将本次提炼的新规则追加在末尾，标注来源主题与日期时间戳。

---

### 步骤四：呈报进化报告

呈报本次规则提炼与沉淀结果：

```markdown
### 🧠 分环节审稿规则自进化沉淀完成报告

**目标环节**：`[环节名称 & phase_id]`  
**目标落盘文件**：[`./learnings/<phase_id>.md`](../learnings/<phase_id>.md)

本次提炼并沉淀的专属规则：
1. ❌ **新增禁用词 / 反面模式**：`...`
2. 🌟 **新增爆款范例 / 降维比喻**：`...`
3. 📝 **环节审查增量硬指标**：`...`

> 💡 **生效提示**：下次执行该环节盲审时，`blind-reviewer` 将同时加载领域基线标准与本项目增量规则文件进行精确质检！
```
