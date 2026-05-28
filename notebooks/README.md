# Notebooks

**Phase 1 — exploration.** Every module of the tutorial starts here. Notebooks let us call Bedrock end-to-end, inspect raw responses, and iterate on prompts without dragging the whole `src/` layout along.

**Phase 2 — graduation.** Once a notebook's logic stabilizes, it moves into the matching package under `src/` (for example, `src/ingestion/` for the EDGAR fetcher), gains type hints and tests, and the notebook becomes a thin demo that imports from `src/`.

## Conventions

- One notebook per module: `01_foundations.ipynb`, `02_ingestion.ipynb`, …
- Notebooks read config from the same `.env` the rest of the repo uses.
- Clear outputs before committing (`jupyter nbconvert --clear-output`).
- If a notebook is more than ~30% boilerplate, it's time to graduate it.
