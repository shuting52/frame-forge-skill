---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: ccdcf6fbcaa4181e41cb05146c498a03_1f0f4e60a7b511f1b67f525400dcc5b3
    ReservedCode1: GqjDVDtowPENuLMp96yBz84zyN69DSB1zP6pU0Yu2AqczRpycN5R+B+a2sh5NLU4jG1dKCZDLf7bOqtsHl8JpFPWG85nPDKoizkmqdGmVnhu2pE3+/q6f3BkfcdOEm5VTAYlVnmJvmHT9xHoWxT80oj9v8R7QS55Qop2I/HqvswALPoEl+boI7ORAtg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: ccdcf6fbcaa4181e41cb05146c498a03_1f0f4e60a7b511f1b67f525400dcc5b3
    ReservedCode2: GqjDVDtowPENuLMp96yBz84zyN69DSB1zP6pU0Yu2AqczRpycN5R+B+a2sh5NLU4jG1dKCZDLf7bOqtsHl8JpFPWG85nPDKoizkmqdGmVnhu2pE3+/q6f3BkfcdOEm5VTAYlVnmJvmHT9xHoWxT80oj9v8R7QS55Qop2I/HqvswALPoEl+boI7ORAtg=
---

# 平台适配器 — H3 / WAN 3.0 / Seedance 2.5

> 图生视频的图已提供主体/布局/颜色,Prompt 不重复图中可见细节,把篇幅留给动作顺序、运镜、氛围与锁定项。

## 1. 平台脾气对照

| 平台 | 单条建议时长 | 声音 | 关键写法 | 复用形象方式 |
|---|---|---|---|---|
| MiniMax H3 | 5-12s | 支持时间线结构写声景/对白 | 公式:主体动作按"先→再→随后"顺序 + 镜头 + 光线风格 + 句尾限制;一条一个主要动作群 + 一种运镜 | 每段都传同一张原图作起始图 |
| 阿里云 WAN 3.0 (wan3.0-video) | 10-15s(上限30s) | audio 参数开关;Prompt 支持分镜时间戳 | 动作 + 机位运动 + 锁定;`[0-3秒]` 时间戳分段;首尾帧模式写两帧之间变化 | 首帧传原图(必要时末帧同图),parameters: resolution 480P/720P/1080P、duration 2-30s(-1 智能)、ratio 由首帧决定 |
| Seedance 2.5 | 5-10s | 按平台实际能力,弱则后期配音 | I2V 三段式:【什么在动/怎么动】+【镜头运动与速度】+【氛围/声音】 | 每段传同一张起始图 |

## 2. H3 写法模板(图生视频)

> 以参考图为起始画面,{动作顺序句}。{镜头句}。{氛围/声音句}。保持{锁定对象};不要{禁止项}。

H3 时间线结构(如需对白/声景稳出):正文写画面动作,声景写入 overall_soundscape 字段;无对白需求不必写满三字段。

## 3. WAN 3.0 写法模板(图生视频)

> 第1个镜头[{t0}-{t1}秒]:{动作+机位+氛围}。
> 第2个镜头[{t1}-{t2}秒]:{动作+机位+氛围}。
> 环境声:{声景}。保持{锁定对象};不要{禁止项}。

参数:input.media 传首帧原图;parameters: duration 建议 10-15(可 -1 智能)、resolution 720P/1080P、audio 开启(平台支持时);prompt_extend 已废弃不要用。

## 4. Seedance 2.5 写法模板(图生视频)

> {对象}{动作方式}。{镜头类型/运动/速度}。{氛围:光/蒸汽/颗粒/环境声与对白情绪}。保持{锁定对象};不要{禁止项}。

## 5. 全平台通用视觉锁定句(拼每条 Prompt 末尾)

保持原图中所有人物面孔、人数、发型、服饰与身形不变;保持同一场景结构与布局;保持{实例色彩锁定}与{实例质感锁定};禁止改变人物形象与服饰,禁止提亮漂白肤色,禁止蓝紫夜景或明亮金黄,禁止现代广告感、锐利数字感、无人机环绕、快速变焦、360度旋转、慢动作滥用。

## 6. 声音兜底策略

若平台音轨对白还原不理想:画面按无声/环境声版生成,对白按台词总表后期配音;环境底噪(泉水/夜虫/竹叶)可在剪辑软件铺一层,保证空间层次。
*（内容由AI生成，仅供参考）*
