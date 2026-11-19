"""Build the offline interactive practice site from YAML exercise banks.

Usage:  python interactive/build.py
Input:  interactive/data/<book>/L<NN>.yaml
        audio/scripts/<book>/L<NN>.yaml + audio/manifest.json   (optional: lesson texts with audio)
Output: dist/practice/index.html  (single self-contained file, works via file://;
        audio clips, when present, are loaded from dist/practice/audio/ next to it)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
TEMPLATE = ROOT / "template.html"
OUT_FILE = ROOT.parent / "dist" / "practice" / "index.html"
AUDIO_DIR = ROOT.parent / "audio"
SCRIPTS_DIR = AUDIO_DIR / "scripts"
MANIFEST = AUDIO_DIR / "manifest.json"

sys.path.insert(0, str(AUDIO_DIR))

# Fields each item must carry, per section type.
REQUIRED = {
    "flashcards": ("cards", ("da", "zh")),
    "order": ("items", ("zh", "answer")),
    "transform": ("items", ("source", "stem", "accept")),
    "correct": ("items", ("wrong", "accept")),
    "translate": ("items", ("zh", "accept")),
    "drill": ("items", ("prompt", "kind")),
    "text": ("paras", ("segs",)),
}
TEXT_TAB = {"dialog": "课文", "prose": "课文", "qa": "课文", "words": "生词表"}


def speak_key(s: str) -> str:
    """Normalisation shared with template.html's speakKey(): lower-case, no markup or punctuation."""
    s = re.sub(r"[*\[\]⟦⟧]", "", s).lower()
    return re.sub(r"\s+", " ", re.sub(r"[.,!?;:\"“”„]", "", s)).strip()


def text_sections(lesson: dict, manifest: dict) -> tuple[list[dict], dict]:
    """Turn the lesson's read-aloud script into 'text' sections; return them plus {speak_key: clip}."""
    path = SCRIPTS_DIR / lesson["book"] / f"L{int(lesson['lesson']):02d}.yaml"
    if not path.exists():
        return [], {}
    from common import segment_audio  # audio/common.py (needs audio/cast.yaml)

    script = yaml.safe_load(path.read_text(encoding="utf-8"))
    sections, clips = [], {}
    for block in script["blocks"]:
        for para in block["paras"]:
            for seg in para["segs"]:
                if seg.get("mute"):        # exam gap like "(1) ___": shown, not spoken
                    continue
                key = segment_audio(seg)[3]
                if key in manifest:
                    seg["a"], seg["dur"] = key, manifest[key]
                    clips.setdefault(speak_key(seg["da"]), key)
        sections.append({"id": f"text-{block['id']}", "type": "text", "kind": block["kind"],
                         "tab": block.get("tab") or TEXT_TAB[block["kind"]],
                         "title": block["title"], "scene": block.get("scene"), "paras": block["paras"]})
    return sections, clips
BLANK = "{{_}}"


def validate_drill_item(item: dict, where: str) -> list[str]:
    kind = item.get("kind")
    if kind == "cloze":
        blanks = item.get("blanks") or []
        if item["prompt"].count(BLANK) != len(blanks):
            return [f"{where}: {item['prompt'].count(BLANK)} blanks in prompt vs {len(blanks)} answers"]
        if any(not alts for alts in blanks):
            return [f"{where}: empty blank answer list"]
        return []
    if kind == "write":
        return [] if item.get("accept") else [f"{where}: write item without 'accept'"]
    return [f"{where}: unknown kind '{kind}'"]


def validate(lesson: dict, path: Path) -> list[str]:
    errors: list[str] = []
    for key in ("book", "lesson", "title_da", "sections"):
        if key not in lesson:
            errors.append(f"{path.name}: missing top-level '{key}'")
    seen_ids: set[str] = set()
    for s_idx, section in enumerate(lesson.get("sections", [])):
        where = f"{path.name} section[{s_idx}]"
        sid, stype = section.get("id"), section.get("type")
        if not sid:
            errors.append(f"{where}: missing 'id'")
        elif sid in seen_ids:
            errors.append(f"{where}: duplicate id '{sid}'")
        seen_ids.add(sid)
        if stype not in REQUIRED:
            errors.append(f"{where}: unknown type '{stype}'")
            continue
        list_key, fields = REQUIRED[stype]
        items = section.get(list_key)
        if not items:
            errors.append(f"{where} ({sid}): empty '{list_key}'")
            continue
        for i_idx, item in enumerate(items):
            for field in fields:
                value = item.get(field)
                if value in (None, "", []):
                    errors.append(f"{where} ({sid}) item {i_idx + 1}: missing '{field}'")
            if "accept" in item and not isinstance(item["accept"], list):
                errors.append(f"{where} ({sid}) item {i_idx + 1}: 'accept' must be a list")
            if stype == "drill" and item.get("prompt"):
                errors += validate_drill_item(item, f"{where} ({sid}) item {i_idx + 1}")
    return errors


def main() -> int:
    files = sorted(DATA_DIR.glob("*/L*.yaml"))
    if not files:
        print(f"No exercise banks found under {DATA_DIR}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    lessons, errors = [], []
    for path in files:
        lesson = yaml.safe_load(path.read_text(encoding="utf-8"))
        texts, clips = text_sections(lesson, manifest)
        if texts:
            lesson["sections"] = texts + lesson["sections"]
            lesson["clips"] = clips
        errors += validate(lesson, path)
        lesson["key"] = f"{lesson['book']}-L{int(lesson['lesson']):02d}"
        lessons.append(lesson)

    if errors:
        print("Exercise bank validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    payload = json.dumps(lessons, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__NCD_DATA__*/[]", payload)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(html, encoding="utf-8")

    for lesson in lessons:
        counts = []
        for s in lesson["sections"]:
            list_key = REQUIRED[s["type"]][0]
            if s["type"] == "text":
                segs = [g for p in s["paras"] for g in p["segs"]]
                counts.append(f"{s['id']}={len(segs)}({sum('a' in g for g in segs)}🔊)")
                continue
            counts.append(f"{s['id']}={len(s[list_key])}")
        print(f"  {lesson['key']}: {', '.join(counts)}")
    print(f"Wrote {OUT_FILE.relative_to(ROOT.parent)} ({len(lessons)} lesson(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
