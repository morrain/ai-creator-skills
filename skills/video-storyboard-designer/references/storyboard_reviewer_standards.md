# Storyboard & Unit Designer Reviewer Standards (视频单元与分镜动作链盲审标准)

本标准供 SubAgent 对 `video-storyboard-designer` 生成的视频单元配置文件（`unit_XX/BRIEF.md`）进行自动化质检。

---

## 1. 动态动作链连贯性 (Motion Chain Continuity)

- 必须包含完整的 3 幕动作演化描述（`Act 1: 引出问题` -> `Act 2: 核心动作` -> `Act 3: 交付结果`）。
- Act 2 的核心动作必须优先继承并延伸原正文插图文件（`illustration_*.md`）中确立的物理隐喻。
- IP Mascot 必须是动作的执行者，严禁沦为背景贴纸或无意义装饰。
- **二次分镜与元素清单硬卡点**: `BRIEF.md` 的 `## Intent` 正文必须明确包含全量画面元素清单（Scene Element Inventory）与带时间戳的镜头切片划分（Sub-shot Timeline Breakdown），特别是对 >20s 的长单元，严禁缺少基于口播文案的二次分镜切片！

---

## 2. 视觉 DNA 与生图 Prompt 规范 (Visual DNA & Prompt Gates)

- **构图与背景**: 强制 16:9 横版构图，通透干净背景（低密度呼吸感空间）。
- **原生中文批注**: 英文 Prompt 中的文本批注须强制保留在引号内部的原生中文（如 `'数据流'`、`'56% OFF'`）。
- **图片与视频参数**: 英文 Prompt 末尾须附加 `--ar 16:9 --v 6.0` 或 i2v 生成控制参数。

---

## 3. 低密度限制与视觉规范质检 (Low-Density & Visual Standards Gates)

质检通过判定依据（任一条不满足即打回）：

- [ ] **无 style_preset**：YAML Frontmatter 中不含 `style_preset` 字段。
- [ ] **`## Customizations` 存在**：板块中含低密度规程声明（One Statement Per Frame、Cap Elements ≤ 5、Suppress Chrome、No Side Panels）。
- [ ] **`## Intent` 按切片分组**：每个切片的活跃构件列表（含 `#mascot`）**≤ 5 个**；超出直接打回。
- [ ] **分时显隐矩阵**：`## Intent` 明确标注各切片的 `opacity:0` 淡出与 `opacity:1` 淡入卡点；无退场动画说明的直接打回。
- [ ] **无侧边栏/多框堆叠**：画面内无 `side-info-card` 或多重框中框；存在即打回。
- [ ] **字号下限**：`## Notes` 含字号下限声明（唱词字幕 ≥ 44px、主标题 ≥ 64px、正文/标签 ≥ 32px、数据大字 ≥ 56px）；缺失即打回。
- [ ] **SVG 3层物理骨架代码硬卡质检**：`## Intent` 中必须直接包含 Raw `<svg>` 3 层 XML 代码片段（Layer 1 基底 + Layer 2 具象特征纹理 `<path>` 如田垄/刻度/电路 + Layer 3 微观细节/螺栓/指示灯/高光切线或可选标示）；物理构件必须拆分为独立 `<g id="...">` 组，严禁打包在单一死板宏组内；图样自解释的实体严禁强行加字；若仅包含高层自然语言描述（如“带有田垄纹理 <path>”），或仅用死板裸方块 `<rect>` + `<text>` / `<div class="card">` 充当物理实体的，直接判定 `[REJECT]` 打回。
- [ ] **IP Mascot 全局最高 Z-Index 置顶质检**：`## Notes` 显式声明 IP Mascot 容器在 HTML 堆叠上下文中处于全局最高层级（`#main-stage` CSS `z-index: 100; pointer-events: none;`，高于浮动卡片 `z-index: 20`），且在 SVG 内部位于末位节点，确保 IP Mascot 在全屏任意位置均为绝对最顶层，且关节旋转使用 GSAP `svgOrigin: "X Y"`（绝对禁止 CSS transformOrigin）。
- [ ] **旋转与摆动构件支点防错位质检**：`## Notes` 显式包含 SVG 旋转与摆动构件支点防错位规程；对仪表指针、天平横梁、阀门齿轮等旋转元素，必须声明统一使用 GSAP `svgOrigin: "cx cy"` 锁定 viewBox 绝对销轴/针座坐标，且天平结构须明确 3 层 DOM 解耦与托盘水平防倾斜补偿约束，违反直接判定 `[REJECT]` 打回。
- [ ] **IP Mascot 走动归位与空白待命注视质检**：`## Intent` 动作切片中必须标注包含动作任务完成后的【空白归位坐标】与 `[Action Recipe: EXECUTE_THEN_RETREAT]` 指令，且 `## Notes` 中写入 IP 走动平移回退与空白待命注视规程（禁止动作完成后长期滞留在构件重叠区）。
- [ ] **9:16 小红书/抖音平台双向 (顶底) UI 避让质检**：`## Notes` 显式写入 9:16 竖屏顶部 Y: 0-200px (至少 200px+) 顶部 UI 避让规程（标题从 Y: 200px 开始）及 底部 Y: 1600px-1920px (至少 320px+) 底部 UI 避让规程，且唱词字幕盒子设在 bottom: 320px 处（绝对禁止文字或物理构件侵入顶部 200px 或底部 320px 平台 UI 遮挡区）。
- [ ] **SVG 文本字体与顶部防裁切质检**：`## Notes` 显式包含 SVG 文本 `font-family` 继承声明与顶部安全距声明（16:9 标题组 `translate.y ≥ 160px`、9:16 标题组 `translate.y ≥ 240px`，第一行 `<text>` 显式指定 `y ≥ 50` 或 `dominant-baseline="hanging"`，禁止向上 `y: -25` 推顶动画），防止字顶向上溢出顶端边缘被截断。
- [ ] **浅色画布标题防突兀黑框质检**：当 Frontmatter 中 `theme.canvas_bg` 为浅色/淡渐变时，`## Intent` 中的 `<g id="title-group">` 绝对禁止包含 `<rect fill="#0f172a">` 或深色矩形黑框；必须采用深色文字无框展示，违反直接判定 `[REJECT]` 打回。
- [ ] **字幕彻底无背景框质检**：`#subtitles` 唱词字幕容器 CSS 必须强制为 `background: transparent; border: none;`，绝对禁止包含任何深/浅背景矩形框或底板；违反直接判定 `[REJECT]` 打回。

---

## 4. 首帧曝光与封面防白硬卡点 (First Frame Exposure Gate)

- 📸 **第 0 帧非空白**: `BRIEF.md` 的 `## Notes` 正文中必须显式写入 `First Frame Exposure & Anti-Blank Cover` 规程。
- 🎬 **`gsap.set` 初始态强制渲染**: 要求动画在 `t=0.0s` 时刻必须通过 `gsap.set` 保持主标题文字、背景卡片容器及 IP Mascot 姿势 `opacity: 1` 可见，禁止全白淡入导致小红书/视频号自动抽取封面一片空白！

---

## 5. 尾部 5s 点赞关注引导硬卡点 (Outro CTA Gate)

- ❤️ **尾部单元 CTA 契约**: 最终单元的 `BRIEF.md` 必须明确包含 5s 点赞关注引导分镜，显式绑定 `[Action Recipe: LIKE_AND_SUBSCRIBE]`。
- 🌟 **IP Mascot 互动表现**: 要求 IP Mascot 做欢快跳跃与举手向观众展示 `👍 点赞`、`⭐ 收藏`、`🔔 关注` 三连徽章。未包含尾部 Outro 单元契约者质检打回！

---

## 6. 渲染后抓帧视效 3 项自检标准 (Post-Render Keyframe Visual Inspection)

渲染完成 MP4 后，必须通过 `ffmpeg` 自动抽取首帧 (`t=0.5s`)、中段 (`t=mid`) 与尾帧 (`t=end`) 关键帧截图，执行 3 项硬核视效质检：

1. 🔍 **清晰度与字号门控 (No Illegible Small Text)**：
   - 检查画面内所有文字与标签，绝不能出现 `<30px` 的模糊看不清文字。
   - 严格卡点字号：正文/标签 $\ge 32px$、主标题 $\ge 64px$、数据大字 $\ge 56px$、唱词字幕 $\ge 44px$。
2. 🙈 **图层避让与遮挡门控 (No Abnormal Occlusion & UI Intrusion)**：
   - 检查 IP Mascot 动作路径，必须全局置顶，禁止被场景构件、数据卡片或标题栏遮挡。
   - 检查顶部标题与唱词字幕，绝对禁止侵入 9:16 顶部 Y: 0-200px 或底部 Y: 1600-1920px (bottom: 320px) 平台 UI 避让区域。
3. 🎯 **旋转原点防甩飞门控 (Pivot & Origin Stability)**：
   - 检查仪表指针、天平横梁、手轮齿轮等旋转元素在 keyframe 中的旋转轨迹，必须精准围绕 `svgOrigin` 销轴/针座旋转，严禁脱离原点甩飞或天平托盘倾斜。
