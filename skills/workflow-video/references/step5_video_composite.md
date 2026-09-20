# Step 5: 合成成品视频与全平台发布文案生成

## 详细缝合与交付规程

1. **前置门控 (Strict Execution Gate)**：
   - **全量单元渲染完成触发**：必须在所有单元（`unit_01` 至 `unit_N`）的 9:16 竖屏切片片段（`unit_XX.mp4`）全部渲染成功且归档完毕后，方可触发 Step 5 缝合！若用户要求生成宽屏版本，则需等待 16:9 切片片段（`unit_XX_16x9.mp4`）也归档完毕。

2. **提取文章标题与极速缝合导出成品视频**：
   - **提取文章标题名**：从 `./<article-slug>/<article-slug>.md` 的 H1 标题或 `video_script.json` 的 `metadata.title` 中提取文章标题名 `<article-title>`（如 `什么是猪周期`）；若无标题则退回到 `<article-slug>`。文件名必须统一使用文章标题名。
   - 调度原子技能 `video-renderer` 运行纯视频拼接脚本，指定输出文章标题名：
     ```bash
     python skills/video-renderer/scripts/render_final_video.py --project-dir ./<article-slug>/assets/video --output-name "<article-title>" --fast-concat
     ```
   - 脚本会自动扫描各个 `unit_XX` 目录下的切片，通过 `ffmpeg -c copy` 极速缝合导出以文章标题命名的成品视频。

3. **交付成品与全平台发布文案生成 (Deliver Video & Generate Publishing Post)**：
   - 校验并在对话框呈报最终在 `./<article-slug>/assets/video/` 目录下导出的成品视频文件路径 Markdown 超链接：
     - 竖屏成品版（默认）：`[<article-title>_9x16.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/<article-title>_9x16.mp4)`
     - 宽屏成品版（仅当显式要求生成宽屏时）：`[<article-title>_16x9.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/<article-title>_16x9.mp4)`
   - **全平台发布文案自动生成规程 (Mandatory Post Copywriting)**：
     - 视频合成成功后，Agent **必须在对话框中同步呈报一份结构化的全平台发布文案**，包含以下 3 大模块（支持主编直接一键复制发布）：
       1) 📌 **多平台差异化标题（严格按各平台字数限制与调性定制）**：
          - **小红书标题**（限制 $\le 20$ 字，带情绪/悬念与 Emoji 视觉点缀）
          - **微信视频号 / 公众号标题**（限制 $\le 16$ 字，偏深度干货/专业解读）
          - **抖音 / 快手标题**（限制 $\le 30$ 字，短平快/爆款痛点/热点引流）
          - **B站 / 横屏标题**（限制 20-30 字，偏硬核原理/科普/求知）
       2) 📝 **精炼内容简介（100 字左右）**：
          - 结合视频核心痛点与结论，撰写一段适合发布在各平台视频简介/正文区的精炼摘要（控制在 90 ~ 110 字），通顺有吸引力。
       3) 🏷️ **核心话题标签（6 ~ 8 个）**：
          - 提取 6 ~ 8 个与视频主题高度相关的热门 Tag，格式为 `#话题名称`（如 `#AI工具` `#硬核科普` 等），方便一键一键复制粘贴发布。

4. **自进化规则提示**：
   - 提示主编可使用 `/workflow-learn video_script` 或 `/workflow-learn video_storyboard` 沉淀自进化规程。
