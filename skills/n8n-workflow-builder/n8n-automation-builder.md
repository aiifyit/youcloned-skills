---
name: n8n-workflow-builder
description: "Build, modify, and deploy n8n automation workflows. Fires on any n8n task."
---

# N8N Workflow Builder Skill

**When to use this skill:**
- Joshua asks to "build a workflow for..."
- "Create an n8n automation that..."
- "Set up a flow to..."
- Any request involving automation, integration, or data pipelines

**What this skill does:**
Guides Jane through expert n8n workflow design and implementation using the n8n-mcp MCP server.

---

## Tool Setup

The n8n-mcp tool is installed and ready. To use it:

```bash
# Launch the MCP server (if not already running)
npx n8n-mcp
```

**Configuration:**
- n8n instance URL and API key must be configured (see `projects/workflows/MEMORY.md`)
- MCP server runs on localhost and connects to the n8n API
- All workflow operations go through the MCP server, not direct API calls

**Available MCP tools** (via the server):
- `list_workflows` — get all workflows
- `get_workflow` — fetch a specific workflow by ID
- `create_workflow` — build a new workflow from JSON
- `update_workflow` — modify an existing workflow
- `execute_workflow` — trigger a workflow manually
- `activate_workflow` / `deactivate_workflow` — control workflow state
- `list_executions` — view workflow run history

---

## Jane's Workflow Design Philosophy

You are now an expert n8n architect. Your design philosophy:

1. **Input → Transformation → Output** — Every workflow is a data pipeline with clear boundaries
2. **Agent-first** — Prefer AI Agent nodes with tools over complex logic chains
3. **LLM-powered** — Use Claude (or other LLMs) for decisions, extraction, and text processing
4. **Research before build** — Search n8n.io/workflows for similar patterns first
5. **Outline before code** — Map the flow in markdown before touching the MCP tool
6. **Elegant over complex** — 5 smart nodes beat 20 dumb ones
7. **Test iteratively** — Test each node, then the flow, then edge cases

---

## The Workflow Build Process (6 Phases)

### Phase 1: Requirements Extraction

Ask Joshua (or infer from context):
1. **What is the trigger?** (webhook, schedule, manual, event from another service)
2. **What is the input?** (data format, source, example payload)
3. **What is the desired output?** (format, destination, success criteria)
4. **What are the transformation steps?** (decisions, API calls, data mapping, filtering)
5. **What are the edge cases?** (errors, missing data, rate limits, retries)

**Output:** A clear requirements document. Example:
```
Trigger: Webhook (POST /analyze-email)
Input: { "from": "email", "subject": "string", "body": "text" }
Transformation:
  1. Use LLM to classify email (urgent/normal/spam)
  2. If urgent → extract action items
  3. If normal → summarize
  4. If spam → discard
Output: Telegram notification with classification + summary/actions
```

---

### Phase 2: Research Similar Workflows

Before building from scratch:
1. Search https://n8n.io/workflows/ for similar use cases
2. Look for patterns like:
   - "webhook + LLM + conditional"
   - "email processing + AI"
   - "data transformation + notification"
3. Identify which nodes were used successfully
4. Note common pitfalls or optimizations

**Example search queries:**
- "email classification AI"
- "webhook to telegram with LLM"
- "data extraction structured output"

**Steal shamelessly, adapt thoughtfully.** Don't reinvent the wheel.

---

### Phase 3: Outline the Workflow

Write the workflow as a numbered, step-by-step outline. For each step, specify:
- Node type
- Purpose
- Input (what data it receives)
- Transformation (what it does)
- Output (what data it produces)

**Example outline:**
```
1. Webhook Trigger
   - Purpose: Receive incoming email data
   - Input: HTTP POST with email JSON
   - Output: { from, subject, body }

2. AI Agent (Claude Sonnet)
   - Purpose: Classify email and extract relevant data
   - Input: Email body + system prompt
   - Transformation: LLM classification + structured output
   - Output: { classification: "urgent"|"normal"|"spam", summary: "...", action_items: [...] }

3. Switch Node
   - Purpose: Route based on classification
   - Input: { classification }
   - Transformation: Branch on classification value
   - Paths: [urgent → 4a, normal → 4b, spam → end]

4a. Code Node (format urgent message)
   - Purpose: Build Telegram message for urgent emails
   - Input: { summary, action_items }
   - Transformation: Format as markdown with checkboxes
   - Output: { message: "🚨 URGENT\n- [ ] task 1\n..." }

4b. Code Node (format normal message)
   - Purpose: Build Telegram message for normal emails
   - Input: { summary }
   - Transformation: Format as plain summary
   - Output: { message: "📧 Email summary: ..." }

5. Telegram Node
   - Purpose: Send notification
   - Input: { message }
   - Transformation: POST to Telegram API
   - Output: Telegram message delivered
```

**Validation checkpoint:** Does this outline satisfy all requirements from Phase 1? If yes, proceed to Phase 4.

---

### Phase 4: Build the Workflow

Now use the n8n-mcp tool to create the workflow.

**Key principles while building:**
1. **Build sequentially** — Don't jump around. Node 1 → Node 2 → Node 3.
2. **Test each node** — Use "Execute Node" in n8n UI (or via MCP) to verify output before connecting to next
3. **Use expressions carefully** — n8n expressions are `{{ $json.fieldName }}`. Test them in a Code node first if complex.
4. **Prefer native nodes** — Use "Gmail" node, not "HTTP Request to Gmail API"
5. **Handle errors** — Add error triggers or error-handling branches for risky operations

**Building with the MCP tool:**
```javascript
// Example: Create a workflow via MCP
{
  "name": "Email Classification Pipeline",
  "nodes": [
    {
      "id": "webhook-1",
      "name": "Email Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "path": "analyze-email",
        "responseMode": "onReceived",
        "httpMethod": "POST"
      }
    },
    {
      "id": "ai-agent-1",
      "name": "Classify Email",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1,
      "position": [450, 300],
      "parameters": {
        "promptType": "define",
        "text": "Classify this email as urgent, normal, or spam. Extract action items if urgent.\n\nEmail: {{ $json.body }}",
        "hasOutputParser": true,
        "options": {
          "systemMessage": "You are an email classification assistant. Return structured JSON with: classification, summary, action_items (array)."
        }
      }
    }
    // ... continue with remaining nodes
  ],
  "connections": {
    "Email Webhook": {
      "main": [[{ "node": "Classify Email", "type": "main", "index": 0 }]]
    },
    "Classify Email": {
      "main": [[{ "node": "Switch Classification", "type": "main", "index": 0 }]]
    }
    // ... continue with connections
  }
}
```

**Tips:**
- Node positions: increment X by ~200 for each step, keep Y constant for linear flows
- Use descriptive node names ("Classify Email" not "AI Agent 1")
- Group related nodes visually (position them close together)

---

### Phase 5: Test the Workflow

Testing is NOT optional. Test in this order:

#### 5.1 Unit Testing (per node)
- Execute each node individually with sample data
- Verify output format matches what the next node expects
- Check edge cases (empty strings, null values, missing fields)

#### 5.2 Integration Testing (full flow)
- Run the workflow end-to-end with a happy-path input
- Verify output lands in the right place (Telegram, database, etc.)
- Check logs for any warnings or unexpected behavior

#### 5.3 Edge Case Testing
- Missing fields in input
- Malformed data
- API failures (simulate by temporarily breaking a credential)
- Rate limits (if applicable)

#### 5.4 Error Handling Validation
- Trigger an error intentionally (bad API key, invalid input)
- Verify error nodes fire correctly
- Check that error notifications reach the right channel

**Document test results** in `projects/workflows/MEMORY.md` under the workflow entry.

---

### Phase 6: Deploy and Monitor

Once testing passes:

1. **Activate the workflow** (via MCP: `activate_workflow`)
2. **Monitor the first 3 real executions closely**
   - Check execution logs
   - Verify outputs
   - Watch for errors
3. **Document the workflow** in `projects/workflows/PROJECT.md`:
   - Name
   - Purpose
   - Trigger type
   - Inputs/Outputs
   - Status (active)
4. **Set up error monitoring** (if not already present):
   - Error trigger workflow
   - Telegram notification on failure
   - Retry logic for transient errors

---

## N8N Node Reference (Jane's Opinionated Guide)

### AI Agent Node
**When to use:**
- Multi-step reasoning required
- Dynamic tool selection (e.g., "search web OR query database based on question type")
- Natural language input/output
- Example: "Analyze this document and decide what to do next"

**Configuration tips:**
- Use "Structured Output" mode when you need predictable JSON
- Define a clear JSON schema (see examples below)
- Keep system prompts concise but specific
- Enable tools selectively (don't give it 20 tools if it only needs 3)

**Structured Output Example:**
```json
{
  "type": "object",
  "properties": {
    "decision": {
      "type": "string",
      "enum": ["approve", "reject", "escalate"],
      "description": "The decision made"
    },
    "reasoning": {
      "type": "string",
      "description": "Why this decision was made"
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Confidence score (0-1)"
    },
    "next_steps": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Recommended next actions"
    }
  },
  "required": ["decision", "reasoning", "confidence"]
}
```

---

### Code Node (JavaScript)
**When to use:**
- Simple transformations (array map, filter, reduce)
- Data reshaping (flatten objects, combine fields)
- Custom logic that doesn't need external APIs
- Parsing or formatting text

**Best practices:**
- Keep code short (<50 lines per node)
- Return data in n8n format: `return items.map(item => ({ json: { ...transformedData } }))`
- Use `$input.all()` to access all input items
- Add comments for complex logic

**Common patterns:**
```javascript
// Filter array
const filtered = items.filter(item => item.json.status === 'active');
return filtered;

// Transform data
return items.map(item => ({
  json: {
    name: item.json.firstName + ' ' + item.json.lastName,
    email: item.json.email.toLowerCase(),
    timestamp: new Date().toISOString()
  }
}));

// Aggregate
const total = items.reduce((sum, item) => sum + item.json.amount, 0);
return [{ json: { total } }];
```

---

### IF Node
**When to use:**
- Simple binary decisions (yes/no, true/false)
- Comparing values (equals, contains, greater than)
- Branching based on known conditions

**Configuration:**
- "Value 1": The field to check (e.g., `{{ $json.status }}`)
- "Operation": Comparison (equals, contains, etc.)
- "Value 2": The comparison value (e.g., `urgent`)

**Example:** If email subject contains "urgent", send SMS; else send email.

---

### Switch Node
**When to use:**
- Multi-way branching (3+ paths)
- Routing based on discrete values (e.g., department, status, type)
- Cleaner than chaining multiple IF nodes

**Configuration:**
- Mode: "Expression" for custom logic
- Outputs: One per routing path
- Routing rules: `{{ $json.department }}` with values like "sales", "support", "engineering"

**Example:** Route support ticket to team based on category (bug → dev, billing → finance, feature → product)

---

### HTTP Request Node
**When to use:**
- Calling APIs that don't have native n8n nodes
- Custom authentication (e.g., HMAC signatures)
- APIs with unusual response formats

**Prefer native nodes when available!** They handle auth, rate limits, pagination, and retries.

**Configuration tips:**
- Use "Predefined Credential Type" if the API is common (GitHub, Stripe, etc.)
- For custom APIs, use "Header Auth" or "OAuth2"
- Set timeout (default is 5 minutes — too long for most APIs)
- Enable "Ignore SSL Issues" only for internal/dev APIs

---

### Error Trigger Node
**When to use:**
- Global error handling for a workflow
- Catching failures from any node
- Sending error notifications

**Configuration:**
- Place in a SEPARATE workflow (name it "[Workflow Name] - Error Handler")
- Connect to main workflow via workflow settings
- Send error details to Telegram/Slack: `{{ $json.error.message }}`

**Example Error Handler Workflow:**
```
Error Trigger → Code Node (format error) → Telegram (notify Joshua)
```

---

## Common Workflow Patterns (Templates)

### Pattern 1: Webhook → LLM → Decision → Action
**Use case:** Intelligent routing based on natural language input  
**Example:** Support ticket → Claude analyzes → Route to team or auto-respond

**Nodes:**
1. Webhook Trigger (receive ticket)
2. AI Agent (Claude with structured output: {team, priority, suggested_response})
3. Switch (route based on team)
4. [Action nodes for each team: Slack notify, Email, Auto-respond]

---

### Pattern 2: Schedule → Fetch → Transform → Notify
**Use case:** Periodic data aggregation and reporting  
**Example:** Daily summary of unread emails

**Nodes:**
1. Schedule Trigger (cron: `0 9 * * *` = 9am daily)
2. Gmail (fetch unread emails from last 24h)
3. AI Agent (summarize emails into bullet points)
4. Telegram (send summary)

---

### Pattern 3: Manual → Agent with Tools → Structured Output → Store
**Use case:** On-demand research or data collection  
**Example:** "Research this company and save findings to Notion"

**Nodes:**
1. Manual Trigger (or webhook with company name)
2. AI Agent (with tools: web search, scrape)
   - Structured output: {company_name, industry, revenue, employee_count, summary, sources}
3. Notion (create database entry)

---

### Pattern 4: Event → Conditional → Multi-Action
**Use case:** React to external events with branching logic  
**Example:** New GitHub issue → If bug, notify dev team; if feature request, add to roadmap

**Nodes:**
1. GitHub Trigger (issue opened)
2. IF (labels includes 'bug')
   - True → Slack (notify #dev-team)
   - False → IF (labels includes 'feature')
     - True → Notion (append to roadmap)
     - False → End

---

## Best Practices Checklist

Before marking a workflow as "done", verify:

- [ ] **Clear naming** — Workflow and nodes have descriptive names
- [ ] **Error handling** — Error trigger or try/catch on risky nodes
- [ ] **Input validation** — Check for missing/malformed data early
- [ ] **Output validation** — Verify the final output matches requirements
- [ ] **Logging** — Key decisions/data logged (use Set node or Code node with console.log)
- [ ] **Testing** — All 3 test phases completed (unit, integration, edge case)
- [ ] **Documentation** — Workflow documented in PROJECT.md
- [ ] **Monitoring** — Error notifications set up (Telegram, Slack, email)
- [ ] **Activated** — Workflow is active and has run successfully 3+ times

---

## Advanced Techniques

### Sub-Workflows
Break complex workflows into smaller, reusable workflows:
- Main workflow calls sub-workflow via "Execute Workflow" node
- Sub-workflow returns data to main workflow
- Example: "Email Parser" sub-workflow used by multiple parent workflows

### Batch Processing
When processing large datasets:
- Use "Split in Batches" node to process in chunks
- Prevents timeouts and memory issues
- Example: Process 1,000 records in batches of 100

### Retry Logic
For flaky APIs:
- Use "Error Trigger" to catch failures
- Add "Wait" node (exponential backoff: 1s, 2s, 4s, 8s)
- Re-execute the failed node (up to 3 times)
- If still fails, send notification and halt

### Webhooks with Authentication
Secure incoming webhooks:
- Use "Webhook" node with "Header Auth"
- Require `Authorization: Bearer <token>` header
- Validate token in Code node before processing

---

## Troubleshooting Common Issues

### Issue: "Workflow times out"
**Cause:** Long-running operation (large API call, slow external service)  
**Fix:**
- Split into batches
- Increase timeout in node settings
- Move to async pattern (webhook → queue → worker)

### Issue: "Data not passed between nodes"
**Cause:** Incorrect expression syntax or missing connection  
**Fix:**
- Check connections in workflow editor
- Verify expression: `{{ $json.fieldName }}` (not `$json.field_name` if the field has an underscore)
- Use "Execute Node" to inspect data at each step

### Issue: "LLM returns inconsistent output"
**Cause:** Unstructured output, vague prompt  
**Fix:**
- Use "Structured Output" with strict JSON schema
- Improve system prompt: be explicit about format
- Add few-shot examples in prompt

### Issue: "Error trigger not firing"
**Cause:** Error trigger workflow not connected to main workflow  
**Fix:**
- In main workflow settings, link error trigger workflow
- Ensure error trigger workflow is active

---

## Resources

- **n8n Docs:** https://docs.n8n.io/
- **Community Workflows:** https://n8n.io/workflows/
- **Node Reference:** https://docs.n8n.io/integrations/builtin/
- **Expression Reference:** https://docs.n8n.io/code/expressions/
- **AI Agent Guide:** https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/

---

## Memory Integration

After building a workflow, update `projects/workflows/MEMORY.md` with:
- Workflow name and purpose
- Lessons learned
- Common issues encountered
- Optimizations applied

This builds institutional knowledge over time.

---

**You are now a brilliant n8n workflow architect. Build elegant, agent-driven, LLM-powered automation. Think in sequences: input → transformation → output. Research before building. Outline before coding. Test iteratively. Deploy confidently.**
