# Claude / Anthropic Adapter for AutoAgent

Drop-in replacement for the OpenAI Agents SDK section of `agent.py`.

## Replace the imports and editable harness section

```python
"""Single-file Harbor agent harness using Anthropic Claude."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone

import anthropic
from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext

# ============================================================================
# EDITABLE HARNESS — prompt, tools, agent construction
# ============================================================================

SYSTEM_PROMPT = "You are an agent that executes tasks. Think step by step."
MODEL = "claude-sonnet-4-6"   # or claude-opus-4, claude-haiku-3-5
MAX_TURNS = 30

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env


def create_tools(environment: BaseEnvironment) -> list[dict]:
    """Create Anthropic-format tool definitions."""
    return [
        {
            "name": "run_shell",
            "description": "Run a shell command in the task environment. Returns stdout and stderr.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to run"}
                },
                "required": ["command"]
            }
        }
    ]


async def run_shell(environment: BaseEnvironment, command: str) -> str:
    """Execute a shell command in the sandbox."""
    try:
        result = await environment.exec(command=command, timeout_sec=120)
        out = ""
        if result.stdout:
            out += result.stdout
        if result.stderr:
            out += f"\nSTDERR:\n{result.stderr}" if out else f"STDERR:\n{result.stderr}"
        return out or "(no output)"
    except Exception as exc:
        return f"ERROR: {exc}"


async def run_task(
    environment: BaseEnvironment,
    instruction: str,
) -> tuple[object, int]:
    """Run the agent on a task using Anthropic tool-use loop."""
    tools = create_tools(environment)
    messages = [{"role": "user", "content": instruction}]
    t0 = time.time()

    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        # Append assistant response
        messages.append({"role": "assistant", "content": response.content})

        # Check stop reason
        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    if block.name == "run_shell":
                        result = await run_shell(environment, block.input["command"])
                    else:
                        result = f"Unknown tool: {block.name}"
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    duration_ms = int((time.time() - t0) * 1000)
    return response, duration_ms
```

## .env for Claude

```bash
ANTHROPIC_API_KEY=your_key_here
```

## Notes

- The Harbor adapter boundary below `run_task` stays **untouched** — only the editable section above changes
- `to_atif()` in the fixed section expects a response object with `.new_items` — you'll need to adapt the trajectory serializer if using Claude's response format
- Simplest approach: keep OpenAI SDK for the adapter boundary, swap only the model inside `create_agent()` using an OpenAI-compatible proxy (LiteLLM) pointing at Claude
- LiteLLM proxy approach: `MODEL = "anthropic/claude-sonnet-4-6"` + set `OPENAI_BASE_URL=http://localhost:4000`
