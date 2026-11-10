#!/bin/bash
# Green gate for mossgarden-rest — run before every commit. Exit 0 = green.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== 0/3 kit"; python3 scripts/kit_lock.py check
echo "== 1/3 sources"; python3 -c "import json;g=json.load(open('games.json'));assert g['id'] and g['name']" && test -f index.html && test -f 404.html
echo "== 2/3 unit tests"; python3 -m unittest discover -s tests -q
echo "GREEN"
