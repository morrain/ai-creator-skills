---
name: workflow-video
command: /讲解视频
description: 动画讲解视频全流程生成编排 Skill。当用户发送 /讲解视频 指令、或需要将文章/知识主题转化为带有配音、IP Mascot 动作链与视频渲染的 MP4 时唤起。
---

# 🎬 动画讲解视频生成业务编排 Skill (Explainer Video Workflow Skill)

本 Skill 为 `ai-creator-skills` 项目的动画讲解视频生成管道，负责接收输入（文章路径 `./<article-slug>/<article-slug>.md` 或独立主题），调度底层原子技能（`video-script-writer`、`voiceover-generator`、`video-storyboard-designer`、`video-renderer`、`cover-designer`）与 HyperFrames 技能，贯穿执行 5 大步骤。

---

## 核心设计原则与执行约束

1. **渐进式加载约束**：主流程仅保留状态机与卡点控制逻辑，各步骤的具体执行规程与 SubAgent Prompt 分别存放于 `references/` 下，Agent 在执行特定 Step 时使用 `view_file` 按需加载。
2. **双模式自适应**：支持文章转视频 (`article_derived`) 与独立主题创作 (`standalone_topic`)。
3. **双节点强制人工审核卡点**：
   - **卡点 1（剧本确认为止）**：Step 1 生成剧本盲审通过后，**强制中途停顿**，向主编呈报拆分方案，获得显式确认回复后方可落盘 `video_script.json` 并进入 Step 2。
   - **卡点 2（首单元风格确认 & 全量终审）**：Step 4 率先单独渲染 `unit_01` 呈报人工审核。主编确认后提炼通用规则继承至后续单元；全量单元渲染完成后再次强制中途停顿，结构化呈报切片超链接进行全片终审，获批后进入 Step 5。
4. **音画字幕单元内固化与纯视频缝合**：Step 5 仅做极速纯视频 `ffmpeg -c copy` 拼接。
5. **路径呈报规范**：代码/规范中使用相对路径 `./`；对话框呈报 MP4 时统一使用 `[unit_XX.mp4](file://<workspace-abs-path>/...)` 绝对路径超链接。

---

## 阶段流程与 Reference 映射

| 阶段 | 阶段名称 | 核心任务与门控 | 按需引用的详细规程 (view_file) |
| :--- | :--- | :--- | :--- |
| **Step 1** | 生成脚本与剧本盲审 | 提炼 4 轨剧本，盲审，**人工确认卡点**，落盘 `video_script.json` | [references/step1_script_design.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step1_script_design.md) |
| **Step 2** | 生成语音与锁定时长 | 运行 TTS，导出切片音频与时间轴，锁定实际时长 $A_i$ | [references/step2_voiceover.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step2_voiceover.md) |
| **Step 3** | 分镜契约与工程初始化| 逐单元初始化 HyperFrames 脚手架，注入 `BRIEF.md` 与资产 | [references/step3_storyboard_spec.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step3_storyboard_spec.md) |
| **Step 4** | 逐单元渲染与批次审核 | 单独渲染 `unit_01` 并**人工审核**；继承规则批量渲染后续单元；全量完成**二次人工终审** | [references/step4_rendering_rules.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step4_rendering_rules.md) |
| **Step 5** | 极速缝合与文案交付 | `ffmpeg -c copy` 缝合成品，生成多平台发布文案与超链接 | [references/step5_video_composite.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step5_video_composite.md) |

---

## 执行步骤概述

1. **Step 1 阶段**：读取 [step1_script_design.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step1_script_design.md)，调度 `video-script-writer` 生成剧本，完成 SubAgent 盲审。向主编呈报剧本草案，**暂停等待确认**。主编确认后存盘 `video_script.json`。
2. **Step 2 阶段**：读取 [step2_voiceover.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step2_voiceover.md)，调度 `voiceover-generator` 生成 TTS 音频与时间轴。
3. **Step 3 阶段**：读取 [step3_storyboard_spec.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step3_storyboard_spec.md)，调度 `video-storyboard-designer` 建立各 `unit_XX` 目录，逐个运行 `npx hyperframes init`，注入 `BRIEF.md` 与 public 资产。
4. **Step 4 阶段**：读取 [step4_rendering_rules.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step4_rendering_rules.md)，主 Agent 封包唤起 SubAgent。先渲染 `unit_01` 呈报人工审核。审核通过后提炼 `[inherited_style_rules]` 批量渲染剩余单元。全部完成后呈报切片超链接进行全片终审。
5. **Step 5 阶段**：读取 [step5_video_composite.md](file:///Users/morrain/Documents/codes/ai-creator-skills/skills/workflow-video/references/step5_video_composite.md)，调用 `video-renderer` 缝合视频，在对话框呈报 MP4 绝对路径超链接与全平台发布文案。提示主编可使用 `/workflow-learn` 沉淀偏好。
