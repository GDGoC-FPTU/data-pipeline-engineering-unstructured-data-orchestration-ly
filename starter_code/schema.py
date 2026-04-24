from pydantic import BaseModel, Field

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================


class UnifiedDocument(BaseModel):
    """
    Unified schema for both PDF and Video records.
    """

    document_id: str = Field(..., description="Unique identifier of the document")
    source_type: str = Field(..., description="Source type, e.g. PDF or Video")
    author: str = Field(..., description="Author or creator of the content")
    category: str = Field(..., description="Document category")
    content: str = Field(..., description="Normalized text content")
    timestamp: str = Field(..., description="Creation or publication timestamp")
