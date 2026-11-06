#!/usr/bin/env python3
"""Write each quiz as text2qti input, then build QTI 1.2 packages with text2qti.

QTI 1.2 imports into Canvas (tested) and Brightspace. Each choice keeps its rationale
as feedback, and the answers are shuffled, since the correct answer is always last in
the source.

Usage:
    python parse_quizzes.py          # quizzes.md -> parsed_quizzes.json
    python export_text2qti.py [OUT]  # -> OUT/*.txt and OUT/*.zip (default: build/qti12)

Requires text2qti (pip install text2qti). See ThinkPython planning/lms_quizzes.md.
"""
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).parent

CHAPTER_TITLES = {
    1: "Programming as a way of thinking", 2: "Variables and Statements", 3: "Functions",
    4: "Functions and Interfaces", 5: "Conditionals and Recursion", 6: "Return Values",
    7: "Iteration and Search", 8: "Strings and Regular Expressions", 9: "Lists",
    10: "Dictionaries", 11: "Tuples", 12: "Text Analysis and Generation",
    13: "Files and Databases", 14: "Classes and Functions", 15: "Classes and Methods",
    16: "Classes and Objects", 17: "Inheritance", 18: "Python Extras",
}

CREDIT = ("From *Think Python*, 3rd edition, by Allen B. Downey "
          "(https://allendowney.github.io/ThinkPython/), CC BY-NC-SA 4.0.")


def quiz_names(quiz):
    """Return (slug, title, description) for a parsed quiz."""
    m = re.fullmatch(r"Chapter (\d+)", quiz["title"])
    if m:
        n = int(m[1])
        return (f"chapter{n:02d}",
                f"Think Python, Chapter {n}: {CHAPTER_TITLES[n]}",
                f"Formative quiz for Chapter {n}. {CREDIT}")
    return ("summative", "Think Python: summative quiz",
            f"Summative quiz covering Chapters 1-18. {CREDIT}")


def indent(text, first, rest):
    """Prefix the first line with `first` and indent the rest to match."""
    lines = text.split("\n")
    out = [first + lines[0]]
    out += [(rest + line) if line else "" for line in lines[1:]]
    return "\n".join(out)


def to_text2qti(quiz):
    slug, title, description = quiz_names(quiz)
    parts = [f"Quiz title: {title}",
             f"Quiz description: {description}",
             "Shuffle answers: true",
             ""]
    for qnum, q in enumerate(quiz["questions"], 1):
        label = f"{qnum}.  "
        parts.append(indent(q["question_text"], label, " " * len(label)))
        for k, (option, rationale) in enumerate(zip(q["options"], q["rationales"])):
            mark = "*" if k == q["correct_answer_index"] else ""
            label = f"{mark}{'abcd'[k]}) ".ljust(4)   # 'a)  ' or '*d) '
            parts.append(indent(option, label, " " * 4))
            parts.append(indent(rationale, "... ", " " * 4))
        parts.append("")
    return slug, "\n".join(parts)


def normalize_zip(path):
    """Rewrite a zip with fixed timestamps, so an unchanged quiz gives identical bytes."""
    with zipfile.ZipFile(path) as z:
        entries = [(info.filename, z.read(info)) for info in z.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = (0o40755 << 16) | 0x10 if name.endswith("/") else 0o644 << 16
            z.writestr(info, data, zipfile.ZIP_DEFLATED)


def main(out_dir):
    quizzes = json.loads((HERE / "parsed_quizzes.json").read_text(encoding="utf-8"))
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    text2qti = shutil.which("text2qti") or str(Path(sys.executable).parent / "text2qti")
    for quiz in quizzes:
        slug, text = to_text2qti(quiz)
        txt = out_dir / f"{slug}.txt"
        txt.write_text(text, encoding="utf-8")
        # text2qti asks for a LaTeX rendering URL on first run; the quizzes have no math
        subprocess.run([text2qti, txt.name], cwd=out_dir, input="\n", text=True,
                       check=True, capture_output=True)
        normalize_zip(out_dir / f"{slug}.zip")
        print(f"{slug}.zip  {len(quiz['questions'])} questions")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE / "build" / "qti12")
