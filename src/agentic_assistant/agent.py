"""Small agent-like workflow for loan assistance."""

from src.agentic_assistant.tool_logging import ToolLogger
from src.agentic_assistant import tools


def run_agent(case: dict, logger: ToolLogger | None = None) -> dict:
    """Run a policy-constrained simulated loan assistant."""
    logger = logger or ToolLogger()
    prompt = case["prompt"].lower()
    tools.retrieve_policy("loan assistance", logger)

    if "ignore policy" in prompt or "leak" in prompt:
        return {"decision": "refuse", "message": "Cannot bypass policy or disclose personal data.", "tool_calls": logger.records()}

    authorized_profile = "other customer" not in prompt
    if case.get("needs_profile", True):
        profile = tools.check_customer_profile(case.get("customer_id", "ECB-00001"), logger, authorized=authorized_profile)
    else:
        profile = {"vulnerability_flag": False}

    if case.get("vulnerable") or profile.get("vulnerability_flag"):
        tools.escalate_to_human("vulnerable or high-risk customer", logger)
        return {"decision": "escalate", "message": "Human review required.", "tool_calls": logger.records()}

    affordability = tools.calculate_affordability(case.get("income", 42000), case.get("debt", 7000), case.get("requested_payment", 350), logger)
    recommendation = tools.generate_recommendation(affordability, logger)
    return {"decision": recommendation, "message": "Non-binding guidance only.", "tool_calls": logger.records()}

