#!/bin/bash
# launchd entry (every 15 min, 12:00-18:45 KST): random afternoon slot gate -> ops/publish_daily.sh (mossgarden journal). Logic + state file docs: ops/journal_gate.py.
set -uo pipefail
export TZ=Asia/Seoul
exec python3 "$(cd "$(dirname "$0")" && pwd)/journal_gate.py"
