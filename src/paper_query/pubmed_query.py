from typing import Any
import requests
import logging 
import time
import math
import xml.etree.ElementTree as ET

from .article_retriever import ArticleRetriever

logger = logging.getLogger(__name__)

PUBMED_DATABASE_LIST = [
    "pubmed",
    "protein",
    "nuccore",
    "ipg",
    "nucleotide",
    "structure",
    "genome",
    "annotinfo",
    "assembly",
    "bioproject",
    "biosample",
    "blastdbinfo",
    "books",
    "cdd",
    "clinvar",
    "gap",
    "gapplus",
    "grasp",
    "dbvar",
    "gene",
    "gds",
    "geoprofiles",
    "medgen",
    "mesh",
    "nlmcatalog",
    "omim",
    "orgtrack",
    "pmc",
    "proteinclusters",
    "pcassay",
    "protfam",
    "pccompound",
    "pcsubstance",
    "seqannot",
    "snp",
    "sra",
    "taxonomy",
    "biocollections",
    "gtr"
]
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def build_query_param(
    mindate: str | None = None,
    maxdate: str | None = None,
    datetype: str = "pdat",
) -> dict:
    mindate_dict = {} if mindate is None else {"mindate": mindate}
    maxdate_dict = {} if maxdate is None else {"maxdate": maxdate}
    datetype_dict = {} if mindate is None and maxdate is None \
        else {"datetype": datetype if datetype is not None else "pdat"}
    return {**mindate_dict, **maxdate_dict, **datetype_dict}

def safe_get(url, params, delay=0.4):
    time.sleep(delay)  # ~3 requests/second
    return requests.get(url, params=params)

def safe_int(s, default=0):
    try:
        return int(s)
    except (ValueError, TypeError):
        logger.error("Error ocurred in converting {s} to int")
        return default

def query_count(
    term: str,
    mindate: str | None = None,
    maxdate: str | None = None,
    datetype: str = "pdat",
) -> int:
    
    query_param = build_query_param(
        mindate=mindate,
        maxdate=maxdate,
        datetype=datetype,
    )
    params = {
        "term": term,
        "retmode": "json",
        "retmax": 0,
        **query_param,
    }
    dbs = ["pubmed"]
    for db in dbs:
        res = None
        try:
            result = safe_get(
                url=ESEARCH_URL,
                params={
                    **params,
                    "db": db,
                }
            )
            res: Any = result.json()
            cnt = safe_int(res['esearchresult']['count'], 0)
            return cnt
        except Exception as e:
            error_in_res = res['error'] if res and 'error' in res else 'unknown error'
            logger.error(f"Error occurred in querying {db}: str(e)\n Error: {error_in_res}")
            return 0
    return 0
    
STEP_COUNT = 100
def query_pmids(
    term: str,
    count: int,
    mindate: str | None = None,
    maxdate: str | None = None,
    datetype: str = "pdat",
):
    query_params = build_query_param(
        mindate=mindate,
        maxdate=maxdate,
        datetype=datetype
    )
    params = {
        "term": term,
        "retmode": "json",
        "retmax": STEP_COUNT,
        "db": "pubmed",
        **query_params,
    }
    for ix in range(math.ceil(count/STEP_COUNT)):
        ids = []
        try:
            result = safe_get(
                url=ESEARCH_URL,
                params= {
                    **params,
                    "retstart": ix*STEP_COUNT,
                }
            )
            res =result.json()
            ids = res['esearchresult']['idlist']
        except Exception as e:
            logger.error(str(e))
        for id in ids:
            yield id
    
def query_title_and_abstract(pmid: str):
    params = {
        "id": pmid,
        "db": "pubmed",
        "retmode": "xml"
    }
    try:
        result = safe_get(
            url=EFETCH_URL,
            params=params,
        )
        root = ET.fromstring(result.content)
        for article in root.findall(".//PubmedArticle"):
            title = article.findtext(".//ArticleTitle")
            abstract = article.findtext(".//Abstract/AbstractText")
            return title, abstract
        
        return None, None
    except Exception as e:
        logger.error(str(e))
        return None, None
    
def query_full_text(pmid: str) -> tuple[bool, str | None]:
    """
    Queries the full text of a paper by its PubMed ID (PMID).
    Args:
        pmid (str): The PubMed ID of the paper.
    Returns:
        tuple: A tuple containing a boolean indicating success and the full text content (html format) or None if not found.
    Raises:
        Exception: If there is an error during the request.
    """
    retriever = ArticleRetriever()
    res, html_content, _ =retriever.request_article(pmid)

    return res, html_content