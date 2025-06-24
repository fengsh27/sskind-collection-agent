
from enum import Enum
from typing import Callable, Optional, TypedDict

from .constants import DEFAULT_TOKEN_USAGE

def increase_token_usage(
    token_usage: Optional[dict] = None,
    incremental: dict = {**DEFAULT_TOKEN_USAGE},
):
    if token_usage is None:
        token_usage = {**DEFAULT_TOKEN_USAGE}
    token_usage["total_tokens"] += incremental["total_tokens"]
    token_usage["completion_tokens"] += incremental["completion_tokens"]
    token_usage["prompt_tokens"] += incremental["prompt_tokens"]

    return token_usage

class ResearchGoalEnum(Enum):
    ALZHEIMERS = "alzheimer"

research_goal_dict = {
    ResearchGoalEnum.ALZHEIMERS: "**Alzheimer's disease** and **single-cell RNA sequencing**",
}

class IdentifyState(TypedDict):
    research_goal: ResearchGoalEnum
    title: str
    abstract: str
    content: str
    step_output_callback: Optional[Callable[[str], None]]  # Callback for step output

    # final answer
    relevant: Optional[bool]
    original: Optional[bool]

    
