---
name: voiceover-generator
description: TTS 配音生成与字幕时间轴提炼技能。当需要基于视频剧本生成语音配音文件（.mp3）及带有时间戳的字幕文件（.srt/.ass/timestamps.json）时调用。
---

# Voiceover Generator Skill (极速配音与字幕时间轴生成技能)

本技能为 **纯粹无状态的原子配音技能**。指导 Agent 或系统读取输入的 4 轨讲解剧本（`video_script.json`），自动生成高音质口播 `.mp3` 音频文件，并提取对齐的 `.srt` 字幕文件与 `timestamps.json` 音画时间轴数据。

---

## 核心设计原则 (Core Principles)

1. **单点输入与无状态生成 (Stateless Voice Output)**：
   - 接收 `video_script.json` 或口播文案，产出配音 `.mp3` 与字幕时间轴。
   - 零项目路径强依赖，纯粹处理音频与字幕提炼。
2. **默认免 Key 高音质引擎 (Edge-TTS)**：
   - 默认使用微软 Edge-TTS 引擎（音色：`zh-CN-YunxiNeural` 磁性知识解说 / `zh-CN-XiaoxiaoNeural` 亲和女声），零成本免配置 API Key。
3. **精准音画时间轴提取 (Audio-Visual Timeline Extraction)**：
   - 输出完整的 `timestamps.json`，精准标记每个视频单元（`unit_id`）的 `start_seconds`、`end_seconds` 与 `duration_seconds`，作为后续 HyperFrames 渲染排版的音画基准。
4. **多格式字幕导出 (Multi-Format Subtitles)**：
   - 同时导出标准播放器专用的 `.srt` 字幕文件，以及代码排版专用的 JSON 文本节点数据。
5. **商业 API 扩展与测试回退兜底 (Robust Pluggable Architecture)**：
   - 架构上预留 `openai` / `minimax` / `elevenlabs` 商业 API 扩展点。
   - 具备本地离线 Mock 时间轴计算与音频兜底机制，确保无网或无第三方依赖下 100% 可测不 Crash。

---

## 关联参考规范

在执行配音生成时，主动读取以下参考规范：
- [`references/tts_providers.md`](references/tts_providers.md)：TTS 供应商与音色参数配置指南。
- [`references/voiceover_reviewer_standards.md`](references/voiceover_reviewer_standards.md)：配音质量与字幕时间戳盲审质检标准。

---

## CLI 调用命令

技能内置 CLI 脚本 `scripts/generate_voiceover.py`：

```bash
python3 skills/voiceover-generator/scripts/generate_voiceover.py \
  --script ./path/to/video_script.json \
  --output-dir ./path/to/output_dir/ \
  --voice zh-CN-YunxiNeural
```

### 交付产物

- `./<output_dir>/unit_01.mp3`, `./<output_dir>/unit_02.mp3` ...（各视频单元独立配音音频）
- `./<output_dir>/full_voiceover.mp3`（全量口播配音音频）
- `./<output_dir>/subtitles.srt`（播放器标准 SRT 字幕）
- `./<output_dir>/timestamps.json`（HyperFrames 渲染音画时间轴）
