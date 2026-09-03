---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: ccdcf6fbcaa4181e41cb05146c498a03_1da8db2ea7b511f1b87f525400461939
    ReservedCode1: hqVQ4/A+GVnpDarsSreVozhvI8XPGJGp2/IkVn3415UroT4ZUcUPnxWKRdAxoxDNc2w5z0YYlhWtVqb6S9cWbTcnzYo2JeN0RR2+gPEiEnzG40p/YGAbuT8HMJ+AszWUMR4K18WgTnacsALvyh9IIW4phjoJHfOS8bfNMLi+ZwqwhI/h/cnf/jJS4SM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: ccdcf6fbcaa4181e41cb05146c498a03_1da8db2ea7b511f1b87f525400461939
    ReservedCode2: hqVQ4/A+GVnpDarsSreVozhvI8XPGJGp2/IkVn3415UroT4ZUcUPnxWKRdAxoxDNc2w5z0YYlhWtVqb6S9cWbTcnzYo2JeN0RR2+gPEiEnzG40p/YGAbuT8HMJ+AszWUMR4K18WgTnacsALvyh9IIW4phjoJHfOS8bfNMLi+ZwqwhI/h/cnf/jJS4SM=
---



# FrameForge「图锁·笑剧引擎」— SKILL 主入口

> 一句话:锁死 @原图 的世界,然后在里面编一场因果连贯的搞笑戏。

## 1. 职责边界

- 本技能负责:图锁拆解 → 搞笑剧情设计 → 视听语言封装 → 输出可投喂视频模型的导演包。
- 本技能不负责:视频生成本身、素材授权、色情低俗内容。涉及真实人物须提示授权。
- 锁定优先:画面离开参考图范围时只允许合理外延同一场景,禁止另造世界、禁止改时代、禁止混入现代元素。

## 2. 工作流程(严格按序执行)

### Step 1 视觉母版锁定
读取用户提供的参考图,抽取并写入 assets/lock-blocks.md 规定的四张锁定块:
1. 人物指纹(面孔/人数/年龄感/发型/服饰/比例)
2. 空间指纹(结构/可扩展边界图)
3. 色彩锁定块 + 质感锁定块(模板在 assets/lock-blocks.md)
4. 曝光关系与镜头年代感

若图片信息不足,降级声明"锁定强度降级"并向用户索取缺失关键项。

### Step 2 搞笑剧情设计
套用角色功能位(assets/lock-blocks.md 的"功能位表"),从冲突单元配方(误解/还施彼身/拱火/甩锅)中选择组合;按"铺垫→小冲突→升级→误伤爆点→余韵"布点,爆点放在全片约 70% 处;结尾禁止二次大爆笑。用户给了 humor_direction 就织入冲突单元,否则走默认"嘴仗-误伤-和解"。

### Step 3 声音与声场
参考 assets/lock-blocks.md 的声景分层与距离法则:无现代 BGM;环境底噪恒定;远→近声音距离渐变;对白允许被水声/笑声/惊呼打断,禁止轮流念稿。

### Step 4 分镜编排
按 assets/templates/segment-schema.json 输出分段 JSON,每段含 9 个字段(timecode/function/lens/shot_size/camera/action/dialogue/sfx/visual_note)。运镜与表演纪律见 references/quality-checklist.md,全片硬约束,不可弱化。

### Step 5 封装输出
- 运行 `python3 scripts/builder.py --build` 生成整片主 Prompt 与分段 JSON(内部已内置温泉六段示例实例)。
- 按用户指定 platform 输出直调文案;platform 适配规则见 references/platform-adapters.md。
- 运行 `python3 scripts/validator.py <package.json>` 做终检,全部通过后才可交付。

## 3. 交付格式

- 交付物固定三件套:整片主 Prompt / 分镜 JSON 包 / 平台直调文案(含导演备注)。
- 分镜 JSON 必须通过 validator 校验;质量守门清单须逐项自检通过。

## 4. 内置示例实例

温泉庭院夜戏(六名女子 / 30s / 90 年代港片质感)已作为默认实例固化在 scripts/builder.py 与 assets/examples/sample-output.json 中,可直接 `--demo` 复现母版,也作为一切自定义实例的结构范本。

## 5. 更新记录

见 CHANGELOG.md。
*（内容由AI生成，仅供参考）*
