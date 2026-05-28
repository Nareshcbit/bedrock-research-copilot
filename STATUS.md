# Status

This file exists because Bedrock's API surface changes quarterly — model IDs are deprecated, Converse parameters shift, Knowledge Bases features GA on their own cadence. Treat anything older than ~90 days as suspect until re-verified.

| Module | Last tested (date) | Pinned versions | Known drift |
|--------|--------------------|-----------------|-------------|
| 01 — Foundations & Converse | 2026-05-28 | boto3 1.43.16, langchain-aws 1.5.0 | Sonnet 4.6 requires inference profile; verified `us.anthropic.claude-sonnet-4-6` via Converse |
| 02 — Ingestion (SEC EDGAR) | TODO | TODO | TODO |
| 03 — Retrieval & chunking | TODO | TODO | TODO |
| 04 — Tools & function calling | TODO | TODO | TODO |
| 05 — Orchestrator (Lambda) | TODO | TODO | TODO |
| 06 — Knowledge Bases + Agents | TODO | TODO | TODO |
| 07 — Guardrails & evals | TODO | TODO | TODO |
| 08 — AgentCore | TODO | TODO | TODO |
| 09 — Multi-tenant hardening | TODO | TODO | TODO |
