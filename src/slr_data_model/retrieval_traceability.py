from typing import Optional
from pydantic import BaseModel, Field
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations


class SourceDatabase(DescriptiveEnum):
    """Database or method through which the record was retrieved."""
    SCOPUS = "Scopus", "Elsevier Scopus"
    WOS = "WoS", "Clarivate Web of Science Core Collection"
    OPENALEX = "OpenAlex", "OpenAlex"
    SNOWBALLING = "snowballing", "Retrieved via forward or backward snowballing"


class RetrievalTraceability(BaseModel):
    """Retrieval traceability for the source record."""
    source: SourceDatabase = Field(
        description="Database or method through which the record was retrieved." + make_type_annotations(SourceDatabase)
    )
    anchor_papers: list[str] = Field(
        default_factory=list,
        description="Anchor paper(s) if retrieved via snowballing. Empty if not applicable."
    )
