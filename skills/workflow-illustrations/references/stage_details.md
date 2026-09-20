# 🎨 正文插图业务编排 - 阶段规程与逻辑细节

## 核心原则

1. **配置文件先行与按需延时生图 (Strict Lazy Generation)**：默认仅生成 `assets/illustration_N.md`，不自动生图。
2. **IP 形象前置短路路由 (Short-Circuit IP Mascot Routing)**：
   检查顺序：`./<article-slug>/character_ip.md` ➔ `./character_ip.md` ➔ `skills/illustration-designer/references/character_ip.md`。命中即止。
3. **磁盘文件最高事实源**：强制重新读取磁盘上的正文源文件 `./<article-slug>/<article-slug>.md`。
4. **代码块图表强制插画化**：凡是用 Markdown 代码块（```mermaid、```ascii、```text 等）描述的流程图/架构图，必须设计为独立认知隐喻插画，用于排版时替换代码块。

---

## 阶段一：正文消化、配置生成与盲审

1. 读取 target `<article-slug>.md`，确认 `assets/` 存在。
2. 按短路规则装载 1 份 IP 描述文件 `character_ip.md`。
3. 提取 4-8 个认知锚点（强制包含所有代码块图表）。
4. 调度原子技能 `illustration-designer` 生成构图与双语 Prompt，存盘 `assets/illustration_N.md`。
5. 唤起 `blind-reviewer` SubAgent（读取 `./learnings/illustrations.md` 若存在），审查通过后呈报列表与可点击链接。

---

## 阶段二：按需延时生图 (Lazy Generation Execution)

- 用户回复“开始生图/生成图片”时触发：
1. 遍历 `assets/illustration_1.md ~ N.md` 提取 `🟢 英文生图版 Prompt`。
2. 调用 `generate_image` 工具渲染 16:9 图片保存至 `./<article-slug>/images/illustration_N.png`。
