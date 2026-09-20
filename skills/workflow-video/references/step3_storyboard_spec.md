# Step 3: 逐单元设计分镜契约与初始化工程 (Design Storyboard & Unit Workspaces)

## 详细规程与初始化契约

1. **调度原子技能 `video-storyboard-designer` 提炼单元契约**：
   - 扫描正文插图描述（若存在），提取静态物理隐喻。
   - 读取 `video_script.json` 中的 `metadata.visual_theme` 提取全集统一视觉配色代币。
   - 将 `video_script.json` 拆解为 $N$ 个独立视频单元（`unit_01`, `unit_02`, ...），在 `./<article-slug>/assets/video/` 下逐单元建立独立工作区。

2. **逐单元独立运行 HyperFrames 初始化命令 (Per-Unit Sequential Init)**：
   - **主 Agent 必须对每一个 `unit_XX` 依次串行执行**初始化命令（**绝对禁止编写 `setup_units.py` 等 Python 脚本进行批量处理**）：
     ```bash
     HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init "./<article-slug>/assets/video/unit_XX" --non-interactive --example=blank
     ```

3. **前置资源与关键契约注入**：
   - 将本单元所需的前置依赖资产逐个拷贝落盘至 `./<article-slug>/assets/video/unit_XX/public/`：
     - `public/mascot.svg`（矢量 IP 角色资产）
     - `public/audio.mp3`（复制自 `../audio/unit_XX.mp3` 本单元配音切片）
     - `public/timestamps.json`（复制自 `../audio/timestamps.json` 本单元字幕时间戳契约）
   - 写入 `./<article-slug>/assets/video/unit_XX/BRIEF.md`，显式注入口播时长 `length: max(A_i + 0.3s, 4.0s)`（在 Frontmatter 注入 `theme` 代币）、3 幕动态动作链二次分镜切片、低密度限制规程、非 16:9 布局防裁剪规程、**全局视觉主题 Token 继承铁律**、**首帧曝光与封面防白规程 (`t=0.0s` 即刻渲染高对比度封面与 IP 姿态)** 以及尾部单元专属 **`[Action Recipe: LIKE_AND_SUBSCRIBE]` 互动引导规程**。

4. **⚠️ Step 3 绝对禁令与脚手架初始化 (Strict Prohibition Rules)**：
   - **严禁修改 `index.html` 或编写 HTML/GSAP 代码**：Step 3 仅负责契约与脚手架逐单元初始化（生成 `BRIEF.md`、拷贝 `public/` 资产与 `hyperframes init`）。**绝对禁止主 Agent 或本阶段技能在 Step 3 中修改、创建或编辑任何 `index.html` 文件**，严禁编写任何批量初始化脚本或拼接 HTML 代码的脚本！`index.html` 的编写与编辑必须且只能在 Step 4 由独立的 SubAgent 进驻执行。

5. **跨阶段上下文轻量化隔离规程 (Cross-Stage Context Pruning Mandate)**：
   - 完成全部单元脚手架初始化与 `BRIEF.md` 落盘后，**主 Agent 仅保留 `metadata` 视觉代币、`units` 映射表及当前 Batch 状态**，清理 Step 1 阶段解析原始大段文章的中间历史，以最极简状态切入 Step 4 逐单元批次渲染与人工审核。
