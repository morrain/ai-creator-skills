# Poster Layout Specifications (海报 10 大经典版式与 Prompt 构图模板)

本文档为 `poster-designer` 技能提供 10 大经典手绘海报版式的结构定义、适用场景与双语 Prompt 构图模板。Agent 在进行单张海报设计时，**必须根据输入知识文本的属性（如痛点对比、步骤流水线、硬核数据测评、避坑指南、Q&A 问答等）灵活匹配最佳版式**。所有版式（特别是封底/末页海报及底部 Footer 区域）均支持搭配手绘胶囊/贴纸组件（如 `'💬 留言或私信获取完整拆解'`）引导读者留言或私信获取完整长文。

---

## 1. Hero 破题冲击版 (Hero Focus & Big Title Layout)
- **适用场景**：核心观点强烈、具备反常识爆点或单一重磅概念（**首选用于海报组图的第 1 张首页**）。
- **视觉结构**：
  - 上部（60%）：大字号极具冲击力的标题 + IP Mascot（默认小智）动态破墙/高警示牌动作。
  - 下部（40%）：3 个核心切入点卡片与悬念金句。
- **Prompt 模板 (EN)**：
  > Hand-drawn hero poster, warm off-white cream paper texture (`#FAF6F0`), Morandi color palette, clean black line art, prominent title at top featuring IP mascot robot dynamically bursting through a wall pointing at key text, 3 key takeaway bullet points at the bottom, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 2. 四宫格/六宫格干货版 (4-Grid / 6-Grid Matrix Layout)
- **适用场景**：4-6 个并列核心要点、四大法则、六项基本原则或矩阵评估。
- **视觉结构**：
  - 均分四个或六个卡片象限，每个象限包含莫兰迪胶囊标题、手绘微图标/IP 动作与 2 行精炼文本。
  - 画面中心或底部带暖橙色金句框。
- **Prompt 模板 (EN)**：
  > Hand-drawn 4-grid matrix infographic poster, warm off-white cream paper texture (`#FAF6F0`), Morandi color palette, 4 distinct card quadrants each with a hand-drawn icon and IP mascot robot interacting with data, clean black line art, structured balanced layout, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 3. 左右/上下双轨对比版 (Dual-Track Comparison Layout)
- **适用场景**：新旧方案对比、传统模式痛点 vs AI Agent 模式优势、正误对照、Before & After。
- **视觉结构**：
  - 左栏/上栏（莫兰迪灰/浅红底）：传统痛点、繁琐过程与混乱手绘表现。
  - 右栏/下栏（莫兰迪蓝/浅绿底）：新架构优势、高效自动化链路与 IP Mascot 姿态。
- **Prompt 模板 (EN)**：
  > Side-by-side comparison infographic poster, warm off-white cream paper texture, Morandi color palette, left column representing traditional flawed approach in grey-red tones, right column showing modern AI solution in vibrant Morandi blue-green, IP mascot standing in middle guiding viewer, clean hand-drawn line art, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 4. 纵向链路/管道流程版 (Vertical Flowchart & Pipeline Layout)
- **适用场景**：多阶段解耦流水线、分步操作 Action Items、从输入到输出的完整技术链路。
- **视觉结构**：
  - 纵向 3-4 个卡片步骤，中间用手绘虚线带头箭头的管道连接。
  - IP Mascot 在关键步骤旁进行操作演绎（如手握扳手调试代码、手持放大镜检查节点）。
- **Prompt 模板 (EN)**：
  > Vertical flowchart infographic poster, warm off-white cream paper texture, Morandi color palette, 4 step-by-step process cards connected by dotted hand-drawn arrows, IP mascot robot holding a wrench operating at step 2, clean line art, structured layout, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 5. 中心破局/脑图辐射版 (Radial Mind-Map & Center Hub Layout)
- **适用场景**：单点核心概念展开多维度支撑、系统生态拆解、核心能力全景图。
- **视觉结构**：
  - 中央放一个大胶囊或核心系统节点，IP Mascot 手持光源站在中心。
  - 四周用极简虚线手绘气泡向外辐射出 4-5 个衍生能力切片。
- **Prompt 模板 (EN)**：
  > Radial mind-map infographic poster, warm off-white cream paper texture, Morandi color palette, central core topic capsule with IP mascot holding a lamp, 4 surrounding subtopic cards connected with thin hand-drawn dotted lines, clean sketch style, balanced composition, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 6. 极简金句闭环版 (Golden Quote & Bookmark Ending Layout)
- **适用场景**：章节末尾总结、全文思想沉淀、组图末页唤起收藏转发与留言/私信互动（**首选用于组图的海报 N 封底页**）。
- **视觉结构**：
  - 中央巨大暖金虚线边框卡片，包裹精炼爆款金句。
  - 右下角放置 IP Mascot 举“点赞+收藏”招招牌或比心动作。
  - 底部/右下显式带入手绘提示胶囊/贴纸组件，渲染原生中文文本 `'💬 留言或私信获取完整拆解'` 或 `'想要解锁完整深度拆解？留言或私信 💬'`。
- **Prompt 模板 (EN)**：
  > Minimalist golden quote infographic poster, warm off-white cream paper texture, Morandi color palette, oversized quote card in center with dashed golden border, IP mascot robot standing in bottom-right holding a sign, small hand-drawn capsule sticker at bottom with call-to-action text guiding viewers to comment or message for full article '💬 留言或私信获取完整拆解', clean hand-drawn style, Morandi accents, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 7. 数据/指标面板版 (Metrics & Specification Dashboard Layout)
- **适用场景**：硬核技术测评、性能提升百分比、基准测试参数对比。
- **视觉结构**：
  - 顶部放大字号量化指标手绘数字（如 `10X`、`99.9%`）。
  - 下部用柱状图/进度条手绘组件配合 3 个关键指标分析卡片。
- **Prompt 模板 (EN)**：
  > Metrics and specification dashboard infographic poster, warm off-white cream paper texture, Morandi color palette, large hand-drawn metric numbers '10X' at top, progress bars and 3 parameter cards below, IP mascot robot analyzing a bar chart with a pointer, clean line art, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 8. 避坑拆弹/红黑榜版 (Myth-Busting & Warning Card Layout)
- **适用场景**：常见误区澄清、实战避坑指南、红黑榜（正确做法 vs 踩坑坑点）。
- **视觉结构**：
  - 红色警告边框卡片（`⚠️ 避坑提醒`） + 黑色手绘炸弹/警戒线图标。
  - 绿色推荐边框卡片（`💡 避坑妙招`）。
  - IP Mascot 手持盾牌挡住踩坑点。
- **Prompt 模板 (EN)**：
  > Myth-busting warning card infographic poster, warm off-white cream paper texture, Morandi color palette, top warning card in Morandi red with hazard icon, bottom solution card in Morandi green, IP mascot robot holding a shield deflecting a mistake icon, clean hand-drawn line art, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 9. Q&A 交互问答对话版 (Interactive Q&A Speech Bubble Layout)
- **适用场景**：自问自答解密场景、用户最关心的热点问题解答、拟人化对话体。
- **视觉结构**：
  - 上方手绘问号提问气泡（`Q: 问句文本`）。
  - 下方手绘解答框（`A: 解答核心`），IP Mascot 扮演专家手持话筒解答。
- **Prompt 模板 (EN)**：
  > Interactive Q&A speech bubble infographic poster, warm off-white cream paper texture, Morandi color palette, top large question bubble 'Q:...', bottom detailed answer card 'A:...', IP mascot robot holding a microphone explaining, clean hand-drawn line art, friendly interactive vibe, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.

---

## 10. 时间线/演进史切片版 (Timeline & Paradigm Evolution Layout)
- **适用场景**：技术发展史、范式转移（1.0 模式 -> 2.0 模式 -> Agent 模式）、版本更新历程。
- **视觉结构**：
  - 贯穿全图的蛇形/直线手绘时间轴线，带有 3-4 个时间里程碑打卡节点。
  - IP Mascot 沿着时间线从小长到大或推着轮胎往前走。
- **Prompt 模板 (EN)**：
  > Timeline paradigm evolution infographic poster, warm off-white cream paper texture, Morandi color palette, horizontal winding timeline with 3-4 milestone nodes and dates, IP mascot robot walking along the timeline pushing a gear, clean line art, structured chronological layout, 3:4 aspect ratio, strictly NO fake subtext underneath capsule headers, NO random garbled text/gibberish, NO unintended bullet points, only render explicitly specified text inside single quotes.
