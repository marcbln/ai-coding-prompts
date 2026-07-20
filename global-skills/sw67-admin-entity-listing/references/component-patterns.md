# Admin Component Patterns

## Component JS (`index.ts`)

```ts
import template from './my-list.html.twig';

const { Component, Mixin } = Shopware;
const { Criteria } = Shopware.Data;

Component.register('topdata-es-my-list', {
    template,

    inject: ['repositoryFactory'],

    mixins: [
        Mixin.getByName('listing'),
    ],

    data() {
        return {
            items: null,
            isLoading: true,
            sortBy: 'createdAt',
            sortDirection: 'DESC',
            limit: 25,
        };
    },

    computed: {
        repository() {
            return this.repositoryFactory.create('topdata_es_my_entity');
        },

        columns() {
            return [{
                property: 'name',
                label: this.$tc('MyFancyPluginSW6.my-module.columnName'),
                allowResize: true,
                primary: true,
                sortable: true,
            }, {
                property: 'createdAt',
                label: this.$tc('MyFancyPluginSW6.my-module.columnCreatedAt'),
                allowResize: true,
                sortable: true,
            }];
        },
    },

    mounted() {
        this.getList();
    },

    methods: {
        getList() {
            this.isLoading = true;

            const criteria = new Criteria(this.page, this.limit);
            criteria.addSorting(Criteria.sort(this.sortBy, this.sortDirection));

            this.repository.search(criteria).then((result) => {
                this.total = result.total;
                this.items = result;
                this.isLoading = false;
            }).catch(() => {
                this.isLoading = false;
            });
        },

        onPageChange(params) {
            this.page = params.page;
            this.limit = params.limit;
            this.getList();
        },

        onSortColumn(column) {
            this.sortBy = column.dataIndex ?? column.property;
            this.sortDirection = column.sortDirection ?? 'ASC';
            this.getList();
        },
    },
});
```

### Critical differences from the mixin stub

| Aspect | Mixin stub (broken) | Working pattern |
|--------|-------------------|-----------------|
| `getList()` | No-op, never called | Calls `repository.search()`, sets `items`, sets `isLoading = false` |
| `items` | Not in `data()` | `items: null` in `data()` |
| `mounted()` | Missing | Calls `this.getList()` |
| `onPageChange()` | Relies on stub that calls `getList()` (no-op) | Implemented: updates page/limit, calls `getList()` |
| `onSortColumn()` | Same issue | Implemented: updates sortBy/sortDirection, calls `getList()` |

## Template (`my-list.html.twig`)

```twig
<sw-page class="topdata-es-my-list-page">
    <template #smart-bar-header>
        <h2>{{ $tc('MyFancyPluginSW6.my-module.title') }}</h2>
    </template>

    <template #content>
        <sw-entity-listing
            v-if="items"
            :dataSource="items"
            :columns="columns"
            :repository="repository"
            identifier="topdata-es-my-entity"
            :show-settings="true"
            :show-selection="false"
            :allow-view="false"
            :allow-edit="false"
            :allow-delete="true"
            :allow-inline-edit="false"
            :full-page="true"
            :sort-by="sortBy"
            :sort-direction="sortDirection"
            :is-loading="isLoading"
            @page-change="onPageChange"
            @column-sort="onSortColumn"
        >
            <template #column-createdAt="{ item }">
                <sw-time-ago :date="item.createdAt" />
            </template>
        </sw-entity-listing>
    </template>
</sw-page>
```

### Key template requirements

- `v-if="items"` — prevents rendering before data loads
- `:dataSource="items"` — feeds data to the listing (NOT `:items="items"` in SW 6.7, though both may work)
- `:sort-by="sortBy"` / `:sort-direction="sortDirection"` — enables column sorting
- `:is-loading="isLoading"` — shows/hides the skeleton overlay
- `@page-change="onPageChange"` — wires pagination
- `@column-sort="onSortColumn"` — wires column sorting
- **Do not omit `:dataSource`** — relying on internal repository mode means `isLoading` stays `true` if `getList()` is not implemented

## Module Registration (`module/topdata-es-my-entity/index.ts`)

```ts
Shopware.Module.register('topdata-es-my-entity', {
    type: 'plugin',
    name: 'my-module',
    title: 'topdata-es-my-entity.title',
    description: 'topdata-es-my-entity.description',
    color: '#189eff',

    routes: {
        list: {
            component: 'topdata-es-my-list',
            path: 'list',
        },
    },

    navigation: [{
        id: 'topdata-es-my-entity-list',
        label: 'topdata-es-my-entity.title',
        color: '#189eff',
        path: 'topdata.es.my.entity.list',
        parent: 'sw-content',
        position: 100,
    }],
});
```

## Context Menu Actions — Modal-Based Edit & Delete

In SW 6.7's `sw-entity-listing`, the context menu for each row is controlled by the `#actions` slot.

### Key Rules

1. **The `#actions` slot REPLACES all default context menu items** — you must provide both Edit and Delete manually.
2. **Do NOT use `:detail-route` for modal editing** — `detailRoute` triggers `$router.push()` which navigates away from the page. The `@edit` event fires but is irrelevant because the component unmounts.
3. **Set `:allow-edit="false"` when using `#actions` slot** — you're providing the Edit button yourself.
4. **Always fetch entity via `repository.get(id)` before editing** — entity objects from `sw-entity-listing` row slots are not guaranteed to be writable proxies.

### Template Pattern

```twig
<sw-entity-listing
    v-if="items"
    :dataSource="items"
    :columns="columns"
    :repository="repository"
    identifier="topdata-es-my-entity"
    :show-settings="true"
    :show-selection="false"
    :allow-view="false"
    :allow-edit="false"
    :allow-delete="false"
    :allow-inline-edit="false"
    :full-page="true"
    :sort-by="sortBy"
    :sort-direction="sortDirection"
    :is-loading="isLoading"
    @page-change="onPageChange"
    @column-sort="onSortColumn"
>
    <template #actions="{ item }">
        <sw-context-menu-item @click="onEdit(item)">
            {{ $tc('global.default.edit') }}
        </sw-context-menu-item>
        <sw-context-menu-item variant="danger" @click="onShowDeleteModal(item)">
            {{ $tc('global.default.delete') }}
        </sw-context-menu-item>
    </template>

    <template #column-createdAt="{ item }">
        <sw-time-ago :date="item.createdAt" />
    </template>
</sw-entity-listing>

<sw-confirm-modal
    v-if="showDeleteModal"
    :title="$tc('global.default.delete')"
    :text="deleteConfirmText"
    :confirmButtonVariant="'danger'"
    @confirm="onConfirmDelete"
    @close="onCloseDeleteModal"
    @cancel="onCloseDeleteModal"
/>
```

### Component JS Pattern

```ts
import template from './my-list.html.twig';

const { Component, Mixin } = Shopware;
const { Criteria } = Shopware.Data;

Component.register('topdata-es-my-list', {
    template,

    inject: ['repositoryFactory'],

    mixins: [
        Mixin.getByName('listing'),
        Mixin.getByName('notification'),
    ],

    data() {
        return {
            items: null,
            isLoading: true,
            sortBy: 'name',
            sortDirection: 'ASC',
            limit: 25,
            activeModal: false,
            currentEntity: null,
            showDeleteModal: false,
            itemToDelete: null,
        };
    },

    computed: {
        deleteConfirmText() {
            if (!this.itemToDelete) return '';
            // Use $t(), NOT $tc() for named parameter interpolation
            return this.$t('MyFancyPluginSW6.my-module.deleteConfirmText', { term: this.itemToDelete.name });
        },

        repository() {
            return this.repositoryFactory.create('topdata_es_my_entity');
        },

        columns() {
            return [ /* ... */ ];
        },
    },

    mounted() {
        this.getList();
    },

    methods: {
        getList() { /* ... */ },
        onPageChange(params) { /* ... */ },
        onSortColumn(column) { /* ... */ },

        onAdd() {
            this.currentEntity = this.repository.create();
            // Set defaults
            this.activeModal = true;
        },

        onEdit(item) {
            this.repository.get(item.id).then((entity) => {
                this.currentEntity = entity;
                this.activeModal = true;
            });
        },

        onCloseModal() {
            this.activeModal = false;
            this.currentEntity = null;
            this.getList();
        },

        onShowDeleteModal(item) {
            this.itemToDelete = item;
            this.showDeleteModal = true;
        },

        onCloseDeleteModal() {
            this.showDeleteModal = false;
            this.itemToDelete = null;
        },

        onConfirmDelete() {
            this.repository.delete(this.itemToDelete.id).then(() => {
                this.createNotificationSuccess({
                    message: this.$tc('MyFancyPluginSW6.my-module.deleteSuccess'),
                });
                this.onCloseDeleteModal();
                this.getList();
            }).catch(() => {
                this.onCloseDeleteModal();
            });
        },
    },
});
```

### Fragment Snippets

```json
{
    "MyFancyPluginSW6": {
        "my-module": {
            "saveSuccess":       "Entity saved successfully.",
            "deleteSuccess":     "Entity deleted successfully.",
            "deleteConfirmText": "Are you sure you want to delete \"{term}\"?"
        }
    }
}
```

### Gotchas

- **`$t()` vs `$tc()` in SW 6.7:** Use `$t(key, { variable: value })` for message interpolation with named `{variable}` placeholders. `$tc()` is for pluralization only and its replacements parameter works differently.
- **`repository.get(id)` is required for editing:** The entity from `#actions` slot `{ item }` is not guaranteed to be a writable proxy. Always fetch a fresh one before binding to a form.
- **`#actions` replaces defaults:** If you add an `#actions` slot, all built-in context menu items (Edit, Delete) disappear. You must add them all back manually.

## Reusable Form Component

For modal-based create/edit forms, extract a reusable form component to avoid duplicating form fields across the list page.

### Directory Structure

```
module/topdata-es-my-entity/
├── component/
│   └── synonym-form/
│       ├── index.ts
│       └── synonym-form.html.twig
├── page/
│   └── synonym-list/
│       ├── index.ts
│       └── synonym-list.html.twig
└── index.ts
```

### Form Component JS (`component/my-form/index.ts`)

```ts
import template from './my-form.html.twig';

const { Component, Mixin } = Shopware;

Component.register('topdata-es-my-form', {
    template,

    mixins: [
        Mixin.getByName('notification'),
    ],

    props: {
        entity: {
            type: Object,
            required: true,
        },
        repository: {
            type: Object,
            required: true,
        },
    },

    data() {
        return {
            isLoading: false,
        };
    },

    computed: {
        isNew() {
            return this.entity.isNew();
        },
        modalTitle() {
            return this.isNew
                ? this.$tc('MyFancyPluginSW6.my-module.modalTitleAdd')
                : this.$tc('MyFancyPluginSW6.my-module.modalTitleEdit');
        },
    },

    methods: {
        onSave() {
            if (!this.entity.name.trim()) return;

            this.isLoading = true;
            this.repository.save(this.entity).then(() => {
                this.createNotificationSuccess({
                    message: this.$tc('MyFancyPluginSW6.my-module.saveSuccess'),
                });
                this.$emit('save', this.entity);
            }).catch(() => {
                this.isLoading = false;
            });
        },

        onCancel() {
            this.$emit('cancel');
        },
    },
});
```

### Form Component Template (`component/my-form/my-form.html.twig`)

```twig
<sw-modal
    :title="modalTitle"
    @modal-close="onCancel"
>
    <sw-text-field
        v-model="entity.name"
        required
        :label="$tc('MyFancyPluginSW6.my-module.labelName')"
    ></sw-text-field>

    <template #modal-footer>
        <sw-button size="small" @click="onCancel">
            {{ $tc('global.default.cancel') }}
        </sw-button>
        <sw-button variant="primary" size="small" @click="onSave" :isLoading="isLoading">
            {{ $tc('global.default.save') }}
        </sw-button>
    </template>
</sw-modal>
```

### Integration in List Page

**Page `index.ts`** — import the form component:
```ts
import template from './my-list.html.twig';
import '../../component/my-form';
```

**Page template** — replace inline modal with the form component:
```twig
<topdata-es-my-form
    v-if="activeModal"
    :entity="currentEntity"
    :repository="repository"
    @save="onCloseModal"
    @cancel="onCloseModal"
/>
```

### Props & Events API

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `entity` | Object | yes | The entity to create/edit |
| `repository` | Object | yes | Repository for save |

| Event | Payload | Description |
|-------|---------|-------------|
| `save` | entity | Fired after successful save |
| `cancel` | none | Fired when user cancels |

## Main Entry (`main.ts`)

```ts
import './module/topdata-es-my-entity';
```

Minimal. Just import the module directories.
