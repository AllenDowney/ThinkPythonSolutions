#!/usr/bin/env python3
"""Export the quizzes as Moodle XML and Brightspace CSV.

Moodle XML imports into a Moodle question bank, one category per quiz. Brightspace
CSV imports into the Brightspace Question Library. In both, every choice keeps its
rationale as feedback, and code is rendered as HTML.

The correct answer is always last in the source. Moodle shuffles answers itself
(shuffleanswers); the Brightspace CSV has no such setting, so the choices are shuffled
here, with a fixed seed so every build gives the same file.

Usage:
    python parse_quizzes.py        # quizzes.md -> parsed_quizzes.json
    python export_lms.py [OUT]     # -> OUT/moodle/*.xml, OUT/brightspace/*.csv
                                   #    (default: build/)

Requires the markdown package (pip install markdown; text2qti installs it too).
See ThinkPython planning/lms_quizzes.md.
"""
import csv
import json
import random
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import markdown

from export_text2qti import quiz_names

HERE = Path(__file__).parent


def to_html(text):
    """Markdown to HTML. Fenced code blocks keep their indentation."""
    return markdown.markdown(text, extensions=["fenced_code"]).strip()


def inline_html(text):
    """Markdown to HTML for a one-line choice or rationale, without the <p>."""
    html = to_html(text)
    if html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        html = html[3:-4]
    return html


def cdata(html):
    assert "]]>" not in html
    return f"<![CDATA[{html}]]>"


def question_id(slug, qnum):
    return f"TP3-{slug}-q{qnum:02d}"


# ---------------------------------------------------------------- Moodle XML

def moodle_questions(quiz):
    slug, title, description = quiz_names(quiz)
    out = [
        '  <question type="category">',
        f"    <category><text>$course$/top/Think Python/{escape(title)}</text></category>",
        f'    <info format="html"><text>{cdata(inline_html(description))}</text></info>',
        "  </question>",
    ]
    for qnum, q in enumerate(quiz["questions"], 1):
        out += [
            '  <question type="multichoice">',
            f"    <name><text>{question_id(slug, qnum)}</text></name>",
            f'    <questiontext format="html"><text>{cdata(to_html(q["question_text"]))}</text></questiontext>',
            '    <generalfeedback format="html"><text></text></generalfeedback>',
            "    <defaultgrade>1</defaultgrade>",
            "    <penalty>0</penalty>",
            "    <hidden>0</hidden>",
            f"    <idnumber>{question_id(slug, qnum)}</idnumber>",
            "    <single>true</single>",
            "    <shuffleanswers>1</shuffleanswers>",
            "    <answernumbering>abc</answernumbering>",
        ]
        for k, (option, rationale) in enumerate(zip(q["options"], q["rationales"])):
            fraction = 100 if k == q["correct_answer_index"] else 0
            out += [
                f'    <answer fraction="{fraction}" format="html">',
                f"      <text>{cdata(inline_html(option))}</text>",
                f'      <feedback format="html"><text>{cdata(inline_html(rationale))}</text></feedback>',
                "    </answer>",
            ]
        out.append("  </question>")
    return out


def write_moodle(quizzes, path):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<quiz>"]
    for quiz in quizzes:
        lines += moodle_questions(quiz)
    lines.append("</quiz>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------- Brightspace CSV

def brightspace_rows(quiz):
    slug, title, _ = quiz_names(quiz)
    rows = []
    for qnum, q in enumerate(quiz["questions"], 1):
        qid = question_id(slug, qnum)
        choices = [(100 if k == q["correct_answer_index"] else 0, option, rationale)
                   for k, (option, rationale) in enumerate(zip(q["options"], q["rationales"]))]
        random.Random(qid).shuffle(choices)   # fixed per question, so builds are stable
        rows += [
            ["NewQuestion", "MC"],
            ["ID", qid],
            ["Title", f"{title}, question {qnum}"],
            ["QuestionText", to_html(q["question_text"]), "HTML"],
            ["Points", "1"],
            ["Difficulty", "1"],
        ]
        for weight, option, rationale in choices:
            rows.append(["Option", str(weight), inline_html(option), "HTML",
                         inline_html(rationale), "HTML"])
        rows.append([])
    return rows


def write_brightspace(quizzes, path):
    # utf-8-sig: Brightspace and Excel both read the BOM as "this is UTF-8"
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        for quiz in quizzes:
            writer.writerows(brightspace_rows(quiz))


# ---------------------------------------------------------------------------

def main(out_dir):
    quizzes = json.loads((HERE / "parsed_quizzes.json").read_text(encoding="utf-8"))
    out_dir = Path(out_dir)
    for sub in ("moodle", "brightspace"):
        (out_dir / sub).mkdir(parents=True, exist_ok=True)
        for old in (out_dir / sub).iterdir():
            old.unlink()
    for quiz in quizzes:
        slug, _, _ = quiz_names(quiz)
        write_moodle([quiz], out_dir / "moodle" / f"{slug}.xml")
        write_brightspace([quiz], out_dir / "brightspace" / f"{slug}.csv")
    write_moodle(quizzes, out_dir / "moodle" / "all_quizzes.xml")
    write_brightspace(quizzes, out_dir / "brightspace" / "all_quizzes.csv")
    n = sum(len(q["questions"]) for q in quizzes)
    print(f"{len(quizzes)} quizzes, {n} questions -> {out_dir}/moodle, {out_dir}/brightspace")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE / "build")
