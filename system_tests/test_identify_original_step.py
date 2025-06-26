
import pytest
import logging
from src.agents.identify_relevant_step import IdentifyRelevanceStep
from src.agents.identify_original_step import IdentifyOriginalDataStep
from src.agents.agent_utils import IdentifyState, ResearchGoalEnum
from src.paper_query.pubmed_query import query_title_and_abstract
from src.workflow.workflow_utils import obtain_full_text

logger = logging.getLogger(__name__)

@pytest.mark.skip()
def test_IdentifyOriginalDataStep(llm, step_callback):
    # pmid = "38987616"
    full_text = ""
    with open("system_tests/data/38987616.txt", "r") as f:
        full_text = f.read()
    state = {
        "research_goal": ResearchGoalEnum.ALZHEIMERS,
        "title": "'Single cell transcriptomes and multiscale networks from persons with and without Alzheimer’s disease'",
        "content": full_text,
        "step_output_callback": step_callback,
    }
    
    # Initialize the IdentifyOriginalDataStep with a mock LLM
    step = IdentifyOriginalDataStep(llm)
    
    # Execute the step
    result_state: dict | None = step.execute(state)
    assert result_state is not None
    
    # Check if the result contains the expected keys
    assert "original" in result_state
    assert isinstance(result_state["original"], bool)  # Should be a boolean value indicating original data availability

def test_IdentifyOriginalDataStep_on_no_fulltext_paper(llm, step_callback):
    # Test with empty content
    pmid = "40448997"
    title, abstract = query_title_and_abstract(pmid)
    full_text = obtain_full_text(pmid)
    state = {
        "research_goal": ResearchGoalEnum.ALZHEIMERS,
        "title": title,
        "abstract": abstract,
        "content": full_text,
        "step_output_callback": step_callback,
    }
    
    # Initialize the IdentifyOriginalDataStep with a mock LLM
    step = IdentifyOriginalDataStep(llm, two_steps_agent=True)
    
    # Execute the step
    result_state: dict | None = step.execute(state)
    assert result_state is not None
    
    # Check if the result contains the expected keys
    assert "original" in result_state
    assert isinstance(result_state["original"], bool)  # Should be a boolean value indicating original data availability
    logger.info(f"PMID: {pmid}, Original Data Available: {result_state['original']}")