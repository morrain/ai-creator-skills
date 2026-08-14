# 🎨 HyperFrames 风格预设库与自适应匹配指南 (Style Presets & Adaptive Matching Guide)

本指南为 `video-storyboard-designer` 提供完整的 **HyperFrames 风格预设 (Style Preset)** 库映射与自适应选型规则。在生成视频单元分镜与 `BRIEF.md` 契约时，Agent **严禁机械硬编码单一风格**，必须结合 `video_script.json` 的主题领域、文案基调与目标受众，从本指南中选择最匹配的 `style_preset`，并**确保全片所有视频单元（`unit_01` ~ `unit_N`）统一使用相同的 `style_preset`**！

---

## 1. 核心选择与一致性约束 (Core Selection & Consistency Rules)

0. **显式指定优先原则 (Explicit Override Priority)**：
   - 若用户或调用方在启动指令中**显式指定了 `--style <preset>` 参数**（如 `--style blue-professional` 或 `--style code-editorial`），Agent 必须强制使用该显式指定的 `style_preset`，覆盖自动匹配逻辑。
1. **内容自适应保底 (Content-Driven Matching Fallback)**：
   - 若用户未显式指定 `--style` 参数，则结合 `video_script.json` 的主题领域、文案基调与目标受众自动匹配：
     - 商业/金融/研报/政策解读 ➔ 首选 `blue-professional` 或 `clean-editorial`
     - 技术/编程/代码重构/架构解析 ➔ 首选 `code-editorial` 或 `cartesian`
     - 科普/原理推演/通用无头讲解 ➔ 首选 `minimal` 或 `swiss-graphic`
     - 重磅发布/观点宣告/高张力报道 ➔ 首选 `broadside` 或 `bold-poster`
     - 品牌设计/新粗犷/潮酷宣发 ➔ 首选 `blockframe` 或 `creative-mode`
     - 轻松/儿童/育儿/生活涂鸦 ➔ 首选 `daisy-days`
2. **全片风格绝对统一 (Project-Wide Consistency)**：
   - 选定的 `style_preset` 会作为全片视频项目的“视觉基因（Visual DNA）”。**必须且只能在第 01 单元设计前锁定一次**，全片后续所有单元的 `BRIEF.md` Frontmatter 必须继承该相同的 `style_preset`，严禁同一视频的不同单元风格游离！

---

## 2. 完整风格预设清单 (Complete Style Preset Inventory)

| 预设标识 (`style_preset`) | 视觉特征与流派 | 适用主题与语气 (Pick When) |
| :--- | :--- | :--- |
| `minimal` | 2D 极简手绘线条、黑白高对比、低密度呼吸感、纯极简白底 | **通用科普 / 原理推演 / 无头讲解**：要求低密度、一屏一结论、强调逻辑流程与 IP 动作隐喻。 |
| `blue-professional` | 咨询级克制、宝蓝 `#1E2BFA` 调性、暖沙米色背景、无阴影圆角卡片 | **商业分析 / 金融理财 / 政策研报 / 行业解读**：要求投研级严谨、高智感与极佳的阅读舒适度。 |
| `code-editorial` | 暖米色纸张 + 暖黑深色代码框 + 珊瑚红 `#CC785C` 高亮、EB Garamond 衬线 display + JetBrains Mono 代码 | **技术架构 / 代码重构 / 算法解析 / 开源宣发**：包含大量代码块、终端指令或技术名词的硬核技术视频。 |
| `clean-editorial` | 报刊杂志排版感、经典衬线体与无衬线体混排、高质感社论布局 | **深度文章转化 / 文化人文 / 观点社论**：长文转视频、强调文字质感与严肃思考的主题。 |
| `swiss-graphic` | 瑞士国际主义平面风、严谨网格系统、精准对齐与模块化排版 | **系统架构 / 模块关系 / 流程图解**：需要展示清晰层级结构、对比表格或系统拓扑的主题。 |
| `broadside` | 大字报/宣言海报风、巨大 Barlow 900 无衬线粗体、黑/火橙高饱和对比 | **重磅发布 / 观点宣告 / 警示提醒 / 破坏性创新**：文案语气极强、带有强烈结论性与宣导色彩的主题。 |
| `cartesian` | 笛卡尔坐标网格、石灰色系、极细线条与数理几何圆环 | **数学 / 物理 / 数据科学 / 图论算法**：涉及公式推导、几何模型或精准测量的数据主题。 |
| `blockframe` | 新粗犷主义 (Neobrutalism)、4px 粗黑边框、8px 纯黑硬阴影、彩色卡片 | **产品功能宣发 / 潮流科技 / 营销活动**：要求年轻化、高饱和冲击力、活泼醒目的内容。 |
| `bold-poster` | 倾斜大标题 (-6°..+2°)、复古红黑白高质感报纸风、经典印章与底纹 | **历史回顾 / 重大事件记录 / 品牌故事**：带有复古纪实感、复盘总结或重磅报道的主题。 |
| `biennale-yellow` | 双年展艺术目录风、暖羊皮纸底色 + 靛蓝墨水 + 太阳黄衬底、无圆角 | **艺术设计 / 审美鉴赏 / 文化展览**：追求艺术品味、博物馆目录质感与沉静优雅的主题。 |
| `cobalt-grid` | 钴蓝孔版印刷 (Risograph) 质感、背景网格线、像素颗粒感 | **创意极客 / 独立开发 / 艺术科技**：喜欢复古印刷质感与独立极客调性的主题。 |
| `creative-mode` | 新粗犷社论风、4px 墨水边框与几何框体、硬朗立体感 | **创新产品演示 / 设计系统宣讲**：强调几何结构感与硬朗设计气场的主题。 |
| `daisy-days` | 涂鸦手绘风、活泼软糖配色、圆润 Fredoka 字体、小花/云朵点缀 | **儿童育儿 / 绘本故事 / 轻松生活**：面向亲子、休闲或轻松幽默风格的内容。 |

---

## 3. 在 BRIEF.md 中的标准落盘格式

在选定 `style_preset` 后（例如选定 `blue-professional`），在每个单元的 `BRIEF.md` 中需按以下格式落盘：

```yaml
---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "本单元的核心摘要描述..."
length: 32.0s
aspect: 1920x1080
style_preset: blue-professional
---
```

并在 `## Customizations` 板块补充匹配的视觉样式说明：
```markdown
## Customizations

- Style Aesthetic: blue-professional (Consulting-grade restraint, warm cream ground, saturated cobalt accent, refined editorial cards).
- Low Density Rules: One Statement Per Frame (only 1 key conclusion per screen), Cap Elements <= 3 (max 3 independent cards/elements per scene), Suppress Chrome.
```
