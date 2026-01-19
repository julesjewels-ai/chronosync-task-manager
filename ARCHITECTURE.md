# Architecture Document

> **Status:** `DRAFT` | `REVIEW` | `LOCKED`  
> **Last Updated:** YYYY-MM-DD

---

## System Overview

[Describe what the system does and its primary purpose]

---

## Component Diagram

```mermaid
graph TB
    subgraph "User Interface"
        CLI[CLI Interface]
    end
    
    subgraph "Core Domain"
        WF[Workflow Engine]
        Models[Domain Models]
    end
    
    subgraph "Services"
        SVC[Services]
    end
    
    CLI --> WF
    WF --> Models
    WF --> SVC
```

---

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.9+ | Team expertise |
| Testing | pytest | Standard, good plugins |
