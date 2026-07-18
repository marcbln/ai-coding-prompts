---
name: create-ai-context-definition
description: Create a new YAML context definition file in _ai/context-definitions/. Use when documenting a core concept, integration, or shared feature that needs a structured definition for AI context.
---

# Create AI Context Definition

Create a new YAML file in `_ai/context-definitions/` that defines a core concept, integration, or shared feature for AI context.

## Process

1. Check existing context definitions for format reference:
   ```bash
   ls _ai/context-definitions/
   ```

2. Create a new YAML file with the following structure:
   ```yaml
   name: <kebab-case-name>
   description: <brief description of the concept>
   tags: [<tag1>, <tag2>]
   related: [<related-file-names>]
   ```

3. Ensure the file follows the same conventions as existing definitions (naming, required fields, tag format).

4. If `_ai/context-definitions/` doesn't exist, create it.
