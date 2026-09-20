# 🧠 自进化反哺业务编排 - 阶段规程与路由映射表

## 确定性环节 ID 路由与增量目标映射表

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

---

## 详细操作步骤

1. **步骤一：识别环节 ID (`phase_id`) 与搜集最近一轮审核意见**：
   - 根据资产文件名推断 `phase_id`（或用户显式指定）。
   - 显式调用 `view_file` 读取磁盘最新文件，收集最近一轮 SubAgent 盲审意见或主编修改。
2. **步骤二：结构化归纳候选规则清单**：
   - 归类为 ❌ 反面黑名单、🌟 正面标杆、📝 审稿硬指标。
3. **步骤三：呈报候选规则与人工选择关卡 (User Selection Gate)**：
   - 呈报带编号清单，暂停等待用户选择回复（如 `1, 3` 或 `全部`）。
4. **步骤四：蒸馏、淘汰与落盘**：
   - 确认写入 `./learnings/<phase_id>.md`。
   - 执行语义去重、冲突覆盖与容量淘汰（黑名单上限 10 条、范例上限 5 条、硬指标上限 5 条，超限 FIFO 淘汰旧规则）。
