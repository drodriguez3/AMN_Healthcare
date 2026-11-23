# Proposed solution architecture and scope

## Hypothesis
A workforce intelligence interface can reduce the effort required to reconcile demand, candidate availability, and recruiting priorities. This hypothesis requires discovery and validation with the prospective customer.

## Proposed production flow
1. Authorized workforce/CRM/credentialing sources → ingestion and data-quality controls.
2. Snowflake → governed demand, supply, placements, and document datasets with documented definitions.
3. Cortex Analyst → natural-language SQL against approved semantic definitions; evaluated for accuracy and permissions.
4. Cortex Search (optional) → retrieval over approved unstructured job or policy content with access controls.
5. Snowpark ML (later phase) → forecasting with temporal validation and monitoring.
6. Streamlit → role-aware workflow and business metrics.

## Demo implementation versus production proposal
| Feature | Demo implementation | Possible production implementation |
|---|---|---|
| Data | Fictional local CSV files | Customer-approved governed Snowflake tables |
| Market dashboard | Local pandas aggregations | Validated KPI definitions and role-based reporting |
| Analyst | Fixed sample-question menu | Cortex Analyst with semantic views, guardrails, evaluation |
| Candidate discovery | Fictional profile filtering | Authorized, compliant retrieval with human oversight |
| Forecasting | Not implemented | Validated ML model only if data and business case support it |
| Security | Local demo only | SSO/RBAC, audit logging, PII minimization, retention controls |

## Non-goals
No production integration, live AI, automated hiring decisions, claims about AMN internal data or priorities, credential verification, or security/compliance certification.

## Suggested pilot acceptance criteria (to negotiate)
- 8–12 approved business questions with a measurable correct-answer threshold.
- Documented reconciliation of KPIs to trusted source reports.
- Measured time-to-answer before and after pilot.
- No access outside explicitly approved roles; logging and review of sensitive outputs.
- Named business owner and go/no-go review.

## Business case
Potential benefits include reduced analyst time, clearer market visibility, and better prioritization. None are quantified in this demo; validate baseline and target during discovery.
