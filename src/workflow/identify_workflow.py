
from typing import Callable, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai.chat_models.base import BaseChatOpenAI

from ..paper_query.pubmed_query import (
    query_title_and_abstract,
    query_full_text,
)
from ..agents.identify_step import (
    IdentifyRelevanceStep,
    IdentifyOriginalDataStep,
)
from ..agents.agent_utils import IdentifyState, ResearchGoalEnum

from .workflow_utils import convert_html_to_plaintext

class IdentifyWorkflow:
    def __init__(
        self, 
        llm: BaseChatOpenAI, 
        step_callback: Optional[Callable] = None
    ):
        self.llm = llm
        self.steps = []
        self.step_callback = step_callback

    def compile(self):
        """
        compile the identify workflow
        """
        self.steps.append(
            IdentifyRelevanceStep(
                llm=self.llm,
            )
        )
        self.steps.append(
            IdentifyOriginalDataStep(
                llm=self.llm,
            )
        )
        def check_relevance(state: IdentifyState) -> bool:
            relevance = state.get("relevant", None)
            if relevance is None:
                return False
            return relevance
        
        graph = StateGraph(IdentifyState)
        graph.add_node("identify_relevance", self.steps[0].execute)
        graph.add_node("identify_original_data", self.steps[1].execute)
        graph.add_edge(START, "identify_relevance")
        graph.add_conditional_edges("identify_relevance", check_relevance, {
            True: "identify_original_data", False: END
        })
        graph.add_edge("identify_original_data", END)

        self.graph = graph.compile()

    def identify(self, pmid: str, research_goal: ResearchGoalEnum) -> bool:
        """
        Identify the relevance and original data of a paper by its PubMed ID (PMID).
        Args:
            pmid (str): The PubMed ID of the paper.
        Returns:
            IdentifyState: The state containing the results of the identification process.
        """
        title, abstract = query_title_and_abstract(pmid)
        if not title or not abstract:
            return False
        res, html_content = query_full_text(pmid)
        if not res or not html_content:
            return False
        full_text = convert_html_to_plaintext(html_content)
        if not full_text:
            return False

        state = IdentifyState(
            research_goal=research_goal,
            title=title,
            abstract=abstract,
            content=full_text,
            step_output_callback=self.step_callback,
            relevant=None,
            original=None
        )

        s = None
        for s in self.graph.stream(
            input=state,
            stream_mode="values",
            config={"recursion_limit": 100},
        ):
            print(s)
        
        if s is None:
            return False
        return s.get("relevant", False) and s.get("original", False)

        