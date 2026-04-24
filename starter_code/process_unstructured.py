import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================


def _normalize_text(text: str) -> str:
    """Remove control noise and collapse whitespace into a readable string."""
    text = re.sub(r"HEADER_PAGE_\d+", " ", text or "")
    text = re.sub(r"FOOTER_PAGE_\d+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def process_pdf_data(raw_json: dict) -> dict:
    # Bước 1: Làm sạch nhiễu (Header/Footer) khỏi văn bản
    raw_text = raw_json.get("extractedText", "")
    cleaned_content = _normalize_text(raw_text)

    # Bước 2: Map dữ liệu thô sang định dạng chuẩn của UnifiedDocument
    return {
        "document_id": str(raw_json.get("docId", "")),
        "source_type": "PDF",
        "author": str(raw_json.get("authorName", "")).strip(),
        "category": str(raw_json.get("docCategory", "")).strip(),
        "content": cleaned_content,
        "timestamp": str(raw_json.get("createdAt", "")),
    }


def process_video_data(raw_json: dict) -> dict:
    # Map dữ liệu thô từ Video sang định dạng chuẩn (giống PDF)
    transcript = raw_json.get("transcript", "")
    cleaned_content = _normalize_text(transcript)

    return {
        "document_id": str(raw_json.get("video_id", "")),
        "source_type": "Video",
        "author": str(raw_json.get("creator_name", "")).strip(),
        "category": str(raw_json.get("category", "")).strip(),
        "content": cleaned_content,
        "timestamp": str(raw_json.get("published_timestamp", "")),
    }
