# Step 2: 生成语音与锁定时长 (Generate Voiceover & Lock Duration)

## 详细规程

1. **读取剧本定稿**：
   - 读取 `./<article-slug>/assets/video/video_script.json`。

2. **调度原子技能 `voiceover-generator` 生成 TTS 音频与精确时间轴**：
   - 提取 `voiceover` 文案，调用 Edge-TTS (音色 `zh-CN-YunxiNeural`) 导出完整配音音频 `./<article-slug>/assets/video/audio/voiceover.mp3` 与字幕时间轴 `./<article-slug>/assets/video/audio/timestamps.json`（同时在 `metadata` 中透传 `visual_theme` 声明）。
   - 自动切分各个视频单元的音频文件 `./<article-slug>/assets/video/audio/unit_XX.mp3`。
   - 精确计算出各视频单元的**实际口播时长 $A_i$**，为 Step 3 注入 `BRIEF.md` 时长契约做前置准备。
