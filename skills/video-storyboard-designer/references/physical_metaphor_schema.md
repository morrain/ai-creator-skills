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

**绝对禁止**输出“单一死板矩形框 + 文字”作为物理实体！任何抽象实体（农田、水库、芯片、阀门、数据库、车辆、机械臂）在 SVG 骨架中必须包含以下 **3 层精细化结构**：

1. **Layer 1: 实体基底 (Base Silhouette & Container)**：具备质感充盈色、柔和圆角与边框线条的底座、容器壁或外壳轮廓。
2. **Layer 2: 具象特征纹理与结构 (Feature Texture & Core Structure)**：表达该实体物理特征的主体纹理与结构路径（例如农田的平行田垄线与芽苞 `<path>`、水库大坝的石缝与斜面坝体、CPU 芯片的引脚与电路金线、阀门手轮的轮辐线与轴心、水管法兰接口）。
3. **Layer 3: 高阶微观细节 / 功能微构件 / 动态指示器 / 可选标示 (Micro-Details, Functional Accents & Optional Label)**：增强实体物理质感与真实度的微观细节元素，例如：
   - **硬件/机械微观细节**：螺栓/铆钉点位 (`<circle r="2..4">`)、固定卡扣、高光切线/金属拉丝 (`<path opacity="0.4..0.6">`)、立体阴影压边。
   - **功能/状态指示**：LED 状态发光灯 (`<circle fill="#00ff88">`)、刻度指针/仪表盘针 (`<polygon/path id="pointer">`)、状态高亮块、插针触点。
   - **💡 核心设计原则：图形自解释与去文字化 (Self-Explanatory Metaphors Don't Need Text)**：
     - **视觉直观即无需文字**：若实体本身的 SVG 图样已经具备极强直观自解释性（如手轮阀门、齿轮咬合、电源开关、芯片微架构、水管弯头），**绝对不要强行添加 `<text>` 标示**！强行加字会显得笨拙累赘、破坏拟物美感与画面精致度。
     - **仅在跨领域抽象概念无法单独依靠图形完全识别时**，才在 Layer 3 精简叠加高对比度的文字或数值批注。

### 具象实体 3 层矢量结构范例库（含微观细节增强与去文字自解释范例）：

```xml
<!-- 🌾 示例 1：实体农田 (包含底座 + 田垄虚线/幼苗纹理 + 芽苞高光/生长状态微细节) -->
<g id="farmland-left">
  <!-- Layer 1: 底座与质感边框 -->
  <rect x="80" y="760" width="320" height="160" rx="12" fill="#e2f0d9" stroke="#385723" stroke-width="3"/>
  <!-- Layer 2: 田垄与幼苗纹理 -->
  <path d="M110 800 L370 800 M110 840 L370 840 M110 880 L370 880" stroke="#a9d08e" stroke-width="2" stroke-dasharray="6,4"/>
  <path d="M140 792 Q145 782 150 792 M220 792 Q225 782 230 792 M300 792 Q305 782 310 792" stroke="#385723" stroke-width="2.5" fill="none"/>
  <path d="M180 832 Q185 822 190 832 M260 832 Q265 822 270 832" stroke="#385723" stroke-width="2.5" fill="none"/>
  <!-- Layer 3: 微观细节与生长状态指示（农田图形直观自解释，无需死板大字） -->
  <circle cx="100" cy="778" r="4" fill="#385723" opacity="0.6"/>
  <circle cx="380" cy="778" r="4" fill="#385723" opacity="0.6"/>
  <path d="M85 765 L395 765" stroke="#ffffff" stroke-width="1.5" opacity="0.5"/> <!-- 高光切线 -->
</g>

<!-- 🏦 示例 2：金融水库大坝 (包含大坝主体 + 刻度/波纹纹理 + 水位警戒指针/固定铆钉/可选标题) -->
<g id="dam-body">
  <!-- Layer 1: 大坝主体与水面底座 -->
  <rect x="700" y="200" width="520" height="280" rx="8" fill="#d9e1f2" stroke="#2f5597" stroke-width="3"/>
  <!-- Layer 2: 水位刻度尺与坝体石缝纹理 -->
  <line x1="720" y1="220" x2="720" y2="450" stroke="#2f5597" stroke-width="3"/>
  <path d="M720 250 L735 250 M720 300 L735 300 M720 350 L735 350 M720 400 L735 400" stroke="#2f5597" stroke-width="2"/>
  <path d="M750 320 Q850 300 950 320 T1150 320" stroke="#8ea9db" stroke-width="2" fill="none" stroke-dasharray="8,4"/>
  <!-- Layer 3: 高阶微观细节（固定铆钉点位 + 动态水位警戒指针） -->
  <circle cx="712" cy="212" r="3" fill="#2f5597"/>
  <circle cx="1208" cy="212" r="3" fill="#2f5597"/>
  <polygon id="water-pointer" points="738,300 748,295 748,305" fill="#e11d48"/> <!-- 红色水位警戒指针 -->
</g>

<!-- 🚰 示例 3：央行水闸与阀门 (包含阀体底座 + 旋转手轮/辐条 + 轴承螺栓/状态 LED/法兰细节，去文字化) -->
<g id="water-valve-group" transform="translate(540, 1300)">
  <!-- Layer 1: 管道与阀门底座 -->
  <rect x="-60" y="-30" width="120" height="60" rx="8" fill="#e2e8f0" stroke="#475569" stroke-width="4"/>
  <!-- Layer 2: 阀门手轮与辐条纹理 -->
  <circle cx="0" cy="0" r="45" fill="#f8fafc" stroke="#0284c7" stroke-width="6"/>
  <path d="M-35 0 L35 0 M0 -35 L0 35 M-25 -25 L25 25 M-25 25 L25 -25" stroke="#0284c7" stroke-width="4"/>
  <circle cx="0" cy="0" r="12" fill="#0284c7"/>
  <!-- Layer 3: 机械微观细节（轴心螺栓点 + 运行状态绿/红 LED 指示灯 + 法兰固定螺栓，极具自解释性，不加中文字） -->
  <circle cx="0" cy="0" r="4" fill="#ffffff"/> <!-- 轴心螺栓点 -->
  <circle cx="32" cy="-32" r="4" fill="#22c55e"/> <!-- 运行状态 LED 绿灯 -->
  <circle cx="-50" cy="-20" r="3" fill="#94a3b8"/> <!-- 法兰固定螺栓 -->
  <circle cx="-50" cy="20" r="3" fill="#94a3b8"/>  <!-- 法兰固定螺栓 -->
</g>

<!-- 💻 示例 4：CPU/AI 芯片内核 (包含基板 + 引脚与金线电路纹理 + 四角金角/晶体管微阵列/光泽切线) -->
<g id="chip-core-group" transform="translate(400, 600)">
  <!-- Layer 1: 芯片基板底座 -->
  <rect x="0" y="0" width="280" height="280" rx="16" fill="#0f172a" stroke="#38bdf8" stroke-width="4"/>
  <!-- Layer 2: 引脚与金线电路纹理 -->
  <path d="M 30 0 L 30 -20 M 70 0 L 70 -20 M 110 0 L 110 -20 M 150 0 L 150 -20 M 190 0 L 190 -20 M 230 0 L 230 -20" stroke="#38bdf8" stroke-width="4"/>
  <path d="M 40 40 L 100 40 L 140 80 M 240 40 L 180 40 L 140 80 M 40 240 L 100 240 L 140 200 M 240 240 L 180 240 L 140 200" stroke="#0ea5e9" stroke-width="2.5" stroke-dasharray="5 3" fill="none"/>
  <!-- Layer 3: 微观硬件细节（四角金角固定点 + 核心晶体管微阵列点 + 边缘光泽高光切线，极富科技质感） -->
  <circle cx="15" cy="15" r="3" fill="#fbbf24"/>
  <circle cx="265" cy="15" r="3" fill="#fbbf24"/>
  <circle cx="15" cy="265" r="3" fill="#fbbf24"/>
  <circle cx="265" cy="265" r="3" fill="#fbbf24"/>
  <rect x="80" y="110" width="120" height="60" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <circle cx="100" cy="140" r="3" fill="#38bdf8"/>
  <circle cx="140" cy="140" r="3" fill="#38bdf8"/>
  <circle cx="180" cy="140" r="3" fill="#38bdf8"/>
  <path d="M 5 5 L 275 5" stroke="#ffffff" stroke-width="1.5" opacity="0.4"/> <!-- 光泽切线 -->
</g>
```

---

## 4. 铁律卡扣 (Strict Rules)

1. 🚫 **严禁使用死板方块+文字**: 任何实体绝对禁止仅用 `<rect>` + `<text>` 替代。农田必须有田垄/幼苗与微观点缀，水库必须有水面/大坝/刻度与指针细节，芯片必须有引脚/电路纹理与晶体管微构件。
2. 🚫 **禁止对自解释图形强行加字**: 视觉形态已经极具辨识度的实体（如阀门手轮、芯片内核、齿轮、水管接口），**严禁强行添加中文字**。Layer 3 应优先使用螺栓、铆钉、指示灯、高光切线、状态点等微观物理细节填充提升精致度。
3. 🚫 **严禁退化为 Dashboard UI 卡片**: 严禁使用 `<div class="card">` 矩形弹窗框、软件 UI 卡片或 Badge 标签框来代表物理实体。
4. 🚫 **必须提供可动节点 ID**: `BRIEF.md` 的 SVG 代码骨架中，所有需要 GSAP 驱动的构件必须赋予明确的 `id`（如 `#farmland-left`, `#valve-wheel`, `#laser-beam`, `#gate-door`, `#water-pointer`）。

---

## 5. IP 角色空间智能避让与留白停留规程 (IP Smart Evasion & Negative Space Idle Matrix)

在讲解视频中，IP Mascot 拥有 **2 种交替状态**，必须通过 GSAP 进行智能空间调度：

1. **交互/操作状态 (Interactive Action State)**：
   - 当 IP 正在摇手柄、推杠杆、点击按钮或拉动管道时，IP 靠近物理实体进行 100% 触碰互动。
2. **停留/观望状态 (Idle / Explanation State)**：
   - 当场景主体物理实体（水坝开闸放水、芯片光刻曝光、数据流快速传导、矩阵对比）正在进行核心演示或高亮展示时，**IP Mascot 必须智能平移避让至画布两侧的通透留白槽 (Negative Space)**，切勿停留在中央区域遮挡主体！

### 空间智能避让对角法则 (Diagonal Complimentarity Rule):
- **主体居右/居中** ➔ IP Mascot 自动平移避让至**左侧/左下留白槽 (`X: 200~300, Y: 500~750`)**。
- **主体居左** ➔ IP Mascot 自动平移避让至**右侧/右下留白槽 (`X: 1600~1700, Y: 500~750`)**。
- **避让动作规范**：
  - **顺滑平移**：使用 GSAP 避让位移 `gsap.to("#mascot", { x: pocketX, y: pocketY, duration: 0.8, ease: "power2.out" })`。
  - **视线与姿态引导**：平移停稳后，微调 `#mascot-head` 倾斜 5~10 度朝向中央主体，结合手臂 `#mascot-arm-*` 呈“侧身观望”或“指引手势”，自然将观众视线聚焦至核心演示区。

---

## 6. IP 角色常驻微呼吸与 5s 习惯性微动作规程 (Continuous Idle Micro-Gestures Protocol)

为防止画面出现长达 5~6s 无主体大动作时的僵硬死寂感，不需要复杂的整屏静止检测逻辑，直接在代码中挂载 **双层常驻微动作引擎**：

---

## 7. 物理实体独立模块化拆分与双比例流式布局矩阵 (Modular Component Decoupling & Responsive Layout Matrix)

为彻底解决“把所有实体打包在单一死板 `<g>` 组中导致 9:16 竖屏下画面缩成一小条”的痛点，所有 SVG 骨架设计必须遵守**模块化拆分解耦与双比例响应式布局规程**：

### 7.1 构件独立解耦规程 (Modular Decoupling Rule)
- **🚫 严禁大包揽打包与全局按 Layer 分组**：
  - 绝对禁止将整个场景硬编码封装在单一巨型 `<g id="all-in-one">` 组中！
  - **绝对禁止按 Layer 1 / Layer 2 / Layer 3 建立全局跨实体大组**（如 `<g id="macro-water-system"><g id="dam-base">...</g><g id="textures">...</g><g id="details">...</g></g>`），这种写法破坏了实体的解耦封装，会导致 9:16 竖屏无法独立调整单实体位置。
- **✅ 必须按物理实体内聚封装 3 层结构**：每个物理实体必须拆分为独立的具名 `<g id="...">` 构件，在其内部包含该实体专属的 Layer 1 底座 + Layer 2 纹理 + Layer 3 细节，并基于自身的局部原点定位：
  ```xml
  <!-- 构件 A：独立大坝 (自带大坝底座 Layer 1 + 刻度 Layer 2 + 铆钉 Layer 3) -->
  <g id="dam-body" transform="translate(100, 350)"> ... </g>

  <!-- 构件 B：独立水闸 (自带水闸底座 Layer 1 + 螺纹 Layer 2 + LED 状态灯 Layer 3) -->
  <g id="water-gate" transform="translate(910, 400)"> ... </g>

  <!-- 构件 C：独立农田 (自带农田底座 Layer 1 + 田垄 Layer 2 + 芽苞高光 Layer 3) -->
  <g id="farmland-target" transform="translate(1150, 650)"> ... </g>

  <!-- 连接通道：水渠水流 -->
  <path id="canal-pipe" d="..." />
  ```

### 7.2 双比例流式布局矩阵 (Responsive Aspect Layout Matrix)

下游渲染技能在生成 HTML 时，根据画幅比例动态适配排列方向与尺寸，保证竖屏画面饱满大气：

| 画布比例与尺寸 | 排列流向 (Flow Direction) | 构件尺寸 (Scaling) | 连接管道 path `d` 形式 |
| :--- | :--- | :--- | :--- |
| **16:9 横屏 (`1920x1080`)** | **水平横向流 (Left-to-Right)**<br>源头(左 `X:300`) ➔ 阀门(中 `X:960`) ➔ 目标(右 `X:1600`) | `scale(1.0)` 标准尺寸 | 横向路径：`M 300,500 H 1600` |
| **9:16 竖屏 (`1080x1920`)** | **垂直纵向瀑布流 (Top-to-Bottom)**<br>源头(顶 `Y:320`) ➔ 阀门(中 `Y:750`) ➔ 目标(底 `Y:1280`) | **`scale(1.3 ~ 1.5)` 放大**<br>充盈 1080px 宽度，气势恢宏 | 纵向路径：`M 540,450 V 1350` |

### 7.3 9:16 视频平台 (小红书/抖音/视频号) 双向 (顶/底) UI 避让留白规程
- **小红书/抖音/视频号平台 UI 顶底遮挡**：
  - **顶部遮挡**：平台会在视频顶部覆盖返回/退出按钮、搜索图标、分类 Tab 栏及手机刘海/状态栏（占用 Y: `0px ~ 200px` 顶部约 200px 空间）。
  - **底部遮挡**：平台会在视频底部覆盖作者头像、账号名 `@xxx`、发布文案、`#话题` 标签及音符/点赞按钮（占用 Y: `1600px ~ 1920px` 底部约 320px 空间）。
- **双向硬性留白避让**：
  - **顶部 200px (Y: 0-200px)**：必须保留为纯净背景留白区（Zero Elements），绝对禁止放置任何标题文字、SVG 构件或图标。主标题组起始 Y 必须从 `200px` 开始。
  - **唱词字幕盒**：必须向上提升放置在 `bottom: 320px` 处（Y: `1460px ~ 1580px`）。
  - **底部 320px (Y: 1600-1920px)**：必须保留为纯净背景留白区（Zero Elements），绝对禁止放置任何物理构件、SVG 文字或字幕盒，防止被平台底层 UI 原生图层遮挡！




