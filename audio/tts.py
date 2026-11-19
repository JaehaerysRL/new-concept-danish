"""Render read-aloud scripts to audio, and optionally QA them by blind transcription.

Usage:  python audio/tts.py ncd2/L05 ncd1/L05 [--qa] [--prune]
        python audio/tts.py --all [--qa] [--prune]
        --prune  delete clips/manifest entries that no script references any more
Input:  audio/scripts/<book>/LNN.yaml, audio/cast.yaml (who -> voice)
Output: dist/practice/audio/<key16>.m4a    one file per segment (content-addressed, committed)
        audio/manifest.json                 {key16: seconds}  -- read by interactive/build.py
        audio/qa/<book>-LNN.json            with --qa: transcript + similarity per segment
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import AUDIO, OUT, client, duration, encode, segment_audio, synth, with_retry  # noqa: E402

WORKERS = 3   # Vertex TTS per-minute quotas are low; more workers mostly buys 429 retries

MANIFEST = AUDIO / "manifest.json"
QA_DIR = AUDIO / "qa"
QA_MODEL = "gemini-3.8-flash"
QA_THRESHOLD = 0.92


ONES = ["nul", "en", "to", "tre", "fire", "fem", "seks", "syv", "otte", "ni", "ti", "elleve", "tolv", "tretten",
        "fjorten", "femten", "seksten", "sytten", "atten", "nitten"]
TENS = {20: "tyve", 30: "tredive", 40: "fyrre", 50: "halvtreds", 60: "tres", 70: "halvfjerds", 80: "firs", 90: "halvfems"}


def num_da(n: int) -> str:
    """Danish number words for 0–999 (enough to compare clock times, prices and minutes in QA)."""
    if n < 20:
        return ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return (f"{ONES[o]}og" if o else "") + TENS[t * 10]
    h, rest = divmod(n, 100)
    head = "hundrede" if h == 1 else f"{ONES[h]} hundrede"
    return head + (f" og {num_da(rest)}" if rest else "")


def words(s: str) -> list[str]:
    s = s.lower().replace("é", "e").replace("kl.", "klokken")
    s = re.sub(r"\d+", lambda m: num_da(int(m.group())) if int(m.group()) < 1000 else m.group(), s)
    return re.findall(r"[a-zæøåü0-9]+", s)


def transcribe(wav: Path) -> str:
    from google.genai import types
    r = with_retry(lambda: client().models.generate_content(
        model=QA_MODEL,
        contents=[types.Part.from_bytes(data=wav.read_bytes(), mime_type="audio/wav"),
                  "Transskribér denne danske lydoptagelse ordret. Skriv tal med bogstaver. "
                  "Ret ikke fejl, og tilføj intet andet end selve teksten."],
    ), "qa")
    return (r.text or "").strip()


def main(argv: list[str]) -> int:
    qa = "--qa" in argv
    if "--all" in argv:
        scripts = sorted((AUDIO / "scripts").glob("*/L*.yaml"))
    else:
        scripts = [AUDIO / "scripts" / f"{a}.yaml" for a in argv if not a.startswith("-")]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}

    for path in scripts:
        lesson = yaml.safe_load(path.read_text(encoding="utf-8"))
        jobs = [(seg, *segment_audio(seg)) for b in lesson["blocks"] for p in b["paras"] for seg in p["segs"]
                if not seg.get("mute")]

        def run(job):
            seg, text, voice, model, key = job
            try:
                wav = synth(text, voice, model)
                encode(wav, OUT / f"{key}.m4a")
                return seg, text, voice, key, wav, None
            except Exception as e:
                return seg, text, voice, key, None, f"{type(e).__name__}: {str(e)[:200]}"

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            results = list(pool.map(run, jobs))
        fails = [r for r in results if r[5]]
        for seg, text, voice, key, wav, err in results:
            if wav:
                manifest[key] = round(duration(wav), 2)
        total = sum(manifest.get(r[3], 0) for r in results)
        print(f"  {path.parent.name}/{path.stem}: {len(results) - len(fails)}/{len(results)} segments, {total / 60:.1f} min")
        for r in fails:
            print(f"    FAIL {r[0]['id']} ({r[2]}): {r[5]}")

        if qa:
            def check(r):
                seg, text, voice, key, wav, _ = r
                try:
                    heard = transcribe(wav)
                except Exception as e:
                    return {"id": seg["id"], "voice": voice, "say": text, "heard": f"(QA failed: {str(e)[:80]})", "ratio": 0.0}
                ratio = difflib.SequenceMatcher(None, words(text), words(heard)).ratio()
                return {"id": seg["id"], "voice": voice, "say": text, "heard": heard, "ratio": round(ratio, 3)}
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                report = list(pool.map(check, [r for r in results if r[4]]))
            QA_DIR.mkdir(parents=True, exist_ok=True)
            (QA_DIR / f"{path.parent.name}-{path.stem}.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
            flagged = [x for x in report if x["ratio"] < QA_THRESHOLD]
            print(f"    QA: {len(report) - len(flagged)}/{len(report)} ok (>= {QA_THRESHOLD})")
            for x in flagged:
                print(f"    ? {x['id']} {x['ratio']}\n        say:   {x['say']}\n        heard: {x['heard']}")

    if "--prune" in argv:  # drop clips no script references any more (old voices, edited sentences)
        live = {segment_audio(seg)[3] for p in (AUDIO / "scripts").glob("*/L*.yaml")
                for b in yaml.safe_load(p.read_text(encoding="utf-8"))["blocks"] for para in b["paras"] for seg in para["segs"]}
        stale = [k for k in manifest if k not in live]
        for k in stale:
            manifest.pop(k)
        files = [f for f in OUT.glob("*.m4a") if f.stem not in live]
        for f in files:
            f.unlink()
        print(f"  pruned {len(stale)} manifest entries, {len(files)} clip files")

    MANIFEST.write_text(json.dumps(dict(sorted(manifest.items())), indent=0), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
