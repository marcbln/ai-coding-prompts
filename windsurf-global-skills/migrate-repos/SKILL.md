---
name: migrate-repos
description: Automates the safe migration of one or multiple Git repositories from Bitbucket to a private GitHub organization or user account. Use this when the user asks to migrate, transfer, or move repositories from Bitbucket to GitHub.
---

# Bitbucket to GitHub Migration Skill

This skill provides a safe, repeatable workflow for migrating repositories from Bitbucket to GitHub using a "perfect mirror" technique to ensure all branches, tags, and commit histories are preserved exactly.

## Safety Rules (CRITICAL)
1. **Never delete** the original Bitbucket repository.
2. **Never delete or modify** the user's existing local working directories unless explicitly asked to update their remotes.
3. Always use a temporary directory (e.g., `/tmp/repo-migrations`) for the mirror clones to avoid interfering with current local setups.
4. Always create the target GitHub repositories as **private** (`--private`) to prevent accidental data leaks.
5. If the target GitHub repo already exists, ask the user before overwriting or pushing.

## Workflow: Single Repository
If the user asks to migrate a single repository, run the following commands step-by-step:
1. `mkdir -p /tmp/repo-migrations && cd /tmp/repo-migrations`
2. `git clone --mirror git@bitbucket.org:<bitbucket-workspace>/<repo-name>.git`
3. `cd <repo-name>.git`
4. `gh repo create <github-org>/<repo-name> --private`
5. `git push --mirror git@github.com:<github-org>/<repo-name>.git`
6. `cd .. && rm -rf <repo-name>.git`

## Workflow: Bulk / Multiple Repositories
If the user provides a list of multiple repositories to migrate, do not run the commands manually. Instead, use the bundled automation script:
1. Locate the `bulk-migrate.sh` script in this skill's directory.
2. Make it executable: `chmod +x bulk-migrate.sh`.
3. Execute it using the format: `./bulk-migrate.sh <bitbucket-workspace> <github-org> <repo1> <repo2> <repo3> ...`

## Post-Migration (Optional)
If the user is currently inside a local clone of a newly migrated repository, ask if they want their local remotes updated. If yes, run:
```bash
git remote rename origin bitbucket
git remote add origin git@github.com:<github-org>/<repo-name>.git
git fetch origin
```

