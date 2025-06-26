
from typing import Callable, Optional, TypedDict
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .common_step import sskindCommonStep
from .common_agent import CommonAgent
from .common_agent_2step import CommonAgentTwoSteps
from .agent_utils import IdentifyState, research_goal_dict

IDENTIFY_RELEVANCE_SYSTEM_PROMPT = ChatPromptTemplate.from_template("""
---

You are an expert in **biomedical research** and a skilled **data scientist**.

We are collecting data from published literature related to {research_goal}.
You will be provided with the **title** and **abstract** of a scientific paper.

Your task is to determine whether the paper is **relevant** to our research focus.

---

### **Input**

**Title:**
{title}

**Abstract:**
{abstract}

---

### **Output**

Please answer the following question:
**Is this paper relevant to research on Alzheimer's disease and single-cell RNA sequencing?**

Respond in the following format:

**FinalAnswer**: [Yes / No]
""")

class IdentifyRelevanceResult(BaseModel):
    reasoning_process: Optional[str] = Field(
        description="The reasoning process used to determine relevance."
    )
    relevant: bool = Field(
        description="Indicates whether the paper is relevant to the research topic."
    )

class IdentifyRelevanceStep(sskindCommonStep):
    """
    This class is a placeholder for the identify step functionality.
    It is currently empty and can be extended in the future.
    """
    def __init__(
        self, 
        llm: BaseChatOpenAI,
        two_steps_agent: bool = False,
    ):
        super().__init__(llm)
        self.llm = llm
        self.step_name = "Identify Relevance Step"
        self.two_steps_agent = two_steps_agent

    def _execute_directly(self, state: dict) -> tuple[dict | None, dict[str, int] | None]:
        typed_state: IdentifyState = IdentifyState(**state)
        research_goal_enum = typed_state.get("research_goal")
        research_goal = research_goal_dict[research_goal_enum]
        title = typed_state.get("title")
        abstract = typed_state.get("abstract")

        agent = CommonAgent(self.llm) if not self.two_steps_agent else CommonAgentTwoSteps(self.llm)
        system_prompt = IDENTIFY_RELEVANCE_SYSTEM_PROMPT.format(
            research_goal=research_goal,
            title=title, 
            abstract=abstract
        )
        res, _, token_usage, reasoning_process = agent.go(
            system_prompt=system_prompt,
            instruction_prompt="Before jumping to final answer, you need to explain **the reasoning process** first.\nNow, let's identify the relevance of this paper.",
            schema=IdentifyRelevanceResult,
        )
        typed_state["relevant"] = res.relevant
        self._print_step(
            typed_state,
            step_output=res.reasoning_process if reasoning_process is None else reasoning_process,
        )

        return dict(typed_state), token_usage
