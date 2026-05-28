# bedrock-research-copilot

bedrock-research-copilot tells you what changed in the companies you follow — across SEC filings, earnings calls, and insider trades — before you've finished re-reading the filing.

<!-- TODO: link to architecture diagram once drawn -->
**Architecture diagram:** _TODO_

## Start here

1. Read `STATUS.md` to confirm which modules are currently green against live Bedrock.
2. Copy `.env.example` → `.env` and fill in your AWS region, model ID, and S3 bucket.
3. Install Python deps: `pip install -r requirements.txt` (Python 3.12).
4. Install infra deps: `cd infra && npm install`.
5. Open `notebooks/` and follow Module 01.

## How this repo maps to the tutorial

Each module of the written series has two phases:

- **Phase 1 — explore in a notebook.** New ideas land in `notebooks/` first. You can run them end-to-end against Bedrock without touching the production layout.
- **Phase 2 — graduate into `src/`.** Once a notebook stabilizes, the logic moves into the matching `src/` package (`ingestion/`, `tools/`, `orchestrator/`, `retrieval/`, `guardrails/`, `agent/`) with tests in `evals/`.

The end state of every module is git-tagged as `end-of-module-N`, so you can `git checkout end-of-module-3` to follow along from any starting point.

## Prerequisites

- AWS account with Bedrock model access enabled in **us-east-1**
- Node.js 20+ (for AWS CDK v2)
- Python 3.12
- AWS credentials configured locally (`aws configure` or SSO)

## License

MIT — see `LICENSE`.
