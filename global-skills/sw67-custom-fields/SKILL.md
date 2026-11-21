---
name: sw67-custom-fields
description: |
  Provision, repair and debug Shopware 6.7 custom fields (custom_field / custom_field_set): the two type planes, the immutable type column, safe type changes by delete+recreate, descriptor naming, and the admin/Store API flags that are constantly confused. Use when adding or installing custom fields, when the admin "Typ" select is empty or a field has no editor, when a field is not editable in the admin, when changing a custom field type, or when debugging checkbox vs switch, customFieldType, or custom field values that are missing from the admin.

  Use this when:
  - Creating, installing or updating a custom field (descriptor JSON, Admin API, installer command)
  - "Typ" select is empty, field renders nothing, or the admin shows no editor
  - A custom field is not editable in the Shopware admin
  - Changing an existing field type (bool/boolean/text, checkbox vs switch)
  - Custom field values exist but the admin shows nothing (definition missing or misnamed)
  - Confusing allowCustomerWrite / storeApiAware / allowCartExpose with admin editability
---

# Shopware 6.7 Custom Fields

Custom fields look simple (a name, a type, a label) and fail in silent ways. Almost every bug
comes from conflating two independent type planes, or from treating the field **definition** as
the place where values live. Both mistakes are cheap to avoid once you know the model.

Verified against `shopware/core` **6.7.10.2**; source anchors at the bottom so you can re-check
after an upgrade.

## 1. The two type planes

| Plane | Column / key | Example | Mutable? |
| --- | --- | --- | --- |
| Data type | `custom_field.type` | `bool` | **No — immutable** |
| Admin component | `config.customFieldType` + `config.type` | `switch` | Yes, plain config patch |

`custom_field.type` is defined as `(new StringField('type', 'type'))->addFlags(new Required(), new Immutable())`.
A `PATCH` with a different value fails:

```
400 FRAMEWORK__WRITE_CONSTRAINT_VIOLATION
The field "type" of "custom_field" is immutable and cannot be updated.
```

Valid data types are the constants of `Shopware\Core\System\CustomField\CustomFieldTypes`:
`bool, checkbox, colorpicker, date, datetime, entity, float, html, int, json, media, number,
price, select, switch, text`. `boolean` is **not** one of them — it silently becomes an
unregistered type (the DAL falls back to a `JsonField` and the admin cannot render it).

### Admin registry (drives the "Typ" select and the editor)

`config.customFieldType` must be a key of the admin's `custom-field.service.js` registry:

| customFieldType | data type written | config written |
| --- | --- | --- |
| `text` | `text` | `componentName: sw-field`, `type: text` |
| `textEditor` | `html` | `componentName: sw-text-editor` |
| `checkbox` | `bool` | `componentName: sw-field`, `type: checkbox` |
| `switch` | `bool` | `componentName: sw-field`, `type: switch` |
| `number` | `int` (or `float` via `numberType`) | `componentName: sw-field`, `type: number` |
| `date` | `datetime` | `componentName: sw-field`, `type: date`, `dateType` |
| `select` | `select` | (options live in `config.options`) |
| `entity` | `select` | `entity` config |
| `media` | `text` | `componentName: sw-media-field` |
| `colorpicker` | `text` | `componentName: sw-field`, `type: colorpicker` |
| `price` | `price` | — |

Two consequences:

* `customFieldType: "bool"` is invalid. The type select stays **empty**, no editor is rendered,
  and the field cannot be edited in the admin.
* `checkbox` vs `switch` is a pure component choice — same `bool` data type, same stored value.

## 2. Values do not live in the definition

Custom field values are JSON in the entity column `<entity>.custom_fields`
(`customer.custom_fields`, `customer_address.custom_fields`, `product.custom_fields`, …).

* Deleting a `custom_field` row does **not** delete values.
* Recreating the same name makes the existing values readable again.
* The only FK to `custom_field` is `product_search_config_field.custom_field_id` (products only,
  cascade delete). Customer/address fields are not referenced by id anywhere.
* Values written without a matching definition are orphaned: they exist in the JSON but the admin
  shows nothing. This is the classic symptom of a misnamed definition.

## 3. Provisioning: descriptor pattern

Field `name` in a descriptor is the **short** name; the installer prefixes the set name.
`topdata_migration_address` + `address_source` becomes `topdata_migration_address_address_source`.
Putting the full name in the descriptor double-prefixes it and orphans every value the mapper
writes.

```json
{
    "customFieldSet": {
        "name": "topdata_tg",
        "config": { "label": { "en-GB": "Topdata TradeGuard" } },
        "relations": [{ "entityName": "customer" }]
    },
    "customFields": [
        {
            "name": "lsva",
            "type": "bool",
            "config": {
                "label": { "en-GB": "LSVA Surcharge (ERP)" },
                "componentName": "sw-field",
                "customFieldType": "switch",
                "type": "switch",
                "customFieldPosition": 10
            }
        }
    ]
}
```

Installer rules:

1. Find the field by its **filtered** name (`filter[name]=<full name>`), not by paging an
   unfiltered `limit: 500` list — a shop with many fields pushes the target past the first page.
2. Existing field, same data type → `PATCH` the config (label, `customFieldType`, position).
   Same `type` in the payload is fine; only a *changed* value is rejected.
3. Existing field, different data type → delete + recreate (next section).
4. Idempotency: a second run must be a no-op and must keep the field id.
5. If a set is shared with durable business data, gate on the existing field shape and refuse to
   repurpose/delete it when the type differs — fail closed before any write.

```php
$existing = $client->search([
    'limit'  => 1,
    'filter' => [Util_Shopware6FilterBuilder::filterEquals('name', $fullName)],
])['data'][0] ?? null;

if ($existing !== null && ($existing['attributes']['type'] ?? null) !== $dataType) {
    $client->deleteOne($existing['id']); // type is immutable: recreate
    $existing = null;
}

$payload = [
    'customFieldSetId' => $setId,
    'name'             => $fullName,
    'type'             => $dataType,
    'config'           => $config,
];

$existing === null
    ? $client->post('custom-field', $payload)
    : $client->patch("custom-field/{$existing['id']}", $payload);
```

## 4. Changing an existing field type

There is no supported in-place type change. The admin also disables the type select for existing
fields (`sw-custom-field-detail`: `:disabled="!currentCustomField._isNew || !acl.can('custom_field.editor')"`),
so an operator cannot fix a wrong type in the UI either.

Procedure:

1. Snapshot the stored values (row count, value split, checksum).
2. Delete the `custom_field` row.
3. Recreate it with the same full name and the corrected type + admin type.
4. Verify the values are still readable and count/checksum are unchanged.
5. Hard-reload the admin (it caches the field config).

Before deleting, confirm the field is not used by:

* `product_search_config_field` (product fields only — cascade delete),
* Shopware rules / flow-builder conditions (`CustomFieldRule` only recognizes registered types),
* sorting/filtering saved in other integrations.

Customer/address custom fields are safe: their values live in the entity JSON and no FK points at
the definition.

## 5. Symptom to cause

| Symptom | Cause | Fix |
| --- | --- | --- |
| "Typ" select empty, no editor | `config.customFieldType` is not a registry key (e.g. `bool`, `boolean`) | set it to `switch`/`checkbox`/… in the definition |
| "Typ" select greyed out | Shopware disables it for every existing field | change the type via descriptor + installer/API, not the UI |
| Value greyed out on customer/address | entity not in edit mode (`:disabled="!customerEditMode"`) | click "Bearbeiten" first |
| Checkbox where a toggle is expected | `customFieldType: checkbox` vs `switch` | config-only change, same data type |
| Field invisible in the admin | set has no relation for the entity, set inactive, or field not in a set | check `custom_field_set_relation` |
| Values exist but nothing shows | definition missing or misnamed (e.g. double prefix) | install a definition with the exact stored key |
| Store API cannot read/write | `storeApiAware` / `allowCustomerWrite` | separate concern; never needed for admin editing |
| Admin save does nothing | entity ACL (`customer.editor` / `product.editor`) or read-only mode | check the role |

`allowCustomerWrite` ("Modifizierbar über Store API") lets *customers* write the field through
the Store API. It has nothing to do with editing in the admin and should stay off for
business-critical flags (billing, tax, eligibility).

## 6. Verification recipes

```bash
TOKEN=...   # Admin API token

# Field shape. NOTE: meta.total is the page size unless total-count-mode is set.
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://shop/api/custom-field?filter[name]=set_field&total-count-mode=1" \
  | jq '{total:.meta.total, fields:[.data[].attributes | {name,type,customFieldType:.config.customFieldType}]}'

# Count entities by custom field value. Use POST /api/search (GET custom-field filters are wrong:
# filter[customFields.key]=true compares strings and can return the opposite count).
curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -X POST \
  -d '{"filter":[{"type":"equals","field":"customFields.set_field","value":true}],"limit":1,"total-count-mode":1}' \
  "https://shop/api/search/customer" | jq '.meta.total'
```

```sql
-- Stored value distribution and the checksum used for before/after comparison
SELECT JSON_UNQUOTE(JSON_EXTRACT(custom_fields, '$.set_field')) AS v,
       JSON_TYPE(JSON_EXTRACT(custom_fields, '$.set_field'))       AS t,
       COUNT(*)                                                    AS c
FROM customer
WHERE JSON_EXTRACT(custom_fields, '$.set_field') IS NOT NULL
GROUP BY v, t;

SELECT COUNT(*) AS rows_with_key,
       BIT_XOR(CRC32(JSON_UNQUOTE(JSON_EXTRACT(custom_fields, '$.set_field')))) AS checksum
FROM customer
WHERE JSON_EXTRACT(custom_fields, '$.set_field') IS NOT NULL;
```

Values must be real JSON booleans, not `1`/`0`/`-1`/`"yes"`. A strict
`$stored === $desired` comparison in an upsert is what silently rewrites stale ints.

## Anti-patterns (do not do)

* `"customFieldType": "bool"` or any other data type copied into the admin type key — empty "Typ"
  select, no editor, field not editable.
* `"type": "boolean"` — not a registered data type; only `bool` is.
* Full technical names in a descriptor that the installer prefixes.
* `PATCH`ing `type` and expecting a change (400 immutable).
* Deleting a definition without checking stored values and FK users.
* Using `allowCustomerWrite` to make a field editable in the admin.
* Unfiltered `limit: 500` lookups in an installer.
* Reading `meta.total` from a `limit=1` GET as the real total.
* Trusting `filter[customFields.key]` on a GET list endpoint.
* Writing values without provisioning the definition (orphaned JSON).

## Source anchors (6.7.10.2)

| What | Path (relative to `vendor/shopware/`) |
| --- | --- |
| `type` immutable | `core/System/CustomField/CustomFieldDefinition.php` |
| valid data types | `core/System/CustomField/CustomFieldTypes.php` |
| immutable enforcement | `core/Framework/DataAbstractionLayer/Dbal/EntityWriteGateway.php` (`validateCommands`) |
| unknown type fallback | `core/System/CustomField/CustomFieldService.php` |
| Store API mapping (`allow_customer_write`) | `core/System/SalesChannel/StoreApiCustomFieldMapper.php` |
| admin type registry | `administration/Resources/app/administration/src/app/service/custom-field.service.js` |
| type select disabled for existing fields | `administration/.../module/sw-settings-custom-field/component/sw-custom-field-detail/sw-custom-field-detail.html.twig` |
| values disabled outside edit mode | `administration/.../module/sw-customer/view/sw-customer-detail-base/sw-customer-detail-base.html.twig` |
