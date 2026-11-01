#!/usr/bin/env bash
# install-git-hooks.sh
# Install this repository's git hooks into the local .git/hooks directory.
#
# Hooks are symlinked so edits in scripts/git-hooks/ take effect immediately.
# An existing foreign hook is backed up instead of being overwritten silently.

# -e: exit on unhandled failure
# -u: treat unset variables as an error
# -o pipefail: fail a pipeline when any command fails
set -euo pipefail

readonly SCRIPT_NAME="$(basename -- "${BASH_SOURCE[0]}")"
readonly HOOK_NAME="post-commit"

# Print usage information.
usage() {
    cat <<EOF
Usage: scripts/${SCRIPT_NAME} [--force] [--uninstall]

Install the ${HOOK_NAME} hook that refreshes skillman after commits that
touch global-skills/.

Options:
  -f, --force      Replace an existing hook, backing it up first.
  -u, --uninstall  Remove the hook if this installer created it.
  -h, --help       Show this help and exit.
EOF
}

force=false
uninstall=false

for arg in "$@"; do
    case "$arg" in
        -h|--help)
            usage
            exit 0
            ;;
        -f|--force)
            force=true
            ;;
        -u|--uninstall)
            uninstall=true
            ;;
        *)
            printf 'Error: unknown argument: %s\n\n' "$arg" >&2
            usage >&2
            exit 2
            ;;
    esac
done

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd -- "$script_dir/.." && pwd)"
source_hook="$repo_root/scripts/git-hooks/$HOOK_NAME"

if [[ ! -f "$source_hook" ]]; then
    printf 'Error: hook source not found: %s\n' "$source_hook" >&2
    exit 1
fi

git_dir="$(git -C "$repo_root" rev-parse --git-path hooks)"
if [[ "$git_dir" != /* ]]; then
    git_dir="$repo_root/$git_dir"
fi
target_hook="$git_dir/$HOOK_NAME"

if [[ "$uninstall" == true ]]; then
    if [[ -L "$target_hook" && "$(readlink -- "$target_hook")" == "$source_hook" ]]; then
        rm -- "$target_hook"
        printf 'Removed %s\n' "$target_hook"
    else
        printf 'Nothing to do: %s is not managed by this installer.\n' "$target_hook"
    fi
    exit 0
fi

mkdir -p -- "$git_dir"

if [[ -e "$target_hook" || -L "$target_hook" ]]; then
    if [[ -L "$target_hook" && "$(readlink -- "$target_hook")" == "$source_hook" ]]; then
        printf 'Already installed: %s\n' "$target_hook"
        exit 0
    fi

    if [[ "$force" != true ]]; then
        printf 'Error: %s already exists.\n' "$target_hook" >&2
        printf 'Re-run with --force to back it up and replace it.\n' >&2
        exit 1
    fi

    backup="$target_hook.backup-$(date +%Y%m%d%H%M%S)"
    mv -- "$target_hook" "$backup"
    printf 'Backed up existing hook to %s\n' "$backup"
fi

chmod +x -- "$source_hook"
ln -s -- "$source_hook" "$target_hook"
printf 'Installed %s -> %s\n' "$target_hook" "$source_hook"
