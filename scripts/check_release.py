#!/usr/bin/env python3
"""Release-note gate for TestFlight builds — thin wrapper over the kit `releases` module. Exit 0 = ready, 1 = not.

  python3 scripts/check_release.py --build 3          # build 3 passes the kit lint (ko+en, items, length, words)
  python3 scripts/check_release.py --build 3 --latest # ... and build 3 is also the newest entry (app = TF = notes)
  python3 scripts/check_release.py --all              # structure of every entry + full lint of the newest (check.sh runs this)

The app repo's deploy_ios.sh calls this script (from the site repo, no --root) before every TestFlight
upload, so a build can no longer go out without its release note (Davy 11-07: app version = TF build =
release note, no bypass). The rules live in vendor/ipe_web_kit/data/release_rules.json; the languages come
from games.json. content/releases.json is this site's data copy of the in-app notes.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "vendor"))
from ipe_web_kit import releases as kr  # noqa: E402


REQUIRED = ("ko", "en")  # notes are written by hand in ko+en only; the other site languages fall back to en (kit RN14 = warning)


def parse_build(raw):
    """'2' or '1.0.0+2' -> '2'; None if it is neither."""
    m = re.match(r"^(?:\d+(?:\.\d+)*\+)?(\d+)$", str(raw).strip())
    return str(int(m.group(1))) if m else None


def langs(root):
    """Languages the site publishes — games.json is the single source of truth."""
    try:
        g = json.loads((Path(root) / "games.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as ex:
        raise SystemExit("check_release: cannot read games.json: %s" % ex)
    ls = tuple(g.get("langs", ()))
    if not ls:
        raise SystemExit('check_release: games.json has no "langs"')
    return ls


def load(root):
    """-> (SiteDoc or None, problems)"""
    f = Path(root) / "content" / "releases.json"
    if not f.is_file():
        return None, ["content/releases.json: missing"]
    try:
        return kr.load_site(f), []
    except (ValueError, KeyError, TypeError) as ex:
        return None, ["content/releases.json: %s" % ex]


def _errors(problems):
    return ["%s %s" % (p.code, p.msg) for p in problems if p.level == "error"]


def check(root, build, latest=False):
    """-> problems (empty = the note for build is complete)."""
    n = parse_build(build)
    if n is None:
        return ["--build must be a build number such as 3 or 1.0.0+3, got %r" % build]
    ls = langs(root)
    site, errs = load(root)
    if site is None:
        return errs
    hits = [r for r in site.releases if r.build == n]
    if not hits:
        return errs + ["build %s: no entry in content/releases.json (add one with notes for %s)" % (n, " + ".join(REQUIRED))]
    if len(hits) > 1:
        errs.append("build %s: %d entries in content/releases.json, expected one" % (n, len(hits)))
    errs += _errors(kr.lint_site(site, langs=REQUIRED, build=n, site_langs=ls))
    if latest:
        newer = sorted({r.build for r in site.releases if r.build_int > int(n)}, key=int)
        if newer:
            errs.append("build %s: not the newest note — content/releases.json already has build %s" % (n, ", ".join(newer)))
    return errs


def check_all(root):
    """-> problems (empty = there is at least one entry, every entry is well-formed, and the newest is complete)."""
    ls = langs(root)
    site, errs = load(root)
    if site is None:
        return errs
    if not site.releases:
        return errs + ["content/releases.json: no entries"]
    return errs + _errors(kr.lint_site(site, langs=REQUIRED, site_langs=ls))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check that the TestFlight release note(s) in content/releases.json are complete.")
    ap.add_argument("--build", help="build number, e.g. 3 or 1.0.0+3")
    ap.add_argument("--all", action="store_true", help="check every entry's structure and the newest entry in full (check.sh)")
    ap.add_argument("--latest", action="store_true", help="also require this build to be the newest entry in releases.json")
    ap.add_argument("--root", default=str(HERE.parent), help="site repo root (default: this repo)")
    a = ap.parse_args(argv)
    if bool(a.build) == a.all:
        ap.error("use exactly one of --build N or --all")
    errs = check_all(a.root) if a.all else check(a.root, a.build, latest=a.latest)
    if errs:
        print("release notes NOT ready:")
        for x in errs:
            print("  - " + x)
        return 1
    print("release notes OK (%s)" % ("all entries" if a.all else "build %s" % parse_build(a.build)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
