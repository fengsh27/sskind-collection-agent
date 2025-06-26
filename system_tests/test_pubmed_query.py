
import pytest
import logging
from src.paper_query.pubmed_query import (
    query_count, 
    query_pmids, 
    query_title_and_abstract, 
    query_full_text,
)
from src.paper_query.html_extractor import HtmlTableExtractor

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

@pytest.mark.skip()
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
    pmid = "38987616"
    title, abstract = query_title_and_abstract(pmid)
    logger.info(title)
    logger.info(abstract)
    assert title is not None
    assert abstract is not None

# @pytest.mark.skip()
def test_full_text():
    pmid = "16143486" # "38987616"
    res, html_content = query_full_text(pmid)
    assert res
    assert html_content is not None

    extractor = HtmlTableExtractor()
    title = extractor.extract_title(html_content)
    assert title is not None and len(title) > 0
    tables = extractor.extract_tables(html_content)
    assert tables is not None
    assert len(tables) > 0

    sections = extractor.extract_sections(html_content)
    assert sections is not None
   
    full_text = "\n".join([sec["section"] + "\n" + sec["content"] for sec in sections])
    assert full_text is not None and len(full_text) > 0
    

@pytest.mark.skip()
def test_query_statement_with_query_count():
    query = '(Alzheimer AND ("single cell" OR "single nucleus" OR "single-cell")) AND ("RNA sequencing" OR "RNA-seq" OR "single-cell RNA-seq")'
    cnt = query_count(
        query,
        mindate="2024/06/01",
        maxdate="2025/06/01",
        datetype="pdat",
    )
    print(cnt)
    logger.info(f'{query} count: {cnt}')