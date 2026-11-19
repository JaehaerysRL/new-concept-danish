"""Voice audition: render the same Danish passage with many Gemini TTS voices for side-by-side listening.

Usage:  python audio/voices.py [--models gemini-3.8-flash-tts]
Output: audio/out/voices/index.html + one .m4a per (model, voice)   (git-ignored)
"""

from __future__ import annotations

import argparse
import html
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import AUDIO, duration, encode, synth  # noqa: E402

MALE = ["Charon", "Orus", "Fenrir", "Puck", "Enceladus", "Iapetus", "Umbriel", "Algieba",
        "Algenib", "Rasalgethi", "Alnilam", "Schedar", "Achird", "Zubenelgenubi", "Sadachbia", "Sadaltager"]
FEMALE = ["Kore", "Aoede", "Leda", "Sulafat", "Achernar", "Vindemiatrix"]

PASSAGE = ("Om morgenen kører bussen hvert tiende minut, men i weekenden kører den kun én gang i timen. "
           "Maja møder klokken syv og tjener hundrede og femogtredive kroner i timen. "
           "Ved du, hvornår hun skal møde, og om kollegerne er søde?")

OUT_DIR = AUDIO / "out" / "voices"


def render(job: tuple[str, str]) -> tuple[str, str, str | None, float, str | None]:
    model, voice = job
    try:
        wav = synth(PASSAGE, voice, model)
        m4a = encode(wav, OUT_DIR / f"{model}__{voice}.m4a")
        return model, voice, m4a.name, duration(wav), None
    except Exception as e:
        return model, voice, None, 0.0, f"{type(e).__name__}: {str(e)[:160]}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="gemini-3.8-flash-tts")
    args = ap.parse_args()
    models = args.models.split(",")
    jobs = [(m, v) for m in models for v in MALE + FEMALE]
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(render, jobs))

    rows = []
    for model in models:
        for group, names in (("男声", MALE), ("女声", FEMALE)):
            cells = []
            for m, v, f, dur, err in results:
                if m != model or v not in names:
                    continue
                body = (f'<audio controls preload="none" src="{html.escape(f)}"></audio><small>{dur:.1f}s</small>'
                        if f else f'<small class="err">{html.escape(err or "")}</small>')
                cells.append(f'<div class="cell"><b>{v}</b>{body}</div>')
            rows.append(f"<h2>{html.escape(model)} · {group}</h2><div class=grid>{''.join(cells)}</div>")
    page = f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>NCD 声音试听</title>
<style>
:root{{--bg:#fff;--fg:#1d2433;--card:#f3f5f9;--muted:#667}}
@media (prefers-color-scheme:dark){{:root{{--bg:#14171d;--fg:#e6e9ef;--card:#1f242d;--muted:#99a}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0 auto;max-width:1100px;padding:16px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}}
.cell{{background:var(--card);border-radius:8px;padding:10px;display:flex;flex-direction:column;gap:6px}}
audio{{width:100%}} small{{color:var(--muted)}} .err{{color:#c33}} blockquote{{color:var(--muted)}}
</style>
<h1>NCD 声音试听</h1><blockquote>{html.escape(PASSAGE)}</blockquote>{''.join(rows)}"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.html").write_text(page, encoding="utf-8")
    ok = sum(1 for r in results if r[2])
    for m, v, f, dur, err in results:
        if err:
            print(f"  FAIL {m} {v}: {err}")
    print(f"{ok}/{len(results)} rendered -> {OUT_DIR / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
