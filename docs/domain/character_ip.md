# 🎨 自定义 IP 形象规范 (Custom IP Mascot Spec Template)

> 💡 **说明**：此文件为项目全局自定义 IP 形象规范。当此文件存在时，`illustrations` 与 `to-poster` 技能将优先继承本规范，并自动跳过 Skill 默认的“小智”IP 描述。

---

## 1. 核心定义 (Identity)

- **IP 名称 (中文)**：[如：小熊 / 极客猫]
- **IP 名称 (英文 Identifier)**：[如：Xiao Xiong / Geek Cat]
- **角色定位**：[如：死理性的科技客座讲师 / 呆萌但严肃的手绘小熊]

---

## 2. 外貌 Prompt 标准描述 (Master Visual Prompt)

在拼装生图 Prompt 的 `Recurring IP character required` 区块时，系统将直接使用以下英文描述：

```text
{IP_MASCOT_NAME}, a minimalist hand-drawn mascot with [外貌特征描述, 如: rounded bear ears, deadpan dot eyes, a simple linen apron], acting as the main conceptual operator.
```

---

## 3. 视觉禁忌 (Visual Taboos)

- 🚫 **严禁样式**：[如：严禁 3D 渲染、严禁炫彩渐变]
- 🚫 **角色的核心职责**：角色必须亲自承担画面的核心物理动作，严禁沦为角落的无用摆件。
