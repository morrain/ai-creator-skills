# Step 4: 逐单元渲染 9:16 竖屏视频片段（及可选 16:9 宽屏片段）

## 详细渲染规程与 SubAgent 调度原则

1. **⚠️ Step 4 核心调度原则 (SubAgent Batch Dispatch Mandate)**：
   - **🔒 主 Agent 工具排他锁 (Main Agent Tool Lock Mandate)**：在 Step 4 渲染阶段，**主 Agent 自身的唯一许可工具动作是调用 `invoke_subagent`**！**绝对禁止主 Agent 亲自调用 `write_to_file`、`replace_file_content` 或 `multi_replace_file_content` 撰写、创建或编辑 `unit_XX/index.html` 文件**！主 Agent 必须严格扮演“调度指挥官”的角色，把所有 HTML 代码编写、GSAP 动画挂载与 MP4 渲染导出任务，封包移交给 `invoke_subagent` 唤起的 SubAgent 独立进程执行。
   - **首单元独立渲染与确认后意见分析继承 (Unit 01 Review & Post-Approval Inheritance Mandate)**：
     - **第一个单元 `unit_01` 必须单独渲染并率先提交人工审核**（Batch 0：仅包含 `unit_01`），在对话框呈报视频 MP4 超链接路径 `[unit_01.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/unit_01/unit_01.mp4)` 给人类主编。
     - **极速修改迭代**：若主编对 `unit_01` 提出修改意见，Agent 仅对 `unit_01` 进驻修改并重新呈报，直至主编满意。
     - **确认通过后的通用规则提炼**：**只有当 `unit_01` 最终获得主编显式“确认/通过”后，主 Agent 才可以集中分析此前针对 `unit_01` 提出的全部修改意见与定稿特征**。主 Agent 将其中适用于全片的通用规则（如调整全局花字字号、背景高光强度、IP Mascot 默认缩放/位置、动画平滑度或特定主题色）提炼汇总为 `[inherited_style_rules]` 契约，传递并应用到后续所有单元。
   - **后续单元免打扰批量连续渲染 (Uninterrupted Batch Rendering for Unit 02..N)**：
     - 主编确认 `unit_01` 并输出通用风格规则后，对于 `unit_02` 至 `unit_N`，主 Agent 将其划分为每 3 ~ 4 个单元为一个 Batch (如 Batch 1: `unit_02` ~ `unit_05`, Batch 2: `unit_06` ~ `unit_09`)。
     - **后续 Batch 渲染过程中绝对不进行人工停顿审核**！主 Agent 连续自动唤起 SubAgent，每个 Batch 渲染成功后直接自动开启下一 Batch，直至 `unit_N` 全部完成，最大化提升效率并封堵 Token 膨胀。
   - **⚠️ 全量单元完成统一人工终审卡点 (Final Full-Video Human Gate)**：
     - 当全量单元（`unit_01` 至 `unit_N`）渲染导出全部完成后，主 Agent **必须强制停顿**，在对话框结构化呈报全量单元视频切片 MP4 超链接路径 `[unit_XX.mp4](file://<workspace-abs-path>/<article-slug>/assets/video/unit_XX/unit_XX.mp4)`，等待人类主编进行全片第二次（最终）审核。主编确认“确认”、“通过”或“同意”后，方可切入 Step 5 合成成品视频。若主编对特定单元提出修改意见，仅针对该单元重新渲染呈报。
   - **极简 SubAgent 交付协议 (Compact Tool Output Protocol)**：SubAgent 完成渲染后，**严禁将详细的代码、抓帧日志或排查过程返回给主 Agent**，只允许返回最简状态标记与产物路径，彻底封堵主 Agent 侧的对话历史膨胀。
   - **强制 SubAgent 写入权限 (SubAgent TypeName Mandate)**：唤起 SubAgent 时**必须显式设置 `TypeName: "self"`**，确保具备文件写入与代码编辑权限。
   - **严禁编写批量 Shell 脚本**：绝对禁止 Agent 编写替代渲染的 Python 脚本或在主进程中直接批量 Shell 渲染，必须逐批次唤起 SubAgent 执行。

2. **批次渲染与 SubAgent 提示词模板**：
   - 调用 `invoke_subagent`（**必须设置 `TypeName: "self"`**），传入超紧凑提示词模板：
     ```text
     请处理批次单元目录：./assets/video/unit_XX 至 ./assets/video/unit_YY。
     【继承首单元通用样式规则】: [inherited_style_rules]

     针对批次内的每一个单元：
     1. 进驻单元目录，读取 BRIEF.md 及 HyperFrames 主控技能（.agents/skills/hyperframes/SKILL.md），并遵守 [inherited_style_rules]。
     2. 严格按 BRIEF.md 契约完成 index.html 代码编写。
     3. ⚠️ **静态原点代码审查**：渲染前核验 index.html，确认所有 SVG 旋转/缩放/倾斜动画构件均**强制使用 GSAP svgOrigin: "X Y" 锁死 viewBox 绝对轴心（绝对禁止使用 CSS transformOrigin，避免包围盒偏移导致脱臼甩尾）**，且禁止 CSS 与 GSAP 同时控制同一构件导致闪烁争用。
     4. 运行渲染命令：
        npx hyperframes render "./assets/video/unit_XX" --output="./assets/video/unit_XX/unit_XX.mp4" --resolution portrait
     5. ⚠️ **动态撕裂与脱离自检**：使用 ffmpeg 在 0.5s、mid、end 抽取 3 张自检截图存入 ./assets/video/unit_XX/frames/ 目录，执行视效硬检（核验无小字、无异常遮挡、原点无甩飞、阀门/指针等构件无脱离底座现象，以及 IP 手臂节点无闪烁跳变与撕裂）。
     6. 若需生成 16:9 宽屏版 (仅在用户显式指令时)，先将 9:16 产物与契约备份存盘（unit_XX.mp4 -> unit_XX_9x16.mp4、BRIEF.md -> BRIEF_9x16.md、index.html -> index_9x16.html），再将 BRIEF.md Frontmatter aspect 改为 1920x1080 并重新渲染导出 unit_XX_16x9.mp4。

     【极简交付契约】全部单元完成后，请严格仅回复以下最简格式（严禁包含代码或长日志）：
     `[BATCH SUCCESS] Batch unit_XX..unit_YY 制作完成。产物路径: ./assets/video/unit_XX/unit_XX.mp4 等。自检结论: 均通过。`
     ```
