# TTS Provider Architecture (语音配音引擎配置规范)

本规范定义 `voiceover-generator` 技能支持的配音供应商与参数配置。

---

## 1. 默认免 Key 引擎：Edge-TTS (`edge_tts`)

无需任何 API Key，使用微软 Edge 极速神经网语音 API，极具自然听感。

- **供应商标识**: `edge_tts`
- **默认音色 (Voice)**: `zh-CN-YunxiNeural`（云希：知识博主、磁性科技解说）
- **可选音色**:
  - `zh-CN-XiaoxiaoNeural`（晓晓：亲和科普女声）
  - `zh-CN-YunjianNeural`（云健：硬核科技评论男声）
  - `en-US-ChristopherNeural`（英文解说男声）
- **速率/语调控制**:
  - `rate`: `+0%` (标准) 到 `+10%` (快节奏)
  - `pitch`: `+0Hz`

---

## 2. 商业扩展 API 引擎 (Commercial API Providers)

若环境变量中配置了 API Key，系统支持平滑切换至商业高阶音色：

### A. OpenAI TTS (`openai`)
- **环境变量**: `OPENAI_API_KEY`
- **模型**: `tts-1` / `tts-1-hd`
- **音色**: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

### B. MiniMax TTS (`minimax`)
- **环境变量**: `MINIMAX_API_KEY`, `MINIMAX_GROUP_ID`
- **模型**: `speech-01-turbo`

### C. ElevenLabs (`elevenlabs`)
- **环境变量**: `ELEVENLABS_API_KEY`
- **模型**: `eleven_multilingual_v2`
