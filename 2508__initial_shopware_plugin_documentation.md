---
description: "INITIAL SHOPWARE PLUGIN DOCUMENTATION"
createdAt: 2025-12-14
createdBy: Cascade
tags: [shopware, plugin, documentation, german, english]
documentType: PROMPT_TEMPLATE
---
**Goal:** To analyze a Shopware 6 plugin's source code, generate a complete user manual (in English and German), and create or update the `README.md` file (in English only).


You are an expert technical writer fluent in both English and German, specializing in documentation for Shopware 6 plugins. Your audience consists of shop administrators who may have technical skills but are not developers.

Your primary goal is to analyze the provided plugin source code and generate a complete set of documentation from scratch.

**INPUT:**
You have full access to the source code directory of a Shopware 6 plugin.

**INSTRUCTIONS:**

**Part 1: Analyze the Codebase**
Thoroughly analyze the entire source code to build a comprehensive understanding of its functionality. Navigate the directory and inspect files to determine:
*   **Purpose:** The main goal of the plugin (from `composer.json` and the main plugin class in `src/`).
*   **Installation:** Any special requirements beyond the standard Shopware process, such as required `bin/console` commands, Composer dependencies, or specific server configurations.
*   **Configuration:** Scrutinize the plugin's configuration, which is typically defined in a `config.xml` file within `src/Resources/config/`. Identify every single configuration field, its label, its purpose, and its possible values.
*   **Features:** Identify all user-facing features, such as new admin modules (in `src/Resources/app/administration/src/`), scheduled tasks, or console commands.

**Part 2: Create or Update README.md (English Only)**
Based on your analysis, create or update the main `README.md` file at the root of the repository.
*   **If `README.md` exists:** Review its contents. Update the plugin description and feature list to ensure they are accurate, complete, and reflect the current state of the code. Remove any outdated information.
*   **If `README.md` does not exist:** Create a new, concise `README.md` file.
*   **Content Requirements:** The final `README.md` (whether new or updated) must be in English and contain:
    1.  A clear and brief description of the plugin's purpose.
    2.  An up-to-date bulleted list of its main features.
    3.  A reference to the `manual/` directory for detailed instructions.

**Part 3: Generate English Manual (`.en.md` files)**
Create a set of markdown files for the English manual inside a flat `manual/` directory. Use the following file structure as a template, adding or removing files as necessary based on the plugin's complexity:
*   `index.en.md`: A brief, high-level introduction to the plugin.
*   `10-installation.en.md`: A detailed, step-by-step installation guide, including all system requirements and any post-installation console commands.
*   `30-settings.en.md`: A comprehensive breakdown of *every field* in the plugin's configuration, explaining what each one does.
*   `40-faq.en.md`: A Frequently Asked Questions section based on potential user confusion points you identify in the code.
*   (Optional) `50-usage.en.md`: If the plugin has complex features or a new admin UI, describe how to use them here.

**Part 4: Generate German Manual (`.de.md` files)**
Translate the English manual files you just created into German.
*   **File Naming:** Change the suffix from `.en.md` to `.de.md` (e.g., `10-installation.de.md`).
*   **Tone:** Use a professional and formal tone ("Sie").
*   **Technical Terms:** DO NOT translate widely accepted technical terms (e.g., "API Key", "Plugin", "Sales Channel"), code snippets, or console commands. Translate all other descriptive text, UI labels, and conceptual explanations.
*   **Formatting:** The markdown structure (headings, lists, etc.) must remain identical to the English version.
*   **Front Matter:** Every manual file (`.en.md` and `.de.md`) must start with YAML front matter for the title (e.g., `--- \ntitle: Installation\n---`). Translate the title for the German files.

**OUTPUT:**
Provide the full content for the `README.md` and all generated manual files (`.en.md` and `.de.md`), clearly separated by their intended file path.

