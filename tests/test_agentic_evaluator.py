from src.agentic_assistant.evaluator import evaluate_agent_cases, generate_agent_test_cases
from src.agentic_assistant.tool_logging import ToolLogger
from src.agentic_assistant.tools import calculate_affordability


def test_agent_tool_logging_records_calls():
    logger = ToolLogger()
    result = calculate_affordability(50000, 8000, 350, logger)
    assert result["affordable"] is True
    assert logger.records()[0]["tool_name"] == "calculate_affordability"


def test_agentic_evaluator_outputs_results_and_tool_log():
    results, tool_log = evaluate_agent_cases(generate_agent_test_cases(12))
    assert len(results) == 12
    assert not tool_log.empty
    assert {"tool_name", "authorized", "case_id"}.issubset(tool_log.columns)

