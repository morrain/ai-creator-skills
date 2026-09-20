# 📝 文章创作业务编排 - 阶段规程与逻辑细节

## 阶段一：前置检索、大纲拟定、SubAgent 盲审、落盘归档与人工卡点

1. **联网事实检索与输入解析**：
   - 解析输入的 `title` / `summary` 或关键词。
   - **显式调用 `search_web` 工具**对主题进行多角度实时检索，收集最新事实。

2. **调度原子技能 `article-writer` 智能识别文风并拟定大纲**：
   - 调度原子技能 `article-writer`（模式 `mode: outline`），基于检索到的事实与主题属性**自适应识别最佳文风**（干货指南/科技深度评论/社会观察/科普解说/故事叙事），生成 3 个爆款备选 H1 标题及带有 `【撰写指令】` 的大纲草案。

3. **SubAgent 大纲盲审闭环**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/article_outline.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（传入 `default_standards: skills/article-writer/references/reviewer_standards.md` 与 `learnings_file: ./learnings/article_outline.md`）；若不存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`（仅传入 `default_standards`）。
   - 若结论为 `[REJECT]`，针对性修正大纲草案直至 `[PASS]`（上限 8 次）。

4. **创建主题工作区与强制落盘归档**：
   - 大纲 `[PASS]` 后，在根目录下新建 `./<article-slug>/` 目录。
   - **前置归档**：将盲审通过的大纲全量原文存盘为固定的 `./<article-slug>/outline.md`。

5. **全量呈报原文与人工 Gate 卡点**：
   - **100% 完整呈报** `outline.md` 原文（附链接 [`./<article-slug>/outline.md`](./<article-slug>/outline.md)），禁止截断。
   - **暂停并等待与统一人工确认提示**：
     > 💡 **主编审阅与自进化提示**：
     > 1. 大纲满意请回复 **`[通过]`** 或 **`[继续]`**，系统将自动开始写作完整正文。
     > 2. 如对大纲进行了人工修饰或提供了调整批注，请在对话框回复 **`/workflow-learn`**，系统将自动提炼您的大纲偏好规则并沉淀落盘，让后续大纲盲审标准自动进化！

---

## 阶段二：定稿读取、正文展开、SubAgent 盲审与正文人工卡点

1. **强制重新读取大纲源文件 (Disk Pre-Read Gate)**：
   - 用户批准大纲后，Agent **必须首先显式调用 `view_file` 重新读取磁盘上的 `./<article-slug>/outline.md` 文件**（以磁盘最新文件内容为唯一事实源，绝对禁止复用 Memory 里的旧大纲缓存）。

2. **调度原子技能 `article-writer` 展开正文**：
   - 调度 `article-writer`（模式 `mode: full_article`），将 `【撰写指令】` 转化为行文推导与爆款金句，应用呼吸感排版（单段 2-4 行）与富 Markdown 组件。

3. **SubAgent 正文盲审闭环**：
   - 检查项目根目录是否存在项目进化规则 `./learnings/article_content.md`。若存在，显式调用 `invoke_subagent` 启动 `blind-reviewer`；若不存在，启动 `blind-reviewer`。
   - 若打回，修正草稿直至 `[PASS]`（上限 8 次）。

4. **纯净 Markdown 落盘交付**：
   - 中英文排版自动加空格处理，存盘至 `./<article-slug>/<article-slug>.md`。

5. **呈报成果与人工 Gate 卡点 2**：
   - 呈报正文完成信息及本地查看链接（[`./<article-slug>/<article-slug>.md`](./<article-slug>/<article-slug>.md)）。
   - 提示回复 `[通过]` 或 `[设计封面]`，也可回复 `/workflow-learn` 沉淀规则。

---

## 阶段三：定稿正文读取、封面设计与图片渲染交付

1. **强制重新读取正文源文件 (Disk Pre-Read Gate)**：
   - Agent **必须首先显式调用 `view_file` 重新读取磁盘上的 `./<article-slug>/<article-slug>.md` 文件**。

2. **自动硬锁调度原子技能 `cover-designer` 提炼封面方案 (`assets/cover.md`)**：
   - **强制技能绑定**：调度原子技能 `name: cover-designer`。一字不差使用正文定稿 H1 标题，落盘至 `./<article-slug>/assets/cover.md`。

3. **呈报设计方案与按需生图卡点提示 (Image Generation Gate)**：
   - 呈报 `assets/cover.md` 链接并提示用户：回复 `[渲染封面]` 或 `[开始生图]` 时，调用 `generate_image` 工具导出图片至 `./<article-slug>/assets/cover.jpg`。

4. **响应图片渲染指令 (Image Generation Execution)**：
   - 当用户回复 `[渲染封面]` 时，调用 `generate_image` 导出图片，交付完成。
