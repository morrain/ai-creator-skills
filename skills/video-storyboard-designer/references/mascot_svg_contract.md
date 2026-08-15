本规范定义了在 `video-storyboard-designer`（视频单元需求构建）技能输出项目专属 IP 矢量图形文件 (`./assets/video/unit_XX/public/mascot.svg`) 时，必须遵循的矢量图节点 ID 契约。下游 HyperFrames 渲染技能将通过这些固定 ID 绑定 GSAP 时间轴动画。

---

## 1. 强制节点 ID 命名契约

生成的 `mascot.svg` 文件内部，矢量根元素与各关节/器官子元素必须包含以下标准的 `id` 属性：

| Element ID | 元素类型 | 作用与动画说明 | 标准 svgOrigin (viewBox 300x400) |
| :--- | :--- | :--- | :--- |
| `id="xiao-zhi-svg"` | `<svg>` 根节点 | 全局 SVG 容器 (viewBox="0 0 300 400") | N/A |
| `id="mascot-head"` | `<g>` 头部组 | 头部动作（倾斜、点头、摇头） | `"150 160"` (颈部) |
| `id="mascot-eye-left"` | `<g>` 左眼 | 左眼眨眼与闭眼 (`scaleY`) | `"115 105"` |
| `id="mascot-eye-right"` | `<g>` 右眼 | 右眼眨眼与闭眼 (`scaleY`) | `"185 105"` |
| `id="mascot-mouth"` | `<g>` 嘴部 | 嘴部表情与微调 | `"150 140"` |
| `id="mascot-arm-left"` | `<g>` 左手臂组 | 左臂姿态/摆动/拉动/托举 | `"90 205"` (左肩) |
| `id="mascot-arm-right"` | `<g>` 右手臂组 | 右臂姿态/摆动/挥手/拉手柄 | `"210 205"` (右肩) |
| `id="mascot-leg-left"` | `<g>` 左腿组 | 左腿行走/跨步/踢腿 (`rotation`) | `"120 300"` (左髋关节) |
| `id="mascot-leg-right"` | `<g>` 右腿组 | 右腿行走/跨步/踢飞 (`rotation`) | `"180 300"` (右髋关节) |
| `id="mascot-body"` | `<g>` 躯干组 | 身体核心躯干与标志 | `"150 245"` (腹心) |
| `id="mascot-prop-slot"`| `<g>` 道具插槽 | 绑定绳索、手柄、放大镜或工具等互动道具 | `"260 270"` |
| `id="mascot-stamp"` | `<g>` 盖章组 (可选) | Act 3 交付阶段的 `[PASS]` 印章 drop 效果 | `"150 350"` |

---

## 2. 推荐 SVG 节点结构示例

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400" id="xiao-zhi-svg">
  <g id="mascot-body">
    <!-- 躯干线条 (x=90, y=190, w=120, h=110, rx=12) -->
  </g>
  <g id="mascot-leg-left">
    <!-- 左腿线条与脚掌 (x1=120, y1=300, x2=120, y2=360, cx=120, cy=366, r=6) -->
  </g>
  <g id="mascot-leg-right">
    <!-- 右腿线条与脚掌 (x1=180, y1=300, x2=180, y2=360, cx=180, cy=366, r=6) -->
  </g>
  <g id="mascot-arm-left">
    <!-- 左手臂线条 (x1=90, y1=205, x2=40, y2=270) -->
  </g>
  <g id="mascot-arm-right">
    <!-- 右手臂线条 (x1=210, y1=205, x2=260, y2=270) -->
  </g>
  <g id="mascot-prop-slot" transform="translate(260, 270)">
    <!-- 绑定的绳索/手柄/放大镜等手持道具 -->
  </g>
  <g id="mascot-head">
    <!-- 方块头部轮廓 (x=75, y=50, w=150, h=130, rx=16) 与天线 -->
    <g id="mascot-eye-left"><!-- 左眼 (cx=115, cy=105, r=6) --></g>
    <g id="mascot-eye-right"><!-- 右眼 (cx=185, cy=105, r=6) --></g>
    <g id="mascot-mouth"><!-- 嘴巴 (x1=135, y1=140, x2=165, y2=140) --></g>
  </g>
</svg>
```

---

## 3. GSAP 关节旋转动画最佳实践 (svgOrigin 强制规范)

在下游 HyperFrames HTML 页面中，使用 GSAP 对 `mascot.svg` 的 `<g>` 节点（如 `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-head`）施加旋转 (`rotation`) 或缩放 (`scale`) 动画时：

- **⚠️ 严禁使用** CSS `transformOrigin: "90px 200px"` 属性：因为 CSS 像素坐标会以元素自身的包围盒 (Bounding Box) 左上角为原点进行二次偏移，导致旋转中心错位到胸口或体外，出现**手臂断裂/脱臼现象**。
- **✅ 强制使用** GSAP 专属属性 `svgOrigin: "X Y"`：直接传入该节点在全局 `viewBox` 画布中的绝对关节点坐标（例如左臂肩膀 `svgOrigin: "90 205"`，右臂肩膀 `svgOrigin: "210 205"`，右腿髋关节 `svgOrigin: "180 300"`），确保旋转轴心牢固锁定在关节处，动画自然流畅不脱节。

```javascript
// ✅ 正确写法：锁定 SVG viewBox 坐标系中的关节点
gsap.set("#mascot-arm-left", { svgOrigin: "90 205", rotation: 0 });
gsap.set("#mascot-arm-right", { svgOrigin: "210 205", rotation: 0 });
gsap.set("#mascot-leg-left", { svgOrigin: "120 300", rotation: 0 });
gsap.set("#mascot-leg-right", { svgOrigin: "180 300", rotation: 0 });
gsap.set("#mascot-head", { svgOrigin: "150 160", rotation: 0 });
```

---

## 4. 下游约束

下游 HyperFrames 将直接读取目标项目路径下的 `public/mascot.svg`。若缺少该文件或节点 ID 不规范，渲染器将报错阻断。

---

## 5. HTML 源码嵌入与 SubAgent 强制契约

在下游 HyperFrames 生成 `index.html` 页面代码时，必须遵循以下矢量源码嵌入约束：

1. **✅ 强制 DOM 节点直接内嵌**：必须将 `public/mascot.svg` 内部包含 `#mascot-head`, `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-leg-left`, `#mascot-leg-right`, `#mascot-body` 等标准 ID 节点的完整 `<g>` 矢量 DOM 结构原样复制/内嵌写入 `index.html` 主 SVG 容器的 `<g id="mascot">` 节点内部。
2. **⚠️ 严禁使用跨文件 `<use>` 引用**：禁止在 `index.html` 中编写 `<use href="./public/mascot.svg#...">` 或 `<use href="mascot.svg#...">`，防止在无 Web Server 的 Headless / Puppeteer 渲染环境下因同源安全/CORS 限制导致外部节点引用失败。
3. 🚫 **绝对禁止脑补/手写草案图形**：绝对禁止在 `index.html` 中自行脑补或手写 `<rect fill="#fbbf24">`、`<rect fill="#f59e0b">`、`<circle fill="#fde68a">` 等替代性的粗线条/彩色块占位图形！

---

## 6. 常驻微呼吸与 5s 习惯性微动作代码标准 (Continuous Idle Micro-Gesture Standard)

为彻底消除分镜切片中画面死寂僵硬感（如 >5s 无大动作的场景），在 `index.html` 的 GSAP 脚本中，必须建立 **双层常驻微动作引擎**：

```javascript
// 1. Layer A: 常驻呼吸浮动与眨眼循环 (Continuous Breathing & Blink Loop)
gsap.to("#mascot", { y: "+=6", duration: 2.2, repeat: -1, yoyo: true, ease: "sine.inOut" });
gsap.to(["#mascot-eye-left", "#mascot-eye-right"], {
  scaleY: 0.1, duration: 0.12, repeat: -1, repeatDelay: 3.5, transformOrigin: "center"
});

// 2. Layer B: 每 4-5 秒循环习惯性微动作 (5-Second Periodic Micro-Gestures)
const idleTimeline = gsap.timeline({ repeat: -1, repeatDelay: 1.5 });
idleTimeline
  // 4s 点头与左臂微摆
  .to("#mascot-head", { rotation: 6, svgOrigin: "150 160", duration: 0.4, ease: "power1.out" })
  .to("#mascot-arm-left", { rotation: -12, svgOrigin: "90 205", duration: 0.4, ease: "power1.out" }, "<")
  .to("#mascot-head", { rotation: 0, duration: 0.4, ease: "power1.inOut" }, "+=0.3")
  .to("#mascot-arm-left", { rotation: 0, duration: 0.4, ease: "power1.inOut" }, "<")
  // 8s 摇头与右臂微抬
  .to("#mascot-head", { rotation: -6, svgOrigin: "150 160", duration: 0.4, ease: "power1.out" }, "+=2.0")
  .to("#mascot-arm-right", { rotation: 10, svgOrigin: "210 205", duration: 0.4, ease: "power1.out" }, "<")
  .to("#mascot-head", { rotation: 0, duration: 0.4, ease: "power1.inOut" }, "+=0.3")
  .to("#mascot-arm-right", { rotation: 0, duration: 0.4, ease: "power1.inOut" }, "<");
```
