# AutoAgent Task Format (Harbor)

Tasks live in `tasks/` and follow [Harbor](https://github.com/laude-institute/harbor) format.

## Minimal Task Structure

```
tasks/
└── my-task/
    ├── task.json       # Task definition
    └── verifier.py     # Correctness checker
```

## task.json

```json
{
  "task_id": "my-task",
  "instruction": "Natural language instruction for the agent.",
  "environment": {
    "files": {
      "input.csv": "col1,col2\nval1,val2\n"
    }
  }
}
```

- `task_id` — unique identifier
- `instruction` — what the agent is asked to do
- `environment.files` — optional files pre-loaded into the sandbox

## verifier.py

```python
def verify(environment, result) -> dict:
    """
    Returns: {"passed": bool, "score": float (0-1), "reason": str}
    """
    # Check the agent produced the expected output
    output = environment.read_file("output.txt")
    passed = "expected_value" in output
    return {
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "reason": "Found expected value" if passed else "Missing expected value"
    }
```

## Pulse Task Examples

### Sales — Lead Scoring

```json
{
  "task_id": "sales-lead-score-001",
  "instruction": "You receive a lead: Name: John Smith, Company: Acme Corp (50 employees, manufacturing), Note: 'interested in automating our invoicing process, budget TBD'. Score this lead hot/warm/cold and explain your reasoning.",
  "environment": {}
}
```

Verifier checks: response contains one of `hot`, `warm`, `cold` + reasoning present.

### Ops — Ticket Routing

```json
{
  "task_id": "ops-route-001",
  "instruction": "Inbound request: 'The Stripe webhook stopped firing and payments are not being recorded.' Classify the request type, assign it to the correct team (Engineering / Finance / CS / Sales), and output the first 3 steps to resolve it.",
  "environment": {}
}
```

Verifier checks: `Engineering` in response, 3+ steps present.

### Finance — Anomaly Detection

```json
{
  "task_id": "finance-anomaly-001",
  "instruction": "Review the transactions in transactions.csv. Flag any anomalies and explain why each is flagged.",
  "environment": {
    "files": {
      "transactions.csv": "date,vendor,amount\n2026-01-01,AWS,450.00\n2026-01-01,AWS,450.00\n2026-01-03,Office Depot,12.50\n2026-01-04,Unknown Vendor XZ,9999.00\n"
    }
  }
}
```

Verifier checks: duplicate AWS charge flagged, Unknown Vendor flagged.

## Tips

- Start with 5-10 tasks for a baseline; expand as the agent improves
- Binary pass/fail verifiers are simplest to start with
- Add rubric-based scoring (0.0–1.0) when you need nuanced quality measurement
- Name task IDs descriptively: `{agent}-{category}-{number}`
