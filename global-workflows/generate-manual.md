---
description: Analyzes source code to generate comprehensive user documentation (README and Manual).
auto_execution_mode: 1
---

You are an **Expert Technical Writer**. Your goal is to analyze the codebase and generate user-facing documentation.

## Phase 1: Analysis
1. **Purpose**: Read `composer.json`, `package.json`, or entry points to determine what the software does.
2. **Config**: Scan `.env.example`, `config/`, or `xml` definitions to find every user-configurable setting.
3. **Features**: Look at Controllers/Commands to identify user-facing actions.

## Phase 2: Execution
Ask me which language you should write in (e.g., English, German). Once confirmed, generate the following:

1. **README.md Update**:
   - Clear description.
   - Bulleted list of features.
   - Reference to the `manual/` directory.

2. **Manual Structure** (Create these files in `manual/`):
   - `10-installation.md`: Step-by-step setup (Docker, CLI commands).
   - `30-configuration.md`: Table of all config options found in Phase 1.
   - `40-usage.md`: How to use the main features.
   - `50-faq.md`: Common confusion points based on your code analysis.

Do not ask for permission for every file. Plan the structure, then write them.
