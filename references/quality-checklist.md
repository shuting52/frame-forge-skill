---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: ccdcf6fbcaa4181e41cb05146c498a03_1f8f5ae7a7b511f1b67f525400dcc5b3
    ReservedCode1: 3raBB1FhEf3sv0tBhOLTkMJgt6QRyTG0USbiR1h/eSB1+nfQT2fk36WQFyYoPUP1Ta33Ax/Cx49YEzhQ35QeUY/7tGorOU8xEZPPopQ6QuP3vt+vKptzEYYnIw8yQWKHN7XTXa2jhD8Z6j3YbYEdXvfEuMEx94icWLCU9YqT/zfb2uKxUcwn9AgefMg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: ccdcf6fbcaa4181e41cb05146c498a03_1f8f5ae7a7b511f1b67f525400dcc5b3
    ReservedCode2: 3raBB1FhEf3sv0tBhOLTkMJgt6QRyTG0USbiR1h/eSB1+nfQT2fk36WQFyYoPUP1Ta33Ax/Cx49YEzhQ35QeUY/7tGorOU8xEZPPopQ6QuP3vt+vKptzEYYnIw8yQWKHN7XTXa2jhD8Z6j3YbYEdXvfEuMEx94icWLCU9YqT/zfb2uKxUcwn9AgefMg=
---

# FrameForge 质量守门清单

> 交付前逐项自检;validator.py 已对可机检项做 lint,其余项由导演人工确认。任一未通过不得交付。

## A. 视觉一致性(最高优先级)
- [ ] 人物:面孔 / 人数 / 年龄感 / 发型 / 服饰 / 身体比例与 @原图 一致
- [ ] 色彩:落在色彩锁定块内;无漂白 / 无提饱和 / 无蓝紫夜景 / 无明亮金黄
- [ ] 空间:外延画面为同一场景的逻辑扩展,无另造建筑 / 改时代 / 现代元素
- [ ] 质感:老港片胶片颗粒与柔焦表述存在,无"干净锐利数字感"

## B. 声音
- [ ] 无现代 BGM 描述
- [ ] 有空间距离法则(远景模糊带混响 / 近景清晰)
- [ ] 环境底噪恒定存在
- [ ] 对白允许被打断,无轮流念稿
- [ ] 尾声保留 1-1.5s 无对白余韵

## C. 表演与摄影
- [ ] 动作有因果链(先因后果),非无源打闹
- [ ] 群像动作差异化(有人退/挡/偷泼/只笑),无齐声笑 / 齐动作 / 全员看镜头
- [ ] 运镜纪律:仅 慢推 / 轻微漂移 / 呼吸感 / 隔物偷窥 / 短弧形 / 渐稳
- [ ] 笑点节奏:有铺垫→升级→误伤爆点(约70%)→余韵;爆点不在开头不在结尾
- [ ] 结尾无二次大爆笑

## D. 风险
- [ ] 无成人向 / 物化镜头 / 刻意性感摆拍
- [ ] 真实人物素材已获授权(必要时提示)
- [ ] 所有段均声明"以 @原图 为唯一视觉母版"

## E. 机检规则(validator.py 已内置)
- 禁用动作词:无人机环绕 / 360度旋转 / 快速变焦 / 突然升空 / 俯拍 / 慢动作(除非母版允许的"轻微运动模糊")
- 禁用风格词:现代商业广告 / 干净锐利 / 高饱和 / 蓝紫夜景 / 漂白
- 必含锁定词:保持原图 / 以参考图 / 同一庭院(实例相关)
- schema:时间码格式、必填字段、segments 数量 ≥1、时长连续
*（内容由AI生成，仅供参考）*
