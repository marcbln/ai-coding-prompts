# Shopware check — <plugin> against <target-tag>

- **Range:** <anchor-tag> → <target-tag> (<maintenance | line-upgrade>)
- **Date:** <YYYY-MM-DD> · **By:** <agent + model, or human>
- **Verification:** <static | smoke | tests | qa> · **Result:** <pass | partial | fail>

## Findings

### Affected

| Signal (symbol / path / event) | Source (UPGRADE § or changelog file) | Impact | Action taken |
|---|---|---|---|
| `Shopware\...\Foo` | UPGRADE-6.7.md § 6.7.15.0 | ... | updated decorator |

### Checked, not affected

- <symbol/path> — <why it was considered and cleared>

## Changes made

- `<file>` — <reason>

## Verification evidence

- <command/test run and its result>

## Follow-ups / risks

- <uncertain behavioral risk, deprecation to revisit before 6.9, missing test coverage, ...>
