# Ruleman corpus map

Canonical source: `~/devel/ruleman` (`$RULEMAN_RULES_DIR` overrides the rules
directory, `$RULEMAN_CATALOG` overrides the catalog path).

## Files

```text
rulesets/<id>.json              one ruleset per file, .json (never .yml)
catalog/technologies.json       technology vocabulary {id, name, description}
_ai/conventions.md              generated artifact of this repo (ruleman project)
_ai/rule_proposals/ledger.md    accepted/rejected proposal history
src/rule_manager/               loader, resolver, CLI
```

The copies in atlas (`seeders/rulesets/`, `seeders/reference/technologies.json`)
are frozen. Never edit them; atlas must consume `rule_manager` instead.

## Ruleset file schema

```json
{
  "ruleset": {
    "id": "python",
    "label": "Python Conventions",
    "summary": "PYTHON CONVENTIONS",
    "kind": "ruleset",
    "includes": ["cli"]
  },
  "rules": [
    {
      "id": "python:example",
      "ruleset_id": "python",
      "topic": "python:example",
      "body": "One dense imperative paragraph with concrete tools.",
      "precedence": 50,
      "enabled": true,
      "status": "active",
      "references": [
        { "kind": "url", "ref": "https://...", "title": "Source" }
      ]
    }
  ],
  "assignments": [
    { "ruleset_id": "python", "target_type": "tech", "target_id": "python" }
  ],
  "topics": [
    { "id": "python:example", "description": "One-line description" }
  ]
}
```

- `kind`: `ruleset` (assignable) or `base` (only reachable through `includes`,
  never assigned directly).
- Rule ids are globally unique: `<ruleset>:<topic-slug>`.
- Every rule `topic` must exist in `topics` or be an ancestor of one; ancestors
  are synthesized.
- A tech `target_id` must exist in `catalog/technologies.json`; unknown ids are
  hard errors, never silently ignored.

## Scope and precedence

- Scope: global `0` < tech `1` < project `2`.
- Includes propagate the parent's scope transitively; the most specific scope
  wins.
- Winner for a topic: `max(scope, precedence)`.
- Base rulesets are reachable only through includes.

## Placement

| Concern | Ruleset |
| --- | --- |
| Language or framework behavior | that tech's ruleset (`python`, `sw67-plugin`) |
| Cross-language CLI behavior | `cli` (inherited through `includes`) |
| Full-screen terminal UI | `tui` (includes `cli`) |
| Web UI behavior | `ui` |
| Docs, release, code style | their existing global rulesets |
| One repository only | a project-scoped ruleset or assignment |

Precedence bands: stay inside the host's existing range (for example `python`
20–85, `cli` 40–95). A refinement gets slightly higher precedence than the rule
it refines. Never use precedence to encode project scope.

## Rule body style

One imperative paragraph, concrete tools, commands, paths, and flags. No vague
"should", no prose sections, no code blocks unless the convention is a snippet.
Add a reference when a canonical URL or document exists. Mirror the voice of the
neighbouring rules.

## CLI recipes

```bash
ruleman search "<keyword>" --json
ruleman search "<keyword>" --tech <tech> --json
ruleman search "<keyword>" --ruleset <id> --topic <prefix>
ruleman show <ruleset> --json
ruleman topics --json
ruleman audit --json
ruleman validate --json
ruleman explain <topic> --json        # requires .ctx/ruleman.yaml
ruleman tree --json                   # requires .ctx/ruleman.yaml
ruleman export                        # regenerate the bound artifact
```

`search --tech` expands the include closure, so it answers "would this rule
reach that technology?" accurately.
