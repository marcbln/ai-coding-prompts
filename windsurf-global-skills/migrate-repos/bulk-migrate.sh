#!/usr/bin/env bash
# A safe automation script for AI agents to bulk-migrate repositories

set -e

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <bitbucket-workspace> <github-org> <repo1> [<repo2> ...]"
    echo "Example: $0 topdata some-company-gmbh scrapers backend frontend"
    exit 1
fi

BITBUCKET_WS=$1
GITHUB_ORG=$2
shift 2
REPOS=("$@")

WORK_DIR="/tmp/repo-migrations"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "Starting migration of ${#REPOS[@]} repositories..."
echo "Source: Bitbucket ($BITBUCKET_WS) | Target: GitHub ($GITHUB_ORG)"
echo "--------------------------------------------------------"

for REPO in "${REPOS[@]}"; do
    echo ">>> Processing: $REPO"
    
    # 1. Mirror clone from Bitbucket
    if ! git clone --mirror "git@bitbucket.org:${BITBUCKET_WS}/${REPO}.git"; then
        echo "❌ Failed to clone ${REPO} from Bitbucket. Skipping."
        continue
    fi
    
    cd "${REPO}.git"
    
    # 2. Create the GitHub repository (fails gracefully if it already exists)
    echo ">>> Creating GitHub repository: ${GITHUB_ORG}/${REPO}"
    if ! gh repo create "${GITHUB_ORG}/${REPO}" --private; then
        echo "⚠️  Repo might already exist or gh cli error. Attempting push anyway..."
    fi
    
    # 3. Mirror push to GitHub
    echo ">>> Pushing mirrored data to GitHub..."
    if ! git push --mirror "git@github.com:${GITHUB_ORG}/${REPO}.git"; then
        echo "❌ Failed to push ${REPO} to GitHub."
    else
        echo "✅ Successfully migrated ${REPO}!"
    fi
    
    # 4. Clean up the temp folder for this repo
    cd ..
    rm -rf "${REPO}.git"
    echo "--------------------------------------------------------"
done

echo "🎉 Bulk migration complete!"

