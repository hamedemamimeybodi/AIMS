# C4 Container

```mermaid
flowchart TD
    CLI[CLI App] --> Workflow[Workflow Engine]
    API[Future API] --> Workflow
    Workflow --> Parser[Parser Framework]
    Parser --> ADF[ADF Model]
    ADF --> ACE[Compliance Engine]
    ACE --> Storage[Storage Provider]
    ACE --> Report[Report Engine]
```
