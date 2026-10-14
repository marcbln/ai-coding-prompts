# Inventory & matching rules

## What `scripts/inventory.sh` extracts, and why

| Inventory kind | Why it matters when checking a release |
|---|---|
| Shopware FQCNs | Extended/implemented/instantiated core classes; namespace moves and renames break these |
| Decorated services | Decorators are the most BC-sensitive integration; changelog names the decorated service or class |
| Referenced services (XML) | Removed/renamed service IDs, changed constructor wiring |
| Event subscribers / XML listeners | Event payload, timing, or removal changes affect these |
| Route paths | Routing changes, route name changes, scope changes |
| Twig extends/include targets | The core template a plugin patches; changes there may require syncing overrides |
| Twig block names | Renamed/removed blocks silently break overrides |
| Shadowed template paths | Full-template copies go stale when core changes; they win over core unless a theme wins over them |
| JS registrations | Storefront plugin names and admin modules referenced by core code |

## Matching rules

- **FQCN**: exact match first. On no exact match, try short class name and namespace suffix (`...\SalesChannel\RegisterRoute`), but verify in the source before acting — short names collide easily.
- **Namespace moves**: when UPGRADE says classes moved (e.g. `Checkout\Document` → `Checkout\DocumentV2`), match plugin FQCNs under the *old* prefix; those are the affected ones.
- **Service IDs**: `decorates=` hits are high-signal; usually the changelog/UPGRADE text names the service ID or its class. `.inner` in referenced services is a decorator chain reference, not a core service.
- **Events**: read `getSubscribedEvents` in the listed subscriber files for event names; XML listeners name events directly. Compare against event changes in changelog/UPGRADE.
- **Twig**: `@Storefront/...` targets map to core templates under `src/Storefront/Resources/views/...`; diff those core paths between anchor and target. Block names: renamed blocks in changed core templates are silent breakage. Shadowed template paths: diff the corresponding core template and consider syncing.
- **JS**: registration names (`PluginManager.register('...')`, `Module.register('...')`, `class X extends Plugin`) ↔ storefront/admin JS changes.

## False positives and false negatives

- Generic substrings (`Rule`, `Product`, `Entity`, `Route`) match everywhere — require symbol + area correlation, or a changed-file path correlation.
- Area-heading-only matches (`# Core` in a changelog file) prove nothing by themselves; read the entry.
- Deprecations are deferred breaks: flag them with their removal version (e.g. "deprecated, removed in 6.9") instead of treating them as current failures.
- No symbol match does **not** mean no impact: defaults, event timing, payload shapes and template behavior change without symbols. UPGRADE prose for features the plugin uses is the place to catch those.
- Inventory covers the main surfaces only. If the plugin does something exotic (custom caching, extension of third-party packages, DB schema assumptions), extend the check manually.
