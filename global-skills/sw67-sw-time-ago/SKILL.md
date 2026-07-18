---
name: sw67-sw-time-ago
description: |
  Patterns for using the `sw-time-ago` component in Shopware 6.7 administration.
  SW 6.7 uses Vue 3, which removed the `| date()` filter. Use the dedicated `sw-time-ago` component instead.

  Use this when:
  - Creating or editing Vue 3 admin components or templates
  - Displaying absolute, relative, or human-friendly date/time values in SW 6.7
  - Replacing deprecated `| date(...)` Twig/Vue filter usages
  - Porting admin components from older Shopware versions to 6.7
---

# SW67 `sw-time-ago` Component

In Shopware 6.7 (Vue 3), the `| date()` filter is **removed**. Always use the `<sw-time-ago>` component for rendering dates in the administration.

## Basic Usage

```vue
<sw-time-ago :date="item.createdAt" />
```

Renders a relative time string (e.g. "2 hours ago") with a full-date tooltip on hover.

## With `v-if` for nullable dates

Always add `v-if` when the date can be `null`, otherwise the component renders nothing:

```vue
<sw-time-ago v-if="item.lastSearchedAt" :date="item.lastSearchedAt" />
```

## Custom Format via `date-time-format`

Override the tooltip format with an `Intl.DateTimeFormat` options object:

```vue
<sw-time-ago
  :date="item.createdAt"
  :date-time-format="{ month: '2-digit', day: '2-digit' }"
/>
```

## In Entity Listing Columns

```vue
<template #column-createdAt="{ item }">
    <sw-time-ago v-if="item.createdAt" :date="item.createdAt" />
</template>
```

## Anti-pattern (DO NOT USE)

```vue
<!-- BROKEN in SW 6.7 / Vue 3: -->
{{ item.createdAt | date(true) }}
```

## Related

- `sw67-admin-entity-listing` — full pattern for entity listing pages
- `AGENTS.md` in `topdata-elasticsearch-hacks-sw6` — real project convention
