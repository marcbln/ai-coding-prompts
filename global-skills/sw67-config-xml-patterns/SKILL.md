---
name: sw67-config-xml-patterns
description: >
  Reference for creating and updating Shopware 6.7 plugin config.xml files.
  Covers valid input-field types and the component-based entity selector pattern.
  Use when creating or updating a Shopware 6.7 plugin's config.xml.
---

# SW6.7 Config XML Patterns

The Shopware 6 `config.xsd` schema only allows these types on `<input-field>`: `text`, `textarea`, `text-editor`, `url`, `password`, `int`, `float`, `bool`, `checkbox`, `datetime`, `date`, `time`, `colorpicker`, `single-select`, `multi-select`, `price`.

Entity-based selectors (e.g., category or manufacturer pickers) are **not** in this set — they must use the `<component>` element instead.

## Usage / Correct Patterns

```xml
<!-- Single entity select (e.g., category picker) -->
<component name="sw-entity-single-select">
    <name>breadcrumbCategory</name>
    <entity>category</entity>
    <label>Breadcrumb Root Category</label>
    <helpText>Description here</helpText>
</component>

<!-- Multi entity select -->
<component name="sw-entity-multi-id-select">
    <name>excludedCategories</name>
    <entity>category</entity>
    <label>Excluded Categories</label>
</component>

<!-- Valid input-field types for reference -->
<input-field type="text">
    <name>apiKey</name>
    <label>API Key</label>
</input-field>

<input-field type="bool">
    <name>enabled</name>
    <label>Enabled</label>
</input-field>

<input-field type="single-select">
    <name>mode</name>
    <label>Mode</label>
    <options>
        <option>
            <id>option_a</id>
            <name>Option A</name>
            <name lang="de-DE">Option A Deutsch</name>
        </option>
        <option>
            <id>option_b</id>
            <name>Option B</name>
        </option>
    </options>
    <defaultValue>option_a</defaultValue>
</input-field>
```

## Anti-patterns (DO NOT USE)

```xml
<!-- ❌ single-entity-select is NOT a valid input-field type -->
<input-field type="single-entity-select">
    <name>breadcrumbCategory</name>
    <entity>category</entity>
</input-field>

<!-- ❌ multi-entity-select is NOT a valid input-field type -->
<input-field type="multi-entity-select">
    <name>excludedCategories</name>
    <entity>category</entity>
</input-field>

<!-- ❌ entity inside input-field is not processed -->
<input-field type="text">
    <name>categoryId</name>
    <entity>category</entity>
</input-field>

<!-- ❌ value/label inside option is silently dropped in SW 6.7 -->
<!-- ConfigReader::optionsToArray() calls getElementsByTagName('id'), -->
<!-- so <value> returns null and the option is skipped via continue. -->
<!-- The admin dropdown appears empty. -->
<input-field type="single-select">
    <name>emptyBrandHandling</name>
    <label>Empty Brand Handling</label>
    <options>
        <option>
            <value>show</value>
            <label>Show all</label>
        </option>
    </options>
</input-field>
```
