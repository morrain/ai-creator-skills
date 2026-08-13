# Voiceover Reviewer Standards (配音与字幕盲审质检标准)

本标准供 SubAgent 对 `voiceover-generator` 导出的配音文件与字幕时间戳进行自动质检。

---

## 1. 音频文件合规性 (Audio Quality Gates)

- 必须产出标准 MP3 格式文件 (`unit_*.mp3` 或 `full_voiceover.mp3`)。
- 音频采样率建议 >= 24kHz，比特率 >= 64kbps。
- 音频无戛然而止截断，末尾应保留 0.3 ~ 0.5 秒静音缓冲 (Padding)。

---

## 2. 时间戳与字幕轴覆盖度 (Timestamp Coverage Gates)

- 必须产出标准 `.srt` 字幕文件及结构化 `timestamps.json` 时间戳文件。
- 字幕时间戳的起始点 `start_time` 必须增加 0.0s 初始偏移，终点 `end_time` 必须与音频实际总时长误差 < 0.3 秒。
- 逐句字幕中的 `text` 必须与原剧本 `voiceover` 文本 100% 字符匹配。
