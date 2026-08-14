# Feature Spec: Multi-Aspect Ratio Progressive Video Rendering

## Problem Statement

When creators build explainer animation videos using `/讲解视频`, the output is fixed to a single 16:9 widescreen format (`1920x1080`). To publish on mobile-first platforms (TikTok, Douyin, WeChat Channels, YouTube Shorts, Xiaohongshu), creators currently have to manually re-run the entire pipeline or manually crop the video, causing poor layout composition, unreadable text, or lost visual context.

Creators need a seamless way to render a secondary aspect ratio (such as 9:16 mobile portrait or 1:1 square) per video unit during the workflow, preserve both aspect source codes and MP4 segments, and automatically export multiple final videos for different platforms at the end of the pipeline.

## Solution

Implement multi-aspect ratio progressive rendering in the explainer video pipeline (`video.md`, `render_final_video.py`, and `video-storyboard-designer`):
1. Support `--aspect <ratio>` flags (e.g. `16:9`, `9:16`, `1:1`, `4:5`) in the `/讲解视频` command.
2. In Stage 3 (SubAgent unit rendering), offer per-unit interactive prompts to render secondary aspect versions (e.g., render 9:16 portrait right after 16:9 widescreen for unit 01) and a batch completion prompt at the end of Stage 3.
3. Manage active `BRIEF.md` / `index.html` files alongside per-aspect snapshot files (`index_16x9.html`, `index_9x16.html`) for 100% HyperFrames CLI compatibility.
4. Enhance `render_final_video.py` to auto-detect multi-aspect unit segments and export corresponding final MP4 versions (`video.mp4` / `video_9x16.mp4`).

## User Stories

1. As a video content creator, I want to specify `--aspect 9:16` when running `/讲解视频`, so that my video units are scaffolded for mobile portrait platforms.
2. As a video content creator, I want to be prompted after rendering a 16:9 unit video whether I'd like to render a 9:16 portrait version for that same unit, so that I can immediately build and review both ratios for a unit.
3. As a video content creator, I want the workflow to retain both `unit_01_16x9.mp4` and `unit_01_9x16.mp4` simultaneously, so that no rendered asset is overwritten.
4. As a video developer, I want the unit directory to store `index_16x9.html` and `index_9x16.html` snapshots while maintaining `./index.html` and `./BRIEF.md` for active rendering, so that official HyperFrames CLI tools work without breaking.
5. As a video content creator, I want the workflow to offer a batch-completion option after Stage 3, so that I can automatically generate 9:16 versions for all remaining units if I only rendered a few during per-unit review.
6. As a video content creator, I want Stage 4 (`render_final_video.py`) to automatically detect multi-aspect unit segments and produce both `./video.mp4` (widescreen) and `./video_9x16.mp4` (portrait), so that I get publish-ready videos for all target platforms in one step.

## Implementation Decisions

1. **Active Target Pointer & Aspect Snapshots**:
   - `unit_XX/` maintains active `./BRIEF.md` and `./index.html` for HyperFrames CLI compatibility.
   - The **Main Agent** manages updating `./BRIEF.md` / `./index.html`, creating snapshots (`BRIEF_<aspect>.md`, `index_<aspect>.html`), and copying output `unit_XX.mp4` to `unit_XX_<aspect>.mp4`.
   - The **SubAgent** prompt and execution logic remain 100% unchanged (consuming `./BRIEF.md` and writing `./unit_XX.mp4`).

2. **Stage 3 Workflow Interactive Gate**:
   - Per-unit interactive prompt: `[1. 渲染 9:16 竖屏版本] [2. 跳过，进入下一单元]`.
   - Stage 3 batch completion gate: `[1. 批量补全所有未渲染单元的 9:16 版本] [2. 跳过，直接进行合成]`.

3. **FFmpeg Multi-Aspect Concat (`render_final_video.py`)**:
   - Scans unit directory for aspect suffixes (`_16x9.mp4`, `_9x16.mp4`).
   - Grouping segments by aspect ratio and executing lossless `-c copy` concatenation for each aspect set.
   - Outputs `./video.mp4` (primary 16:9) and `./video_<aspect>.mp4` (secondary versions).

## Testing Decisions

1. **Unit Testing & Script Execution**:
   - Verify `render_final_video.py --project-dir <path>` auto-detects single aspect (`unit_*.mp4`) vs multi-aspect (`unit_*_9x16.mp4`).
   - Verify lossless `-c copy` concatenation produces valid playable MP4s for both 16:9 and 9:16 resolutions.

2. **Workflow Seam**:
   - High-level workflow seam at Stage 3 & Stage 4 in `workflows/video.md`.
   - Script-level seam at `render_final_video.py`.

## Out of Scope

1. Automatic AI repositioning of third-party 3D WebGL assets (focused on 2D SVG/HTML GSAP layouts).
2. Live streaming multi-aspect transcoding.

## Further Notes

- Architecture decision recorded in [0002-multi-aspect-ratio-video-pipeline.md](file:///Users/morrain/Documents/codes/ai-creator-skills/docs/adr/0002-multi-aspect-ratio-video-pipeline.md).
