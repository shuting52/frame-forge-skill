---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: ccdcf6fbcaa4181e41cb05146c498a03_1e2ce2eca7b511f1ac80525400aeaaa3
    ReservedCode1: xh/Wl60eJ2Onjt3u4GBFNLVgkKGUs362VD02973111aNCOedFH2IJ9f+WFqXhfghlCVTGq3HVQ/aoWc0mmUr0WJ+5mI5UiGxtVpsD8IJfrnxRSH2f6UC5k4JpZd6ptZg/J5AERu/8vCXbRSWliuMnx5OQQ5/M+LEeWdQQRDdfQMDRnUezH72yAIjIgw=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: ccdcf6fbcaa4181e41cb05146c498a03_1e2ce2eca7b511f1ac80525400aeaaa3
    ReservedCode2: xh/Wl60eJ2Onjt3u4GBFNLVgkKGUs362VD02973111aNCOedFH2IJ9f+WFqXhfghlCVTGq3HVQ/aoWc0mmUr0WJ+5mI5UiGxtVpsD8IJfrnxRSH2f6UC5k4JpZd6ptZg/J5AERu/8vCXbRSWliuMnx5OQQ5/M+LEeWdQQRDdfQMDRnUezH72yAIjIgw=
---

# FrameForge「图锁·笑剧引擎」Skill 包

> 开局一张图,剧情全靠编。以参考图(@原图)为唯一视觉母版,产出可投喂 H3 / WAN 3.0 / Seedance 2.5 的导演级搞笑剧情视频包。

## 一、这是什么

一个可安装、可校验、可复用的 Agent Skill 包。不是一篇文档,而是一个含主入口、资源库、模板、脚本、示例、质检器的完整工作流。

## 二、目录结构

```
frame-forge-skill/
├── SKILL.md                        # 主入口(元信息 + 五步工作流),平台加载入口
├── README.md                       # 本文件
├── CHANGELOG.md                    # 版本记录
├── assets/
│   ├── lock-blocks.md              # 视觉/色彩/质感/声音锁定块 + 角色功能位(公共约束库)
│   ├── templates/
│   │   ├── segment-prompt.tmpl     # 单段 Prompt 渲染模板(string.Template)
│   │   ├── main-prompt.tmpl        # 整片主 Prompt 渲染模板
│   │   └── segment-schema.json     # 分镜 JSON Schema(v1)
│   └── examples/
│       └── sample-output.json      # 温泉六段 30s 完整示例包(生产可用)
├── references/
│   ├── platform-adapters.md        # H3 / WAN3.0 / Seedance2.5 适配要点与参数表
│   └── quality-checklist.md        # 质量守门清单(视觉/声音/表演/摄影/风险)
└── scripts/
    ├── __init__.py
    ├── config.py                   # 平台配置与默认参数
    ├── builder.py                  # 导演包生成器(渲染模板→整片/分段输出)
    └── validator.py                # 质检器(schema 校验 + 质量守门 lint)
```

## 三、安装

1. 将 `frame-forge-skill/` 整个目录放入平台的技能目录(本机为 `/app/AgentCore/skills/`),即得到 `/app/AgentCore/skills/frame-forge-skill/`。
2. 平台加载新技能后(按平台规则刷新/注册),即可通过技能名 `frame-forge-comedy-skit` 触发。
3. 命令行快速验证:
   ```bash
   python3 scripts/builder.py --demo        # 生成温泉六段示例导演包
   python3 scripts/builder.py --build out.json --platform wan3.0
   python3 scripts/validator.py out.json     # 终检
   ```

## 四、使用方式

### 4.1 作为 Agent Skill(推荐)
对话中上传参考图并说"按这张图编一段搞笑温泉剧情做成视频 Prompt",主控 Agent 加载 SKILL.md 后按五步流程执行,产出三件套交付物。

### 4.2 作为命令行工具
```bash
# 生成默认温泉实例导演包(整片 prompt + 分段 json 写入 output/)
python3 scripts/builder.py --demo

# 自定义参数构建(后续版本支持从输入文件读实例)
python3 scripts/builder.py --build package.json --platform all
```

### 4.3 模板与脚本约定
- 模板文件使用 Python 标准库 `string.Template` 语法:`${variable}`;脚本优先用标准库,零第三方依赖。
- 分镜 JSON 必须通过 `validator.py`,否则视为不合格交付。

## 五、输出物规范

每次完整执行产出:
1. `package.json` — 分镜 JSON 包(整片主 prompt、分段数组、cast、storyline、visual_lock)
2. `prompt/main_prompt.txt` — 整片主 Prompt 纯文本(可直接复制投喂)
3. `prompt/segment_NN.txt` — 每段直调 Prompt
4. `director_notes.md` — 导演备注(锁定强度 / 扩展边界 / 参数取舍 / 风险提示)

## 六、迭代方向

- 输入文件驱动:支持从 `input.yaml/json` 定义任意新实例(人物/场景/剧情)。
- 平台适配器插件化:新增视频模型只需在 `config.py` 注册写法规则。
- 直连图生视频 API 封装(需用户提供 API 凭据)。
*（内容由AI生成，仅供参考）*
