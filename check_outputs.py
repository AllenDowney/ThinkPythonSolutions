#!/usr/bin/env python3
"""Keep the stored outputs in the solution notebooks honest.

Guards two failure modes, both invisible to `make tests`:

  MISSING   The book is built with `execute_notebooks: 'off'`, so the website
            renders the outputs stored in each .ipynb and never runs the code.
            A chapter committed unexecuted keeps all its prose and silently
            loses every result and figure. `pytest --nbmake` cannot catch this:
            it executes notebooks itself and never looks at what is stored.
            This is not hypothetical -- Think Stats published three chapters
            with no figures at all for seven months, with CI green throughout.

  BLOATED   Cells tagged `remove-cell` or `remove-output` are discarded by
            every consumer -- the Jupyter Book prep, the student and blank
            notebook builds, and latex/remove_cells.py -- but their outputs are
            still stored in the .ipynb. chap07 reached 2.2 MB, 97% of it a word
            list no reader ever sees, which made it unrenderable on GitHub and
            froze Colab on low-memory machines (ThinkPythonSolutions#16).

Usage:
    python check_outputs.py            # check, read-only, nonzero exit on failure
    python check_outputs.py --strip    # clear the hidden outputs, in place
"""

import sys
from pathlib import Path

import nbformat as nbf

# Tags whose cells no build target ever renders.
HIDDEN_TAGS = {"remove-cell", "remove-output"}

# A notebook with at least this many code cells should have stored outputs.
# Below it, a chapter may legitimately be all prose.
MIN_CODE_CELLS = 5

# Hidden outputs under this are not worth a failed build. chap07 held 1.5 MB.
BLOAT_LIMIT = 50 * 1024


def output_chars(cell):
    total = 0
    for out in cell.get("outputs", []):
        text = out.get("text") or (out.get("data") or {}).get("text/plain") or ""
        if isinstance(text, list):
            text = "".join(text)
        total += len(str(text))
    return total


def survey(path):
    nb = nbf.read(path, nbf.NO_CONVERT)
    code = [c for c in nb.cells if c["cell_type"] == "code"]
    hidden = [c for c in code if HIDDEN_TAGS & set(c["metadata"].get("tags") or [])]
    return {
        "nb": nb,
        "code": len(code),
        "with_outputs": sum(1 for c in code if c.get("outputs")),
        "hidden_chars": sum(output_chars(c) for c in hidden),
        "hidden_cells": [c for c in hidden if c.get("outputs")],
        "size": Path(path).stat().st_size,
    }


def main(argv):
    strip = "--strip" in argv
    paths = sorted(Path(__file__).parent.glob("soln/chap*.ipynb"))
    if not paths:
        print("no notebooks found", file=sys.stderr)
        return 2

    missing, bloated, stripped = [], [], []

    for path in paths:
        info = survey(path)

        if info["code"] >= MIN_CODE_CELLS and info["with_outputs"] == 0:
            missing.append((path.name, info))

        if info["hidden_chars"] > BLOAT_LIMIT:
            if strip:
                for cell in info["hidden_cells"]:
                    cell["outputs"] = []
                nbf.write(info["nb"], str(path))
                stripped.append((path.name, info, path.stat().st_size))
            else:
                bloated.append((path.name, info))

    if stripped:
        print("Stripped outputs from hidden cells:")
        for name, info, new in stripped:
            print(f"  {name:14} {info['size']/1024:8.0f} KB -> {new/1024:7.0f} KB")
        print()

    if missing:
        print("FAIL: committed with no stored outputs -- the website would")
        print("      publish these chapters with every result missing.")
        for name, info in missing:
            print(f"  {name:14} {info['code']} code cells, 0 with outputs")
        print()

    if bloated:
        print("FAIL: outputs stored for cells that no build target renders.")
        print("      These bloat the file on GitHub and Colab. Run:")
        print("          python check_outputs.py --strip")
        for name, info in bloated:
            print(f"  {name:14} {info['size']/1024:8.0f} KB, "
                  f"{info['hidden_chars']:>9,} chars hidden but stored")
        print()

    if missing or bloated:
        return 1

    print(f"outputs ok: {len(paths)} notebooks"
          + (" (stripped above)" if stripped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
