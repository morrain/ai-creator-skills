# 🧠 动态物理隐喻与 SVG 矢量生成思维指南 (Generative Physical Metaphor Guide)

在动画讲解视频中，不同主题（金融、AI科技、芯片、操作系统、量子力学、生物医学、经济学）会涉及千变万化的感性/抽象概念。

**绝对禁止**将本文件当作死板硬编码的静态模板库！
`video-storyboard-designer` 必须学会**根据任意输入的领域主题，动态解构抽象概念，通用推导出具象的 SVG 物理结构与 GSAP 物理动作轨迹**。

---

## 1. 全领域动态具象化推演 3 步法 (3-Step Dynamic Metaphor Synthesis)

当拿到任意领域的抽象概念（如 Transformer Self-Attention、操作系统内核调度、逆回购水利模型、光刻机曝光、期权行权）时，按以下 3 步动态推演：

### 第一步：抽象概念 ➔ 基础物理形态解构 (Deconstruct to Physical Primitives)
将任何抽象逻辑拆解为 4 种通用的基础物理形态：
1. **流体/通道态 (Flow & Stream)**：代表资金、数据包、光子、神经信号、血液。
   - **SVG 表达**：`<path stroke-dasharray="...">` (流体管道/轨道/流向)
2. **调控/门闸态 (Control Gate & Valve)**：代表政策开关、CPU 门控、阀门、过滤网、阈值触发器。
   - **SVG 表达**：`<g id="...">` 包含可平移的闸门 `<rect>`, 旋转手轮 `<circle>`, 旋转杠杆 `<line>`
3. **容器/负载态 (Container & Load)**：代表资金池、内存缓冲区、农田实体、芯片晶圆、数据库。
   - **SVG 表达**：`<rect id="..." rx="...">`, 容器罐 `<ellipse>`, 储水槽/容积盒
4. **传导/联动态 (Transmission & Mechanics)**：代表产业链、齿轮传导、链条、传动带、机械臂。
   - **SVG 表达**：啮合齿轮 `<path>`, 皮带 `<path id="belt">`, 机械推杆 `<line>`

### 第二步：动态生成 SVG 矢量骨架 (Generative SVG Code Skeleton)
根据解构出的物理形态，**实时动态编写具象的 2D SVG 结构草案**（包含 `<svg viewBox="...">`, 具名 `<g id="...">`, 可动 `<path id="...">`），并写入 `BRIEF.md` 的 `## Intent`。

### 第三步：绑定 GSAP 具象物理动作 (GSAP Physics Binding)
为每个可动 SVG 节点的 `id` 显式绑定物理动作：
- 位移 (`x`, `y`) ➔ 开闸升降、推杠杆、抽屉推拉、芯片插入
- 旋转 (`rotation`, `transformOrigin`) ➔ 阀门转动、齿轮咬合、指针摆动
- 描边打点 (`strokeDashoffset`) ➔ 数据流灌注、资金喷涌、光速传导
- 形变/缩放 (`scale`, `height`) ➔ 水位涨落、容器充盈、压力膨胀

---

## 2. 全领域动态具象化推演示例 (Universal Domain Examples)

以下展示 `video-storyboard-designer` 如何针对不同主题**动态发散生成** SVG 骨架：

| 输入主题 | 抽象感性描述 | 动态推演出的 SVG 物理结构 | GSAP 物理动作 |
| :--- | :--- | :--- | :--- |
| **金融货币** | "央行开闸向市场注入万亿资金" | 水库水坝 `<rect id="dam">` + 升降水闸 `<rect id="gate">` + 水渠 `<path id="canal">` | `gsap.to("#gate", {y: -80})` 闸门升起，水流喷涌 |
| **AI 大模型** | "Self-Attention 机制动态分配注意力权重" | 多头光束手电筒 `<path class="beam">` + 矩阵透镜 `<polygon id="lens">` | `gsap.to(".beam", {opacity: 1, strokeWidth: 12})` 光束聚焦 |
| **操作系统** | "内核进程调度器分配 CPU 时间片" | 旋转传送带 `<path id="belt">` + 进程滑块 `<rect class="process">` + CPU 槽位 | `gsap.to(".process", {x: 400})` 滑块压入 CPU 槽 |
| **芯片半导体** | "极紫外光刻机在晶圆上蚀刻纳米电路" | 光束发射塔 `<g id="laser">` + 硅晶圆圆盘 `<circle id="wafer">` | `gsap.to("#laser-beam", {strokeDashoffset: 0})` 蚀刻线条 |
| **生物医学** | "抗体精准识别并封堵病毒受体" | 锁钥结构 `<path id="antibody">` + 病毒刺突蛋白质 `<g id="virus">` | `gsap.to("#antibody", {x: 120})` 锁扣契合扣紧 |

---

## 3. 物理实体 3 层矢量精细化指南 (3-Layer Detailed SVG Synthesis)

**绝对禁止**输出“单一死板矩形框 + 文字”作为物理实体！任何抽象实体（农田、水库、芯片、阀门、数据库、车辆）在 SVG 骨架中必须包含以下 **3 层精细化结构**：

1. **Layer 1: 实体基底 (Base Silhouette)**：具备质感充盈色、柔和圆角与边框线条的底座或轮廓。
2. **Layer 2: 具象特征纹理 (Feature Texture & Micro Graphics)**：表达该实体物理特征的具象 SVG 路径（例如农田的平行田垄线与芽苞 `<path>`、水库大坝的石缝与刻度尺、CPU 芯片的引脚与电路纹理、阀门手轮的轮辐线）。
3. **Layer 3: 标示文字 (Label Typography)**：清晰高对比度的名称或数值批注。

### 具象实体 3 层矢量结构范例库（直接复制/适配写入 BRIEF.md）：

```xml
<!-- 🌾 示例 1：实体农田 (包含底座 + 田垄虚线/农作物幼苗 `<path>` 纹理 + 标示) -->
<g id="farmland-left">
  <!-- Layer 1: 底座 -->
  <rect x="80" y="760" width="320" height="160" rx="12" fill="#e2f0d9" stroke="#385723" stroke-width="3"/>
  <!-- Layer 2: 田垄与幼苗纹理 -->
  <path d="M110 800 L370 800 M110 840 L370 840 M110 880 L370 880" stroke="#a9d08e" stroke-width="2" stroke-dasharray="6,4"/>
  <path d="M140 792 Q145 782 150 792 M220 792 Q225 782 230 792 M300 792 Q305 782 310 792" stroke="#385723" stroke-width="2.5" fill="none"/>
  <path d="M180 832 Q185 822 190 832 M260 832 Q265 822 270 832" stroke="#385723" stroke-width="2.5" fill="none"/>
  <!-- Layer 3: 标示 -->
  <text x="240" y="905" text-anchor="middle" font-size="28" fill="#274412" font-weight="bold">实体农田</text>
</g>

<!-- 🏦 示例 2：金融水库大坝 (包含大坝主体 + 石缝纹理/水位刻度尺 `<path>` + 标题) -->
<g id="dam-body">
  <!-- Layer 1: 大坝主体与水面底座 -->
  <rect x="700" y="200" width="520" height="280" rx="8" fill="#d9e1f2" stroke="#2f5597" stroke-width="3"/>
  <!-- Layer 2: 水位刻度尺与坝体石缝纹理 -->
  <line x1="720" y1="220" x2="720" y2="450" stroke="#2f5597" stroke-width="3"/>
  <path d="M720 250 L735 250 M720 300 L735 300 M720 350 L735 350 M720 400 L735 400" stroke="#2f5597" stroke-width="2"/>
  <path d="M750 320 Q850 300 950 320 T1150 320" stroke="#8ea9db" stroke-width="2" fill="none" stroke-dasharray="8,4"/>
  <!-- Layer 3: 标题 -->
  <text x="960" y="255" text-anchor="middle" font-size="38" fill="#1f3864" font-weight="bold">金融水库</text>
</g>

<!-- 🚰 示例 3：央行水闸与阀门 (包含手轮/阀体 + 旋转辐条/管道纹理 `<path>` + 标示) -->
<g id="water-valve-group" transform="translate(540, 1300)">
  <!-- Layer 1: 管道与阀门底座 -->
  <rect x="-60" y="-30" width="120" height="60" rx="8" fill="#e2e8f0" stroke="#475569" stroke-width="4"/>
  <!-- Layer 2: 阀门手轮与辐条纹理 -->
  <circle cx="0" cy="0" r="45" fill="#f8fafc" stroke="#0284c7" stroke-width="6"/>
  <path d="M-35 0 L35 0 M0 -35 L0 35 M-25 -25 L25 25 M-25 25 L25 -25" stroke="#0284c7" stroke-width="4"/>
  <circle cx="0" cy="0" r="12" fill="#0284c7"/>
  <!-- Layer 3: 标示 -->
  <text x="0" y="75" text-anchor="middle" font-size="26" fill="#0f172a" font-weight="bold">央行资金水闸</text>
</g>

<!-- 💻 示例 4：CPU/AI 芯片内核 (包含基板 + 引脚与金线电路纹理 `<path>` + 标示) -->
<g id="chip-core-group" transform="translate(400, 600)">
  <!-- Layer 1: 芯片基板底座 -->
  <rect x="0" y="0" width="280" height="280" rx="16" fill="#0f172a" stroke="#38bdf8" stroke-width="4"/>
  <!-- Layer 2: 引脚与金线电路纹理 -->
  <path d="M 30 0 L 30 -20 M 70 0 L 70 -20 M 110 0 L 110 -20 M 150 0 L 150 -20 M 190 0 L 190 -20 M 230 0 L 230 -20" stroke="#38bdf8" stroke-width="4"/>
  <path d="M 40 40 L 100 40 L 140 80 M 240 40 L 180 40 L 140 80 M 40 240 L 100 240 L 140 200 M 240 240 L 180 240 L 140 200" stroke="#0ea5e9" stroke-width="2.5" stroke-dasharray="5 3" fill="none"/>
  <!-- Layer 3: 标示 -->
  <rect x="80" y="110" width="120" height="60" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <text x="140" y="148" text-anchor="middle" font-size="28" fill="#38bdf8" font-weight="bold">NPU 核心</text>
</g>
```

---

## 4. 铁律卡扣 (Strict Rules)

1. 🚫 **严禁使用死板方块+文字**: 任何实体绝对禁止仅用 `<rect>` + `<text>` 替代。农田必须有田垄/幼苗，水库必须有水面/大坝/刻度，芯片必须有引脚/电路纹理。
2. 🚫 **严禁退化为 Dashboard UI 卡片**: 严禁使用 `<div class="card">` 矩形弹窗框、软件 UI 卡片或 Badge 标签框来代表物理实体。
3. 🚫 **必须提供可动节点 ID**: `BRIEF.md` 的 SVG 代码骨架中，所有需要 GSAP 驱动的构件必须赋予明确的 `id`（如 `#farmland-left`, `#valve-wheel`, `#laser-beam`, `#gate-door`）。
