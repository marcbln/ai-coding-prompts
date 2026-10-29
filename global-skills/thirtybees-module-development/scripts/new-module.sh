#!/usr/bin/env bash
#
# Scaffold a thirty bees module from assets/module-skeleton.
#
# Usage:
#   new-module.sh <module-name> [modules-dir] [options]
#
# Options:
#   --author NAME          Module author (default: git user.name or "Your Company")
#   --display-name NAME    Human-readable name (default: derived from module name)
#   --description TEXT     Module description
#   --version VERSION      Initial version (default: 1.0.0)
#   -h, --help             Show this help
#
# The module name is lowercased; hyphens become underscores because the main
# class name must match the module directory case-insensitively.

set -u

usage() {
    sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skeleton_dir="$script_dir/../assets/module-skeleton"

if [ ! -d "$skeleton_dir" ]; then
    echo "Skeleton not found: $skeleton_dir" >&2
    exit 1
fi

module_name=""
target_dir="."
author="${TB_MODULE_AUTHOR:-$(git config user.name 2>/dev/null || true)}"
author="${author:-Your Company}"
display_name=""
description=""
version="1.0.0"

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        --author)
            [ $# -ge 2 ] || { echo "--author requires a value" >&2; exit 2; }
            author="$2"
            shift 2
            ;;
        --display-name)
            [ $# -ge 2 ] || { echo "--display-name requires a value" >&2; exit 2; }
            display_name="$2"
            shift 2
            ;;
        --description)
            [ $# -ge 2 ] || { echo "--description requires a value" >&2; exit 2; }
            description="$2"
            shift 2
            ;;
        --version)
            [ $# -ge 2 ] || { echo "--version requires a value" >&2; exit 2; }
            version="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
        *)
            if [ -z "$module_name" ]; then
                module_name="$1"
            elif [ "$target_dir" = "." ]; then
                target_dir="$1"
            else
                echo "Unexpected argument: $1" >&2
                usage >&2
                exit 2
            fi
            shift
            ;;
    esac
done

if [ -z "$module_name" ]; then
    echo "Missing module name." >&2
    usage >&2
    exit 2
fi

original_name="$module_name"
module_name="$(printf '%s' "$module_name" | tr '[:upper:]-' '[:lower:]_')"

if ! printf '%s' "$module_name" | grep -Eq '^[a-z][a-z0-9_]*$'; then
    echo "Invalid module name: $original_name" >&2
    echo "Use lowercase letters, digits and underscores; start with a letter." >&2
    exit 2
fi

case "$module_name" in
    module|paymentmodule|carriermodule|index|admin|config|classes|controllers|views)
        echo "Reserved module name: $module_name" >&2
        exit 2
        ;;
esac

if [ "$module_name" != "$original_name" ]; then
    echo "Note: module name normalized to '$module_name' so the class name can match the directory."
fi

class_name="$(printf '%s' "${module_name:0:1}" | tr '[:lower:]' '[:upper:]')${module_name:1}"
prefix="$(printf '%s' "$module_name" | tr '[:lower:]' '[:upper:]' | sed 's/[^A-Z0-9]/_/g')"

if [ -z "$display_name" ]; then
    display_name="$(printf '%s' "$module_name" | tr '_' ' ' | sed 's/\b\([a-z]\)/\u\1/g')"
fi

if [ -z "$description" ]; then
    description="$display_name module for thirty bees."
fi

year="$(date +%Y)"
dest="$target_dir/$module_name"

if [ -e "$dest" ]; then
    echo "Target already exists: $dest" >&2
    exit 1
fi

mkdir -p "$target_dir" || exit 1
cp -a "$skeleton_dir" "$dest" || exit 1
mv "$dest/__MODULE__.php" "$dest/$module_name.php" || exit 1

escape_sed() {
    printf '%s' "$1" | sed -e 's/[\\&|]/\\&/g'
}

v_module="$(escape_sed "$module_name")"
v_class="$(escape_sed "$class_name")"
v_prefix="$(escape_sed "$prefix")"
v_display="$(escape_sed "$display_name")"
v_description="$(escape_sed "$description")"
v_author="$(escape_sed "$author")"
v_version="$(escape_sed "$version")"
v_year="$(escape_sed "$year")"

find "$dest" -type f \( -name '*.php' -o -name '*.tpl' \) -print0 |
    while IFS= read -r -d '' file; do
        sed -i \
            -e "s|__MODULE__|$v_module|g" \
            -e "s|__CLASS__|$v_class|g" \
            -e "s|__PREFIX__|$v_prefix|g" \
            -e "s|__DISPLAY_NAME__|$v_display|g" \
            -e "s|__DESCRIPTION__|$v_description|g" \
            -e "s|__AUTHOR__|$v_author|g" \
            -e "s|__VERSION__|$v_version|g" \
            -e "s|__YEAR__|$v_year|g" \
            "$file" || exit 1
    done

echo "Created $dest"
echo
echo "Next steps:"
echo "  1. Review $dest/$module_name.php (metadata, hooks, settings)."
echo "  2. Copy or symlink the module into a shop's modules/ directory."
echo "  3. Install it from the Module Manager (or a dev bootstrap)."
echo "  4. Run: $script_dir/check-module.sh $dest"

if command -v php >/dev/null 2>&1; then
    echo
    echo "Syntax check:"
    find "$dest" -name '*.php' -print0 | while IFS= read -r -d '' file; do
        php -l "$file" >/dev/null && echo "  OK   $file" || echo "  FAIL $file"
    done
fi

if [ -x "$script_dir/check-module.sh" ]; then
    "$script_dir/check-module.sh" "$dest" || true
fi
