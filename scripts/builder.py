#!/usr/bin/env python3
"""FrameForge 导演包生成器。

用法:
    python3 scripts/builder.py --demo [--outdir PATH] [--platform all|h3|wan3.0|seedance2.5]
    python3 scripts/builder.py --package pkg.json --outdir PATH [--platform all|h3|wan3.0|seedance2.5]

产物:
    package.json          # 分镜 JSON 包(原输入 + main_prompt)
    prompt/main_prompt.txt
    prompt/segments.txt   # 各段直调 Prompt(按平台适配)
    director_notes.md
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from string import Template

try:
    from config import PLATFORMS, DEFAULT_PLATFORM, SUPPORTED_PLATFORMS
except ImportError:  # 允许从 skill 根目录直接运行
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import PLATFORMS, DEFAULT_PLATFORM, SUPPORTED_PLATFORMS

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE_JSON = os.path.join(SKILL_ROOT, "assets", "examples", "sample-output.json")
MAIN_TMPL = os.path.join(SKILL_ROOT, "assets", "templates", "main-prompt.tmpl")
SEG_TMPL = os.path.join(SKILL_ROOT, "assets", "templates", "segment-prompt.tmpl")

FORBIDDEN_TAIL = "禁止改变人物形象与服饰,禁止提亮漂白肤色,禁止蓝紫夜景或明亮金黄,禁止现代广告感、锐利数字感、无人机环绕、快速变焦、360度旋转、慢动作滥用。"
LOCK_TMPL = "保持原图中所有人物面孔、人数、发型、服饰与身形不变;保持同一庭院场景与布局;保持{color};保持{texture};" + FORBIDDEN_TAIL


def load_package(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_lock_sentence(pkg: dict) -> str:
    vlock = pkg.get("visual_lock", {})
    color = vlock.get("color", "原图综合色调")
    texture = vlock.get("texture", "原图质感")
    return LOCK_TMPL.format(color=color, texture=texture)


def render_main_prompt(pkg: dict, lock: str) -> str:
    with open(MAIN_TMPL, "r", encoding="utf-8") as f:
        tmpl = Template(f.read())
    color = pkg["visual_lock"].get("color", "")
    texture = pkg["visual_lock"].get("texture", "")
    seg_blocks = "\n".join(
        "[分镜段 %d | %s | %s]\n%s\n" % (s["id"], s["timecode"], s["function"], build_segment_prompt(s, lock))
        for s in pkg["segments"]
    )
    return tmpl.safe_substitute(
        master_image_line="以%s为唯一视觉母版。" % pkg["master_image"],
        visual_lock_block="【视觉母版锁定】\n- 色彩:%s\n- 质感:%s\n- 空间:%s\n" % (color, texture, pkg["visual_lock"].get("space_rule", "")),
        texture_lock_block="【全片声音总设定】无现代BGM;环境底噪恒定(水声/夜虫/竹叶);远距离人声模糊带混响,近景才清晰;对白可被水声/笑声打断;尾声保留无对白余韵。",
        sound_design_block="【人物声音】%s" % " | ".join("%s(%s)" % (c["role"], c["voice"]) for c in pkg["cast"]),
        voice_block="【全片表演纪律】大量微表情;动作有因果;群像动作差异化;禁止全员看镜头/现代短视频表演/刻意的性感摆拍/舞蹈动作。",
        performance_discipline="【全片摄影纪律】仅允许远景慢推、中景轻微漂移、长焦隔物偷窥、高潮短弧形、结尾渐稳;禁止无人机环绕、360度旋转、快速变焦、突然升空俯拍、频繁焦段跳变。",
        camera_discipline=seg_blocks,
        segments_block="",
    )


def _fmt_dialogue(d: dict) -> str:
    who, text = d.get("who", ""), d.get("text", "")
    inter = d.get("interrupt") or ""
    if inter:
        return "%s:%s(%s)" % (who, text, inter)
    return "%s:%s" % (who, text)


def build_segment_prompt(seg: dict, lock: str) -> str:
    lines = []
    lines.append("%s镜头,景别:%s。" % (seg.get("lens", ""), seg.get("shot_size", "")))
    lines.append("运镜:%s。" % seg.get("camera", ""))
    lines.append("画面:" + " ".join(seg.get("action", [])) + "。")
    dlg = seg.get("dialogue") or []
    if dlg:
        lines.append("对白:" + ";".join(_fmt_dialogue(d) for d in dlg) + "。")
    lines.append("声音:%s。" % seg.get("sfx", ""))
    lines.append("锁定:%s" % lock)
    return "".join(lines)


def adapt_segment_for_platform(seg: dict, platform: str, lock: str) -> str:
    """按平台写法适配单段 Prompt(演示级适配,规则来自 references/platform-adapters.md)。"""
    base = build_segment_prompt(seg, lock)
    if platform == "wan3.0":
        t0 = seg["timecode"].split("-")[0].replace(":", ":")
        t1 = seg["timecode"].split("-")[1].replace(":", ":")
        body = " ".join(seg.get("action", [])) + ";对白:" + ";".join(_fmt_dialogue(d) for d in (seg.get("dialogue") or []))
        cam = seg.get("camera", "")
        return "第%d个镜头[%s-%s秒]:%s。运镜:%s。环境声:%s。锁定:%s" % (
            seg["id"], t0, t1, body, cam, seg.get("sfx", ""), lock,
        )
    if platform == "seedance2.5":
        action = " ".join(seg.get("action", []))
        cam = "%s镜头,运镜:%s" % (seg.get("shot_size", ""), seg.get("camera", ""))
        atmos = "声音氛围:%s。对白:%s" % (seg.get("sfx", ""), ";".join(_fmt_dialogue(d) for d in (seg.get("dialogue") or [])))
        return "%s。%s。%s。锁定:%s" % (action, cam, atmos, lock)
    # h3 / 默认:动作顺序式
    return base


def build(pkg: dict, platform: str = DEFAULT_PLATFORM, outdir: str = "generated") -> dict:
    os.makedirs(os.path.join(outdir, "prompt"), exist_ok=True)
    lock = build_lock_sentence(pkg)
    main_prompt = render_main_prompt(pkg, lock)

    pkg_out = dict(pkg)
    pkg_out["main_prompt"] = main_prompt
    with open(os.path.join(outdir, "package.json"), "w", encoding="utf-8") as f:
        json.dump(pkg_out, f, ensure_ascii=False, indent=2)
    with open(os.path.join(outdir, "prompt", "main_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(main_prompt)

    platforms = SUPPORTED_PLATFORMS if platform == "all" else [platform]
    with open(os.path.join(outdir, "prompt", "segments.txt"), "w", encoding="utf-8") as f:
        for pf in platforms:
            f.write("======== %s ========\n" % PLATFORMS[pf]["label"])
            for seg in pkg["segments"]:
                f.write("[段%d %s %s]\n%s\n\n" % (seg["id"], seg["timecode"], seg["function"], adapt_segment_for_platform(seg, pf, lock)))
            f.write("\n")

    notes = [
        "# 导演备注",
        "- 锁定强度:高(人物 %d 位 / 场景空间已锁定)" % len(pkg.get("cast", [])),
        "- 空间扩展律:%s" % pkg["visual_lock"].get("space_rule", ""),
        "- 平台适配提示:",
    ] + ["  - %s:%s" % (pf, PLATFORMS[pf]["advice"]) for pf in platforms]
    notes.append("- 生成后用 validator.py 做终检。")
    with open(os.path.join(outdir, "director_notes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(notes) + "\n")

    return {"outdir": outdir, "package": os.path.join(outdir, "package.json"), "platforms": platforms}


def main() -> int:
    ap = argparse.ArgumentParser(description="FrameForge 导演包生成器")
    ap.add_argument("--demo", action="store_true", help="生成内置温泉母版示例")
    ap.add_argument("--package", help="输入分镜 JSON 包路径")
    ap.add_argument("--outdir", default="generated", help="产物目录(默认 generated/)")
    ap.add_argument("--platform", default=DEFAULT_PLATFORM, choices=["all"] + SUPPORTED_PLATFORMS)
    args = ap.parse_args()

    if args.demo:
        pkg = load_package(EXAMPLE_JSON)
    elif args.package:
        pkg = load_package(args.package)
    else:
        ap.error("请提供 --demo 或 --package")
    res = build(pkg, args.platform, args.outdir)
    print("FrameForge build OK")
    print("  package     : %s" % res["package"])
    print("  main_prompt : %s" % os.path.join(res["outdir"], "prompt", "main_prompt.txt"))
    print("  segments    : %s" % os.path.join(res["outdir"], "prompt", "segments.txt"))
    print("  notes       : %s" % os.path.join(res["outdir"], "director_notes.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
