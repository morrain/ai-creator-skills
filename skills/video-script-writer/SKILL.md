---
name: video-script-writer
description: 4 轨动画讲解视频剧本提炼技能。当需要将文章正文或知识主题拆解提炼为包含口播、画面与 IP 动作的 video_script.json 剧本时调用。
---

# Video Script Writer Skill (4 轨讲解剧本提炼技能)

本技能为 **纯粹无状态的原子剧本提炼技能**。指导 AI Agent 根据输入的长文章 Markdown（模式 1）或知识主题（模式 2），解耦并输出严格符合 4 轨规范的结构化 `video_script.json` 讲解剧本。

---

## 核心设计原则 (Core Principles)

1. **单点输入与无状态提炼 (Stateless Script Output)**：
   - 技能接收文章 Markdown 文本或知识主题名称，以及模式参数（`mode: article_derived` 或 `mode: standalone_topic`）。
   - 纯粹处理文本逻辑并返回标准的 4 轨 JSON 剧本，零主题工作区存盘与文件流转依赖。
2. **4 轨解耦结构 (Four-Track Script Schema)**：
   - 每个视频单元解耦为 4 个独立轨道：
     - `time_code` & `duration_seconds`: 单元编号与精准预估时长（单位：秒）。
     - `voiceover`: 极具知识博主/科普解说听感的逐字口播文案。
     - `visual_prompt & ip_action`: 画面背景描述与 IP Mascot（IP 角色）的具体物理动作指示。
     - `on_screen_elements` (可选与克制原则): 画面标题花字 `title_card`（**通常仅在 Unit 01 Hook 开篇或重大章节转折时设置，严禁在每个单元机械堆叠**）、唱词高亮词 `highlight_keywords`（可选，非必要不堆砌）及视觉组件提示 `graphics_hint`（可选）。主要视觉布局与节奏交由下游 `video-storyboard-designer` 灵活排布。
3. **双模式支持 (Dual-Mode Support)**：
   - **模式 1 (文章衍生 `article_derived`)**：分析长文的正文脉络与金句，保留文章插图中已确立的物理隐喻方向，将其重构为流畅的视频单元。
   - **模式 2 (独立主题 `standalone_topic`)**：直接根据输入的知识主题，自动规划引钩 (Hook)、原理解析与总结，生成 0 到 1 的讲解脚本。
4. **口播听感与短句呼吸感 (Natural Voiceover Pacing)**：
   - 必须使用口语化、接地气的听觉语言，杜绝“综上所述”、“显而易见”等书面套话。
   - 语速控制在 **4 ~ 5 字/秒**（例如 10 秒单元，口播在 35 ~ 45 字之间），单句控制在 25 字以内，具备自然呼吸停顿。
5. **IP 角色动作核心化 (IP Action Centricity)**：
   - 剧本提炼阶段无须加载具体的 IP 形象规范。在 `ip_action` 与 `visual_prompt` 字段中，统一使用泛称 **`IP Mascot 角色`**，确保剧本绝对无状态与解耦。角色不是背景贴纸或卖萌吉祥物，而是正在拉扯线缆、推推闸门、盖章或操作机器的核心系统操作员。

---

## 关联参考规范

在执行剧本提炼时，主动读取以下参考规范：
- [`references/script_schema.json`](references/script_schema.json)：4 轨 JSON Schema 协议定义。
- [`references/script_examples.md`](references/script_examples.md)：标准 4 轨剧本 JSON 示范文件。
- [`references/script_reviewer_standards.md`](references/script_reviewer_standards.md)：脚本盲审与质检标准。

---

## 规范输出格式

调用本技能将直接输出符合 JSON Schema 的 `video_script.json` 内容：

```json
{
  "metadata": {
    "title": "视频大标题",
    "target_duration_seconds": 60,
    "genre": "科普解说",
    "mode": "article_derived",
    "source_article_path": "./path/to/article.md"
  },
  "units": [
    {
      "unit_id": "Unit 01",
      "duration_seconds": 8,
      "voiceover": "逐字口播文案...",
      "visual_prompt": "16:9 纯白背景，黑色手绘线条风格...",
      "ip_action": "IP Mascot 角色手持数据线缆...",
      "on_screen_elements": {
        "title_card": "单元标题",
        "highlight_keywords": ["关键词1", "关键词2"],
        "graphics_hint": "HyperFrames 视觉组件提示"
      }
    }
  ]
}
```
