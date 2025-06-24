import argparse
import os
from typing import Optional
from dotenv import load_dotenv
import logging

from langchain_openai.chat_models import AzureChatOpenAI

from src.agents.agent_utils import ResearchGoalEnum, increase_token_usage
from src.agents.constants import DEFAULT_TOKEN_USAGE

from src.paper_query.pubmed_query import (
    query_count,
    query_pmids,
)
from src.workflow.identify_workflow import IdentifyWorkflow
from src.log_utils import initialize_logger

load_dotenv()

logger = initialize_logger(
    log_file="app.log",
    app_log_name="app_logger",
    app_log_level=logging.INFO,
    log_entries={
        "src": logging.INFO,
    }
)

def get_azure_openai():
    return AzureChatOpenAI(
        api_key=os.environ.get("OPENAI_4O_API_KEY", None),
        azure_endpoint=os.environ.get("AZURE_OPENAI_4O_ENDPOINT", None),
        api_version=os.environ.get("OPENAI_4O_API_VERSION", None),
        azure_deployment=os.environ.get("OPENAI_4O_DEPLOYMENT_NAME", None),
        model=os.environ.get("OPENAI_4O_MODEL", None),
        max_retries=5,
        # temperature=0.0,
        max_completion_tokens=int(os.environ.get("OPENAI_MAX_OUTPUT_TOKENS", 4096)),
    )

def output_info(msg: str):
    logger.info(msg)

g_token_usage = {**DEFAULT_TOKEN_USAGE}
def output_step(
    step_name: Optional[str] = None,
    step_description: Optional[str] = None,
    step_output: Optional[str] = None,
    step_reasoning_process: Optional[str] = None,
    token_usage: Optional[dict] = None,
):
    global g_token_usage
    if step_name is not None:
        output_info("=" * 64)
        output_info(step_name)
    if step_description is not None:
        output_info(step_description)
    if token_usage is not None:
        usage_str = f"step total tokens: {token_usage['total_tokens']}, step prompt tokens: {token_usage['prompt_tokens']}, step completion tokens: {token_usage['completion_tokens']}"
        output_info(usage_str)
        g_token_usage = increase_token_usage(g_token_usage, token_usage)
        usage_str = f"overall total tokens: {g_token_usage['total_tokens']}, overall prompt tokens: {g_token_usage['prompt_tokens']}, overall completion tokens: {g_token_usage['completion_tokens']}"
        output_info(usage_str)
    if step_reasoning_process is not None:
        output_info(f"\n\n{step_reasoning_process}\n\n")
    if step_output is not None:
        output_info(step_output)

def main_alzheimers():
    query = '(Alzheimer AND ("single cell" OR "single nucleus" OR "single-cell")) AND ("RNA sequencing" OR "RNA-seq" OR "single-cell RNA-seq")'
    mindate = "2024/06/01"
    maxdate = "2025/06/01"
    count = query_count(query, mindate, maxdate)
    logger.info(f"Total articles found: {count}")
    pmids = query_pmids(query, count, mindate, maxdate)
    wf = IdentifyWorkflow(
        llm=get_azure_openai(),
        step_callback=output_step,
    )
    wf.compile()
    valid_pmids = []
    for pmid in pmids:
        logger.info(f"PMID: {pmid}")
        valid = wf.identify(
            pmid=pmid,
            research_goal=ResearchGoalEnum.ALZHEIMERS,
        )
        if valid:
            valid_pmids.append(pmid)
            logger.info(f"PMID {pmid} is relevant to Alzheimer's disease and single-cell RNA sequencing.")
        else:
            logger.info(f"PMID {pmid} is NOT relevant to Alzheimer's disease and single-cell RNA sequencing.")
    
    logger.info(f"Total relevant PMIDs: {len(valid_pmids)}")
    logger.info(f"Relevant PMIDs: {valid_pmids}")

    return valid_pmids

    


def main():
    main_alzheimers()

if __name__ == "__main__":
    main()
