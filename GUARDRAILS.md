# Agent Guardrails

> Hard constraints for automated agents operating on this repository.

---

## Technology Stack

### Allowed

| Category | Technologies |
|----------|--------------|
| Language | Python 3.9+ |
| Testing | pytest, pytest-cov |
| Linting | ruff, black, mypy |

### Forbidden

| Technology | Reason |
|------------|--------|
| Heavy frameworks | Overkill for current scope |

---

## Security & Privacy

- **NO hardcoded secrets** - All credentials via environment variables
- **NO logging of PII** - Mask or exclude sensitive fields
- **NO committing `.env`** - Must be in `.gitignore`

---

## Performance & Cost Limits

| Metric | Limit | Action on Exceed |
|--------|-------|------------------|
| Max iterations | 50 | Terminate with `ITERATION_LIMIT` |
| Max API calls | 100 | Terminate with `API_LIMIT` |
| Max runtime | 30 min | Terminate with `TIMEOUT` |

---

## Context Management

### Rotation Policy

Agents SHOULD rotate context when:
- Same command fails 3+ times
- Diff size churn exceeds 500 lines
- Token count approaches model limit

### State Persistence

- Long-lived state MUST be persisted to files, not prompt memory
- Use git commits as checkpoints

---

## Escalation Paths

| Condition | Action |
|-----------|--------|
| Security vulnerability | STOP, create issue, notify human |
| Breaking change | STOP, request human review |
| 3+ failed iterations | STOP, emit `CONTEXT_POLLUTED` |
