import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def detect_pdf_type(path: str, max_pages: int = 5) -> dict:
    pages_checked = 0
    pages_with_text = 0

    with fitz.open(path) as doc:
        for page in doc:
            if pages_checked >= max_pages:
                break

            text = page.get_text().strip()
            pages_checked += 1

            if len(text) > 50:  # threshold to avoid noise 
                pages_with_text += 1

    if pages_checked == 0:
        logger.warning("No readable pages found in PDF: %s", path)
        return {"pdf_type": "scanned", "confidence": 0.0}

    ratio = pages_with_text / pages_checked
    pdf_type = "digital" if ratio >= 0.5 else "scanned"

    logger.info(
        "PDF classified as %s with confidence %.2f (%d/%d pages contained text)",
        pdf_type,
        ratio,
        pages_with_text,
        pages_checked,
    )

    return {
        "pdf_type": pdf_type,
        "confidence": round(ratio, 2),
    }
