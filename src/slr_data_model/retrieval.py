from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum


class RetrievalSource(DescriptiveEnum):
    """Retrieval source per §3.7."""
    SCOPUS = "Scopus", "Retrieved via Scopus database search"
    WOS = "WoS", "Retrieved via Web of Science database search"
    OPENALEX = "OpenAlex", "Retrieved via OpenAlex search"
    SNOWBALLING = "snowballing", "Retrieved via backward/forward snowballing from anchor paper(s)"


class RetrievalTraceability(BaseModel):
    """Retrieval traceability (§3.7; LLM pre-fill; R1 verifies 100%)."""
    source: RetrievalSource = Field(
        description="Source the record was retrieved from." + make_type_annotations(RetrievalSource)
    )
    source_reasoning: str = reasoning_field()
    anchor_papers: list[str] = Field(
        default_factory=list,
        description="Anchor paper(s) (DOI or citation) the record was snowballed from. Required if source is "
        "'snowballing', otherwise empty."
    )

    @model_validator(mode="after")
    def validate_anchor_papers(self):
        """Anchor papers are required iff the source is snowballing."""
        snowballed = self.source == RetrievalSource.SNOWBALLING
        if snowballed and not self.anchor_papers:
            raise ValueError("anchor_papers is required when source is 'snowballing'")
        if not snowballed and self.anchor_papers:
            raise ValueError("anchor_papers must be empty unless source is 'snowballing'")
        return self
