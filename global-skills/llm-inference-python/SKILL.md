---
name: llm-inference-python
description: Use when writing, reviewing, or debugging Python code that calls an LLM (Pydantic AI v2, OpenAI SDK, Anthropic SDK, LiteLLM). Covers structured outputs, tool/agent loops, all three streaming surfaces (run_stream, run_stream_events, iter), retries, token accounting, cancellation, and the universal "print provider/model first" rule so prompts and outputs are reproducible.
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

Pydantic AI v2 has **three** streaming surfaces and picking the wrong one
silently drops events. Pick by what the caller needs to see.

| You want… | Surface | Yields | Use when |
|---|---|---|---|
| Just the final text, fast | `agent.run_stream(prompt)` → `stream.stream_text(delta=True)` | text chunks | "typewriter" UX on `output_type=str`. **Stops at first matching output; drops later tool calls.** |
| Final text *plus* tool calls | `agent.run(prompt, event_stream_handler=...)` *or* `agent.run_stream_events(prompt)` | `PartStartEvent`, `PartDeltaEvent`, `FunctionToolCallEvent`, `FunctionToolResultEvent`, `FinalResultEvent`, ending with `AgentRunResultEvent` | Operator debugging, logging, "what is the model doing" UX, structured output with interleaved tools |
| Per-graph-node control | `agent.iter(prompt)` | `UserPromptNode`, `ModelRequestNode`, `CallToolsNode`, `End` | Injecting logic at specific stages, custom cancellation, advanced multi-agent flows |

#### Plain-text final output (`run_stream`)

```python
async with agent.run_stream(prompt) as stream:
    async for chunk in stream.stream_text(delta=True):
        print(chunk, end="", flush=True)
    final = await stream.get_output()
```

Best when `output_type=str` and you don't care about tools running in
parallel with the text. With structured output, it stops at the first
tool match and never executes the rest — fine if you don't have parallel
tools; risky if you do.

#### All events + final structured output (`run_stream_events`)

This is the surface you want for "operator sees model text and tool
calls in real time". With `output_type=<Model>` it ends with
`AgentRunResultEvent` carrying the typed `result.output` — no need to
reconstruct the JSON from deltas.

```python
from pydantic_ai import (
    AgentRunResultEvent,
    FinalResultEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    PartDeltaEvent,
    PartStartEvent,
    TextPartDelta,
    ToolCallPartDelta,
)

async with agent.run_stream_events(prompt) as events:
    async for event in events:
        if isinstance(event, PartStartEvent) and isinstance(event.part, TextPart):
            print(f"[text] {event.part.content}", flush=True)
        elif isinstance(event, PartStartEvent) and event.part.__class__.__name__ == "ToolCallPart":
            print(f"[tool-call] {event.part.tool_name}({event.part.args})", flush=True)
        elif isinstance(event, PartDeltaEvent) and isinstance(event.delta, TextPartDelta):
            print(event.delta.content_delta, end="", flush=True)
        elif isinstance(event, PartDeltaEvent) and isinstance(event.delta, ToolCallPartDelta):
            sys.stderr.write(event.delta.args_delta); sys.stderr.flush()
        elif isinstance(event, FunctionToolCallEvent):
            print(f"[tool] {event.part.tool_name}({event.part.args}) id={event.part.tool_call_id}")
        elif isinstance(event, FunctionToolResultEvent):
            preview = (event.part.content or "")[:200].replace("\n", " ")
            print(f"[tool-result] {event.tool_call_id} => {preview}")
        elif isinstance(event, FinalResultEvent):
            print("[result] final result ready")
        elif isinstance(event, AgentRunResultEvent):
            ticket = event.result.output  # typed SupportTicket
            break
```

Equivalent shape using `run(..., event_stream_handler=...)` if you also
want to keep the non-streaming happy-path for free:

```python
async def handle_event(ctx, event_stream):
    async for event in event_stream:
        # same dispatch as above

result = await agent.run(
    prompt,
    event_stream_handler=handle_event,
)
ticket = result.output
```

`handle_event` is invoked on the run's task; you can do real-time I/O
inside it. The handler is given the `RunContext` and the iterable of
`AgentStreamEvent`s.

#### Per-graph-node control (`agent.iter`)

Use only when you need to inspect or mutate the agent graph itself —
e.g. cancel between tool calls, swap a node, persist history mid-run.

```python
from pydantic_ai import Agent
from pydantic_graph import End

async with agent.iter(prompt, deps=db) as agent_run:
    async for node in agent_run:
        if Agent.is_model_request_node(node):
            # node.stream(run.ctx) gives you the same PartStartEvent / PartDeltaEvent
            async with node.stream(run.ctx) as request_stream:
                async for event in request_stream:
                    ...
        elif Agent.is_end_node(node):
            assert run.result is not None
            ticket = run.result.output
```

`run.result` is only populated once an `End` node appears.

#### Cancellation while streaming

- **From outside the run** (stop button, another task): mint a
  `CancellationToken`, pass it to `run` / `run_stream_events` /
  `run_sync`, and call `token.cancel()`. Surfaces as `RunCancelled`
  carrying the resumable `exc.all_messages()`.
- **From inside a tool or handler**: `ctx.cancel()`. Same outcome.
- **From the consuming task**: `events.cancel()` on the
  `AgentRunEvents` handle from `run_stream_events`.

Token usage after cancellation is partial and provider-dependent — do
not rely on cancelled-stream usage for cost-critical accounting.

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
- **Don't validate streamed partial JSON by hand**. With structured
  output, prefer `run_stream_events` (or `run(..., event_stream_handler=...)`)
  and read the typed `AgentRunResultEvent.result.output` at the end —
  Pydantic AI only validates the whole output once, on the terminal
  event. Hand-reconstructing from `PartDeltaEvent`s will silently
  accept malformed intermediates.
- **Don't use `run_stream` for "show me tools too"**. With
  `output_type=<Model>` it stops at the first matching tool call and
  drops subsequent tool traffic. Use `run_stream_events` (or `iter`)
  when you need to see tool calls in real time.

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