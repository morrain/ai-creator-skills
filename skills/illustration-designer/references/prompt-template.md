# 提示词模板与生成规范 (Prompt Templates & Specs)

本文档提供单张配图生成的标准生图提示词模板、原生中文批注法则及图像编辑/修复提示词。

---

## 1. 单张生图提示词模板 (Master Image Generation Template)

在为每张插图生成 Markdown 配置文件（`assets/illustration_N.md`）中的 `🟢 英文生图版 Prompt` 时，严格遵循以下结构拼装提示词，并配合 [`references/illustration_reviewer_standards.md`](illustration_reviewer_standards.md) 进行 SubAgent 盲审：

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Clean absurd product-sketch feeling with self-explanatory visual composition. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring IP character required:
{IP_MASCOT_NAME} ({IP_MASCOT_DESCRIPTION_EN,引自 references/character_ip.md}). {IP_MASCOT_NAME} must perform the core conceptual action, not decorate the scene. Make {IP_MASCOT_NAME} serious, deadpan, and slightly bizarre, not cute.

Theme:
{正文配图主题}

Structure type:
{结构类型: Workflow / System Component / Before-After Contrast / Character State / Conceptual Metaphor / Method Layering / Route Map / Comic Storyboard}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体具象画面: 详尽描述空间构图(左中右分布/视角)、低科技道具的具体材质与结构(如带手摇把的木箱/生锈齿轮/金属漏斗)、IP 角色具体身体倾角/手部动作与 deadpan 表情，以及数据/路径物理流动细节。严禁抽象概括，字数保持在 80-150 英文单词}

Suggested elements:
{具象低科技元素1} / {具象低科技元素2} / {具象低科技元素3} / {具象低科技元素4}

Chinese handwritten labels:
"{原生中文批注1,仅极少数无法图形解歧时填写}"

Color use:
Black for main line art and {IP_MASCOT_NAME}. Orange for main flow/path/arrows. Red only for key warnings/problems/results. Blue only for secondary feedback/system state.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Rely on the hand-drawn composition, IP Mascot physical action, and visual structure itself to accurately convey the text's core meaning. Do not add any random, made-up, or pseudo-characters; strictly use only the exact text labels provided in the prompt. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual presentation for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

---

## 1.1 具象提示词 vs 劣质抽象提示词标杆对比 (Concrete vs Abstract Prompt Examples)

为了防止提示词过分简单空洞，在拼装 `prompt_en` 时必须参照以下标杆：

❌ **劣质抽象提示词 (Bad Sparse Prompt - 严禁打回)**：
```text
Composition: Xiao Zhi is operating a machine. Data flows from left to right.
Suggested elements: machine / cable
```

🟢 **高质量视觉具象提示词 (Good Concrete Prompt - 标杆推荐)**：
```text
Composition: On the left side of the 16:9 canvas, a wobbly hand-drawn paper hopper collects loose data strips. In the center, a retro wooden box machine sits with an exposed iron crank and a rusty gear mechanism. Xiao Zhi (a young male engineer with messy dark hair, black-rimmed glasses, wearing a simple dark blue hoodie, deadpan blank expression) stands in the center, leaning back 30 degrees with both hands straining to pull down a large wooden lever connected to the gear. An orange dotted arrow flows out from the bottom slot of the machine, carrying neat stackable cards to the right side where a small wooden sorting tray catches them. The overall scene is sparse, clean, hand-drawn black line art on pure white paper, with generous negative white space around the top and background.
Suggested elements: hand-drawn paper hopper / retro wooden box machine with exposed rusty gears / oversized wooden lever / orange dotted flow line / small wooden sorting tray
```

---

## 2. ⚠️ 批注原生中文法则 (Native Chinese Annotation Rule)

在拼装英文 `prompt_en` 时：
- **画面风格、低科技物件、IP 角色外观与动作**：使用准确的英文描述。
- **手写批注词文本**：**必须保留在双引号 `""` 或单引号 `'...'` 内部的原生中文**（如 `"输入数据源" / "断点" / "主路径"`），**绝对禁止**将其机械翻译为英文词汇！生图模型识别双引号内的中文文本并在画面上呈现手写文字效果。

---

## 3. 图像编辑与修图提示词 (Image Editing Prompts)

当发现生成的图片存在局部瑕疵（如左上角多出了标题、角色不够怪诞）时，调用 `generate_image` 传入原图路径与以下编辑提示词进行修图：

### 剔除左上角标题 (Remove Top-Left Title)
```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

### 强化 IP 角色核心动作与怪诞感 (Enhance Absurd Action)
```text
Regenerate this illustration with the same core meaning and simple layout, but make {IP_MASCOT_NAME} more central to the conceptual action. {IP_MASCOT_NAME} should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, and not cute.
```
