from dataclasses import dataclass
@dataclass
class PromptResult:
    prompt : str
    response: str
    latency: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int