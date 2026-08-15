---
name: video-renderer
description: FFmpeg 极速视频拼接技能。当需要将各单元视频片段（包含横/竖屏多比例）极速无损拼接导出成品 MP4 时调用。
---

# Video Renderer (视频最终合成器)

本技能作为一个**纯粹的 FFmpeg 视频极速无损拼接原子技能**。它负责扫描各视频单元（`unit_01` 至 `unit_N`）输出的片段（如 `unit_01_16x9.mp4`, `unit_01_9x16.mp4` 或 `unit_01.mp4`），极速完成 `-c copy` 无损拼合，并自动拷贝成品视频到项目根目录。由于各单元视频在 HyperFrames 渲染阶段已包含原生音轨与 HTML 唱词字幕，拼接过程无需重新压制字幕或重排声音。

## Agent 执行协议 (Protocol)

1. **环境准备确认**：
   Agent 确认目标项目资产目录（如 `./<article-slug>/assets/video/`）下存在各单元视频片段。
2. **执行拼接合并**：
   调用本技能下的 Python 脚本，传入目标项目目录。脚本会自动智能扫描并拼接各比例切片（若存在背景音乐 `bgm.mp3` 则自动混入背景音乐）：
   ```bash
   python skills/video-renderer/scripts/render_final_video.py --project-dir ./<article-slug>/assets/video/ --fast-concat
   ```

## 交付产物

在项目根目录及 `assets/video/` 目录下生成最终视频：
- `video_16x9.mp4` / `video_9x16.mp4` / `video.mp4`

## 核心实现说明
- **极速无损拼接**：HyperFrames 各单元在渲染 MP4 时已原生固化压制口播音频轨与 HTML 唱词字幕，本技能直接进行极速 `-c copy` 拼合，毫秒级导出最终视频，彻底杜绝字幕重叠与视频二次重编码损耗。

