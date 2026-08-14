# 2. Multi-Aspect Ratio Progressive Video Pipeline Architecture

Date: 2026-08-14

## Status

Accepted

## Context

The video creation workflow previously rendered videos strictly in a fixed 16:9 widescreen format (`1920x1080`). Modern content creators require publishing the same video content across multiple platforms with varying aspect ratios:
- PC / B站 / YouTube (16:9 widescreen, `1920x1080`)
- Mobile / 抖音 / 视频号 / Shorts (9:16 portrait, `1080x1920`)
- 小红书 / Instagram (1:1 square, `1080x1080` / 4:5 vertical, `1080x1350`)

To support multi-aspect rendering without duplicating projects or destroying existing HTML/GSAP compositions, the pipeline requires an architectural convention for per-unit multi-aspect code snapshots, active BRIEF/HTML management, and multi-aspect final concatenation.

## Decision

We decide to extend the video pipeline architecture (`video.md`, `render_final_video.py`) with a **Multi-Aspect Progressive Rendering Protocol**:

1. **Active File + Aspect Snapshot File Management**:
   - `unit_XX/` root always maintains standard `./BRIEF.md` and `./index.html` as the active targets for 100% compatibility with official HyperFrames CLI & agent skills.
   - The **Main Agent** manages active `./BRIEF.md` / `./index.html` file swapping, saves per-aspect source snapshots (`BRIEF_<aspect>.md`, `index_<aspect>.html`), and copies `unit_XX.mp4` to `unit_XX_<aspect>.mp4`.
   - The **SubAgent** remains 100% unchanged in logic and prompt template, simply consuming `./BRIEF.md` and writing `./unit_XX.mp4`.

2. **Per-Unit Interactive Prompt & Stage 3 Multi-Aspect Switch**:
   - In Stage 3 (SubAgent unit rendering), after a unit completes its primary aspect render (e.g., 16:9), the workflow pauses and offers an interactive gate: `[Render 9:16 vertical version for Unit XX now] [Skip to next unit]`.
   - At the end of Stage 3, a batch completion prompt checks if any unit has secondary aspect renders and offers to batch-complete missing secondary aspect renders across all remaining units.

3. **Stage 4 Multi-Aspect Export Strategy (`render_final_video.py`)**:
   - `render_final_video.py` scans `assets/video/` for aspect suffixes (`_16x9.mp4`, `_9x16.mp4`, etc.).
   - It performs fast, lossless `-c copy` concatenation per aspect ratio, producing separate final MP4 artifacts:
     - `./video.mp4` / `./video_16x9.mp4` (Primary widescreen version)
     - `./video_9x16.mp4` (Secondary mobile vertical version)
   - If any unit lacks a specific aspect render, fallback padded/blurred background composition is applied for complete video output.

## Consequences

- **Positive**:
  - 100% backward compatible with HyperFrames official CLI & agent skills (reads standard `BRIEF.md` and `index.html`).
  - Source code for both 16:9 and 9:16 layouts are cleanly preserved without overwriting or code loss.
  - Multi-platform creators can produce widescreen and portrait versions in a single workflow session.
- **Negative**:
  - Requires maintaining multiple HTML/CSS layout snapshots when modifying unit designs.
