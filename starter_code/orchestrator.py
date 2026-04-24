import os
import json
import glob

# Import các thành phần
from schema import UnifiedDocument
from process_unstructured import process_pdf_data, process_video_data
from quality_check import run_semantic_checks

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, "..", "raw_data")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "processed_knowledge_base.json")


def _serialize_document(document: UnifiedDocument) -> dict:
    if hasattr(document, "model_dump"):
        return document.model_dump()
    return document.dict()


def run_pipeline():
    final_kb = []

    # Xử lý Group A (PDFs)
    pdf_files = sorted(glob.glob(os.path.join(RAW_DATA_DIR, "group_a_pdfs", "*.json")))
    for file_path in pdf_files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        processed = process_pdf_data(raw_data)
        if run_semantic_checks(processed):
            final_kb.append(_serialize_document(UnifiedDocument(**processed)))

    # Xử lý Group B (Videos)
    video_files = sorted(glob.glob(os.path.join(RAW_DATA_DIR, "group_b_videos", "*.json")))
    for file_path in video_files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        processed = process_video_data(raw_data)
        if run_semantic_checks(processed):
            final_kb.append(_serialize_document(UnifiedDocument(**processed)))

    # Lưu kết quả
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_kb, f, indent=4, ensure_ascii=False)
        print(f"Pipeline finished! Saved {len(final_kb)} records.")


if __name__ == "__main__":
    run_pipeline()
