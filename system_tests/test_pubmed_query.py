
import pytest
import logging
from src.paper_query.pubmed_query import (
    query_count, 
    query_pmids, 
    query_title_and_abstract, 
    query_full_text,
)

logger = logging.getLogger(__name__)

@pytest.mark.skip()
def test_query_count():
    query = "(Alzheimer[ti] OR Alzheimer[ab]) AND (single[ab] OR single[ti]) AND (RNA OR RNA-seq OR snRNA OR scRNA)"
    cnt = query_count(
        query,
        mindate="2024/06/01",
        maxdate="2025/06/01",
        datetype="pdat",
    )
    print(cnt)

# @pytest.mark.skip()
def test_query_pmids():
    # query = "Alzheimer[ti] OR Alzheimer[ab]"
    query = "(Alzheimer[ti] OR Alzheimer[ab]) AND (single[ab] OR single[ti]) AND (RNA OR RNA-seq OR snRNA OR scRNA)"
    pmid_cnt = query_count(
        query,
        mindate="2024/06/01",
        maxdate="2025/06/01",
        datetype="pdat",
    )
    ids = query_pmids(
        query,
        pmid_cnt,
        mindate="2024/06/01",
        maxdate="2025/06/01",
        datetype="pdat",
    )
    pmids = list(ids)
    for id in pmids:
        logger.info(id)
    assert pmids is not None and len(pmids) > 0

@pytest.mark.skip()
def test_query_title_and_abstract():
    pmid = "40546497"
    title, abstract = query_title_and_abstract(pmid)
    logger.info(title)
    logger.info(abstract)
    assert title is not None
    assert abstract is not None

@pytest.mark.skip()
def test_full_text():
    pmid = "40546497"
    res, full_text = query_full_text(pmid)
    assert res
    assert full_text is not None