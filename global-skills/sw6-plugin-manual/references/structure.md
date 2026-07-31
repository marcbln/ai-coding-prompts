# Manual Structure & Section Templates

Reference for section templates, based on existing Topdata SW6 plugin manuals (e.g. `topdata-category-filter-sw6`, `topdata-demo-data-importer-sw6`, `topdata-webservice-connector-sw6`).

## Section numbering

- Two-digit prefix, steps of 10: `10-`, `20-`, `30-`, `40-`, `50-`.
- Insert additional sections at the next free number or between (e.g. `35-` between `30-` and `40-`).
- Every file must exist as `.en.md` and `.de.md` pair.

## Sections observed in real plugins

| Prefix | Name | Used by |
|--------|------|---------|
| 10 | installation | most plugins |
| 20 | installation / usage | control-center / compare-products |
| 30 | settings | most plugins |
| 35 | config-translation | machine-translations |
| 36 | snippet-translation | machine-translations |
| 40 | faq / features / plugin-registration | various |
| 50 | usage / demo-setup / faq / troubleshooting | various |

## index.{en,de}.md

Landing page with TOC, overview, features, getting started, support.

```markdown
# Topdata <Name> SW6 User Manual  (EN) / Benutzerhandbuch (DE)

## Table of Contents / Inhaltsverzeichnis

1. [Installation Guide](10-installation.en.md)  (EN) / [Installationshandbuch](10-installation.de.md) (DE)
2. [Settings Guide](30-settings.en.md) / [Einstellungsleitfaden](30-settings.de.md)
3. [FAQ & Troubleshooting](40-faq.en.md) / [FAQ & Fehlerbehebung](40-faq.de.md)

## Overview / Überblick

1-3 sentences describing what the plugin does for the user.

### Key Features / Hauptmerkmale

- feature bullets

## Getting Started / Einstieg

1. Follow the [Installation Guide](...) ...
2. Configure ... [Settings Guide](...) ...
3. Refer to ... [FAQ](...) ...

## Support

For support contact ... [support portal](https://support.topdata.com).
(DE: Für zusätzlichen Support wenden Sie sich bitte an unser technisches Support-Team oder besuchen Sie unseren [Support-Portal](https://support.topdata.com).)

## Release Notes (only if verifiable, otherwise omit)
```

Note: keep only the language-matching links (`.en.md` links in the EN file, `.de.md` links in the DE file).

## 10-installation.{en,de}.md

```markdown
# Topdata <Name> SW6 Installation Guide / Installationshandbuch

## System Requirements / Systemanforderungen

- Shopware 6.4.x or higher / Shopware 6.5.x oder höher
- PHP 8.0 or higher / PHP 8.0 oder höher

## Installation Steps / Installationsschritte

### 1. Install via Composer / Installation über Composer

```bash
composer require topdata/<package-name>
```

### 2. Activate the Plugin / Aktivieren des Plugins

#### Option A: Using the Shopware Admin Panel / Über das Shopware-Admin-Panel

1. Log in to your Shopware admin panel
2. Go to **Extensions** > **My extensions**  (DE: **Erweiterungen** > **Meine Erweiterungen**)
3. Find "<Plugin Name>" in the list
4. Click **Activate** (DE: **Aktivieren**)

#### Option B: Using the Command Line / Über die Befehlszeile

```bash
bin/console plugin:install --activate <TechnicalName>
```

### 3. Clear Cache / Cache leeren

```bash
bin/console cache:clear
```

## Verification / Überprüfung

- How the user can confirm the plugin works (storefront/admin).

## Troubleshooting / Fehlerbehebung

- Common installation issues.
```

`<TechnicalName>` is the plugin class name (e.g. `TopdataCategoryFilterSW6`), `<package-name>` from composer.json (e.g. `topdata/topdata-category-filter-sw6`).

## 30-settings.{en,de}.md

One table per `<card>` in `config.xml`, listing every `<input-field>` (and `<component>`, e.g. `sw-entity-multi-id-select` — both use `name`, `label`, `helpText`, optional `defaultValue`):

```markdown
# Topdata <Name> SW6 Settings Guide / Einstellungsleitfaden

This guide provides detailed information about all the configuration options available in the plugin. (DE: Dieser Leitfaden beschreibt alle Konfigurationsoptionen des Plugins.)

## <Card Title>

| Setting | Default | Description |
|---------|---------|-------------|
| `showCategoryFilter` | true | Enables or disables the category filter. (from label/helpText) |
| `hideHiddenCategories` | false | Hides categories marked "Hide in navigation". |
```

- Setting = raw `<name>`, Default = `<defaultValue>` (omit if absent), Description = `<label>` + `<helpText>` (use the de-DE label for the German file).
- Group tables by the `card` title from `config.xml` (title + `title lang="de-DE"`).
- Optionally add a "Recommended Configurations" section with practical tips.

## 40-faq.{en,de}.md

```markdown
# Topdata <Name> SW6 FAQ & Troubleshooting / FAQ & Fehlerbehebung

## Common Issues / Häufige Probleme

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| <symptom> | <cause> | <fix, referencing settings keys> |

## Troubleshooting Guide / Fehlerbehebungsanleitung

### 1. <Issue>

1. step
2. step

### 2. <Next issue>
```

## 50-usage / 50-demo-setup / 40-features

Describe user-facing behavior with concrete steps and screenshots placeholders:

- `50-usage`: how the user works with the plugin day-to-day (storefront and admin).
- `50-demo-setup`: step-by-step setup of a demo/example configuration.
- `40-features`: feature overview with sub-sections per feature.
- `35-config-translation` / `36-snippet-translation`: specialized guides (machine-translations plugin).

Structure: numbered sub-steps, admin paths in bold, settings keys in backticks, code blocks for CLI.
