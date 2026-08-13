# 🎨 共享 IP 形象规范 (Shared IP Mascot Specification)

为了保证在插画 (`illustration-designer`)、海报 (`poster-designer`) 及视频单元设计 (`video-storyboard-designer`) 中 IP 角色的视觉一致性与可扩展性，特制定本规范。

---

## 1. 默认 IP 形象：小智 (Xiao Zhi)

### 角色基本信息
- **IP 名称**：小智 (Xiao Zhi)
- **英文 prompt 名称**：Xiao Zhi robot
- **角色定位**：文章正文配图、海报及动画视频的固定视觉 IP 主角。它不是可爱吉祥物，不是静态贴纸，不是无意义装饰，而是正在认真参与系统运转的荒诞工作者。

### 外观特征 (Visual Appearance)
- **头部 (Head)**：1:1 正方形小方块头，带 16px 轻微圆角 (1:1 square head with slight 16px rounded corners)。
- **天线 (Antenna)**：头顶正中央垂直立起一根极简单天线，顶端带有小圆球 (vertical single antenna with small ball tip)。
- **眼睛 (Eyes)**：经典双眼对称死鱼眼/纯黑点点眼 (symmetric black dot eyes)，表达呆萌冷静无表情状态。
- **嘴巴 (Mouth)**：平直微小的极简黑线嘴 (flat straight line mouth)，死板冷静。
- **躯干 (Body)**：纯白矩形躯干，4px 纯黑手绘线条描边。
- **四肢 (Limbs)**：极简 4px 纯黑手绘线条双臂与双腿，双脚顶端为极简小圆点脚掌 (thin 4px black line limbs with small dot feet)，具备完整走、跑、踢腿、拉扯能力。
- **画风与线条 (Line Art Style)**：2D 纯正手绘黑线 (2D minimalist black line art on plain background, 4px stroke width)，轮廓软萌带抖动感，无渐变、无阴影、无 3D 金属高光。

### 性格与气质 (Personality & Vibe)
- **Deadpan / Blank Expression**：极度认真，但做的事带有荒诞幽默感。
- **低调系统操作员**：冷幽默，绝对不主动卖萌。
- **笨拙但专业**：像在白纸草图里真的负责某个硬核或怪异的工作流程。

---

## 2. 外貌 Prompt 标准描述 (Master Visual Prompt)

在拼装生图及视频分镜 Prompt 时，系统将统一使用以下极精细描述：

```text
Xiao Zhi robot, a 2D minimalist hand-drawn mascot with a 1:1 square head (slight rounded corners), vertical single antenna with ball tip, symmetric black dot eyes, flat line mouth, 4px thin line limbs with small dot feet, plain white body, 4px black outline stroke art, deadpan expression, acting as the main conceptual operator.
```

---

## 3. 核心动作与职责 (Core Action Pool)

IP 角色必须作为画面的核心动作主体：

- 搬运素材方块、数据块、逻辑芯片。
- 用细手/线缆拉引、拖拽、操作杠杆（Pull / Drag / Push）。
- 单腿踢飞、踩踏障碍物或故障节点 (Kick / Step)。
- 操作机器上的“判断”闸门、摇杆或转动阀门开关 (Operate Lever/Wheel)。
- 变成筛选漏斗、数据过滤器。
- 切开“素材鱼”、拆解复杂的解耦信息包。
- 发射极简扫描光束读取内容、给承接话术盖章。
- 从洞里伸出机械手，或在旁搬砖、搭桥、开门、分拣、调试回路。

---

## 4. 视觉禁忌 (Visual Taboos)

- 🚫 **严禁画成卖萌吉祥物**：不要给复杂的表情包、大闪亮眼睛、红扑扑脸蛋。
- 🚫 **严禁画成儿童卡通**：不要给精致服装、花哨饰品。
- 🚫 **严禁画成 3D 金属/高光渲染**：必须保持 2D 轻柔手绘线稿质感。
- 🚫 **严禁沦为角落装饰**：如果去掉 IP 角色，画面隐喻依然完全成立，说明角色太装饰，必须重写 Prompt 使其成为动作主体。

---

> 💡 **说明**：本文件为 `illustration-designer` 的默认 IP 资产（小智）。若项目存在主题级（`./<article-slug>/character_ip.md`）或项目级（`./character_ip.md`）自定义 IP 规范，技能会在执行第一步时进行短路拦截，优先读取更高级别文件，不再读取本默认文件。
