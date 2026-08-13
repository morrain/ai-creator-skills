# 1. HyperFrames Official Skill Synergy & FFmpeg Video Pipeline Architecture

Date: 2026-08-12

## Status

Accepted

## Context

Originally, the explainer video pipeline used a monolithic Remotion template to render the entire video in a single Headless Chrome instance. For long videos (over 3 minutes), this approach suffered from severe performance degradation, memory spikes, frame drops, and browser crashes.

Furthermore, static local templates and rigid GSAP macro libraries crippled AI visual creativity, preventing dynamic frame-by-frame HTML/SVG design.

HyperFrames officially ships a suite of 19 Agent Skills (`heygen-com/hyperframes`), including `/faceless-explainer` (for concept/explainer videos) and `/hyperframes-cli` (for checks, preview, single and batch rendering).

## Decision

We decide to refactor the video generation pipeline to leverage HyperFrames official skills alongside our local content engineering skills with a strict **Two-Level Separation of Concerns**:

1. **Two-Level Separation of Concerns**:
   - **Outer Business Video Units**: Our business workflow (`video.md`) splits the script into $N$ independent **Video Units** (`unit_01`, `unit_02`, ...). Each unit is assigned an isolated workspace `./assets/video/unit_XX/`.
   - **Inner HyperFrames Compositions**: For each Video Unit, HyperFrames master entrypoint (`/hyperframes`) is invoked to inspect `BRIEF.md` and route autonomously to the appropriate internal workflow (e.g. `/faceless-explainer`), performing its own internal frame splitting (`compositions/frames/NN-*.html`), GSAP coding, and validation.
2. **Removal of Redundant Local Renderers & Generators**:
   - Deprecate and remove local `skills/hyperframes-renderer` and `skills/video-scene-configurator`. All scene HTML generation, animation coding, and unit rendering are 100% delegated to HyperFrames official skills (via `/hyperframes` entrypoint & `/hyperframes-cli`).
3. **HyperFrames Native `BRIEF.md` Contract Handoff (Stage 2)**:
   - `video-storyboard-designer` outputs a native, compliant HyperFrames `BRIEF.md` into each `./assets/video/unit_XX/` workspace, specifying target duration (`length: X.Xs`), core message, and 3-act motion chain (Hook ➔ Core Action ➔ Delivery).
   - Each unit workspace contains `./assets/video/unit_XX/public/mascot.svg` adhering to vector node contracts (`#mascot-head`, `#mascot-arm-left`, etc.).
4. **SubAgent Context Isolation & Sequential Human Review Gate (Stage 3)**:
   - Process video units sequentially: for each Video Unit `unit_XX`, spawn an isolated SubAgent via `invoke_subagent` to enter `./assets/video/unit_XX/` and invoke HyperFrames master entrypoint (`/hyperframes`), completely preventing cross-unit context and token pollution.
   - Upon SubAgent completion, present the rendered MP4 preview. Explicitly block and wait for human confirmation (`[通过]`) for `unit_XX` before spawning the SubAgent for `unit_XX+1`. If non-compliant, modify `unit_XX/BRIEF.md` and re-dispatch the SubAgent to regenerate.
5. **Zero-Reencode Concat & Audio Ducking (Stage 4)**:
   - All unit reviews passed, `video-renderer` traverses each `./assets/video/unit_XX/` directory to gather HyperFrames generated video files, executes FFmpeg fast, lossless stream concatenation (`-c:v copy`), and applies `sidechaincompress` for voiceover/BGM audio ducking into the final `video.mp4`.

## Consequences

- **Positive**:
  - Clear architectural separation between business workflow video units and inner HyperFrames HTML compositions.
  - Eliminates redundant local rendering and template code (`hyperframes-renderer` and `video-scene-configurator` deleted).
  - 100% compliance with HyperFrames native project contract (`BRIEF.md`).
  - Zero browser memory leaks across long videos due to isolated per-unit rendering.
  - Fast, lossless final video concatenation with professional audio ducking.
- **Negative**:
  - Requires `video-storyboard-designer` to produce accurate target duration timestamps matching outer TTS audio segments.
