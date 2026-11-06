"""Import a QTI zip into the Canvas sandbox course and report what Canvas made of it.

Usage: python canvas_import.py [--new] path/to/quiz.zip

Reads ~/.config/canvas/config (CANVAS_URL, CANVAS_TOKEN, CANVAS_COURSE_ID) and writes only
to the sandbox course. Never prints the token. --new asks for New Quizzes instead.
"""
import sys
import time
from pathlib import Path

import requests

SANDBOX = "629"
NEW_QUIZZES = "--new" in sys.argv


def load_config():
    cfg = {}
    for line in Path("~/.config/canvas/config").expanduser().read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    return cfg["CANVAS_URL"].rstrip("/"), cfg["CANVAS_TOKEN"], cfg["CANVAS_COURSE_ID"]


def main(zip_path):
    url, token, course = load_config()
    assert course == SANDBOX, f"refusing to write to course {course}"
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {token}"
    api = f"{url}/api/v1/courses/{course}"
    zip_path = Path(zip_path)

    before = {q["id"] for q in s.get(f"{api}/quizzes", params={"per_page": 100}).json()}

    # 1. create the migration, with a pre-attachment slot for the file
    r = s.post(f"{api}/content_migrations", data={
        "migration_type": "qti_converter",
        "pre_attachment[name]": zip_path.name,
        "pre_attachment[size]": zip_path.stat().st_size,
        **({"settings[import_quizzes_next]": "true"} if NEW_QUIZZES else {}),
    })
    r.raise_for_status()
    mig = r.json()
    pre = mig["pre_attachment"]

    # 2. upload the file (the upload URL is pre-signed, so no auth header)
    with open(zip_path, "rb") as f:
        up = requests.post(pre["upload_url"], data=pre["upload_params"],
                           files={"file": (zip_path.name, f)}, allow_redirects=False)
    if up.status_code in (301, 302, 303):
        s.get(up.headers["Location"])
    elif not up.ok:
        sys.exit(f"upload failed: HTTP {up.status_code} {up.text[:300]}")

    # 3. poll until the migration finishes
    for _ in range(90):
        m = s.get(f"{api}/content_migrations/{mig['id']}").json()
        if m["workflow_state"] in ("completed", "failed"):
            break
        time.sleep(2)
    print(f"{zip_path.name}: migration {mig['id']} -> {m['workflow_state']}")

    # 4. what Canvas said, and what it made
    for issue in s.get(f"{api}/content_migrations/{mig['id']}/migration_issues",
                       params={"per_page": 100}).json():
        print(f"  issue [{issue.get('issue_type')}]: {issue.get('description')}")
        if issue.get("error_message"):
            print(f"    {issue['error_message'][:300]}")
    if NEW_QUIZZES:
        nq = s.get(f"{url}/api/quiz/v1/courses/{course}/quizzes").json()
        print(f"  New Quizzes in course: {[(q.get('id'), q.get('title')) for q in nq]}")
        for q in nq:
            items = s.get(f"{url}/api/quiz/v1/courses/{course}/quizzes/{q['id']}/items").json()
            print(f"    {q['title']!r}: {len(items)} items")
            for it in items[:2]:
                e = it.get("entry", {})
                print(f"      {e.get('interaction_type_slug')}: {str(e.get('item_body'))[:90]!r}")
        return
    new = [q for q in s.get(f"{api}/quizzes", params={"per_page": 100}).json()
           if q["id"] not in before]
    if not new:
        print("  no quizzes created")
    for q in new:
        qs = s.get(f"{api}/quizzes/{q['id']}/questions", params={"per_page": 100}).json()
        print(f"  quiz {q['id']} {q['title']!r}: {len(qs)} questions")
        for qq in qs[:2]:
            answers = [(a.get('text') or a.get('html') or '')[:40] + (' *' if a.get('weight') else '')
                       for a in qq.get('answers', [])]
            print(f"    {qq['question_type']}: {qq['question_text'][:70]!r}")
            print(f"      answers: {answers}")


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")][0])
