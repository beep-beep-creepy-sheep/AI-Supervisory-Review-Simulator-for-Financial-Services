from src.genai_assistant.evaluator import evaluate_genai_cases
from src.genai_assistant.test_cases import generate_genai_test_cases


def test_genai_evaluator_outputs_scored_rows():
    cases = generate_genai_test_cases(16)
    results = evaluate_genai_cases(cases)
    assert len(results) == 16
    assert {"id", "risk_category", "passed", "severity_score", "rationale"}.issubset(results.columns)
    assert results["severity_score"].between(0, 3).all()

