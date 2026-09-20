# Step 1: 生成脚本与剧本盲审 (Generate Script & Review)

## 详细规程与算法逻辑

1. **输入解析与短路模式识别**：
   - 解析命令行参数 `/讲解视频 [文章路径或主题]`。
   - 若传入已有主题目录或文章路径（如 `./<article-slug>/<article-slug>.md`），进入**模式 1 (文章转视频)**。
   - 若传入纯主题字符串（如 `Vue 3.5 响应式原理`），进入**模式 2 (独立主题创作)**。
   - **低密度视觉排版规程**：在 `BRIEF.md` 中不填写 `style_preset` 字段。视频排版严格遵循低密度呼吸感规程（70%+ 留白空间，一屏仅表达 1 个核心结论，单切片活跃元素 $\le 5$）。

2. **调度原子技能 `video-script-writer` 提炼 4 轨剧本**：
   - 调度 `video-script-writer`（传入模式与输入文本），生成包含 `metadata.visual_theme` 全局视觉主题代币、`time_code`、`voiceover`、`visual_prompt & ip_action` 及 `on_screen_elements` 4 轨结构的 `video_script.json` 草案。
   - 在撰写各单元 `voiceover` 时，必须融入原文过渡词句，确保单元间逻辑紧密挂钩；**必须根据上下文语义执行多音字按需精准识别**，遵循高频词组免注音避让原则，仅为存在发音歧义的单字标注 `{原字|带声调拼音}` 格式（**绝对禁止使用同音字替代**，**严禁对高频固定词组过度注音**）；在设计 `visual_prompt` 与 `ip_action` 时，**必须根据内容推演具象场景演进与高级动效，严禁以文字卡片平移/浮动作为主画面动效**。

3. **SubAgent 剧本盲审与前置自检闭环 (Pre-Flight Self-Audit & Blind Review)**：
   - **前置自检门控 (Pre-Flight Self-Check)**：在唤起 `blind-reviewer` SubAgent 之前，主 Agent 必须先进行一次剧本硬性指标自检（对照核验：1. 多音字 `{原字|带声调拼音}` 按需标记与高频词组免注音避让；2. 口播单句语义闭环与严禁谓语/宾语悬空；3. 优先 5-12s 短单元；4. `title_card` 极简克制；5. 尾部 5s 独立 Outro 单元）。自检无误后再唤起 `blind-reviewer`，确保盲审一次性 `[PASS]`。
   - 检查项目根目录是否存在自进化规则 `./learnings/video_script.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/video-script-writer/references/script_reviewer_standards.md` 与 `learnings_file: ./learnings/video_script.md`）；若不存在，启动 `blind-reviewer`（仅传入 `default_standards`）。
   - 校验语速节奏（4-5字/秒）、短句呼吸感、单元拆分粒度与动画充分性（优先 5-12s 短单元，动作密集处切细）、IP Mascot 动作定位、单元间口播承上启下过渡词句与因果推理链完整性、口播单句语义闭环、多音字按需带声调拼音标记完整性、全局视觉主题 `visual_theme` 代币完整性、画面高级感动效设计与拒绝文字卡片平移硬卡点、`title_card` 极简克制门控及尾部 5s 点赞关注 Outro 单元契约。若结论为 `[REJECT]`，针对性修正直至 `[PASS]`。

4. **剧本拆分方案输出与人工确认卡点 (Human Approval Gate - 强制停顿确认)**：
   - **⚠️ 暂不落盘文件**：盲审 `[PASS]` 后，Agent **严禁直接写入 `video_script.json`**，必须先在对话中将剧本方案结构化呈报给人类主编审阅。
   - **方案呈报格式要求**：呈报内容必须包含以下 5 大核心要素：
     1) 📌 **单元拆分总数、逻辑递进与承上启下衔接**：明确全片拆分为多少个 `unit_XX`，各单元对应的文章章节与知识脉络，并显式标注单元间的承上启下过渡逻辑；
     2) ⏱️ **单元预估时长**：逐单元标注预计口播时长（`duration_seconds`）；
     3) 🎙️ **逐字口播台词**：逐单元输出包含自然过渡句与完整主谓宾/事实闭环的 `voiceover` 完整解说文案；
     4) 🎨 **画面视觉与高级动效/IP 动作设计**：逐单元输出 `visual_prompt` 具象物理场景演进与 `ip_action` 角色物理交互动作；
     5) 🔤 **上屏元素与花字**：标注包含的 `on_screen_elements`。
   - **⚠️ 尾部 5s 独立单元强制规程**：剧本结尾 **必须单独划分为一个独立的视频单元**（即最后一个 `unit_N`，`duration_seconds: 5s`），专门用于互动引导（如 "深度完整拆解，留言或者私信获取吧。如果对你有启发，记得点赞关注，我们下期见！"）。
   - **交互修改与落盘门控 (Human Feedback Loop & File Save Mandate)**：
     - 向主编发问提示：“*以上为视频剧本拆分与分镜设计草案，请主编审阅并提出修改意见。确认通过后我将为您生成 `video_script.json` 并进入后续语音生成与视频渲染流程。*”
     - 若主编提出修改意见，Agent 必须针对性修改剧本方案并重新呈报；
     - **只有当主编回复“确认”、“通过”或“同意”后**，Agent 方可将最终定稿落盘至 `./<article-slug>/assets/video/video_script.json`。
