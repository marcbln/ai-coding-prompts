---
name: comment-shell-commands
description: Enforces a `# ==== summary ====` banner as the first line of every bash/shell command payload, with each step preceded by a `# -- ` comment. Use whenever running terminal commands, scripts, or automated tools.
---

# Comment Shell Commands

## Purpose
Ensure all commands executed via the shell or terminal tool are self-documenting and immediately clear to human observers.

## Rule
Whenever you execute a command using the `bash` or terminal tool:
1. **The first line inside the command payload must be a banner**: `# ==== <one-line summary of the whole payload> ====`.
2. The banner states **what** the payload does and **why** at the highest level. It replaces the old top summary comment.
3. **Each executable step is preceded by a `# -- <description>` comment** so commands are easy to separate visually.
4. Step comments describe the action; they must not repeat the banner's wording.

## Examples

### ❌ Bad:
```bash
for i in $(seq 1 24); do txt=$(agent-browser eval 'document.body.innerText.slice(0,80)' 2>/dev/null); ...
```

### ✅ Good (single step):
```bash
# ==== Inspect the repository cache after the page settles ====
# -- Poll the browser until 'Look again' appears (up to 6m)
for i in $(seq 1 24); do txt=$(agent-browser eval 'document.body.innerText.slice(0,80)' 2>/dev/null); ...
```

### ✅ Good (multi-step):
```bash
# ==== Set light theme, open the app, and capture a screenshot ====
# -- Persist the light theme in local storage
agent-browser eval 'localStorage.setItem("topdata.theme.v1","light")' >/dev/null
# -- Open the app, wait for render, then capture the screenshot
agent-browser open http://localhost:5183 && sleep 2 && agent-browser screenshot /tmp/opencode/rm-cached.png
```

### ✅ Good (nested multi-step):
```bash
# ==== Deploy gl_query.rb to srv3, run it in the GitLab container, then clean up ====
# -- Copy the query script to srv3
scp -q -o IdentitiesOnly=yes -o BatchMode=yes -i ~/.ssh/customers-marc /tmp/opencode/gl_query.rb root@srv3.christenfeldt-edv.de:/tmp/gl_query.rb \
  && ssh -o IdentitiesOnly=yes -o BatchMode=yes -i ~/.ssh/customers-marc root@srv3.christenfeldt-edv.de '
# -- Copy the script into the GitLab container and execute it with Rails in production
docker cp /tmp/gl_query.rb gl3christenfeldt-edvde-gitlab-1:/tmp/gl_query.rb >/dev/null
docker exec -i gl3christenfeldt-edvde-gitlab-1 sudo -u git -H env RAILS_ENV=production bundle exec rails runner /tmp/gl_query.rb 2>&1 | grep -v "warning\|deprecated\|DEPRECATION" | head -140
# -- Remove the temporary script from the host
rm -f /tmp/gl_query.rb
'
```
