#!/bin/bash
# Daily journal publish (one post a day, in the random afternoon slot picked by ops/journal_gate.py):
#   pull -> push leftovers -> build the site "as of today" (the post dated today appears) -> green gate -> commit -> push -> live check -> IndexNow.
# Posts are written ahead as content/journal/<YYYY-MM-DD>-<slug>{,.en}.md; a post dated in the future is simply not built yet (scripts/build_site.py).
# Needs: python3, git (non-interactive push access to origin), network for the live check / IndexNow.
#
# Safety rules (same as the sibling inkisle-rest ops)
#   - Runs only in a dedicated publish clone (MOSSGARDEN_PUBLISH_DIR, default ~/Developer/mossgarden-rest) checked out on `main` with a clean tree;
#     otherwise it does nothing and exits 0 (see the log). Never point it at a clone where feature branches / work in progress live.
#   - Local commits not yet on origin/main (a previous push failed) are pushed first.
#   - Publishing is all-or-nothing: if anything before the commit fails, the tree is reset to the commit it started from.
#   - One run at a time: .git/publish.lock (stale after its process is gone or 3 h).
#   - Only the paths a build creates are staged (never `git add -A` on the whole tree); no deletions are allowed.
#   - The private ipe_web_kit in vendor/ (gitignored) must match vendor/ipe_web_kit.lock; the run re-syncs from MOSSGARDEN_KIT_DIR
#     (default ~/Developer/ipe_web_kit) and fails loudly (KIT_MISMATCH) if it still does not match.
# Last line of a good run (read by journal_gate.py): "publish_daily: pushed <slug>" or "publish_daily: nothing to publish".
# Test hooks: MOSSGARDEN_CHECK_CMD (default "bash scripts/check.sh"), MOSSGARDEN_SKIP_NET=1 (no sleep / live check / IndexNow / notification),
#             MOSSGARDEN_KIT_CHECK_CMD, MOSSGARDEN_KIT_SYNC_CMD, MOSSGARDEN_TODAY (YYYY-MM-DD, default today in KST).
set -euo pipefail
export TZ=Asia/Seoul
export GIT_TERMINAL_PROMPT=0     # under launchd nobody can type a password: fail instead of hanging
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S') KST] publish_daily: $*"; }
skip() { log "SKIP — $*"; exit 0; }

REPO="${MOSSGARDEN_PUBLISH_DIR:-$HOME/Developer/mossgarden-rest}"
CHECK_CMD="${MOSSGARDEN_CHECK_CMD:-bash scripts/check.sh}"
KIT_DIR="${MOSSGARDEN_KIT_DIR:-$HOME/Developer/ipe_web_kit}"
KIT_CHECK_CMD="${MOSSGARDEN_KIT_CHECK_CMD:-python3 scripts/kit_lock.py check}"
KIT_SYNC_CMD="${MOSSGARDEN_KIT_SYNC_CMD:-python3 scripts/kit_lock.py sync --kit \"$KIT_DIR\"}"
TODAY="${MOSSGARDEN_TODAY:-$(date '+%Y-%m-%d')}"
# Everything build_site.py may create or change. The language dirs must be exactly the non-English languages of games.json (en lives at the root).
PUBLISH_PATHS="index.html 404.html sitemap.xml llms.txt robots.txt journal contact privacy ko ja zh-Hant es fr de pt-BR id th vi tr"

[ -d "$REPO/.git" ] || skip "$REPO is not a git clone"
cd "$REPO"

lock="$REPO/.git/publish.lock"
if ! mkdir "$lock" 2>/dev/null; then
  holder="$(cat "$lock/pid" 2>/dev/null || true)"
  if { [ -n "$holder" ] && ! kill -0 "$holder" 2>/dev/null; } || [ -n "$(find "$lock" -maxdepth 0 -mmin +180 2>/dev/null)" ]; then
    log "stale lock (pid ${holder:-?}) — taking over"; rm -rf "$lock"; mkdir "$lock" || skip "could not take the lock"
  else
    skip "another publish run is in progress (pid ${holder:-?})"
  fi
fi
echo $$ > "$lock/pid"
trap 'rm -rf "$lock"' EXIT

branch="$(git symbolic-ref --short -q HEAD || echo '(detached)')"
[ "$branch" = "main" ] || skip "branch is '$branch', not main"
[ -z "$(git status --porcelain)" ] || skip "working tree is not clean"

git fetch -q origin main || { log "FAIL — git fetch"; exit 1; }

# Unpushed local commits must only touch the publish set (+ the journal sources) — never let other work ride along to the public main.
if [ "$(git rev-list --count origin/main..HEAD)" -gt 0 ]; then
  stray=""
  while IFS= read -r f; do
    ok=0
    for p in $PUBLISH_PATHS content/journal; do case "$f" in "$p"|"$p"/*) ok=1;; esac; done
    [ "$ok" = 1 ] || stray="$stray $f"
  done < <(git diff --name-only origin/main...HEAD)
  [ -z "$stray" ] || skip "unpushed commits touch paths outside the publish set:${stray:0:200} — not pushing (move them to a feature branch)"
fi

git rebase -q origin/main || {
  conflicts="$(git diff --name-only --diff-filter=U | head -5 | tr '\n' ' ')"
  git rebase --abort 2>/dev/null || true
  log "FAIL — cannot rebase onto origin/main (conflicts: ${conflicts:-?}) — clone left as it was"
  exit 1
}

if [ "$(git rev-list --count origin/main..HEAD)" -gt 0 ]; then
  log "pushing $(git rev-list --count origin/main..HEAD) unpushed commit(s)"
  git push -q origin HEAD:main || { log "FAIL — push of unpushed commits"; exit 1; }
fi

if ! bash -c "$KIT_CHECK_CMD" >/dev/null 2>&1; then
  log "kit does not match vendor/ipe_web_kit.lock — syncing from $KIT_DIR"
  git -C "$KIT_DIR" fetch -q --tags origin 2>/dev/null || true
  if ! sync_out="$(bash -c "$KIT_SYNC_CMD" 2>&1)" || ! kit_out="$(bash -c "$KIT_CHECK_CMD" 2>&1)"; then
    log "FAIL — KIT_MISMATCH: vendor/ipe_web_kit does not match vendor/ipe_web_kit.lock and the sync from $KIT_DIR failed: ${sync_out:-${kit_out:-?}}"
    if [ "${MOSSGARDEN_SKIP_NET:-0}" != "1" ] && command -v osascript >/dev/null 2>&1; then
      osascript -e 'display notification "ipe_web_kit lock mismatch — journal publish did not run (see mossgarden-publish.log)" with title "mossgarden publish FAILED"' >/dev/null 2>&1 || true
    fi
    exit 1
  fi
  log "kit re-synced: $sync_out"
fi

# Which post is today's? No post dated today = nothing to publish (done for today, the series simply has a gap — make it loud in the log).
post="$(ls content/journal/"$TODAY"-*.md 2>/dev/null | grep -v '\.en\.md$' | head -1 || true)"
if [ -z "$post" ]; then
  log "NO_POST — no content/journal/$TODAY-*.md; write more posts ahead or the daily series has a gap"
  log "nothing to publish"; exit 0
fi
slug="$(basename "$post" .md)"; slug="${slug#"$TODAY"-}"
ahead="$(ls content/journal/*.md 2>/dev/null | grep -v '\.en\.md$' | awk -F/ '{print substr($3,1,10)}' | awk -v t="$TODAY" '$0>t' | sort -u | wc -l | tr -d ' ')"
[ "$ahead" -gt 2 ] || log "QUEUE_LOW $ahead — only $ahead day(s) of posts written after today; write more soon"

base="$(git rev-parse HEAD)"
stage=prepublish
rollback() {
  local ok=1
  git reset -q --hard "$base" || ok=0
  git clean -fdq || ok=0
  stage=rolledback
  if [ "$ok" = 1 ]; then log "ROLLBACK — tree restored to ${base:0:7}"
  else log "ROLLBACK FAILED — the working tree in $REPO is NOT clean; fix by hand (git status; git reset --hard ${base:0:7}; git clean -fd) or every later run SKIPs"; fi
}
on_exit() { local rc=$?; rm -rf "$lock"; if [ "$rc" -ne 0 ] && [ "$stage" = prepublish ]; then rollback; fi; }
trap on_exit EXIT
trap 'log "signal received"; exit 143' INT TERM

if ! out="$(python3 scripts/build_site.py --today "$TODAY" 2>&1)"; then
  echo "$out"; rollback; log "FAIL — build_site"; exit 1
fi
echo "$out"
if [ -z "$(git status --porcelain)" ]; then log "nothing to publish"; exit 0; fi

if ! bash -c "$CHECK_CMD"; then rollback; log "FAIL — green gate"; exit 1; fi

add=""
for p in $PUBLISH_PATHS; do [ -e "$p" ] && add="$add $p"; done
# shellcheck disable=SC2086
git add -A -- $add
if [ -n "$(git status --porcelain | grep -v '^[MADR] ')" ]; then
  git status --short; rollback; log "FAIL — unexpected paths outside the publish set"; exit 1
fi
if [ -n "$(git diff --cached --name-only --diff-filter=D)" ]; then
  rollback; log "FAIL — unexpected deleted files"; exit 1
fi
git diff --cached --stat | tail -1
git commit -q -m "journal: publish ${slug} ($(date '+%Y-%m-%d %H:%M') KST)"
stage=committed
log "committed ${slug}"
git push -q origin HEAD:main || { log "FAIL — push (commit kept locally; the next run pushes it first)"; exit 1; }
log "pushed ${slug}"

[ "${MOSSGARDEN_SKIP_NET:-0}" = "1" ] && exit 0
# IndexNow only after the deploy is live: wait for Pages, then submit today's post and the journal/home pages.
sleep 120
python3 scripts/check_sitemap.py --live || log "live check failed — retry later: python3 scripts/check_sitemap.py --live"
python3 scripts/indexnow.py https://mossgarden.ipe.rest/ https://mossgarden.ipe.rest/journal/ "https://mossgarden.ipe.rest/journal/${slug}/" \
  "https://mossgarden.ipe.rest/ko/journal/${slug}/" || log "IndexNow failed (not critical)"
