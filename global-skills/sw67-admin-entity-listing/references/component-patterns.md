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
                label: this.$tc('my-module.columnName'),
                allowResize: true,
                primary: true,
                sortable: true,
            }, {
                property: 'createdAt',
                label: this.$tc('my-module.columnCreatedAt'),
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
        <h2>{{ $tc('my-module.title') }}</h2>
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

## Main Entry (`main.ts`)

```ts
import './module/topdata-es-my-entity';
```

Minimal. Just import the module directories.
