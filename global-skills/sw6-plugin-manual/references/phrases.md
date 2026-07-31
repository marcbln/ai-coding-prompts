# Standard Commands & German Admin Terms

Phrases and commands that appear in every Topdata SW6 plugin manual.

## Standard commands

| Context | Command |
|---------|---------|
| Install | `composer require topdata/<package-name>` |
| Activate (CLI) | `bin/console plugin:install --activate <TechnicalName>` |
| Clear cache | `bin/console cache:clear` |

- `<package-name>`: `name` field in composer.json, e.g. `topdata/topdata-category-filter-sw6`.
- `<TechnicalName>`: plugin class name in `src/`, e.g. `TopdataCategoryFilterSW6`, `TopdataTopFinderProSW6`.

## Shopware admin navigation (EN / DE)

| English | German |
|---------|--------|
| Extensions | Erweiterungen |
| My extensions | Meine Erweiterungen |
| Activate | Aktivieren |
| Deactivate | Deaktivieren |
| Install | Installieren |
| Uninstall | Deinstallieren |
| Settings | Einstellungen |
| Configuration | Konfiguration |
| Save | Speichern |
| Clear cache | Cache leeren |
| Admin panel | Admin-Panel |
| Storefront | Storefront (unchanged) |
| Product listing | Produktliste / Produktübersicht |
| Checkout | Kaufabschluss / Checkout |

## German writing style

- Always formal "Sie" (never "du").
- Plugin names: keep the English marketing name even in German files (e.g. "Topdata Category Filter SW6"), only UI labels and sentences are translated.
- Console commands and settings keys stay untranslated in code blocks.
- Use the de-DE labels from `config.xml` (`<label lang="de-DE">`, `<helpText lang="de-DE">`) as the authoritative German terms for settings.
- German file titles:
  - `index` → "Benutzerhandbuch"
  - `10-installation` → "Installationshandbuch"
  - `30-settings` → "Einstellungsleitfaden"
  - `40-faq` → "FAQ & Fehlerbehebung"
  - `50-usage` → "Bedienungsanleitung" (or per content)
  - `40-features` → "Funktionen"
  - `50-demo-setup` → "Demo-Setup"

## Standard index sections (EN / DE headings)

| English | German |
|---------|--------|
| Table of Contents | Inhaltsverzeichnis |
| Overview | Überblick |
| Key Features | Hauptmerkmale |
| Getting Started | Einstieg |
| Support | Support |
| Release Notes | Versionshinweise |
| Installation Guide | Installationshandbuch |
| Settings Guide | Einstellungsleitfaden |
| FAQ & Troubleshooting | FAQ & Fehlerbehebung |
| Usage Guide | Bedienungsanleitung |

## Support sentence

- EN: "For additional support, please contact our technical support team or visit our [support portal](https://support.topdata.com)."
- DE: "Für zusätzlichen Support wenden Sie sich bitte an unser technisches Support-Team oder besuchen Sie unseren [Support-Portal](https://support.topdata.com)."

## Technical name derivation

Plugin class name = composer.json `autoload.psr-4` namespace suffix or the class in `src/<PluginName>.php` (e.g. `TopdataCategoryFilterSW6`). Use it exactly in `plugin:install --activate` commands.
