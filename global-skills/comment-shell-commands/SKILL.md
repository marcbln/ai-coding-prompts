---
name: comment-shell-commands
description: Enforces a `# ==== summary ====` banner as the first line of every bash/shell command payload, with each step preceded by a `# -- ` comment. Remote commands must name the host in the banner, e.g. `# ==== [my-server.de] <summary> ====`. Use whenever running terminal commands, scripts, or automated tools.
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
5. **Remote commands name the host in the banner.** When the payload drives `ssh`, `scp`, `rsync`, `docker -H`, an API host, etc., prefix the summary with the host in brackets: `# ==== [<host>] <summary> ====`. The reader must see *which* machine is being touched without scanning the command body. Use the hostname as written in the command (`my-server.de`, `root@srv3...` → `srv3...`), not an alias the reader cannot map.
6. **Prefer specific, concrete banners over vague ones.** Say *why* the command exists ("try single-key auths to avoid MaxAuthTries") rather than restating the obvious ("run ssh"). Keep it one line, lower-case after the bracket if that reads better.

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

### ✅ Good (remote host named in the banner):
```bash
# ==== [my-server.de] try single-key auths to avoid MaxAuthTries ====
# -- Probe each candidate key with BatchMode and IdentitiesOnly so only that key is offered
for k in ~/.ssh/id_rsa ~/.ssh/topdata-marc ~/.ssh/aaa-sk ~/.ssh/customers-marc; do
  printf '=== %s ===\n' "$k"
  ssh -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=8 -i "$k" my-server.de 'id -un; ls -ld /srv/shipping-platform/prod/app/var 2>&1' 2>&1 | head -5
done
```

### ❌ Bad (remote host only discoverable inside the body):
```bash
# ==== try single-key auths to avoid MaxAuthTries ====
ssh -o BatchMode=yes -o IdentitiesOnly=yes -i ~/.ssh/id_rsa my-server.de 'id -un'
```

### ✅ Good (nested multi-step):
```bash
# ==== [srv3.christenfeldt-edv.de] deploy gl_query.rb, run it in the GitLab container, then clean up ====
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
