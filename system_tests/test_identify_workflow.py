import pytest

from src.agents.agent_utils import ResearchGoalEnum
from src.workflow.identify_workflow import IdentifyWorkflow

# @pytest.mark.skip()
def test_IdentifyWorkflow(llm, step_callback):
    # Initialize the IdentifyWorkflow with a mock LLM and step callback
    workflow = IdentifyWorkflow(llm=llm, step_callback=step_callback)
    
    # Compile the workflow
    workflow.compile()
    
    # Define a sample PMID and research goal
    pmid = "40166175" # "39641382" # "39951525" # "38987616"
    research_goal = ResearchGoalEnum.ALZHEIMERS
    
    # Execute the identify method
    result = workflow.identify(pmid=pmid, research_goal=research_goal)
    
    # Check if the result is a boolean indicating relevance
    assert isinstance(result, bool)

@pytest.mark.skip()
def test_IdentifyWorkflow_on_spatial(llm, step_callback):
    # Initialize the IdentifyWorkflow with a mock LLM and step callback
    workflow = IdentifyWorkflow(llm=llm, step_callback=step_callback)
    
    # Compile the workflow
    workflow.compile()
    
    # Define a sample PMID and research goal
    pmid = "40462993" # "39641382" # "39951525" # "38987616"
    research_goal = ResearchGoalEnum.SPATIAL
    
    # Execute the identify method
    result = workflow.identify(pmid=pmid, research_goal=research_goal)
    
    # Check if the result is a boolean indicating relevance
    assert isinstance(result, bool)