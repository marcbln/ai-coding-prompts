---
name: llm-inference-python
description: Use when writing, reviewing, or debugging Python code that calls an LLM (Pydantic AI v2, OpenAI SDK, Anthropic SDK, LiteLLM). Covers structured outputs, tool/agent loops, streaming, retries, token accounting, and the universal "print provider/model first" rule so prompts and outputs are reproducible.
---

# LLM Inference in Python

Universal rules first, then Pydantic AI v2 specifics.

## Universal rules (every SDK)

- **Print `provider/model` first** — before any LLM call, log the exact
  `provider/model` string (e.g. `openai/gpt-4o`, `anthropic/claude-sonnet-4-6`,
  `ollama/llama3.1:8b`). One line, at the top of the run. Without it you
  cannot reproduce a result or compare models. No exceptions.
- **Make temperature, max_tokens, and seed explicit** — never inherit defaults
  silently. If you don't care, set them on purpose (e.g. `temperature=0`).
- **Pin model + provider version in code** — read from env / config, never
  hard-code the call site. A single `settings.model` beats ten literals.
- **Log token usage on every call** — input/output/total. Costs and
  regressions live there.
- **Structured output beats parsing** — if downstream code needs fields, ask
  the model for JSON / a schema. Don't regex parse prose.
- **Stream for UX, batch for tests** — `stream=True` in user-facing paths;
  use the non-streaming variant in tests so failures surface as exceptions.
- **Retries with backoff + jitter**, only on transient errors
  (429, 5xx, connection). Never retry on 400 / validation errors — you'll
  burn budget on the same bad request.
- **Timeouts are not optional** — set per-call timeouts. A hung inference call
  is worse than a fast failure.
- **Never put secrets in prompts or logs** — redact API keys, system prompts
  may contain them. Use a redactor before logging full request bodies.
- **Test the prompt, not just the code** — golden-output tests with a small
  fixture model (or recorded cassette) catch prompt regressions a unit test
  can't see.

## Pydantic AI v2 specifics

Pydantic AI v2 reorganized the API around `Agent`, `RunContext`, and explicit
model strings. Old v1 imports (`pydantic_ai.Agent` from the root, `result.data`)
still work but are deprecated.

### Installation

```bash
uv add 'pydantic-ai>=2.0'
```

### Basic agent with structured output

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class SupportTicket(BaseModel):
    category: str
    priority: int
    summary: str

agent = Agent(
    "openai:gpt-4o",          # provider:model
    output_type=SupportTicket,
    system_prompt="Extract the ticket fields from the user message.",
    retries=2,                # built-in validation retries
)

result = await agent.run("My laptop won't boot since this morning, urgent!")
ticket: SupportTicket = result.output
```

### Print provider/model first

```python
import logging
log = logging.getLogger(__name__)

def run_agent(prompt: str) -> SupportTicket:
    log.info("model=%s", agent.model)   # 'openai:gpt-4o' — every run
    result = agent.run_sync(prompt)
    log.info("usage=%s", result.usage())
    return result.output
```

### Streaming

```python
async with agent.run_stream(prompt) as stream:
    async for chunk in stream.stream_text(delta=True):
        print(chunk, end="", flush=True)
    final = await stream.get_output()
```

### Tools

```python
from pydantic_ai import Agent, RunContext

@agent.tool
async def lookup_order(ctx: RunContext[DbConn], order_id: str) -> str:
    """Look up an order by id. Use this whenever the user mentions an order."""
    return await ctx.deps.orders.get(order_id)

result = await agent.run("Where is order #1234?", deps=db_conn)
```

- Tool docstrings are **the** description the model sees. Write them like a
  short README.
- Keep tools pure and idempotent when possible — the agent may call them
  multiple times.
- Inject state via `RunContext[YourDeps]`, not globals.

### Multi-model / dynamic model

```python
from pydantic_ai.models import Model
from pydantic_ai import Agent

def pick_model(task: str) -> Model:
    return "anthropic:claude-sonnet-4-6" if task == "summarize" else "openai:gpt-4o-mini"

agent = Agent(pick_model, output_type=SupportTicket)
```

Validate the model string once at startup; fail fast on typos.

### Testing

- Use `pydantic_ai.models.test.TestModel` to stub a deterministic model — no
  network, no cost, perfect for CI.
- Use `ModelSettings` to override temperature/seed per test.
- Assert on `result.output` (typed) and `result.all_messages()` (full trace).

```python
from pydantic_ai.models.test import TestModel

def test_extracts_ticket():
    with agent.override(model=TestModel(custom_output_args=SupportTicket(category="auth", priority=2, summary="…"))):
        result = agent.run_sync("can't log in")
        assert result.output.category == "auth"
```

### Common pitfalls

- `output_type=` must be a **type**, not an instance. `output_type=SupportTicket`, not `SupportTicket()`.
- `result.data` (v1) → `result.output` (v2). Type checker will catch it.
- `Agent(...)` is async-first. Use `run_sync` only outside event loops.
- Streaming with structured output: collect deltas, validate at the end —
  partial JSON is not guaranteed valid.

## Other SDKs (lite rules)

- **OpenAI SDK** — prefer `client.beta.chat.completions.parse(...)` with a
  Pydantic model over `json_mode=True` + manual parsing. It auto-retries on
  schema failure.
- **Anthropic SDK** — `client.messages.create(...)` + `tool_use` blocks for
  structured output; define the tool schema once, reuse it.
- **LiteLLM** — drop-in router; still print `model=` per call (LiteLLM's
  `completion(...)` accepts a `model=` arg you control).

## Environment

- Load keys via env, never via hard-coded literals:
  `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OLLAMA_HOST`, etc.
- For local models (ollama, vllm), set a sane `OPENAI_BASE_URL` and verify
  reachability before the first call.