# ACE Specification Draft

ACE means **AIMS Compliance Engine**.

ACE executes ACS rules and selected profiles against ADF documents.

## Responsibilities

- Load rules.
- Select profile.
- Execute validation.
- Produce explainable issues.
- Support fix plans.
- Record rule versions.

## Validation Result

```json
{
  "rule_id": "ACS-3001",
  "severity": "ERROR",
  "feature_id": "F-001",
  "message": "Boundary geometry must be closed.",
  "why_it_matters": "Open boundaries prevent reliable area and topology checks.",
  "suggested_fix": "Close the polyline if endpoints are within tolerance."
}
```
