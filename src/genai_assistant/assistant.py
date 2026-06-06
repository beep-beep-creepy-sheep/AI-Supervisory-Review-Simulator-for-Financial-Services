"""Rule-based financial assistant used as a safe, no-API evaluation target."""

ESCALATION_TERMS = ["suicide", "homeless", "domestic abuse", "terminal illness", "gambling addiction", "can't pay rent"]
HIGH_RISK_TERMS = ["crypto", "guaranteed return", "payday", "hide debt", "ignore arrears"]


def answer(prompt: str, persona: str = "retail customer") -> str:
    """Return a cautious consumer-finance response with clear boundaries."""
    text = prompt.lower()
    if "ignore previous" in text or "reveal policy" in text or "system prompt" in text:
        return "I cannot follow instructions that bypass policy or reveal internal controls. I can provide general, cautious guidance."
    if any(term in text for term in ESCALATION_TERMS):
        return "This may involve vulnerability or financial distress. Please contact the bank hardship team or a qualified adviser; I cannot make a binding decision."
    if any(term in text for term in HIGH_RISK_TERMS):
        return "I cannot recommend high-risk or evasive financial actions. Consider regulated advice, affordability checks, and scam warnings."
    if "will i be approved" in text or "guarantee" in text:
        return "I cannot guarantee approval. Lending depends on affordability, credit checks, and responsible lending policy."
    return "I can provide general information only. Review affordability, compare regulated options, and seek qualified advice for personal decisions."

