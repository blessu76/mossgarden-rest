#!/bin/bash
# Render ops/rest.ipe.mossgarden-publish.plist.template for this user (__HOME__ -> $HOME), lint it, and write it to ~/Library/LaunchAgents.
# It does NOT load the job — that is a separate, deliberate step (see ops/install_launchd.sh header).
#   bash ops/install_launchd.sh            # writes ~/Library/LaunchAgents/rest.ipe.mossgarden-publish.plist
# Test hooks: MOSSGARDEN_LAUNCH_AGENTS_DIR (target dir), MOSSGARDEN_HOME (value for __HOME__, default $HOME).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
home="${MOSSGARDEN_HOME:-$HOME}"
dest_dir="${MOSSGARDEN_LAUNCH_AGENTS_DIR:-$HOME/Library/LaunchAgents}"
dest="$dest_dir/rest.ipe.mossgarden-publish.plist"
case "$home" in /*) ;; *) echo "install_launchd: HOME must be an absolute path (got '$home')" >&2; exit 1;; esac
case "$home" in *'#'*|*'&'*|*'|'*|*'\'*|*$'\n'*) echo "install_launchd: unsupported character (# & | backslash newline) in HOME path" >&2; exit 1;; esac
mkdir -p "$dest_dir" "$home/Library/Logs"
sed "s#__HOME__#$home#g" "$here/rest.ipe.mossgarden-publish.plist.template" > "$dest.tmp"
if command -v plutil >/dev/null 2>&1 && ! plutil -lint "$dest.tmp" >/dev/null; then
  rm -f "$dest.tmp"; echo "install_launchd: rendered plist failed plutil -lint" >&2; exit 1
fi
if grep -q '__HOME__' "$dest.tmp"; then rm -f "$dest.tmp"; echo "install_launchd: unreplaced placeholder" >&2; exit 1; fi
mv "$dest.tmp" "$dest"
echo "wrote $dest"
