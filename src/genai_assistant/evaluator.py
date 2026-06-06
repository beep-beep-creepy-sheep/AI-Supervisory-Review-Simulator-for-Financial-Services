"""Evaluation harness for the GenAI consumer finance assistant."""

from pathlib import Path
import json
import pandas as pd

from src.genai_assistant.assistant import answer
from src.genai_assistant.scoring import score_response


def evaluate_genai_cases(cases: list[dict]) -> pd.DataFrame:
    records = []
    for case in cases:
        response = answer(case["prompt"], case["persona"])
        records.append(score_response(case, response))
    return pd.DataFrame(records)


def save_genai_results(results: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".json":
        path.write_text(json.dumps(results.to_dict(orient="records"), indent=2), encoding="utf-8")
    else:
        results.to_csv(path, index=False)

