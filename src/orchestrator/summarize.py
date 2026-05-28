"""Bedrock Converse summarizer. Module 1 vertical slice.

Filled out in Module 05 with retries, chunking + map-reduce for long inputs,
streaming, and structured output. Module 1: one-shot Converse on truncated text.
"""

from __future__ import annotations

import os

import boto3
from dotenv import load_dotenv

load_dotenv()

# Module-1 simplification: hard cap inputs to ~15k chars (~4k tokens). Real
# 10-K risk sections run 30-80k chars; Module 05 replaces this with chunking
# and map-reduce summarization.
MAX_INPUT_CHARS = 15_000

_SYSTEM_PROMPT = (
    "You are a senior equity research analyst. Summarize the supplied 10-K "
    "Risk Factors text in exactly 5 bullet points capturing the dominant risk "
    "themes. Each bullet must be factual and grounded in the source text. "
    "Do not give investment advice. Do not invent risks the text does not mention."
)


def summarize_risk_factors(risk_text: str) -> str:
    model_id = os.environ.get("BEDROCK_MODEL_ID", "").strip()
    if not model_id:
        raise RuntimeError("BEDROCK_MODEL_ID is empty. Set it in .env.")
    if not risk_text.strip():
        raise ValueError("risk_text is empty.")

    region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("bedrock-runtime", region_name=region)
    resp = client.converse(
        modelId=model_id,
        system=[{"text": _SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": risk_text[:MAX_INPUT_CHARS]}]}],
        inferenceConfig={"maxTokens": 600, "temperature": 0.2},
    )
    return resp["output"]["message"]["content"][0]["text"]


if __name__ == "__main__":
    from src.ingestion.edgar import get_latest_10k

    filing = get_latest_10k("MSFT")
    print(
        f"--- summarizing {filing['ticker']} 10-K "
        f"(filed {filing['filing_date']}, {len(filing['risk_factors_text'])} chars) ---"
    )
    print(summarize_risk_factors(filing["risk_factors_text"]))
