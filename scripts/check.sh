#!/bin/bash
# Green gate for mossgarden-rest — run before every commit. Exit 0 = green.
#   scripts/check.sh              # kit + sources + tests + build (into a temp copy) + sitemap check
#   scripts/check.sh --all-langs  # additionally require all languages for every page
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== 0/5 kit"; python3 scripts/kit_lock.py check
echo "== 1/5 sources"; python3 scripts/build_site.py --check ${1:+--require-all}
echo "== 2/5 unit tests"; python3 -m unittest discover -s tests -q
echo "== 3/5 build is up to date"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
rsync -a --exclude='.git' ./ "$tmp/"
# "as of" the newest post already built into the committed /journal/ (empty = today): posts scheduled for later days are not "stale"
asof="$(python3 scripts/build_site.py --built-through)"
python3 scripts/build_site.py --root "$tmp" ${asof:+--today "$asof"} >/dev/null
if ! diff -r -q --exclude='.git' --exclude='__pycache__' --exclude='scripts' --exclude='tests' --exclude='docs' --exclude='ops' --exclude='.github' \
   --exclude='content' --exclude='assets' --exclude='*.md' --exclude='*.txt' --exclude='CNAME' --exclude='.nojekyll' . "$tmp" >/dev/null 2>&1; then
  echo "generated files are stale — run: python3 scripts/build_site.py"; exit 1
fi
for f in llms.txt robots.txt; do cmp -s "$f" "$tmp/$f" || { echo "$f is stale — run: python3 scripts/build_site.py"; exit 1; }; done
echo "== 4/5 sitemap"; python3 scripts/check_sitemap.py
echo "== 5/5 journal gate (ops/)"; bash -n ops/journal_gate.sh ops/publish_daily.sh ops/install_launchd.sh
echo "GREEN"
