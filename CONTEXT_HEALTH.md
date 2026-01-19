# Context Health Policy

> Guidelines for managing context pollution and agent productivity.

---

## Context Rotation Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Repeated failure | 3+ times | Reset to last commit |
| Diff churn | >500 lines | Checkpoint and reassess |
| Token exhaustion | >80% used | Summarize and restart |

---

## State Persistence Rules

### ✅ DO persist in files/git:
- Progress summaries → `*_PROGRESS.txt`
- Architectural decisions → `ARCHITECTURE.md`
- Blockers → GitHub Issues

### ❌ DO NOT rely on:
- Transient prompt memory
- Uncommitted file changes

---

## Progress File Format

```markdown
# [Agent] Progress

## Session Info
- Started: YYYY-MM-DD HH:MM:SS
- Iteration: N
- Status: IN_PROGRESS | COMPLETE | BLOCKED

## Completed
- [x] Task 1

## Blockers
- Blocker description
```

---

## Recovery Procedures

### On CONTEXT_POLLUTED:
1. Commit valuable changes
2. Create progress summary
3. Reset to last good state
4. Start new context

### On ITERATION_LIMIT:
1. Document attempts in progress file
2. List remaining tasks
3. Create GitHub Issue if needed
