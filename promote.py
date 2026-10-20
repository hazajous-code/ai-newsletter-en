"""Scheduled publishing: promote issues listed in scheduled.json to the front page on their publish date (KST).

- issues/<id>.html            -> index.html    (Newsletter)
- issues/<id>-marketer.html   -> marketer.html (Marketer Kit)
- adds one line under <!-- ARCHIVE:START --> in archive.html
- marks the entry "promoted": true in scheduled.json (safe to run repeatedly)

Run every morning by .github/workflows/daily.yml.
"""
import datetime as dt
import json
import pathlib
import re
import sys

T = pathlib.Path(__file__).resolve().parent  # repo root
KST = dt.timezone(dt.timedelta(hours=9))


def to_root(html: str, iid: str) -> str:
    html = html.replace('href="../', 'href="')
    html = html.replace(f'href="{iid}-marketer.html"', 'href="marketer.html"')
    html = html.replace(f'href="{iid}.html"', 'href="index.html"')
    return html


def main(today: str | None = None) -> int:
    today = today or dt.datetime.now(KST).strftime("%Y-%m-%d")
    path = T / "scheduled.json"
    if not path.exists():
        print("no scheduled.json")
        return 0
    items = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for it in sorted(items, key=lambda x: x["date"]):
        if it.get("promoted") or it["date"] > today:
            continue
        iid = it["id"]
        nl = (T / "issues" / f"{iid}.html").read_text(encoding="utf-8")
        mk = (T / "issues" / f"{iid}-marketer.html").read_text(encoding="utf-8")
        (T / "index.html").write_text(to_root(nl, iid), encoding="utf-8")
        (T / "marketer.html").write_text(to_root(mk, iid), encoding="utf-8")
        ar = (T / "archive.html").read_text(encoding="utf-8")
        if f'issues/{iid}.html' not in ar:
            line = (f'  <li><time>{it["date"].replace("-", ".")}</time><span><a href="issues/{iid}.html">{it["title"]}</a>'
                    f' · <a href="issues/{iid}-marketer.html" class="muted">Marketer Kit</a></span></li>')
            ar = ar.replace("<!-- ARCHIVE:START -->", "<!-- ARCHIVE:START -->\n" + line, 1)
            (T / "archive.html").write_text(ar, encoding="utf-8")
        it["promoted"] = True
        it["promoted_at"] = dt.datetime.now(KST).isoformat(timespec="minutes")
        changed = True
        print(f"published: {iid} — {it['title']}")
    if changed:
        path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print(f"nothing scheduled for {today}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
