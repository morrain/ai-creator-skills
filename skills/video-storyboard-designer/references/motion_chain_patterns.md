# 3 幕动态动作链设计范例 (3-Act Motion Chain Patterns)

本文件说明 `video-storyboard-designer` 将正文插图中的静态隐喻动作推演解耦为 3 幕动态动作链的标准模式。

---

## 核心设计法则

任何从正文插图（`illustration_*.md`）继承的静态 IP Mascot 动作，必须推演为以下 3 幕连续的场景：

1. **Act 1 (引出问题 / Problem Hook)**:
   - IP Mascot 角色面对混乱的数据线缆、堵塞的管道或断裂的逻辑网格。
   - 神情冷静认真带冷幽默（Deadpan），开始准备工具。

2. **Act 2 (动作核心 / Core Action - 继承插图)**:
   - IP Mascot 亲自操作关键低科技道具（拉动缆线、旋转巨大阀门、手持放大镜观察节点、踩下锁扣）。
   - 画面呈现核心物理隐喻发生瞬间（如断点连接发光、齿轮咬合）。

3. **Act 3 (交付结果 / Delivery & Stamping)**:
   - IP Mascot 完成操作，手持钢印在成果或数据管道上盖上 `[PASS]` 或 `[OPTIMIZED]` 印章。
   - 系统线路顺畅运行，显示定量优化指标。

---

## 典型动作链范例

### 模式 A: 数据线缆与断点拼接链 (Cable & Bridge Chain)
- **Act 1**: IP Mascot 发现两条断裂的发光数据缆线，间隙中电火花冒出。
- **Act 2**: IP Mascot 从小背包抽出连接插头，用力将两条缆线插入中间的止逆阀门中。
- **Act 3**: 数据流顺畅通过阀门，IP Mascot 给电路节点盖上绿色 OK 章。

### 模式 B: 齿轮与高压力阀门调节链 (Valve & Gear Chain)
- **Act 1**: 巨大的机械齿轮疯狂转动，管道压力指针飙升至红色警示区。
- **Act 2**: IP Mascot 站在高台梯子上，奋力用细手旋转巨大的金属摇杆阀门。
- **Act 3**: 压力指针瞬间回落至绿区，管道喷出清爽冷气，IP Mascot 面露平静收工。

---

## 长单元（>20s）二次分镜拆解模式 (Secondary Storyboard Subdivision)

当视频单元时长大于 20 秒时，在 `BRIEF.md` 中需深度结合口播文案（Voiceover）进行多切片二次分镜：

### 模式范例：多阶段智能闸机分流链 (Multi-Subshot Intelligent Gate Chain)
- **口播文本**: *"这就好比把传统的漫长排队大厅改造为了智能分流窗口。当数据发生变动时，系统不再通知所有无关节点，而是通过双向链表精准找到订阅者，实现毫秒级响应。"*
- **画面元素全量清单**: `#bg-hall` (办事大厅), `#queue-lines` (长队伍), `#gate-system` (智能闸机), `#light-beam` (精准光束), `#timer-card` (毫秒计时卡片), `#mascot-*` (IP 角色节点)。
- **镜头切片划分**:
  - **[Sub-shot 1: 00:00-00:10] (传统痛点/引出问题)**:
    - *Voiceover*: "这就好比把传统的漫长排队大厅改造为了智能分流窗口。"
    - *画面/动作*: `#bg-hall` 背景淡入，`#queue-lines` 人群拥挤晃动。IP Mascot 手持警告牌指示队伍（`[Action Recipe: HOLD_SIGN]`）。
  - **[Sub-shot 2: 00:10-00:20] (智能重构/核心动作)**:
    - *Voiceover*: "当数据发生变动时，系统不再通知所有无关节点，而是通过双向链表精准找到订阅者..."
    - *画面/动作*: `#bg-hall` 向两侧展开退场，`#gate-system` 旋转降入中央，`#light-beam` 绿色光束穿透两端。IP Mascot 踩下切换闸机踏板（`[Action Recipe: KICK_STEP]`）并拉动分流杠杆。
  - **[Sub-shot 3: 00:20-00:25] (毫秒响应/交付结果)**:
    - *Voiceover*: "...实现毫秒级响应。"
    - *画面/动作*: `#timer-card`（`[0.1ms]`）自底部弹显跳变，IP Mascot 手持盖章器在闸机旁盖上 `[PASS]` 绿色印章（`[Action Recipe: STAMP_SEAL]`）。
