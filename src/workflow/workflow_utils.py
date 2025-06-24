
import logging

from ..paper_query.html_extractor import HtmlTableExtractor

logger = logging.getLogger(__name__)

def convert_html_to_plaintext(html: str) -> str | None:
    """
    Converts HTML content to plain text by removing HTML tags and decoding HTML entities.
    Args:
        html (str): The HTML content to convert.
    Returns:
        str: The plain text content.
    """
    try:
        extractor = HtmlTableExtractor()
        sections = extractor.extract_sections(html)
        if sections is None:
            return None
        return "\n".join([sec["section"].strip() + "\n" + sec["content"].strip() \
                          for sec in sections])
    except Exception as e:
        logger.error(f"Error converting HTML to plaintext: {e}")
        return None  # Return original HTML if conversion fails