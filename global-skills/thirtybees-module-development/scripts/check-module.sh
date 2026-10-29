#!/usr/bin/env bash
#
# Validate a thirty bees module directory.
#
# Usage: check-module.sh <module-dir>
#
# Checks naming, guards, PHP syntax, hook implementations, registered front
# controllers, and upgrade/version consistency. Exits non-zero on errors.

set -u

usage() {
    sed -n '2,8p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

if [ $# -ne 1 ]; then
    usage >&2
    exit 2
fi

module_dir="${1%/}"
if [ ! -d "$module_dir" ]; then
    echo "Not a directory: $module_dir" >&2
    exit 2
fi

module_dir="$(cd "$module_dir" && pwd)"
module_name="$(basename "$module_dir")"
main_file="$module_dir/$module_name.php"

errors=0
warnings=0

err() {
    echo "ERROR: $*" >&2
    errors=$((errors + 1))
}

warn() {
    echo "WARN:  $*" >&2
    warnings=$((warnings + 1))
}

ok() {
    echo "OK:    $*"
}

lower() {
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

# --- Main class -----------------------------------------------------------

if [ ! -f "$main_file" ]; then
    err "missing main file: $main_file (module directory and main file must match)"
else
    actual_class="$(grep -Eoi 'class[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]+extends[[:space:]]+(Module|PaymentModule|CarrierModule|CurrencyRateModule|ImportModule|ModuleGridEngine|ModuleGraphEngine|StockManagerModule|TaxManagerModule|ErrorModule)' "$main_file" | head -1 | awk '{print $2}')"

    if [ -z "$actual_class" ]; then
        err "no module class (extending Module, PaymentModule, CarrierModule, ...) found in $main_file"
    elif [ "$(lower "$actual_class")" != "$(lower "$module_name")" ]; then
        err "main class '$actual_class' does not match folder name '$module_name' (case-insensitive match required)"
    else
        ok "main class: $actual_class"
    fi
fi

# --- _TB_VERSION_ guard in PHP files --------------------------------------

while IFS= read -r file; do
    base="$(basename "$file")"
    rel="${file#"$module_dir"/}"

    if [ "$base" = "index.php" ]; then
        continue
    fi

    if grep -q '_TB_VERSION_' "$file"; then
        continue
    fi

    case "$rel" in
        controllers/*|upgrade/upgrade-*.php)
            err "missing _TB_VERSION_ guard: $file"
            ;;
        */*)
            warn "missing _TB_VERSION_ guard (library file): $file"
            ;;
        *)
            err "missing _TB_VERSION_ guard: $file"
            ;;
    esac
done < <(find "$module_dir" -type f -name '*.php' \
    -not -path '*/.git/*' \
    -not -path '*/.tbstore/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/vendor/*' | sort)

# --- index.php guards in directories --------------------------------------

while IFS= read -r dir; do
    case "$dir" in
        */.git*|*/.tbstore*|*/node_modules*|*/vendor*)
            continue
            ;;
    esac

    if [ ! -f "$dir/index.php" ]; then
        warn "missing index.php guard in $dir"
    fi
done < <(find "$module_dir" -type d \
    -not -path '*/.git*' \
    -not -path '*/.tbstore*' \
    -not -path '*/node_modules*' \
    -not -path '*/vendor*' | sort)

# --- PHP syntax -----------------------------------------------------------

if command -v php >/dev/null 2>&1; then
    while IFS= read -r file; do
        if ! output="$(php -l "$file" 2>&1)"; then
            err "PHP syntax error: $file"
            printf '%s\n' "$output" >&2
        fi
    done < <(find "$module_dir" -type f -name '*.php' \
        -not -path '*/.git/*' \
        -not -path '*/.tbstore/*' \
        -not -path '*/node_modules/*' \
        -not -path '*/vendor/*' | sort)
    ok "php -l"
else
    warn "php not found; skipped syntax checks"
fi

# --- Hooks ----------------------------------------------------------------

if [ -f "$main_file" ]; then
    hook_alias() {
        case "$(lower "$1")" in
            payment)              echo "displayPayment" ;;
            displaypayment)       echo "payment" ;;
            paymentreturn)        echo "displayPaymentReturn" ;;
            displaypaymentreturn) echo "paymentReturn" ;;
            home)                 echo "displayHome" ;;
            displayhome)          echo "home" ;;
            header)               echo "displayHeader" ;;
            displayheader)        echo "header" ;;
            leftcolumn)           echo "displayLeftColumn" ;;
            displayleftcolumn)    echo "leftColumn" ;;
            rightcolumn)          echo "displayRightColumn" ;;
            displayrightcolumn)   echo "rightColumn" ;;
            footer)               echo "displayFooter" ;;
            displayfooter)        echo "footer" ;;
            top)                  echo "displayTop" ;;
            displaytop)           echo "top" ;;
            neworder)             echo "actionValidateOrder" ;;
            updatequantity)       echo "actionUpdateQuantity" ;;
            paymentconfirm)       echo "actionPaymentConfirmation" ;;
            *)                    echo "" ;;
        esac
    }

    hooks="$(grep -Eo 'registerHook[[:space:]]*\([^)]*\)' "$main_file" |
        grep -Eo "'[^']+'" | tr -d "'" | sort -u)"

    if [ -z "$hooks" ]; then
        warn "no literal registerHook() calls found in $main_file (dynamic registration not checked)"
    else
        while IFS= read -r hook; do
            [ -n "$hook" ] || continue

            if grep -Eqi "function[[:space:]]+hook${hook}[[:space:]]*\(" "$main_file"; then
                continue
            fi

            alias="$(hook_alias "$hook")"
            if [ -n "$alias" ] && grep -Eqi "function[[:space:]]+hook${alias}[[:space:]]*\(" "$main_file"; then
                continue
            fi

            err "registered hook '$hook' has no hook${hook}() method in $main_file"
        done <<< "$hooks"
    fi
fi

# --- Registered front controllers -----------------------------------------

if [ -f "$main_file" ]; then
    controllers="$(grep -Eo "([$]this->controllers|public[[:space:]]+[$]controllers)[[:space:]]*=[[:space:]]*\[[^]]*\]" "$main_file" |
        head -1 | grep -Eo "'[^']+'" | tr -d "'" | sort -u)"

    if [ -n "$controllers" ]; then
        while IFS= read -r controller; do
            [ -n "$controller" ] || continue
            if [ ! -f "$module_dir/controllers/front/$controller.php" ]; then
                err "registered front controller '$controller' is missing: controllers/front/$controller.php"
            fi
        done <<< "$controllers"
    fi
fi

# --- Version and upgrade files --------------------------------------------

version=""
if [ -f "$main_file" ]; then
    version="$(grep -Eo "[$]this->version[[:space:]]*=[[:space:]]*'[^']+'" "$main_file" |
        head -1 | sed -E "s/.*'([^']+)'.*/\1/")"
fi

if [ -z "$version" ]; then
    warn "could not read \$this->version from $main_file"
fi

if [ -d "$module_dir/upgrade" ]; then
    while IFS= read -r file; do
        [ -e "$file" ] || continue

        base="$(basename "$file" .php)"
        upgrade_version="${base#upgrade-}"
        upgrade_func="upgrade_module_${upgrade_version//./_}"
        alternate_func="upgradeModule$(printf '%s' "$upgrade_version" | tr -d '.')"

        if ! grep -Eq "function[[:space:]]+${upgrade_func}[[:space:]]*\(" "$file" &&
            ! grep -Eq "function[[:space:]]+${alternate_func}[[:space:]]*\(" "$file"; then
            err "upgrade script $(basename "$file") has no ${upgrade_func}() (or ${alternate_func}()) function"
        fi

        if [ -n "$version" ]; then
            newest="$(printf '%s\n%s\n' "$version" "$upgrade_version" | sort -V | tail -1)"
            if [ "$newest" != "$version" ]; then
                err "upgrade version $upgrade_version is newer than class version $version"
            fi
        fi
    done < <(find "$module_dir/upgrade" -maxdepth 1 -type f -name 'upgrade-*.php' | sort -V)
fi

# --- Summary --------------------------------------------------------------

echo
if [ "$errors" -gt 0 ]; then
    echo "FAILED: $errors error(s), $warnings warning(s)"
    exit 1
fi

echo "PASSED: 0 errors, $warnings warning(s)"
