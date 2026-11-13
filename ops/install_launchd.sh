#!/bin/bash
# Render ops/rest.ipe.mossgarden-publish.plist.template for this user (__HOME__ -> $HOME), lint it, and write it to ~/Library/LaunchAgents.
# Also checks the Mac's time zone is KST (the plist ticks are LOCAL time) and that the dedicated publish clone ~/ipe-publish/mossgarden-rest exists
# (a separate clone of the real origin — create it first: git clone <origin-url> ~/ipe-publish/mossgarden-rest); marks it `ipe.publishClone true`.
# It does NOT load the job — that is a separate, deliberate step (see ops/install_launchd.sh header).
#   bash ops/install_launchd.sh            # writes ~/Library/LaunchAgents/rest.ipe.mossgarden-publish.plist
# Test hooks: MOSSGARDEN_LAUNCH_AGENTS_DIR (target dir), MOSSGARDEN_HOME (value for __HOME__, default $HOME),
#             MOSSGARDEN_LOCAL_UTC_OFFSET (e.g. +0900, instead of `date +%z`), MOSSGARDEN_SKIP_CLONE_CHECK=1.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
home="${MOSSGARDEN_HOME:-$HOME}"
dest_dir="${MOSSGARDEN_LAUNCH_AGENTS_DIR:-$HOME/Library/LaunchAgents}"
dest="$dest_dir/rest.ipe.mossgarden-publish.plist"
case "$home" in /*) ;; *) echo "install_launchd: HOME must be an absolute path (got '$home')" >&2; exit 1;; esac
case "$home" in *'#'*|*'&'*|*'|'*|*'\'*|*$'\n'*) echo "install_launchd: unsupported character (# & | backslash newline) in HOME path" >&2; exit 1;; esac
offset="${MOSSGARDEN_LOCAL_UTC_OFFSET:-$(env -u TZ date +%z)}"
if [ "$offset" != "+0900" ]; then
  echo "install_launchd: this Mac's local time zone is UTC$offset, not KST (+0900) — launchd ticks use local time and would fire at the wrong hours. Fix: sudo systemsetup -settimezone Asia/Seoul" >&2; exit 1
fi
clone="$home/ipe-publish/mossgarden-rest"
if [ "${MOSSGARDEN_SKIP_CLONE_CHECK:-0}" != "1" ]; then
  if [ ! -d "$clone/.git" ]; then
    echo "install_launchd: publish clone missing: $clone — create it: git clone <origin-url> $clone" >&2; exit 1
  fi
  [ "$(git -C "$clone" symbolic-ref --short -q HEAD || true)" = "main" ] || { echo "install_launchd: $clone is not on main" >&2; exit 1; }
  git -C "$clone" config --local ipe.publishClone true
fi
mkdir -p "$dest_dir" "$home/Library/Logs"
sed "s#__HOME__#$home#g" "$here/rest.ipe.mossgarden-publish.plist.template" > "$dest.tmp"
if command -v plutil >/dev/null 2>&1 && ! plutil -lint "$dest.tmp" >/dev/null; then
  rm -f "$dest.tmp"; echo "install_launchd: rendered plist failed plutil -lint" >&2; exit 1
fi
if grep -q '__HOME__' "$dest.tmp"; then rm -f "$dest.tmp"; echo "install_launchd: unreplaced placeholder" >&2; exit 1; fi
mv "$dest.tmp" "$dest"
echo "wrote $dest"
