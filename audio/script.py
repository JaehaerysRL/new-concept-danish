"""Extract read-aloud scripts (朗读稿) from lesson .tex files.

Usage:  python audio/script.py ncd2/L05 ncd1/L05      # specific lessons
        python audio/script.py --all                  # every lesson
Output: audio/scripts/<book>/LNN.yaml   (files whose first line is '# hand-made' are never overwritten)

Script schema
  book, lesson, title_da
  blocks: list of
    id, title, kind (dialog | prose | qa | words), scene (optional, zh)
    paras: list of
      zh (translation, optional), note (pronunciation note, optional), cue (optional label)
      segs: list of {id, who, da, say?}
        da   display text; **x** = \\dabold (word order focus), [[x]] = \\da (highlight)
        say  what the TTS actually reads, when it must differ from da (numbers, abbreviations…)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "interactive"))
from extract import flatten, read_group, strip_comments  # noqa: E402

OUT = ROOT / "audio" / "scripts"
HAND_MADE = "# hand-made"
CJK = re.compile(r"[\u3400-\u9fff]")
B_OPEN, B_CLOSE, H_OPEN, H_CLOSE = "\x01", "\x02", "\x03", "\x04"


# ---------------------------------------------------------------- tex helpers
def mark_emphasis(s: str) -> str:
    """\\dabold{x} -> **x**, \\da{x} -> [[x]] (via control chars that survive flatten)."""
    out, i = [], 0
    while i < len(s):
        m = re.compile(r"\\(dabold|da)\{").match(s, i)
        if m:
            arg, j = read_group(s, m.end() - 1)
            inner = mark_emphasis(arg)
            out.append(f"{B_OPEN}{inner}{B_CLOSE}" if m.group(1) == "dabold" else f"{H_OPEN}{inner}{H_CLOSE}")
            i = j
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def text(s: str) -> str:
    t = flatten(mark_emphasis(s), italic=False).replace("{{_}}", "___")
    t = t.replace(B_OPEN, "**").replace(B_CLOSE, "**").replace(H_OPEN, "[[").replace(H_CLOSE, "]]")
    t = t.replace("[[ ", " [[").replace(" ]]", "]] ").replace("** **", " ")
    return re.sub(r"\s+", " ", t).strip()


def bare(da: str) -> str:
    return da.replace("**", "").replace("[[", "").replace("]]", "")


def drop_env(s: str, env: str) -> str:
    return re.sub(rf"\\begin\{{{env}\}}.*?\\end\{{{env}\}}", "", s, flags=re.S)


def env_bodies(s: str, env: str) -> list[str]:
    return re.findall(rf"\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}", s, flags=re.S)


def sentences(par: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[\"”A-ZÆØÅ])|(?<=[.!?]”)\s+", par)
    return [p.strip() for p in parts if p and p.strip()]


def section(tex: str, title_prefix: str) -> str:
    """Body of the \\ncdsubsec whose title starts with title_prefix, up to the next \\ncdsubsec."""
    m = re.search(r"\\ncdsubsec\{" + re.escape(title_prefix), tex)
    if not m:
        return ""
    nxt = tex.find("\\ncdsubsec{", m.end())
    return tex[m.start(): nxt if nxt > 0 else len(tex)]


# ---------------------------------------------------------------- block parsers
def strip_notes(s: str) -> str:
    """Drop parenthesised Chinese notes such as （ikke 前移！） or (光疗灯) from a Danish line."""
    s = re.sub(r"（[^（）]*[㐀-鿿][^（）]*）", "", s)
    s = re.sub(r"\s*\([^()]*[㐀-鿿][^()]*\)", "", s)
    return re.sub(r"^\[\d+(\.\d+)?(pt|em)\]\s*", "", s).strip()   # leftover from \[4pt]


def spoken(da: str) -> str | None:
    """TTS text when it must differ from the display text: drop gap markers, read '｜' as a pause."""
    s = bare(da)
    t = re.sub(r"[(\[]\d+[)\]]\s*_{3,}\s*|_{3,}\s*[(\[]\d+[)\]]|_{3,}|\(Z\)\s*", "", s).replace("｜", ". ")
    t = t.replace(" → ", ", ").replace("→", ", ")
    t = re.sub(r"(?<!\w)@|@(?!\w)", "", t)           # stray marker '@', but keep e-mail addresses
    t = re.sub(r"\s+([,.!?])", r"\1", re.sub(r"\s{2,}", " ", t)).strip()
    return t if t != s else None


LABEL = re.compile(r"^\(?[A-Z0-9]{1,2}[.)]$")        # "A." "1." "(3)" — shown, not read
try:
    CAST_NAMES = set(yaml.safe_load((ROOT / "audio" / "cast.yaml").read_text(encoding="utf-8"))["roles"]) - {"narrator"}
except FileNotFoundError:
    CAST_NAMES = set()


def box_title(s: str, i: int) -> tuple[str, int]:
    """After \\begin{tcolorbox}: skip the [options] (returning their title=…) and return the index after them."""
    if s[i:i + 1] != "[":
        return "", i
    depth, j, title = 0, i, ""
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
        elif s[j] == "]" and depth == 0:
            break
        j += 1
    m = re.search(r"title=\{", s[i:j])
    if m:
        title, _ = read_group(s, i + m.end() - 1)
    return title, j + 1


def mark_containers(body: str) -> str:
    """emailbox/tcolorbox -> paragraph breaks around a @@CUE title@@ marker."""
    out, i = [], 0
    pat = re.compile(r"\\begin\{(emailbox|tcolorbox)\}|\\end\{(emailbox|tcolorbox)\}")
    for m in pat.finditer(body):
        if m.start() < i:
            continue
        out.append(body[i:m.start()])
        i = m.end()
        if m.group(2):
            out.append("\n\n")
            continue
        if m.group(1) == "emailbox":
            title, i = read_group(body, i) if body[i:i + 1] == "{" else ("", i)
        else:
            title, i = box_title(body, i)
        out.append(f"\n\n@@CUE {title}@@\n\n")
    out.append(body[i:])
    return "".join(out)


def mark_items(body: str) -> str:
    """itemize -> one paragraph whose lines (\\\\) are the items, each tagged @@I@@."""
    def repl(m):
        inner = re.sub(r"^\s*\[[^\]\n]*\]", "", m.group(1))     # itemize options: [label={}, leftmargin=…]
        items = [x.strip() for x in re.split(r"\\item\b", inner) if x.strip()]
        return "\n\n" + "\\\\".join(f"@@I@@{x}" for x in items) + "\n\n"
    return re.sub(r"\\begin\{itemize\}(.*?)\\end\{itemize\}", repl, body, flags=re.S)


def split_top(s: str) -> list[str]:
    """Split on \\\\ line breaks that are not inside a {...} group."""
    parts, depth, start, i = [], 0, 0, 0
    while i < len(s):
        if s.startswith("\\\\", i) and depth == 0:
            parts.append(s[start:i])
            i += 2
            start = i
            continue
        if s[i] == "\\":
            i += 2
            continue
        depth += {"{": 1, "}": -1}.get(s[i], 0)
        i += 1
    parts.append(s[start:])
    return parts


SPEAKER = re.compile(r"^([A-ZÆØÅ][a-zæøåé]+)(\s*\(\d+\))?\s*:\s*(.*)$")   # "Sara:" or exam-chat "Sara (1):"
ITEM_LABEL = re.compile(r"^(\(?[A-Z0-9]{1,2}[.)])\s+(.*)$")             # "A. Jonas: …" in a list of voices


def prose_paras(body: str, prefix: str, default_who: str) -> tuple[list[dict], bool]:
    """Generic text parser: paragraphs, e-mail/notice boxes, item lists with 'Name: line' speakers.

    Returns (paras, boxed); each para's segs carry nl=True where a new line starts and
    label=<speaker> on lines spoken by a named person.
    """
    for env in ("tipbox", "transbox", "enumerate", "tabularx", "xltabular", "quote"):   # xltabular = answer grids
        body = drop_env(body, env)
    body = re.sub(r"\\(sub)*section\*?\{.*?\}", "", body)
    body = re.sub(r"\\(vspace|hspace)\*?\{[^}]*\}|\\hrule|\\renewcommand\{?\\arraystretch\}?\{[^}]*\}|\\(small|footnotesize)\b",
                  "", body)
    boxed = bool(re.search(r"\\begin\{(emailbox|tcolorbox)\}", body))
    body = mark_items(mark_containers(body))

    paras, cue, n = [], None, 0
    for chunk in re.split(r"\n\s*\n", body):
        chunk = chunk.strip()
        opens, closes = chunk.count("{") - chunk.count("\\{"), chunk.count("}") - chunk.count("\\}")
        if opens > closes and chunk.startswith("{"):    # "{\small ..." group opened in this paragraph
            chunk = chunk[1:].strip()
        elif closes > opens and chunk.endswith("}"):    # "... }" closing a group opened earlier
            chunk = chunk[:-1].strip()
        if not chunk:
            continue
        if chunk.startswith("@@CUE"):
            cue = text(chunk[5:-2]) or None
            continue
        segs = []
        for line in split_top(chunk):
            item = "@@I@@" in line
            try:
                t = strip_notes(text(line.replace("@@I@@", "")))
            except ValueError as e:
                print(f"    ! {prefix}: skipped unparsable line ({e})")
                continue
            if not t or CJK.search(t) or "：" in t:   # Chinese headings, "Spørgsmål：" style task prompts
                continue
            who, label = default_who, None
            pre = ITEM_LABEL.match(t)
            if pre and (m := SPEAKER.match(pre.group(2))) and m.group(1) in CAST_NAMES:
                t, label = pre.group(2), pre.group(1)
            m = SPEAKER.match(t)
            if m and m.group(3).strip() and (item or m.group(1) in CAST_NAMES) or m and m.group(2) and m.group(1) in CAST_NAMES:
                who = m.group(1)
                label = f"{label} {who}{m.group(2) or ''}" if label else f"{who}{m.group(2) or ''}"
                t = m.group(3).strip() or "___"
            first = True
            for s in sentences(t):
                if LABEL.match(s):          # "A." / "1." becomes a visual label on the next sentence
                    label = f"{label} {s}" if label else s
                    continue
                n += 1
                seg = {"id": f"{prefix}{n}", "who": who, "da": s}
                say = spoken(s)
                if say == "":               # nothing left to read: an exam gap such as "(1) ___"
                    seg["mute"] = True
                elif say:
                    seg["say"] = say
                if first and segs:
                    seg["nl"] = True
                if label:
                    seg["label"] = label
                    label = None
                segs.append(seg)
                first = False
        if segs:
            paras.append({"cue": cue, "segs": segs})
            cue = None
    return paras, boxed


def parse_enum_dialog(body: str, block_id: str, title: str) -> dict | None:
    """NCD 1 review lessons that write the exam rounds as an enumerate:
    \\item <round title>\\\\ \\textbf{Eksaminator:} \\textit{…}\\\\ \\textbf{Svar:} \\textit{…}\\\\ {中文：…}"""
    m = re.search(r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}", body, flags=re.S)
    if not m or "Eksaminator:" not in m.group(1):
        return None
    paras = []
    for n, item in enumerate((x for x in re.split(r"\\item\b", m.group(1)) if x.strip()), 1):
        q = re.search(r"\\textbf\{Eksaminator:\}\s*\\textit\{", item)
        a = re.search(r"\\textbf\{(?:Svar|Kursist):\}\s*\\textit\{", item)
        if not (q and a):
            continue
        zh = re.search(r"中文：(.*?)\}\}", item, flags=re.S)
        cue = strip_notes(text(split_top(item)[0]))
        paras.append({"cue": cue or None, "segs": [{"id": f"{block_id}-{n}q", "who": "Eksaminator",
                                                   "da": text(read_group(item, q.end() - 1)[0])}]})
        paras.append({"zh": text(zh.group(1)) if zh else None,
                      "segs": [{"id": f"{block_id}-{n}a", "who": "Kursist", "da": text(read_group(item, a.end() - 1)[0])}]})
    return {"id": block_id, "title": title, "tab": title.split("：")[0], "kind": "dialog", "paras": paras} if paras else None


def parse_dialog(body: str, block_id: str = "dialog", title: str = "Dialog") -> dict | None:
    turns = []
    for m in re.finditer(r"\\dialogturn\{(\w+)\}", body):
        i, args = m.end(), []
        for _ in range(4):
            while body[i].isspace():
                i += 1
            a, i = read_group(body, i)
            args.append(a)
        turns.append(args)
    if not turns:
        return None
    scene = [b for b in env_bodies(body, "tipbox") if "场景" in b[:20] or not re.match(r"\s*\{[^}]*(发音|Udtale)", b)]
    paras = [{"zh": text(zh), "note": text(note),
              "segs": [{"id": f"{block_id}-{n}", "who": text(who), "da": text(da)}]}
             for n, (who, da, note, zh) in enumerate(turns, 1)]
    return {"id": block_id, "title": title, "tab": "课文" if block_id == "dialog" else title.split("：")[0], "kind": "dialog",
            "scene": text(re.sub(r"^\{[^}]*\}", "", scene[0].strip())) if scene else None, "paras": paras}


def transbox_paras(chunk: str) -> list[str]:
    zh = []
    for body in env_bodies(chunk, "transbox"):
        body = re.sub(r"^\s*\\small", "", body.strip())
        body = re.sub(r"^\\textbf\{.*?\}\\\\", "", body.strip(), flags=re.S)  # "[Tekst A 中文精译]\\"
        for p in re.split(r"\n\s*\n|\\\\\s*\n", body):
            if p.strip():
                zh.append(text(p))
    return zh


def parse_tekst(chunk: str, label: str) -> dict:
    """One 'Tekst X' subsection of an NCD 2 lesson: prose paragraphs, or a Q/A table."""
    head = re.match(r"\\subsection\*\{(.*?)\}\s*\n", chunk, flags=re.S)
    title = text(head.group(1)) if head else f"Tekst {label}"
    # some lessons (NCD 2 L01) put the translation in a plain tcolorbox headed "[Tekst X 中文…]"
    chunk = re.sub(r"\\begin\{tcolorbox\}(?:\[[^\n]*\])?\s*((?:\\small\s*)?\\textbf\{\\color\{NCDTeal\}\[[^\]]*中文.*?)\\end\{tcolorbox\}",
                   r"\\begin{transbox}\n\1\\end{transbox}", chunk, flags=re.S)
    zh = transbox_paras(chunk)
    body = chunk[head.end():] if head else chunk

    rows = []
    for tab in env_bodies(body, "tabularx"):
        tab = tab[tab.index("@{}}") + 4:] if "@{}}" in tab else tab
        for row in re.split(r"\\\\\s*(?:\\midrule|\\bottomrule)?", tab):
            row = row.replace("\\toprule", "").strip()
            cells = [c.strip() for c in row.split("&")]
            # a spoken Q/A table has whole sentences in its cells, not single-word answer options
            if len(cells) >= 3 and "\\textit" in row and any(len(text(c).split()) >= 3 for c in cells[1:]):
                rows.append(cells)
    if rows:  # question/answer table: first column = cue, last = Kursist B, the rest = Kursist A
        paras = []
        for n, cells in enumerate(rows, 1):
            segs = []
            for k, c in enumerate(cells[1:], 1):
                if "\\textit" not in c:
                    continue
                segs.append({"id": f"{label.lower()}{n}-{k}", "who": "Kursist B" if k == len(cells) - 1 else "Kursist A",
                             "da": text(c)})
            paras.append({"cue": text(cells[0]), "zh": zh[n - 1] if n - 1 < len(zh) else None, "segs": segs})
        return {"id": f"tekst{label}", "title": title, "tab": f"Tekst {label}", "kind": "qa", "paras": paras}

    return prose_block(body, f"tekst{label}", title, f"Tekst {label}", f"{label.lower()}", "narrator", zh)


def prose_block(body: str, block_id: str, title: str, tab: str, prefix: str, who: str, zh: list[str]) -> dict:
    """Prose/e-mail block; translations are attached per paragraph only when the counts line up."""
    paras, boxed = prose_paras(body, prefix, who)
    if zh and not boxed and len(zh) == len(paras):
        for p, z in zip(paras, zh):
            p["zh"] = z
    elif zh and paras:  # cannot align: show the whole translation once, after the text
        paras[-1]["zh_all"] = "\n".join(zh)
    return {"id": block_id, "title": title, "tab": tab, "kind": "prose", "paras": paras}


def gloser_say(da: str, forms: str) -> str:
    """Lemma, plus the inflected forms when they are complete words (not '-er' style endings)."""
    toks = [t.strip().replace("/", " eller ") for t in forms.split(",") if t.strip() not in ("", "—", "–", "-")]
    if toks and not any("-" in t or CJK.search(t) or "kun" in t for t in toks):
        return f"{da}. {', '.join(re.sub(r'\s+', ' ', t) for t in toks)}."
    return f"{da}."


def parse_gloser(tex: str) -> dict | None:
    bodies = env_bodies(tex, "glosertable")
    if not bodies:
        return None
    items = []
    for row in re.split(r"\\\\", bodies[0]):
        row = row.replace("\\midrule", "").strip()
        cells = [c.strip() for c in row.split("&")]
        if len(cells) != 4:
            continue
        pos, da, forms, zh = (bare(text(cells[0])).replace("[er]", "").strip(), bare(text(cells[1])),
                              bare(text(cells[2])).strip(), text(cells[3]))
        if forms.startswith("(") and forms.endswith(")"):
            forms = forms[1:-1].strip()
        if forms in ("—", "–", "-", "不变"):
            forms = ""
        lemmas = [x.strip() for x in da.split(" / ")]
        form_parts = [x.strip() for x in forms.split(" / ")]
        zh_parts = [x.strip() for x in re.split(r"\s*/\s*", zh)]
        if len(lemmas) > 1 and len(form_parts) == len(lemmas):
            pairs = list(zip(lemmas, form_parts))
        elif len(lemmas) > 1:
            pairs = [(lemma, "") for lemma in lemmas]
        else:
            pairs = [(da, forms)]
        for n, (lemma, f) in enumerate(pairs):
            f = re.sub(r"^[a-zæøå]+\s*\((.*?)\)?$", r"\1", f)  # "nysgerrig (-t, -e)" -> "-t, -e"
            f = "" if f in ("—", "–", "-", "不变") else f
            z = zh_parts[n] if len(pairs) > 1 and len(zh_parts) == len(pairs) else zh
            items.append({"id": f"g{len(items) + 1}", "pos": pos, "da": lemma, "forms": f, "zh": z})
    paras = [{"zh": it["zh"], "note": f"{it['pos']} · {it['forms']}" if it["forms"] else it["pos"],
              "segs": [{"id": it["id"], "who": "narrator", "da": it["da"],
                        "say": gloser_say(it["da"], it["forms"]) if it["forms"] else None}]}
             for it in items]
    return {"id": "gloser", "title": "Gloser（生词表 · 点读）", "tab": "生词表", "kind": "words", "paras": paras}


# ---------------------------------------------------------------- lesson
def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items() if v not in (None, "", [])}
    if isinstance(obj, list):
        return [clean(v) for v in obj]
    return obj


def parse_lesson(path: Path, book: str) -> dict:
    tex = strip_comments(path.read_text(encoding="utf-8"))
    m = re.search(r"\\ncdlesson\{(\d+)\}\s*\{(.*?)\}", tex, flags=re.S)
    blocks = []
    sec = section(tex, "二、")
    tekst_heads = [h.start() for h in re.finditer(r"\\subsection\*\{Tekst ([A-Z])", sec)]
    if tekst_heads:  # NCD 2: Tekst A / Tekst B
        for k, start in enumerate(tekst_heads):
            chunk = sec[start: tekst_heads[k + 1] if k + 1 < len(tekst_heads) else len(sec)]
            blocks.append(parse_tekst(chunk, re.match(r"\\subsection\*\{Tekst ([A-Z])", chunk).group(1)))
    elif "\\subsection*" not in sec:  # NCD 1 regular lesson: one dialogue
        dialog = parse_dialog(sec)
        if dialog:
            blocks.append(dialog)
    else:  # NCD 1 review lesson: monologue (Del 1, possibly untitled) + examiner dialogue (Del 2)
        heads = [h.start() for h in re.finditer(r"\\subsection\*\{", sec)]
        parts = [(None, sec[sec.index("\n"): heads[0]])] + [
            (sec[s:], sec[s: heads[k + 1] if k + 1 < len(heads) else len(sec)]) for k, s in enumerate(heads)]
        for n, (_, chunk) in enumerate(parts):
            head = re.match(r"\\subsection\*\{(.*?)\}\s*\n", chunk, flags=re.S)
            title = text(head.group(1)) if head else "Del 1：Monolog"
            title = title if title.startswith("Del") else f"Del {n or 1}：{title}"
            body = chunk[head.end():] if head else chunk
            bid = f"del{len(blocks) + 1}"
            if "\\dialogturn" in body:
                blocks.append(parse_dialog(body, bid, title))
            elif "Eksaminator:" in body and parse_enum_dialog(body, bid, title):
                blocks.append(parse_enum_dialog(body, bid, title))
            else:
                b = prose_block(body, bid, title, title.split("：")[0], f"m{len(blocks) + 1}-", "Kursist",
                                transbox_paras(body))
                if b["paras"]:
                    blocks.append(b)
    gl = parse_gloser(tex)
    if gl:
        blocks.append(gl)
    return clean({"book": book, "lesson": int(m.group(1)), "title_da": text(m.group(2)), "blocks": blocks})


def main(argv: list[str]) -> int:
    if "--all" in argv:
        targets = [p for b in ("ncd1", "ncd2", "ncd3") for p in sorted((ROOT / b / "lessons").glob("L*.tex"))]
    else:
        targets = [ROOT / a.split("/")[0] / "lessons" / f"{a.split('/')[1]}.tex" for a in argv if not a.startswith("-")]
    for path in targets:
        book = path.parent.parent.name
        out = OUT / book / f"{path.stem}.yaml"
        if out.exists() and out.read_text(encoding="utf-8").startswith(HAND_MADE):
            print(f"  skip (hand-made) {out.relative_to(ROOT)}")
            continue
        data = parse_lesson(path, book)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
        nseg = sum(len(p["segs"]) for b in data["blocks"] for p in b["paras"])
        kinds = ", ".join(f"{b['id']}:{b['kind']}" for b in data["blocks"])
        print(f"  {book}/{path.stem}: {nseg} segments ({kinds}) -> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
