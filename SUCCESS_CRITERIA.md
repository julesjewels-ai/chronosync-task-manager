# Success Criteria

> Machine-checkable signals for each development phase.  
> Agents emit `<promise>PHASE_NAME</promise>` when criteria are met.

---

## Phase: ARCHITECTURE_LOCKED

**Promise Token:** `<promise>ARCHITECTURE_LOCKED</promise>`

### Verification Commands

```bash
test -f ARCHITECTURE.md
test -f src/core/interfaces.py
```

---

## Phase: SKELETON_VALID

**Promise Token:** `<promise>SKELETON_VALID</promise>`

### Verification Commands

```bash
python -m py_compile src/**/*.py
python -c "import src"
```

---

## Phase: SOLID_COMPLETE

**Promise Token:** `<promise>SOLID_COMPLETE</promise>`

### Verification Commands

```bash
pytest tests/ -v
pytest --cov=src/core --cov-fail-under=60
```

---

## Phase: TESTS_PASSING_ALL

**Promise Token:** `<promise>TESTS_PASSING_ALL</promise>`

### Verification Commands

```bash
pytest tests/ -v
pytest --cov=src --cov-fail-under=80
```

---

## Phase: READY_FOR_DEPLOYMENT

**Promise Token:** `<promise>READY_FOR_DEPLOYMENT</promise>`

### Verification Commands

```bash
make lint
make test
bandit -r src/ -ll -x tests/
```

---

## Failure Tokens

| Token | Meaning |
|-------|---------|
| `CONTEXT_POLLUTED` | Too many failed attempts |
| `ITERATION_LIMIT` | Max iterations reached |
| `HUMAN_REVIEW_REQUIRED` | Decision beyond agent authority |
