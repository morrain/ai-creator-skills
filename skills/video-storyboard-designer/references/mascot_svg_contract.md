本规范定义了在 `video-storyboard-designer`（视频单元需求构建）技能输出项目专属 IP 矢量图形文件 (`./assets/video/unit_XX/public/mascot.svg`) 时，必须遵循的矢量图节点 ID 契约。下游 HyperFrames 渲染技能将通过这些固定 ID 绑定 GSAP 时间轴动画。

---

## 1. 强制节点 ID 命名契约

生成的 `mascot.svg` 文件内部，矢量根元素与各关节/器官子元素必须包含以下标准的 `id` 属性：

| Element ID | 元素类型 | 作用与动画说明 |
| :--- | :--- | :--- |
| `id="xiao-zhi-svg"` | `<svg>` 根节点 | 全局 SVG 容器 |
| `id="mascot-head"` | `<g>` 头部组 | 头部动作（倾斜、点头、摇头） |
| `id="mascot-eye-left"` | `<g>` 左眼 | 左眼眨眼与闭眼 (`scaleY`) |
| `id="mascot-eye-right"` | `<g>` 右眼 | 右眼眨眼与闭眼 (`scaleY`) |
| `id="mascot-mouth"` | `<g>` 嘴部 | 嘴部表情与微调 |
| `id="mascot-arm-left"` | `<g>` 左手臂组 | 左臂姿态/摆动 (`rotation`) |
| `id="mascot-arm-right"` | `<g>` 右手臂组 | 右臂姿态/摆动（挥手、指向、按按纽、拉阀门） |
| `id="mascot-body"` | `<g>` 躯干组 | 身体核心躯干与标志 |
| `id="mascot-stamp"` | `<g>` 盖章组 (可选) | Act 3 交付阶段的 `[PASS]` 印章 drop 效果 |

---

## 2. 推荐 SVG 节点结构示例

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400" id="xiao-zhi-svg">
  <g id="mascot-body">
    <!-- 躯干线条与画幅 -->
  </g>
  <g id="mascot-arm-left">
    <!-- 左手臂线条 -->
  </g>
  <g id="mascot-arm-right">
    <!-- 右手臂线条 -->
  </g>
  <g id="mascot-head">
    <!-- 方块头部轮廓与天线 -->
    <g id="mascot-eye-left"><!-- 左眼 --></g>
    <g id="mascot-eye-right"><!-- 右眼 --></g>
    <g id="mascot-mouth"><!-- 嘴巴 --></g>
  </g>
</svg>
```

---

## 3. GSAP 关节旋转动画最佳实践 (svgOrigin 强制规范)

在下游 HyperFrames HTML 页面中，使用 GSAP 对 `mascot.svg` 的 `<g>` 节点（如 `#mascot-arm-left`, `#mascot-arm-right`, `#mascot-head`）施加旋转 (`rotation`) 或缩放 (`scale`) 动画时：

- **⚠️ 严禁使用** CSS `transformOrigin: "90px 200px"` 属性：因为 CSS 像素坐标会以元素自身的包围盒 (Bounding Box) 左上角为原点进行二次偏移，导致旋转中心错位到胸口或体外，出现**手臂断裂/脱臼现象**。
- **✅ 强制使用** GSAP 专属属性 `svgOrigin: "X Y"`：直接传入该节点在全局 `viewBox` 画布中的绝对关节点坐标（例如左臂肩膀 `svgOrigin: "90 200"`，右臂肩膀 `svgOrigin: "210 200"`），确保旋转轴心牢固锁定在关节处，动画自然流畅不脱节。

```javascript
// ✅ 正确写法：锁定 SVG viewBox 坐标系中的关节点
gsap.set("#mascot-arm-left", { svgOrigin: "90 200", rotation: 0 });
gsap.set("#mascot-arm-right", { svgOrigin: "210 200", rotation: 0 });
gsap.set("#mascot-head", { svgOrigin: "150 160", rotation: 0 });
```

---

## 4. 下游约束

下游 HyperFrames 将直接读取目标项目路径下的 `public/mascot.svg`。若缺少该文件或节点 ID 不规范，渲染器将报错阻断。
