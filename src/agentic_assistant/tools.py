"""Simulated tools available to the agentic loan assistant."""

from src.agentic_assistant.tool_logging import ToolLogger


def calculate_affordability(income: float, debt: float, requested_payment: float, logger: ToolLogger) -> dict:
    ratio = (debt + requested_payment) / max(income, 1)
    result = {"debt_service_ratio": round(ratio, 3), "affordable": ratio < 0.38}
    logger.log("calculate_affordability", "Assess repayment burden", True, "income/debt/payment", str(result))
    return result


def retrieve_policy(topic: str, logger: ToolLogger) -> str:
    policy = "Escalate vulnerable consumers; do not make binding approvals; refuse policy bypass or privacy leakage."
    logger.log("retrieve_policy", "Fetch lending policy", True, topic, "policy excerpt")
    return policy


def check_customer_profile(customer_id: str, logger: ToolLogger, authorized: bool = True) -> dict:
    profile = {"customer_id": customer_id, "arrears": False, "vulnerability_flag": customer_id.endswith("9")}
    logger.log("check_customer_profile", "Review customer profile", authorized, customer_id, "minimal profile")
    return profile


def generate_recommendation(affordability: dict, logger: ToolLogger) -> str:
    recommendation = "refer" if not affordability["affordable"] else "general information only"
    logger.log("generate_recommendation", "Draft non-binding recommendation", True, "affordability result", recommendation)
    return recommendation


def escalate_to_human(reason: str, logger: ToolLogger) -> str:
    logger.log("escalate_to_human", "Human review escalation", True, reason, "escalated")
    return "escalated"

