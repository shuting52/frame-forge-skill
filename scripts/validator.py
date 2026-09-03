#!/usr/bin/env python3
"""FrameForge 质检器(schema 校验 + 质量守门 lint)。

用法:
    python3 scripts/validator.py package.json [--demo-json assets/examples/sample-output.json]
退出码:0 通过;1 存在错误;2 存在警告(不阻断)。

机检项:
    A. schema:必填键 / 时间码格式 / 分段连续
    E1. 禁用动作词(无人机环绕/360度旋转/快速变焦/突然升空俯拍等)
    E2. 禁用风格词(现代广告/锐利/高饱和/蓝紫/漂白等)
    E3. 必含锁定词(保持原图/以参考图等至少其一)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

try:
    from config import FORBIDDEN_MOTION_WORDS, FORBIDDEN_STYLE_WORDS, REQUIRED_LOCK_PHRASES
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import FORBIDDEN_MOTION_WORDS, FORBIDDEN_STYLE_WORDS, REQUIRED_LOCK_PHRASES

REQUIRED_TOP = ["schema_version", "master_image", "total_duration", "visual_lock", "cast", "storyline", "segments"]
REQUIRED_SEG = ["id", "timecode", "function", "lens", "shot_size", "camera", "action", "sfx", "visual_note"]
TIMECODE_RE = re.compile(r"^\d{2}:\d{2}-\d{2}:\d{2}$")


def check_schema(pkg: dict) -> list[str]:
    errors = []
    for key in REQUIRED_TOP:
        if key not in pkg:
            errors.append("[schema] 缺少顶层字段: %s" % key)
    if pkg.get("schema_version") != "1.0":
        errors.append("[schema] schema_version 必须为 1.0")
    if not isinstance(pkg.get("cast"), list) or len(pkg.get("cast", [])) < 2:
        errors.append("[schema] cast 至少 2 人")
    segs = pkg.get("segments") or []
    if not segs:
        errors.append("[schema] segments 不能为空")
    prev_end = None
    for s in segs:
        for key in REQUIRED_SEG:
            if key not in s:
                errors.append("[schema] 段%d 缺少字段: %s" % (s.get("id", "?"), key))
        if not TIMECODE_RE.match(s.get("timecode", "")):
            errors.append("[schema] 段%d 时间码格式错误: %s" % (s.get("id", "?"), s.get("timecode")))
        else:
            start, end = s["timecode"].split("-")
            if prev_end is not None and start != prev_end:
                errors.append("[schema] 段%d 时间不连续: 期望从 %s 开始" % (s.get("id", "?"), prev_end))
            prev_end = end
    return errors


def lint_text(text: str) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    for w in FORBIDDEN_MOTION_WORDS:
        if w in text:
            errors.append("[lint] 命中禁用动作词: %s" % w)
    for w in FORBIDDEN_STYLE_WORDS:
        if w in text:
            errors.append("[lint] 命中禁用风格词: %s" % w)
    if not any(p in text for p in REQUIRED_LOCK_PHRASES):
        warnings.append("[lint] 未命中锁定词(保持原图/以参考图/同一庭院等),请确认已含视觉锁定声明")
    return errors, warnings


def _segments_text(pkg: dict) -> str:
    parts = []
    for s in pkg.get("segments", []):
        parts.append(s.get("camera", ""))
        parts.append(" ".join(s.get("action", [])))
        parts.append(s.get("sfx", ""))
        parts.append(s.get("visual_note", ""))
        for d in s.get("dialogue") or []:
            parts.append(d.get("text", ""))
    return " ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description="FrameForge 质检器")
    ap.add_argument("package", nargs="?", default="", help="分镜 JSON 包路径(或 --demo-json)")
    ap.add_argument("--demo-json", action="store_true", help="校验内置示例包")
    args = ap.parse_args()

    if args.demo_json:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "examples", "sample-output.json")
    else:
        path = args.package
    if not os.path.exists(path):
        print("文件不存在: %s" % path)
        return 1

    with open(path, "r", encoding="utf-8") as f:
        pkg = json.load(f)

    errors = check_schema(pkg)
    lint_errors, warnings = lint_text(_segments_text(pkg))
    errors += lint_errors
    lock_obj = pkg.get("visual_lock", {})
    for key in ["color", "texture", "space_rule"]:
        if key not in lock_obj or not str(lock_obj.get(key, "")).strip():
            warnings.append("[schema] visual_lock.%s 为空,视觉锁定不完整" % key)

    for e in errors:
        print("[FAIL] %s" % e)
    for w in warnings:
        print("[WARN] %s" % w)
    print("结果: %d 错误, %d 警告" % (len(errors), len(warnings)))
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
