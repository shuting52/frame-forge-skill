# CHANGELOG

## [1.0.0] - 2026-09-04
### Added
- SKILL.md 主入口:五步工作流(视觉母版锁定 → 搞笑剧情设计 → 声音与声场 → 分镜编排 → 封装输出)
- assets/lock-blocks.md:视觉/色彩/质感/声音锁定块 + 角色功能位表(母版基因固化)
- assets/templates/:整片主 Prompt 模板、单段 Prompt 模板、segment-schema.json(v1)
- assets/examples/sample-output.json:温泉六段 30s 完整示例包
- references/platform-adapters.md:H3 / WAN 3.0 / Seedance 2.5 适配要点与参数速查
- references/quality-checklist.md:终检清单(视觉一致性/声音/表演摄影/风险)
- scripts/builder.py:导演包生成器(内置温泉母版实例,支持 --demo/--build/--platform)
- scripts/validator.py:质检器(schema 校验 + 禁用词 lint + 视觉/笑点节拍规则检查)
- scripts/config.py:平台配置与默认参数

## [Unreleased]
- 输入文件驱动(builder 支持从 yaml/json 读自定义实例)
- 平台适配器插件化注册
- 直连图生视频 API 封装(需用户 API 凭据)
