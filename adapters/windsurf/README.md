# Windsurf Adapter

This adapter wires the content of `ai-coding-prompts` into
[Windsurf](https://www.windsurf.com/) (Cascade).

## 1 – Distribute rules with Ruler

Run this from the repository root to generate Windsurf's `AGENTS.md`:

```bash
ruler apply --config adapters/windsurf/ruler.toml
```

Ruler reads the files in `.ruler/` and writes `AGENTS.md` to the project root,
which Windsurf picks up automatically.

## 2 – Install global skills (optional)

The `windsurf-global-skills/` directory contains Windsurf skills that are
available in every workspace.

> **Note on paths**: On Mac/Linux the Windsurf data directory is
> `~/.codeium/windsurf-next/`; on Windows it is
> `%APPDATA%\Codeium\Windsurf\`. These are the actual platform-specific paths
> used by Windsurf.

**Mac / Linux**

```bash
# Remove (or back up) the existing global skills folder
rm -rf ~/.codeium/windsurf-next/skills

# Create a symlink
ln -s "$(pwd)/windsurf-global-skills" ~/.codeium/windsurf-next/skills
```

**Windows (as Administrator)**

```cmd
rmdir /s /q "%APPDATA%\Codeium\Windsurf\global_skills"
mklink /D "%APPDATA%\Codeium\Windsurf\global_skills" "%CD%\windsurf-global-skills"
```

## 3 – Install global workflows (optional)

The `windsurf-global-workflows/` directory contains reusable workflow prompts.

**Mac / Linux**

```bash
rm -rf ~/.codeium/windsurf-next/global_workflows
ln -s "$(pwd)/windsurf-global-workflows" ~/.codeium/windsurf-next/global_workflows
```

**Windows (as Administrator)**

```cmd
rmdir /s /q "%APPDATA%\Codeium\Windsurf\global_workflows"
mklink /D "%APPDATA%\Codeium\Windsurf\global_workflows" "%CD%\windsurf-global-workflows"
```

Restart Windsurf after creating symlinks to load the new skills and workflows.
