---
name: sw6-plugin-manual
description: Creates and updates bilingual (German and English) user manuals for Topdata Shopware 6 plugins. Use when writing a new manual for a plugin without one, extending an existing manual (adding sections like usage, demo-setup, features), or updating a manual for a new plugin release. Generates numbered markdown files (10-installation, 30-settings, 40-faq, etc.) in the plugin's manual/ folder, always as matching .de.md and .en.md pairs. Derives content from the plugin source code (config.xml settings, composer.json), the plugin README, and previous manual versions in /topdata/sw6-plugin-manuals. Do not use for technical developer documentation or API references.
---

# SW6 Plugin User Manual

Create or update end-user documentation (not developer docs) for Topdata Shopware 6 plugins: bilingual `.de.md` / `.en.md` markdown files in the plugin repository's `manual/` folder. During a release, `sw-build` copies this folder into `/topdata/sw6-plugin-manuals`, from which the docs site (docs.topinfra.de) is built.

## When to use

- Plugin has no `manual/` folder yet → create a complete manual.
- Plugin has an existing manual → extend it (new sections, e.g. `50-usage`) or update it for a new release (reuse unchanged content, refresh changed parts).

## Workflow

1. **Locate sources**
   - Plugin repo: `<plugin>/manual/` (existing manual), `composer.json` (package name, description), `src/Resources/config/config.xml` (settings with bilingual labels), `README.md`.
   - Prior versions: `/topdata/sw6-plugin-manuals/docs/<PluginName>/` (copy unchanged content from the latest version instead of rewriting).

2. **Determine sections** (flexible with defaults)
   - Defaults: `10-installation`, `30-settings`, `40-faq`, plus `index`.
   - Add plugin-specific sections as needed: `50-usage`, `50-demo-setup`, `40-features`, `35-config-translation`, `20-usage`, `50-troubleshooting`. Skip sections that do not apply (e.g. no FAQ → omit `40-faq`).

3. **Write the `index.{en,de}.md`** with TOC linking to the section files, Overview, Key Features, Getting Started, Support. See [structure.md](references/structure.md).

4. **Write each section** in both languages:
   - `10-installation`: system requirements, `composer require`, admin activation, cache clear, verification.
   - `30-settings`: tables per config card from `config.xml` (bilingual label/helpText).
   - `40-faq`: symptom/cause/solution table plus troubleshooting steps.
   - Custom sections: describe the feature from the user's perspective (how to use it), not the implementation.

5. **Keep both languages in sync**: every section file must exist as `.en.md` AND `.de.md`; content must be equivalent, not one a translation of the other by machine.

## Conventions

- File naming: `NN-name.{en,de}.md` with two-digit numbers in steps of 10 (leaves room to insert `35-`, `45-` later). `index.{en,de}.md` is the landing page.
- German: formal "Sie" form; use official German Shopware admin terms (see [phrases.md](references/phrases.md)).
- Settings tables: `| Setting | Default | Description |` with the raw config key as first column.
- Support link: https://support.topdata.com
- Do NOT fabricate release notes or version numbers; only include what is verifiable in the repo (README, CHANGELOG).

## Verification checklist

- [ ] Every section exists as `.en.md` and `.de.md` (no file without its counterpart)
- [ ] Numbered prefixes ascending, gaps of 10
- [ ] `index` TOC links point to files with the correct language suffix (`.de.md` from `index.de.md`, `.en.md` from `index.en.md`)
- [ ] All settings from `config.xml` covered in `30-settings`
- [ ] German files use formal "Sie", no untranslated UI labels
- [ ] Commands are correct for the plugin (package name from composer.json, technical name from the plugin class)

## References

- [structure.md](references/structure.md) — section templates and real-world examples
- [phrases.md](references/phrases.md) — standard commands and German admin terms
