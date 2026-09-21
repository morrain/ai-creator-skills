---
name: workflow-poster
command: /海报
description: 知识总结与社媒海报生成工作流。当用户发送 /海报 指令、/知识海报 指令、或需要将长文/知识点转化为多张手绘风格海报与社媒文案时唤起。
---

# 🖼️ 图文海报派生业务编排 Skill (Poster Workflow Skill)

本 Skill 为 `ai-creator-skills` 项目的多图文海报与社媒文案派生管道，负责读取 `./<article-slug>/` 资产，规划故事线蓝图与 10 大版式映射，并发调度 `poster-designer` 渲染单张海报设计，运行 3 阶段 SubAgent 盲审，落盘 `assets/poster_N.md` 配置文件与 100% 纯文本社媒文案 `poster_post.md`。

---

## 核心设计原则

1. **按需延时生图 (Strict Lazy Generation)**：默认仅生成 Markdown 配置文件与社媒文案，严禁自动调用 `generate_image` 生图，除非用户显式下达“开始生图”指令。
2. **社媒文案纯文本隔离 (Clean Plain Text Rule)**：`poster_post.md` 必须保持纯文本格式，无 Markdown 标签。
3. **插图隐喻继承**：优先继承正文插图配置 (`assets/illustration_*.md`) 中的核心隐喻与 IP Mascot 动作。
4. **全渠道留言与私信引导**：海报 Footer 与文案末尾强引导留言/私信索取完整拆解。

---

## 阶段流程与 Reference 映射

详细步骤说明与版式映射表请参阅：
[references/stage_details.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-poster/references/stage_details.md)

1. **阶段一（蓝图提炼）**：读取文章与插图，规划 N 张卡片与版式，唤起 `blind-reviewer` 审稿蓝图。
2. **阶段二（配置生成）**：并发调度 `poster-designer` 提炼卡片，唤起 SubAgent 审查，落盘 `./<article-slug>/assets/poster_1.md ~ poster_N.md`。
3. **阶段三（文案合成）**：合成带 8 个爆款备选标题、高密度 Emoji、留言引导、评论区提问与 6-10 个金字塔 `#话题标签` 的纯文本 `poster_post.md`，盲审后落盘呈报。
