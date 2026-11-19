"""Generate exercise banks (YAML) from the LaTeX lesson sources.

Usage:
    python interactive/extract.py              # write banks that do not exist yet
    python interactive/extract.py --force      # regenerate every non-hand-made bank
    python interactive/extract.py --check      # only print the review report

Each lesson yields:
    gloser   flashcards from the glosertable
    order    word-order drill built from the exercise-C (translation) answers
    A/B/C    the lesson's Mønsterøvelser, as a "drill" section whose items are
             either "cloze" (inline blanks) or "write" (type the whole answer)

Banks whose first line is the HAND_MADE marker are never overwritten.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent / "data"
BOOKS = ("ncd1", "ncd2", "ncd3", "ncd4")
HAND_MADE = "# hand-made"

BLANK = "{{_}}"          # blank marker inside prompts
I_OPEN, I_CLOSE = "⟦", "⟧"  # italic markers inside prompts/explanations
CJK = re.compile(r"[\u3400-\u9fff]")
NOTHING = ("\u00d7", "x", "-", "\u2013", "0", "/")  # accepted inputs for "leave this blank empty"


# ---------------------------------------------------------------- LaTeX helpers
def strip_comments(tex: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in tex.splitlines())


def read_group(s: str, i: int) -> tuple[str, int]:
    """s[i] must be '{'; return (content, index after the closing brace)."""
    assert s[i] == "{", s[i:i + 30]
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError("unbalanced braces: " + s[i:i + 60])


def macro_args(s: str, name: str, n: int) -> list[str]:
    i = s.index("\\" + name + "{") + len(name) + 1
    args = []
    for _ in range(n):
        while s[i].isspace():
            i += 1
        arg, i = read_group(s, i)
        args.append(arg)
    return args


ITALIC_MACROS = ("textit", "da", "dabold")
KEEP_MACROS = ("textbf", "text", "mbox", "emph", "ipa", "textsc")
DROP_WITH_ARG = ("color", "vspace", "hspace", "label")
SYMBOLS = {
    "rightarrow": "→", "leftrightarrow": "↔", "Rightarrow": "⇒", "times": "×",
    "quad": "  ", "qquad": "   ", "newline": " ", "ldots": "…", "dots": "…",
    "small": "", "footnotesize": "", "normalsize": "", "par": " ", "noindent": "",
}


def flatten(s: str, italic: bool = True) -> str:
    """Convert a LaTeX fragment to plain text (optionally keeping italic markers)."""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([a-zA-Z]+)\*?", s[i:])
            if not m:  # escaped char such as \& \% \\ \,
                nxt = s[i + 1:i + 2]
                out.append({"\\": " ", ",": " ", " ": " "}.get(nxt, nxt))
                i += 2
                continue
            name, i = m.group(1), i + m.end()
            if name == "underline" and s[i:i + 1] == "{":
                _, i = read_group(s, i)
                out.append(BLANK)
            elif name in ITALIC_MACROS and s[i:i + 1] == "{":
                arg, i = read_group(s, i)
                inner = flatten(arg, italic)
                out.append(f"{I_OPEN}{inner}{I_CLOSE}" if italic and name != "dabold" else inner)
            elif name in KEEP_MACROS and s[i:i + 1] == "{":
                arg, i = read_group(s, i)
                out.append(flatten(arg, italic))
            elif name in DROP_WITH_ARG and s[i:i + 1] == "{":
                _, i = read_group(s, i)
            elif name in SYMBOLS:
                out.append(SYMBOLS[name])
            # any other macro is dropped silently
        elif c == "$":
            i += 1
        elif c in "{}":
            i += 1
        elif c == "~":
            out.append(" ")
            i += 1
        else:
            out.append(c)
            i += 1
    text = "".join(out)
    text = text.replace("---", "—").replace("--", "–")
    text = re.sub(rf"{I_CLOSE}(\s*){I_OPEN}", r"\1", text)  # merge adjacent italics
    text = re.sub(rf"{I_OPEN}\s*{I_CLOSE}", "", text)
    text = re.sub(r"[ \t\r\n]+", " ", text)
    text = re.sub(r"\s+([,.?!;:)])", r"\1", text)
    return text.strip()


def plain(s: str) -> str:
    return flatten(s, italic=False).replace(BLANK, "___")


def split_items(block: str) -> list[str]:
    """Split an exercise/answer block into items (enumerate or tabularx rows)."""
    if "\\begin{tabularx}" in block:
        body = block[block.index("\\begin{tabularx}"):]
        body = body[body.index("@{}}") + 4: body.index("\\end{tabularx}")]
        cells = [c.strip() for row in re.split(r"\\\\", body) for c in row.split("&")]
        numbered = []
        for cell in cells:
            m = re.match(r"(\d+)\.\s*(.*)", cell, re.S)
            if m:
                numbered.append((int(m.group(1)), m.group(2).strip()))
        return [text for _, text in sorted(numbered)]
    m = re.search(r"\\begin\{enumerate\}(.*)\\end\{enumerate\}", block, re.S)
    if not m:
        # inline numbering: "\textbf{1.} answer \quad \textbf{2.} answer \\ ..."
        parts = re.split(r"\\textbf\{(\d+)\.\}", block)
        numbered = [(int(parts[k]), re.sub(r"(\\q?quad|\\\\)\s*$", "", parts[k + 1].strip()).strip())
                    for k in range(1, len(parts) - 1, 2)]
        return [text for _, text in sorted(numbered)]
    items = []
    for it in re.split(r"\\item\b", m.group(1))[1:]:
        # several answers packed into one \item: "\da{a} \quad 2. \da{b} \quad 3. ..."
        items += [p.strip() for p in re.split(r"\\q?quad\s*\d+\.\s*", it) if p.strip()]
    return items


# ---------------------------------------------------------------- answers
def parse_answer(raw: str) -> dict:
    """Split an answer item into Danish segments, alternatives and Chinese commentary.

    Segments are top-level \\textit / \\da / \\dabold groups outside full-width
    parentheses. Text between two segments decides whether they are parts of
    one answer (concatenate) or alternatives ('/' or '或').
    """
    segments, gaps, comment = [], [], []
    depth, i, gap = 0, 0, []
    while i < len(raw):
        c = raw[i]
        if c == "（":
            depth += 1
            comment.append(c)
            i += 1
            continue
        if c == "）":
            depth = max(0, depth - 1)
            comment.append(c)
            i += 1
            continue
        m = re.match(r"\\(textit|da|dabold|textbf)\{", raw[i:]) if depth == 0 else None
        if m:
            arg, end = read_group(raw, i + m.end() - 1)
            if m.group(1) == "textbf" and CJK.search(plain(arg)):
                # bold Chinese label/commentary, not an answer
                gap.append(raw[i:end])
                i = end
                continue
            segments.append(plain(arg))
            gaps.append("".join(gap))
            gap = []
            i = end
            continue
        (comment if depth else gap).append(c)
        i += 1
    gaps.append("".join(gap))

    groups: list[list[str]] = []  # each group = alternatives for one slot/answer
    for k, seg in enumerate(segments):
        between = plain(gaps[k]) if k else ""
        if k and re.search(r"/|或|也可", between):
            groups[-1].append(seg)
        else:
            groups.append([seg])

    lead = plain(gaps[0]).strip(" ：:；;，,")
    tail_parts = [plain(g) for g in gaps[1:]]
    explain_bits = [lead] if CJK.search(lead) else []
    explain_bits += [t for t in tail_parts if CJK.search(t)]
    paren = flatten("".join(comment))
    if CJK.search(paren):
        explain_bits.append(paren.strip("（）"))
    explain = "；".join(b.strip(" ：:；;，,（）") for b in explain_bits if b.strip(" ：:；;，,（）"))
    return {"groups": groups, "segments": segments, "gaps": [plain(g) for g in gaps], "explain": explain}


def align_to_prompt(prompt: str, sentence: str, n: int) -> list[list[str]] | None:
    """Recover blank answers by matching a full answer sentence against the prompt.

    e.g. prompt "Jeg har brug for {{_}} energi og {{_}} venner." and answer
    "Jeg har brug for mere energi og flere venner." -> [["mere"], ["flere"]]
    """
    text = re.sub(rf"[{I_OPEN}{I_CLOSE}]", "", prompt)
    if "→" in text and BLANK in text.rsplit("→", 1)[1]:
        text = text.rsplit("→", 1)[1]                          # "Jeg så Peter. ... → Jeg så ___."
    text = re.sub(r"^[^：]*[㐀-鿿][^：]*：", "", text)   # leading Chinese instruction
    text = re.sub(r"\s*[（(][^（）()]*[）)]", "", text)            # hints such as "(at rejse)"
    pieces = text.split(BLANK)
    if len(pieces) != n + 1:
        return None
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    pattern = r"\s*(.+?)\s*".join(re.escape(norm(p)) for p in pieces)
    m = re.fullmatch(r"\s*" + pattern.rstrip(r"\.\?\!") + r"[.?!]*\s*", norm(sentence), re.I)
    if not m:
        return None
    return [[g.strip()] for g in m.groups()]


def expand_slashes(s: str) -> list[str]:
    """'Jeg så Peter / ham gå' -> ['Jeg så Peter gå', 'Jeg så ham gå'] (single-word alternatives)."""
    m = re.search(r"(\S+) / (\S+)", s)
    if not m:
        return [s]
    out = []
    for word in (m.group(1), m.group(2)):
        out += expand_slashes(s[:m.start()] + word + s[m.end():])
    return out


def align_alternatives(prompt: str, answers: list[str], n: int) -> list[list[str]] | None:
    """Align every alternative full answer with the prompt and merge per-blank options."""
    per_blank: list[list[str]] = [[] for _ in range(n)]
    for alt in answers:
        for variant in expand_slashes(alt):
            got = align_to_prompt(prompt, variant, n)
            if not got:
                return None
            for k, (value,) in enumerate(got):
                if value not in per_blank[k]:
                    per_blank[k].append(value)
    return per_blank


def map_blanks(prompt: str, ans: dict, n: int) -> list[list[str]] | None:
    """Try to turn an answer whose parts don't match the blank count into n blanks."""
    if len(ans["groups"]) == 1:
        aligned = align_alternatives(prompt, ans["groups"][0], n)
        if aligned:
            return aligned
    segs = [s for s in ans["segments"] if s.strip()]
    if len(segs) == n:                          # "på / på", "ham ... løbe": one segment per blank
        return [[s] for s in segs]
    if len(ans["groups"]) != 1:
        return None
    whole = ans["groups"][0][0]
    for sep in (r"\s*(?:\.\.\.|…)\s*", r"\s+/\s+", r",\s+", r"\s+"):
        parts = [p for p in re.split(sep, whole.strip().rstrip(".!?") if sep != r",\s+" else whole.strip())
                 if p.strip()]
        if len(parts) == n:
            return [[p.strip()] for p in parts]
        # "laver / lavede (1 类)": the verb class sits outside the italic answer
        klass = re.search(r"(\d+)\s*类", " ".join(ans["gaps"]))
        if klass and len(parts) == n - 1 and sep == r"\s+/\s+":
            return [[p.strip()] for p in parts] + [[klass.group(1)]]
    return None


# ---------------------------------------------------------------- lesson parsing
def exercise_blocks(text: str, answers: bool) -> dict[str, tuple[str, str]]:
    """Return {letter: (heading, block)} for exercises or their answers."""
    pat = re.compile(r"\\textbf\{练习 ?([A-Z])" + (r" ?答案" if answers else r"："))
    hits = list(pat.finditer(text))
    out = {}
    for k, m in enumerate(hits):
        head, after = read_group(text, m.start() + len("\\textbf"))
        stops = [hits[k + 1].start()] if k + 1 < len(hits) else []
        # only a \textbf at the start of a line opens a new block; inline bold is content
        for stopper in (r"\n\s*\\textbf\{(?!练习|\d+\.\})", r"\\ncdsubsec", r"\\end\{answerbox\}", r"\\begin\{tcolorbox\}"):
            s = re.search(stopper, text[after:])
            if s:
                stops.append(after + s.start())
        out[m.group(1)] = (head, text[after:min(stops) if stops else len(text)])
    return out


def parse_lesson(path: Path, book: str) -> tuple[dict, list[str]]:
    tex = strip_comments(path.read_text(encoding="utf-8"))
    report: list[str] = []
    num, title_da, title_zh, _align, grammar = macro_args(tex, "ncdlesson", 5)
    tag = f"{book}/L{int(num):02d}"
    lesson = {
        "book": book,
        "lesson": int(num),
        "title_da": plain(title_da),
        "title_zh": plain(title_zh),
        "grammar": plain(grammar),
        "sections": [],
    }

    # flashcards
    g = re.search(r"\\begin\{glosertable\}(.*?)\\end\{glosertable\}", tex, re.S).group(1)
    cards = []
    for row in re.split(r"\\\\", g):
        cols = [c.strip() for c in row.replace("\\midrule", "").split("&")]
        if len(cols) != 4:
            continue
        pos, da, forms, zh = (plain(c) for c in cols)
        card = {"pos": pos, "da": da, "zh": zh}
        if forms.strip("()（） "):
            card["forms"] = forms.strip("()（） ")
        cards.append(card)
    lesson["sections"].append({"id": "gloser", "type": "flashcards", "title": "生词闪卡（Gloser）", "cards": cards})

    ex_start = tex.index("Mønsterøvelser")
    ex_text = tex[ex_start:tex.index("\\ncdsubsec", ex_start + 20)]
    ans_text = tex[tex.index("\\begin{answerbox}"):tex.index("\\end{answerbox}") + 15]
    exercises = exercise_blocks(ex_text, answers=False)
    answers = exercise_blocks(ans_text, answers=True)

    drills = []
    for letter in sorted(exercises):
        head, block = exercises[letter]
        ans_head, ans_block = answers.get(letter, ("", ""))
        items_raw, ans_raw = split_items(block), split_items(ans_block)
        where = f"{tag} {letter}"
        if len(items_raw) != len(ans_raw):
            report.append(f"{where}: {len(items_raw)} items vs {len(ans_raw)} answers — section skipped")
            continue
        title = plain(head)
        heading_plain = title + " " + plain(ans_head)
        is_correction = bool(re.search(r"纠错|改错|找错|找出并改正", heading_plain))
        is_open = "参考" in heading_plain
        example = None
        q = re.search(r"\\begin\{quote\}(.*?)\\end\{quote\}", block, re.S)
        if q:
            example = plain(q.group(1)).removeprefix("例：").strip()

        items = []
        for k, (p_raw, a_raw) in enumerate(zip(items_raw, ans_raw), start=1):
            prompt = flatten(p_raw)
            ans = parse_answer(a_raw)
            groups = [grp for grp in ans["groups"] if any(x.strip() for x in grp)]
            n_blanks = prompt.count(BLANK)
            if not groups and re.match(r"\s*\$?\\times", a_raw) and n_blanks == 1:
                # "×" = nothing goes in the blank (e.g. zero article)
                groups = [list(NOTHING)]
                ans["explain"] = "此处不填（输入 × 或 -）" + ("；" + ans["explain"] if ans["explain"] else "")
            if not groups:
                report.append(f"{where}{k}: no Danish answer found — item skipped ({plain(a_raw)[:50]})")
                continue
            item: dict = {"prompt": prompt}
            # a full-sentence answer is aligned with the prompt even when the counts already
            # match, so a single blank gets "mest populære" rather than the whole sentence
            if n_blanks and (n_blanks != len(groups) or len(groups[0][0].split()) > 3):
                mapped = map_blanks(prompt, ans, n_blanks)
                if mapped:
                    groups = mapped
            if n_blanks and n_blanks == len(groups):
                item["kind"] = "cloze"
                item["blanks"] = groups
            else:
                if n_blanks:
                    # blanks do not map 1:1 to answer parts: ask for the whole answer instead
                    item["prompt"] = prompt.replace(BLANK, "___")
                    if len(groups) > 1:
                        report.append(f"{where}{k}: {n_blanks} blanks vs {len(groups)} answer parts — using write")
                item["kind"] = "write"
                item["accept"] = groups[0] if len(groups) == 1 else [" ".join(grp[0] for grp in groups)]
                if is_correction:
                    italics = re.findall(rf"{I_OPEN}(.*?){I_CLOSE}", prompt)
                    if len(italics) == 1:
                        item["prefill"] = italics[0]
            if ans["explain"]:
                item["explain"] = ans["explain"]
            items.append(item)
        if not items:
            continue
        section = {"id": letter, "type": "drill", "title": title, "items": items}
        if example:
            section["example"] = example
        if is_open:
            section["open"] = True
        drills.append(section)

    # word-order drill from the translation exercise (C)
    c = next((d for d in drills if d["id"] == "C"), None)
    order = []
    for it in (c["items"] if c else []):
        if it["kind"] != "write":
            continue
        sentence = it["accept"][0]
        if 4 <= len(sentence.split()) <= 16 and not re.search(r"[—/()]", sentence) and CJK.search(it["prompt"]):
            order.append({"zh": re.sub(f"[{I_OPEN}{I_CLOSE}]", "", it["prompt"]), "answer": sentence})
    if order:
        lesson["sections"].append({
            "id": "order", "type": "order", "title": "语序拼句（由中译丹答案生成）",
            "instruction": "点击词块，按正确语序拼出句子。", "items": order,
        })
    else:
        report.append(f"{tag}: no usable exercise-C sentences — no order drill")

    lesson["sections"].extend(drills)
    return lesson, report


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="overwrite generated banks")
    ap.add_argument("--check", action="store_true", help="only print the report")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    written, kept, report = 0, 0, []
    for book in BOOKS:
        for path in sorted((ROOT / book / "lessons").glob("L*.tex")):
            out = DATA / book / f"{path.stem}.yaml"
            if out.exists() and out.read_text(encoding="utf-8").startswith(HAND_MADE):
                kept += 1
                continue
            lesson, rep = parse_lesson(path, book)
            report += rep
            if args.check or (out.exists() and not args.force):
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            header = (f"# Generated by interactive/extract.py from {book}/lessons/{path.name}.\n"
                      f"# Put '{HAND_MADE}' on the first line to protect manual edits from --force.\n")
            out.write_text(header + yaml.safe_dump(lesson, allow_unicode=True, sort_keys=False, width=1000),
                           encoding="utf-8")
            written += 1

    print(f"written={written} hand-made kept={kept}")
    print(f"review items: {len(report)}")
    for line in report:
        print("  -", line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
