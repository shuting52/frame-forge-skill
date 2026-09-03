"""FrameForge 平台配置与默认参数。"""

# 平台适配器配置
PLATFORMS = {
    "h3": {
        "label": "MiniMax H3",
        "style": "action_order",
        "advice": "动作按先/再/随后顺序;一条一个主要动作群+一种运镜;保持项放句尾;声景可入 overall_soundscape。",
    },
    "wan3.0": {
        "label": "阿里云 WAN 3.0 (wan3.0-video)",
        "style": "timestamp",
        "advice": "Prompt 支持 [0-3秒] 分镜时间戳;首帧传原图;duration 2-30(-1 智能);resolution 480P/720P/1080P;勿用已废弃的 prompt_extend。",
    },
    "seedance2.5": {
        "label": "Seedance 2.5",
        "style": "triple",
        "advice": "I2V 三段式:【什么在动/怎么动】+【镜头运动与速度】+【氛围/声音】;不重述图中可见细节。",
    },
}

# 默认生成参数
DEFAULT_DURATION = 30
DEFAULT_PLATFORM = "all"
SUPPORTED_PLATFORMS = list(PLATFORMS.keys())

# 质检规则:禁用动作词(命中即告警)
FORBIDDEN_MOTION_WORDS = [
    "无人机环绕", "360度旋转", "360°旋转", "快速变焦", "突然升空", "突然俯拍", "大幅运镜",
]

# 质检规则:禁用风格词
FORBIDDEN_STYLE_WORDS = [
    "现代商业广告", "干净锐利", "高饱和", "蓝紫夜景", "漂白", "慢动作滥用",
]

# 质检规则:必须出现一次的锁定词(至少命中其一)
REQUIRED_LOCK_PHRASES = ["保持原图", "以参考图", "同一庭院", "视觉母版", "原图中", "与原图一致"]
