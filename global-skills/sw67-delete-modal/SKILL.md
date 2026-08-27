---
name: sw67-delete-modal
description: >
  Shopware 6.7 delete-confirmation pattern using sw-confirm-modal.
  Use when building or fixing a delete button in admin listing or detail
  pages, when debugging "this.$refs.deleteModal.showDeleteModal is not a
  function", or when porting old sw-delete-modal usage to SW 6.7.
---

# SW67 Delete Modal

In Shopware 6.7 the `sw-delete-modal` component no longer exposes the
imperative `showDeleteModal(item)` method. Code that calls
`this.$refs.deleteModal.showDeleteModal(item)` crashes with
`TypeError: ...showDeleteModal is not a function`. The supported pattern
is the declarative `sw-confirm-modal`, controlled by a boolean flag and a
`itemToDelete` data property. This applies to both entity-listing context
menus and single/detail-view delete buttons.

## Correct Pattern

```javascript
data() {
    return {
        showDeleteModal: false,
        itemToDelete: null,
    };
},

methods: {
    onDelete(item) {
        this.itemToDelete = item;
        this.showDeleteModal = true;
    },
    onCloseDeleteModal() {
        this.showDeleteModal = false;
        this.itemToDelete = null;
    },
    onConfirmDelete() {
        if (!this.itemToDelete) return;
        this.repository.delete(this.itemToDelete.id, Shopware.Context.api)
            .then(() => {
                this.onCloseDeleteModal();
                this.getList();   // or reload detail page
            });
    },
},
```

Template (listing `#actions` slot or a detail-page button both use the same modal):

```twig
<sw-confirm-modal
    v-if="showDeleteModal"
    :title="$tc('MyPlugin.admin.delete')"
    :text="$tc('MyPlugin.admin.deleteConfirmText')"
    :confirm-button-variant="'danger'"
    @confirm="onConfirmDelete"
    @close="onCloseDeleteModal"
    @cancel="onCloseDeleteModal"
/>
```

For `{term}` interpolation in the confirm text, use `$t(key, { term: item.name })`
NOT `$tc(key, 0, {...})` (see sw67-admin-entity-listing snippet gotcha).

## Anti-patterns (DO NOT USE)

```twig
<!-- ❌ Removed in SW 6.7: sw-delete-modal has no showDeleteModal() method -->
<sw-delete-modal ref="deleteModal" ... />
```

```javascript
// ❌ Crashes: TypeError: this.$refs.deleteModal.showDeleteModal is not a function
onDelete(item) {
    this.$refs.deleteModal.showDeleteModal(item);
}
```

```javascript
// ❌ Don't delete directly in the click handler without confirmation
onDelete(item) {
    this.repository.delete(item.id, Shopware.Context.api);
}
```

## Notes
- `sw-confirm-modal` is the 6.7 replacement for the old `sw-delete-modal`
  imperative API. Control it declaratively with `v-if` + a boolean.
- The same pattern works in `sw-entity-listing` `#actions` slots AND in
  single/detail-view pages (just reload the detail route or navigate back
  to the list after delete).
- Related: `sw67-admin-entity-listing` for the full listing + `#actions`
  slot context.
