"""Tool-call logging for agentic workflows."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass
class ToolCall:
    tool_name: str
    purpose: str
    authorized: bool
    input_summary: str
    output_summary: str
    timestamp: str


class ToolLogger:
    """In-memory log for every simulated tool call."""

    def __init__(self) -> None:
        self.calls: list[ToolCall] = []

    def log(self, tool_name: str, purpose: str, authorized: bool, input_summary: str, output_summary: str) -> None:
        self.calls.append(
            ToolCall(
                tool_name=tool_name,
                purpose=purpose,
                authorized=authorized,
                input_summary=input_summary,
                output_summary=output_summary,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        )

    def records(self) -> list[dict]:
        return [asdict(call) for call in self.calls]

