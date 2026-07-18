---
name: self-contained-python-script
description: Write self-installing, self-contained Python scripts using uv and PEP 723. Use when creating a Python script that should manage its own dependencies without a separate virtualenv or requirements file.
---

Use this to write Python tools / scripts / clis as single files.

Using PEP 723 inline metadata, you can create self-contained Python scripts that declare their own dependencies. This allows you to run your scripts in isolated environments without needing to manually set up virtual environments or install dependencies.

To do that, embed the invocation of the uv command right in the shebang line.

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "httpx",
# ]
# ///
import httpx
.
.
.
```
