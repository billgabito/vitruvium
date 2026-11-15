#!/bin/sh
# Vitruvium self-update. Works when the skill is installed as a Git clone (or a symlink to one).
#   update.sh check            at most once per 24 h: prints one status line (see below)
#   update.sh check --force    check now, ignoring the 24 h limit
#   update.sh apply            fast-forward to the latest release tag, print what changed
#   update.sh mode ask|auto|off   remember the user's choice
# Status lines from `check`:
#   UP_TO_DATE <version> | SKIPPED (checked <24 h ago) | DISABLED (mode off)
#   UPDATE_AVAILABLE <local> <remote> mode=<ask|auto> | NOT_A_GIT_INSTALL <dir> | CHECK_FAILED <reason>
# User settings live in ${VITRUVIUM_HOME:-~/.vitruvium}/update.conf — never inside the skill folder.

set -u
HOME_DIR="${VITRUVIUM_HOME:-$HOME/.vitruvium}"
CONF="$HOME_DIR/update.conf"
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd -P)
ROOT=$(git -C "$SKILL_DIR" rev-parse --show-toplevel 2>/dev/null) || ROOT=""

conf_get() { [ -f "$CONF" ] && sed -n "s/^$1=//p" "$CONF" | tail -1; }
conf_set() {
  mkdir -p "$HOME_DIR"; touch "$CONF"
  grep -v "^$1=" "$CONF" > "$CONF.tmp" 2>/dev/null; echo "$1=$2" >> "$CONF.tmp"; mv "$CONF.tmp" "$CONF"
}
latest_remote() { git -C "$ROOT" ls-remote --tags --refs origin 2>/dev/null | sed 's#.*refs/tags/##' | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sed 's/^v//' | sort -t. -k1,1n -k2,2n -k3,3n | tail -1 | sed 's/^/v/'; }
current() { git -C "$ROOT" describe --tags --abbrev=0 --match 'v[0-9]*' 2>/dev/null; }
newer() { [ "$1" != "$2" ] && [ "$(printf '%s\n%s\n' "$1" "$2" | sed 's/^v//' | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)" = "${2#v}" ]; }

case "${1:-}" in
  mode)
    case "${2:-}" in ask|auto|off) conf_set mode "$2"; echo "MODE $2";; *) echo "usage: update.sh mode ask|auto|off"; exit 2;; esac ;;
  check)
    mode=$(conf_get mode); mode=${mode:-ask}
    [ "$mode" = off ] && { echo "DISABLED"; exit 0; }
    [ -z "$ROOT" ] && { echo "NOT_A_GIT_INSTALL $SKILL_DIR"; exit 0; }
    now=$(date +%s); last=$(conf_get last_check); last=${last:-0}
    if [ "${2:-}" != "--force" ] && [ $((now - last)) -lt 86400 ]; then echo "SKIPPED"; exit 0; fi
    remote=$(latest_remote) || remote=""
    [ -z "$remote" ] && { echo "CHECK_FAILED no access to the repository (offline or no permission)"; exit 0; }
    conf_set last_check "$now"
    local_v=$(current)
    if newer "${local_v:-v0.0.0}" "$remote"; then echo "UPDATE_AVAILABLE ${local_v:-unknown} $remote mode=$mode"; else echo "UP_TO_DATE ${local_v:-unknown}"; fi ;;
  apply)
    [ -z "$ROOT" ] && { echo "NOT_A_GIT_INSTALL $SKILL_DIR"; exit 1; }
    if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then echo "BLOCKED local changes in $ROOT — not touching them"; exit 1; fi
    old=$(current); git -C "$ROOT" fetch --quiet --tags origin || { echo "CHECK_FAILED fetch"; exit 1; }
    new=$(latest_remote)
    newer "${old:-v0.0.0}" "$new" || { echo "UP_TO_DATE ${old:-unknown}"; exit 0; }
    git -C "$ROOT" merge --ff-only --quiet "$new" || { echo "BLOCKED cannot fast-forward to $new (local commits?)"; exit 1; }
    echo "UPDATED $old -> $new"; git -C "$ROOT" log --oneline --no-decorate "$old..$new" ;;
  *) sed -n '2,12p' "$0"; exit 2 ;;
esac
