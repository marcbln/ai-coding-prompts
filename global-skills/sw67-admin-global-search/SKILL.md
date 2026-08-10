---
name: sw67-admin-global-search
description: |
  Patterns for integrating the Shopware 6.7 admin global search bar (`sw-search-bar`) with custom plugin entities. Use when adding search to an admin listing page, debugging why a custom entity never appears in the admin search bar, or setting up backend term search on custom entities.

  Use this when:
  - Adding search functionality to an admin `sw-entity-listing` page
  - Debugging why a custom entity is not found / not searchable in the admin search bar
  - Setting up backend term search on a custom entity: `SearchRanking` flags, `tokenize` semantics, whether an `EntitySearchDefinition` is needed
  - Wiring `initial-search-type` or the `#`-type switch in the search bar
---

# SW67 Admin Global Search

Patterns for making custom plugin entities searchable through the standard Shopware 6.7 admin search bar, verified against `vendor/shopware/administration` (`sw-search-bar`, `listing.mixin.ts`, `search-type.service.js`) and `vendor/shopware/core` (`EntityScoreQueryBuilder`).

## Context

The admin search bar (`sw-search-bar`) only knows built-in types (customer, order, product, ...) held in the `searchTypeService` — a plain JS store at `src/app/service/search-type.service.js`. Custom plugin entities are invisible to the bar unless explicitly registered via `upsertType`. A module's `default-search-configuration.js` alone does **not** make the entity discoverable in the bar.

Backend: since 6.7, term search no longer requires the old `EntitySearchDefinition`. `EntityScoreQueryBuilder::buildScoreQueries()` builds score queries from `SearchRanking` flags, falling back to all `StringField`s of the entity when no flags exist.

## Correct Patterns

### 1. Page template — `#search-bar` slot

The `listing` mixin already provides `term` (data), `onSearch()` (debounced 750 ms, syncs `?term=` into the URL, resets page) and `getList()`. The slot replaces the default global bar on this page:

```twig
<sw-page class="my-contact-list">
    <template #search-bar>
        <sw-search-bar
            initial-search-type="tdcl_customer_contact"
            :initial-search="term"
            @search="onSearch"
        />
    </template>

    <template #smart-bar-header>
        <h2>{{ $tc('MyPluginSW6.contactList.list.title') }}</h2>
    </template>
</sw-page>
```

With `initial-search-type` set, typing in the bar emits `@search` (list-search mode) instead of running a cross-entity global search.

### 2. Search type registration — REQUIRED

Without this the bar does not know the entity type exists (unknown `initial-search-type` degrades to global search mode). New file `src/Resources/app/administration/src/app/service/my-plugin-search-type.js`, imported from admin `main.js`:

```js
Shopware.Application.addServiceProviderDecorator('searchTypeService', (searchTypeService) => {
    searchTypeService.upsertType('tdcl_customer_contact', {
        entityName: 'tdcl_customer_contact',
        placeholderSnippet: 'MyPluginSW6.contactList.list.placeholderSearchBar',
        listingRoute: 'topdata.contact.login.list', // module routePrefixName + route name
        hideOnGlobalSearchBar: true,                // keep out of the type picker on other pages
    });

    return searchTypeService;
});
```

Semantics:
- `hideOnGlobalSearchBar: true` — type usable via `initial-search-type` and the `#`-type switch on the page, but does not appear in other pages' global search type picker/results.
- `hideOnGlobalSearchBar: false` — adds an "all contacts"-style section to global search results on every admin page.
- `listingRoute` = the module's route name (`routePrefixName` from `Module.register` + the route's key, e.g. `topdata.contact.login` + `list`).

### 3. Snippet for the placeholder

```json
"MyPluginSW6": {
    "contactList": {
        "list": {
            "placeholderSearchBar": "Search all contacts..."
        }
    }
}
```

Ship it in every admin locale (de-DE / en-GB / fr-FR).

### 4. Backend — `SearchRanking` flags on the entity definition

Code-only change, no migration needed. Verified behavior of `EntityScoreQueryBuilder`:
- **No flags** → fallback to all `StringField`s of the entity (contact `email`/`firstName`/`lastName` match) — associations are **not** traversed.
- **Flagged `ManyToOneAssociationField`** → recursion into the referenced definition. `CustomerDefinition` already carries `SearchRanking` on `customerNumber`/`firstName`/`lastName`/`email`/`company` in core → linked-customer search comes free.
- `SearchRanking(score, tokenize)`: `tokenize: false` matches only the whole token (use for email and associations), omitted/true allows token parts.

```php
(new StringField('email', 'email'))->addFlags(new Required(), new SearchRanking(500, false)),
(new StringField('first_name', 'firstName'))->addFlags(new Required(), new SearchRanking(400)),
(new StringField('last_name', 'lastName'))->addFlags(new Required(), new SearchRanking(400)),
(new ManyToOneAssociationField('customer', 'customer_id', CustomerDefinition::class, 'id', false))
    ->addFlags(new SearchRanking(200, false)),
```

Keep the scores consistent with the admin-side `default-search-configuration.js` scores so ranking behaves identically in list search and typeahead.

### 5. Build & test

```bash
bin/console cache:clear            # after PHP definition changes
bin/build-administration.sh        # from the Shopware root, after JS/twig changes
```

Manual checks: type in the bar → list filters after the debounce, URL gains `?term=...`; clear term → full list; reload keeps the term; `#Kontakte`/`#Contacts` selects the type.

## Anti-patterns (DO NOT USE)

```javascript
// ❌ default-search-configuration.js alone — does NOT make the entity discoverable in the bar
Module.register('my-module', { defaultSearchConfiguration });
// upsertType() registration is mandatory for the bar to know the type.

// ❌ custom search field in the smart bar — non-standard, duplicates the global bar
<sw-field type="search" v-model="term" @input="getList" />
// No core module does this; the standard is the #search-bar slot.

// ❌ sw-search-bar without initial-search-type — falls back to doGlobalSearch() mode
<sw-search-bar :initial-search="term" @search="onSearch" />
// The @search event (list mode) only fires when a currentSearchType is active.

// ❌ getList() without criteria.setTerm(this.term) — term never reaches the backend
getList() {
    const criteria = new Criteria(this.page, this.limit);
    criteria.addSorting(Criteria.sort(this.sortBy, this.sortDirection));
    // criteria.setTerm(this.term) missing
}
```

## Related

- `sw67-admin-entity-listing` — parent topic: creating the listing page itself (mixins, `updated_at`, builds)
- `sw67-entity-definition` — entity definition patterns the `SearchRanking` flags build upon
- Reference implementation in the wild: `ScopPlatformRedirecter` plugin registers its custom entity via the same `addServiceProviderDecorator('searchTypeService', ...)` pattern