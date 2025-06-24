
import pytest

from src.agents.identify_step import IdentifyRelevanceStep, IdentifyOriginalDataStep
from src.agents.agent_utils import IdentifyState, ResearchGoalEnum

@pytest.mark.skip()
def test_IdentifyRelevanceStep(llm, step_callback):
    # Create a mock state with title and abstract
    state = {
        "research_goal": ResearchGoalEnum.ALZHEIMERS,
        "title": "Single cell transcriptomes and multiscale networks from persons with and without Alzheimer's disease",
        "abstract": "The emergence of single nucleus RNA sequencing (snRNA-seq) offers to revolutionize the study of Alzheimer's disease (AD). Integration with complementary multiomics data such as genetics, proteomics and clinical data provides powerful opportunities to link cell subpopulations and molecular networks with a broader disease-relevant context. We report snRNA-seq profiles from superior frontal gyrus samples from 101 well characterized subjects from the Banner Brain and Body Donation Program in combination with whole genome sequences. We report findings that link common AD risk variants with CR1 expression in oligodendrocytes as well as alterations in hematological parameters. We observed an AD-associated CD83(+) microglial subtype with unique molecular networks and which is associated with immunoglobulin IgG4 production in the transverse colon. Our major observations were replicated in two additional, independent snRNA-seq data sets. These findings illustrate the power of multi-tissue molecular profiling to contextualize snRNA-seq brain transcriptomics and reveal disease biology.",
        "step_output_callback": step_callback,
    }
    
    # Initialize the IdentifyRelevanceStep with a mock LLM
    step = IdentifyRelevanceStep(llm)
    
    # Execute the step
    result_state: dict | None = step.execute(state)
    assert result_state is not None
    
    # Check if the result contains the expected keys
    assert "final_answer" in result_state
    assert isinstance(result_state["final_answer"], bool)  # Should be a boolean value indicating relevance


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
    assert "final_answer" in result_state
    assert isinstance(result_state["final_answer"], bool)  # Should be a boolean value indicating original data availability