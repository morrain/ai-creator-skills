# 🎬 IP Mascot GSAP 物理动作范例库 (Physical Metaphor GSAP Action Recipes)

本指南为下游 HyperFrames SubAgent 提供规范化的 GSAP 物理动作代码范例，解决 IP 形象“单纯摇头晃脑”无真实动作的问题。HyperFrames 在编写 GSAP HTML 动画代码时，必须根据 `BRIEF.md` 指定的 Recipe 引入以下组合代码范例。

---

## 1. 关节原点初始化 (GSAP Set Baseline)

在编写任何动画前，必须显式锁定 300x400 viewBox 下的关节点绝对坐标原点：

```javascript
// 锁定关节 Origin
gsap.set("#mascot-arm-left",  { svgOrigin: "90 205" });
gsap.set("#mascot-arm-right", { svgOrigin: "210 205" });
gsap.set("#mascot-leg-left",  { svgOrigin: "120 300" });
gsap.set("#mascot-leg-right", { svgOrigin: "180 300" });
gsap.set("#mascot-head",      { svgOrigin: "150 160" });
gsap.set("#mascot-body",      { svgOrigin: "150 245" });
```

---

## 2. 核心物理动作代码模式 (Action Code Recipes)

### 模式 A: 拖 / 拉 (PULL / DRAG)
* **物理隐喻场景**：拉引数据线缆、拖拽权重滑动条、拉动绳索把手。
* **动作要领**：双手向后发力拉拽，躯干后倾（倾斜 `-10deg`），整体 `x` 坐标向后位移，道具插槽与绳索弯曲联动。

```javascript
const pullTl = gsap.timeline({ defaults: { ease: "power2.inOut" } });

// 1. 蓄力前倾抓住绳索/手柄
pullTl.to("#mascot-arm-right", { rotation: -45, duration: 0.4 })
      .to("#mascot-body", { rotation: 5, x: 10, duration: 0.4 }, "<")
// 2. 爆发力向后拖拉
      .to("#mascot-arm-right", { rotation: 40, duration: 0.8, ease: "back.out(1.5)" })
      .to("#mascot-body", { rotation: -12, x: -35, duration: 0.8 }, "<")
      .to("#mascot-head", { rotation: -8, duration: 0.8 }, "<")
      .to("#target-rope-or-slider", { x: -60, duration: 0.8 }, "<");
```

---

### 模式 B: 推 / 按 (PUSH / PRESS)
* **物理隐喻场景**：将模块压入槽位、按下启动大按钮、推平阻抗关卡。
* **动作要领**：手臂向前延伸，躯干前倾 `15deg`，全身体重向前压下，目标元件下沉/滑入。

```javascript
const pushTl = gsap.timeline({ defaults: { ease: "power3.out" } });

// 1. 举手准备
pushTl.to("#mascot-arm-left", { rotation: 60, duration: 0.3 })
      .to("#mascot-arm-right", { rotation: -60, duration: 0.3 }, "<")
// 2. 猛烈向下/向前推压
      .to("#mascot-arm-left", { rotation: 110, duration: 0.5, ease: "bounce.out" })
      .to("#mascot-arm-right", { rotation: -110, duration: 0.5, ease: "bounce.out" }, "<")
      .to("#mascot-body", { rotation: 15, y: 15, duration: 0.5 }, "<")
      .to("#mascot-head", { y: 20, duration: 0.5 }, "<")
      .to("#target-button-or-block", { y: 40, scaleY: 0.8, duration: 0.5 }, "<");
```

---

### 模式 C: 踢 / 踩 (KICK / STEP)
* **物理隐喻场景**：踢开冗余阻抗节点、踩碎异常抛错块、把非法包踢出回路。
* **动作要领**：支撑腿不动，右腿以髋关节为中心快速向上甩踢 `70deg`，目标物体做抛物线飞出。

```javascript
const kickTl = gsap.timeline();

// 1. 身体微后仰抬腿
kickTl.to("#mascot-leg-right", { rotation: -30, duration: 0.25 })
      .to("#mascot-body", { rotation: -8, duration: 0.25 }, "<")
// 2. 快速爆发向前踢出
      .to("#mascot-leg-right", { rotation: 75, duration: 0.2, ease: "power4.out" })
      .to("#mascot-body", { rotation: 10, duration: 0.2 }, "<")
      .to("#mascot-head", { rotation: 12, duration: 0.2 }, "<")
// 3. 目标物体被踢飞
      .to("#target-error-node", { x: 300, y: -150, rotation: 360, opacity: 0, duration: 0.6, ease: "power2.out" }, "-=0.15");
```

---

### 模式 D: 摇手柄 / 转阀门 (OPERATE LEVER / WHEEL)
* **物理隐喻场景**：调节流量闸门、转动解耦阀门、切换分流路线。
* **动作要领**：右臂旋转与手柄/阀门旋转轴 1:1 同步，头部跟随看视。

```javascript
const leverTl = gsap.timeline({ repeat: 2, yoyo: true, defaults: { ease: "sine.inOut" } });

leverTl.to("#mascot-arm-right", { rotation: 65, duration: 0.6 })
       .to("#target-valve-wheel", { rotation: 180, svgOrigin: "260 270", duration: 0.6 }, "<")
       .to("#mascot-head", { rotation: 5, duration: 0.6 }, "<");
```

---

### 模式 E: 托举 / 展示 (LIFT / DISPLAY)
* **物理隐喻场景**：将核心概念、解耦架构图或最终印章托举展示给观众。
* **动作要领**：双手平举抬高，双腿略微蹲下起跳后站直，目标信息卡片从下方平滑弹升。

```javascript
const liftTl = gsap.timeline({ defaults: { ease: "back.out(1.7)" } });

liftTl.to("#mascot-arm-left", { rotation: -135, duration: 0.7 })
      .to("#mascot-arm-right", { rotation: 135, duration: 0.7 }, "<")
      .to("#mascot-body", { y: -10, duration: 0.7 }, "<")
      .to("#target-hero-card", { y: -120, opacity: 1, scale: 1, duration: 0.7 }, "<");
```

---

## 3. 规范约束

HyperFrames 在为视频单元编写 GSAP HTML 动画时，必须在代码中注入对应的 Recipe，**严禁生成仅对 `#mascot-head` 施加微弱旋转的偷懒代码**！
