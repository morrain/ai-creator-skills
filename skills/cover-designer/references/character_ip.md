# 🎨 共享 IP 形象规范 (Shared IP Mascot Specification)

为了保证在插画 (`illustration-designer`)、海报 (`poster-designer`)、视频单元设计 (`video-storyboard-designer`) 及封面设计 (`cover-designer`) 中 IP 角色的视觉一致性与可扩展性，特制定本规范。

---

## 1. 默认 IP 形象：小智 (Xiao Zhi)

### 角色基本信息
- **IP 名称**：小智 (Xiao Zhi)
- **英文 prompt 名称**：Xiao Zhi robot
- **角色定位**：文章正文配图、海报、动画视频及封面的固定视觉 IP 主角。它不是可爱吉祥物，不是静态贴纸，不是无意义装饰，而是正在认真参与系统运转的荒诞工作者。

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

在拼装封面生图及视频分镜 Prompt 时，系统将统一使用以下极精细描述：

```text
Xiao Zhi robot, a 2D minimalist hand-drawn mascot with a 1:1 square head (slight rounded corners), vertical single antenna with ball tip, symmetric black dot eyes, flat line mouth, 4px thin line limbs with small dot feet, plain white body, 4px black outline stroke art, deadpan expression, acting as the main conceptual operator.
```

---

## 3. 封面爆款互动姿态库 (Interactive Cover Gestures)

在封面设计中，IP Mascot 必须作为画面的核心动作主体，呈现具备**互动发问感（Interactive Gestures）**的定格动作：

- ⚖️ **双向站队发问**：站在分叉口/天平中央，双手分别指向两侧，微倾头部呈发问思考姿态。
- 🔢 **盘点测试指引**：手持投票牌或伸出右手食指逐一盘点编号图卡，左手指向评论区。
- ❓ **震撼探查与冷幽默**：单手拿着发光放大镜聚焦神秘宝箱/问号，另一手做出震撼托腮动作。
- 💥 **死板坚韧重压**：双手拉紧防爆闸机或扛着巨型杠铃，展示死板（Deadpan）坚韧表情。
- 🔄 **倒挂翻转探查**：倒挂在齿轮导轨上翻转视角，伸手探查旋转的逆向轴承。

---

## 4. 视觉禁忌 (Visual Taboos)

- 🚫 **严禁画成卖萌吉祥物**：不要给复杂的表情包、大闪亮眼睛、红扑扑脸蛋。
- 🚫 **严禁画成儿童卡通**：不要给精致服装、花哨饰品。
- 🚫 **严禁画成 3D 金属/高光渲染**：必须保持 2D 轻柔手绘线稿质感。
- 🚫 **严禁沦为角落装饰**：如果去掉 IP 角色，画面隐喻依然完全成立，说明角色太装饰，必须重写 Prompt 使其成为动作主体。

---

## 5. IP Mascot 短路路由加载机制 (Short-Circuit IP Routing)

在提炼封面视觉方案与生图 Prompt 时， Agent 必须按以下优先级**显式检查且仅装载 1 份 IP 描述规范**（统一文件名为 `character_ip.md`）：

1. **主题级**：`./<article-slug>/character_ip.md`
2. **项目级**：`./character_ip.md`
3. **默认技能级**：`skills/cover-designer/references/character_ip.md`（本文件）

> ⚠️ **命中即止原则**：一旦在上层找到 `character_ip.md`，即刻停止向下查找，拦截下位文件。
