# 4 轨讲解脚本规范范例 (Four-Track Explainer Script Example)

本文件展示符合 `references/script_schema.json` 规范的标准 4 轨讲解脚本范例 JSON 内容。

```json
{
  "metadata": {
    "title": "Vue 3.5 响应式原理与双向绑定降维解构",
    "target_duration_seconds": 60,
    "genre": "科普解说",
    "mode": "article_derived",
    "source_article_path": "./vue35-reactivity/vue35-reactivity.md"
  },
  "units": [
    {
      "unit_id": "Unit 01",
      "duration_seconds": 5,
      "voiceover": "为什么你的 Vue 界面能自动更新？秘密藏在每一个数据的微小变化里。",
      "visual_prompt": "16:9 纯白背景，黑色手绘线条风格，左侧为繁复的数据网格，右侧为发光的界面屏幕。",
      "ip_action": "IP Mascot 角色站在数据网格旁，神情认真冷静（Deadpan），手持一根发光线缆连接数据点与屏幕。",
      "on_screen_elements": {
        "title_card": "Vue 3.5 响应式机制",
        "highlight_keywords": ["自动更新", "微小变化"],
        "graphics_hint": "显示 Vue Logo 浮动，数据流动箭头动画"
      }
    },
    {
      "unit_id": "Unit 02",
      "duration_seconds": 8,
      "voiceover": "在旧版 Vue 中，响应式就像一个无休止拉取消息的轮询管道，既吃内存又容易阻塞。",
      "visual_prompt": "16:9 清爽高对比背景，展示粗暴笨重的轮询齿轮与剧烈震动堵塞的数据管道，管壁持续冒出红色过载蒸汽脉冲。",
      "ip_action": "IP Mascot 角色在震动的平台上手握摇杆，奋力转动巨大齿轮阀门，配合阀门自转与蒸汽喷出产生物理排气响应。",
      "on_screen_elements": {
        "title_card": null,
        "highlight_keywords": ["吃内存", "阻塞"],
        "graphics_hint": "齿轮狂转震动 & 管道过载蒸汽喷出动画"
      }
    },
    {
      "unit_id": "Unit 03",
      "duration_seconds": 7,
      "voiceover": "而 Vue 3.5 {重|chóng}构了反应式双向链表，内存占用骤{降|jiàng} 56%，更新性能直接拉满。",
      "visual_prompt": "16:9 纯白背景，线条变得精简清爽，两条并行自愈的发光双向链表横跨画面。",
      "ip_action": "IP Mascot 角色轻巧地将两块双向插头锁扣踩入槽位，手持钢印在数据节点上盖上 [56% OFF] 绿色印章。",
      "on_screen_elements": {
        "title_card": null,
        "highlight_keywords": ["内存骤降 56%", "性能拉满"],
        "graphics_hint": "内存对比柱状图从 100% 降至 44%"
      }
    },
    {
      "unit_id": "Unit 04",
      "duration_seconds": 25,
      "voiceover": "这就好比把传统的漫长排队大厅改造为了智能分流窗口。当数据发生变动时，系统不再通知所有无关节点，而是通过双向链表精准找到订阅者，实现毫秒级响应。",
      "visual_prompt": "16:9 纯白背景。[0-10s] 拥挤的办事大厅与长队伍 ➔ [10-20s] 墙面结构重组变为智能分流闸机与精准光束 ➔ [20-25s] 毫秒计时器弹显与绿色通路通畅图景。",
      "ip_action": "IP Mascot 角色在不同阶段执行动作：[0-10s] 手持指示牌劝导拥挤队伍 ➔ [10-20s] 拉动分流杠杆，启动精准光束导轨 ➔ [20-25s] 在闸机旁按下绿色通行按钮并展示 [0.1ms] 仪表盘。",
      "on_screen_elements": {
        "title_card": null,
        "highlight_keywords": ["智能分流", "毫秒级响应"],
        "graphics_hint": "办事大厅变闸机动画 & 0.1ms 计时卡片"
      }
    },
    {
      "unit_id": "Unit 05",
      "duration_seconds": 5,
      "voiceover": "深度完整拆解，留言或者私信获取吧。如果对你有启发，记得点赞关注，我们下期见！",
      "visual_prompt": "16:9 纯白背景，中央弹起发光的 [点赞] [收藏] [关注] 三连交互徽章，四周伴随欢快的星光与爱心粒子。",
      "ip_action": "IP Mascot 角色开心地原地向上小跃（[Action Recipe: LIKE_AND_SUBSCRIBE]），双臂向上高举并指向三个互动徽章，做热情的点赞关注招手引导动作。",
      "on_screen_elements": {
        "title_card": null,
        "highlight_keywords": ["点赞关注"],
        "graphics_hint": "点赞、收藏、关注三连徽章弹性弹出动画"
      }
    }
  ]
}
```
