---
name: video-renderer
description: FFmpeg 视频拼接与音频 Ducking 混流技能。当需要将各单元视频片段无损拼接，混入配音与 BGM 并压制硬字幕导出最终 MP4 时调用。
---

# Video Renderer (视频最终合成器)

本技能作为一个**纯粹的 FFmpeg 视频拼装与音频混流的原子技能**。它负责将各视频单元输出的片段（如 `./unit_01/unit_01.mp4`, `./unit_02/unit_02.mp4` 或 `unit_*.mp4`）无损拼合，并混入人声配音 (`voiceover.mp3`) 和背景音乐 (`bgm.mp3`)。

## Agent 执行协议 (Protocol)

1. **环境准备确认**：
   Agent 确认目标项目资产目录（如 `./<article-slug>/assets/video/`）下存在 `unit_01/unit_01.mp4`, `unit_02/unit_02.mp4` 等单元视频片段。
2. **执行拼接合并**：
   调用本技能下的 Python 脚本，传入目标项目目录。脚本会自动智能检测：当单元视频已自带音频/字幕时，自动开启 `--fast-concat` 极速拼接模式（纯 `-c copy` 无损拼合，保留 HTML 卡片字幕并避免二次压字幕与重合音轨）；若存在背景音乐 `bgm.mp3`，则自动混入背景音乐。
   ```bash
   python skills/video-renderer/scripts/render_final_video.py --project-dir ./<article-slug>/assets/video/ --fast-concat
   ```

## 交付产物

在项目的 `assets/video/` 目录下生成最终视频：
- `final_video.mp4` / `video.mp4`

## 核心实现说明
- **极速拼接模式 (`--fast-concat`)**：当 HyperFrames 各单元在渲染 MP4 时已包含口播音频轨与 HTML 字幕节点，本技能直接进行极速 `-c:v copy -c:a copy` 拼合，毫秒级导出最终视频，避免字幕重叠与二次重编码损失。
- **降噪混流模式 (`--force-remux`)**：若单元视频无音频轨，利用 `ffmpeg` 的 `sidechaincompress` 滤镜或者 `volume` ducking 算法实现有人声说话时自动压低背景音乐，并二次压制 ASS 字幕。
