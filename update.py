#!/usr/bin/env python3
"""Rebuild everything downstream of soln/ and publish it.

soln/*.ipynb is the canonical source. Four targets are generated from it,
each by its own build.sh:

    chapters/   student notebooks + ThinkPythonNotebooks.zip   commits & pushes
    blank/      code-free notebooks                            commits & pushes
    jb/         Jupyter Book HTML                              PUBLISHES to Pages
    top level   support files, SVG -> PNG                      commits & pushes

Step 5 makes the website live. You are asked to confirm before it runs;
pass --yes to skip the prompt.

    python update.py                 # test, commit, push, build, confirm, publish
    python update.py --yes           # no confirmation
    python update.py --skip-tests    # skip `make tests` (~2 minutes)
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()   # ThinkPythonSolutions
BOOK = ROOT.parent                       # ThinkPython


def banner(text):
    print(f"\n{'=' * 70}\n{text}\n{'=' * 70}", flush=True)


def run(cmd, cwd, check=True):
    """Run a command, streaming its output. Stop the script if it fails.

    The old version captured output and merely warned on a nonzero exit, so a
    failed build still ended with a success message.
    """
    print(f"\n>>> {cmd}\n    in {cwd}", flush=True)
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if check and result.returncode:
        sys.exit(
            f"\nFAILED (exit {result.returncode}): {cmd}\n"
            f"    in {cwd}\n"
            f"Stopping. Later steps have not run."
        )
    return result.returncode


def nothing_to_commit(cwd):
    return subprocess.run(
        "git diff --cached --quiet && git diff --quiet",
        shell=True, cwd=cwd
    ).returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--yes", action="store_true",
                        help="do not ask before publishing the website")
    parser.add_argument("--skip-tests", action="store_true",
                        help="skip `make tests`")
    args = parser.parse_args()

    banner("STEP 1: check and test the solution notebooks")
    if args.skip_tests:
        print("skipping `make tests` at your request; running the outputs check only")
        run("python check_outputs.py", ROOT)
    else:
        run("make tests", ROOT)

    banner("STEP 2: commit and push soln/")
    # The old version committed here and never pushed, so the solutions repo
    # could sit unpushed indefinitely while ThinkPython went out.
    if nothing_to_commit(ROOT):
        print("nothing to commit in ThinkPythonSolutions")
    else:
        # -u stages tracked files only, so gitignored copies such as
        # soln/diagram.py cannot abort the run.
        run("git add -u soln/", ROOT)
        run('git commit -m "Update solution notebooks"', ROOT)
    run("git push", ROOT)

    banner("STEP 3: build chapters/ (student notebooks and the zip)")
    run("bash build.sh", BOOK / "chapters")

    banner("STEP 4: build blank/")
    # The old version skipped this target entirely, which is why blank/ drifted.
    run("bash build.sh", BOOK / "blank")

    banner("STEP 5: build and PUBLISH the website")
    print("jb/build.sh ends in `ghp-import -n -p -f`, which pushes straight to")
    print("GitHub Pages. The site goes live as soon as this step finishes.")
    if not args.yes:
        if input("\nPublish the website? [y/N] ").strip().lower() not in ("y", "yes"):
            sys.exit("Stopped before publishing. Steps 1-4 are done and pushed.")
    run("rm -rf _build", BOOK / "jb")   # stale pages have been published before
    run("bash build.sh", BOOK / "jb")

    banner("STEP 6: top-level support files")
    run("bash build.sh", BOOK)

    banner("Done. All four targets built; the website is live.")


if __name__ == "__main__":
    main()
