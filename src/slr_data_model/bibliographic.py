from typing import Optional
from pydantic import BaseModel, Field
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations


class VenueType(DescriptiveEnum):
    Q1_Q2_JOURNAL = "q1-q2-journal", "Scimago or JCR Q1-Q2 journal at time of publication"
    Q3_Q4_JOURNAL = "q3-q4-journal", "Scimago or JCR Q3-Q4 journal at time of publication"
    CONFERENCE = "conference", "Peer-reviewed conference proceedings"
    PREPRINT = "preprint", "Tier 1 preprint with institutional affiliation"
    GREY_LITERATURE = "grey-literature", "Grey literature source"


class BibliographicMetadata(BaseModel):
    """Bibliographic metadata extracted from the source header/footer."""
    doi: Optional[str] = Field(default=None, description="Digital Object Identifier. NR if absent.")
    title: str = Field(description="Full title of the publication.")
    authors: list[str] = Field(description="List of author names as reported.")
    affiliations: list[str] = Field(description="Author affiliations as reported.")
    country: str = Field(description="Country of the corresponding author.")
    publication_year: int = Field(description="Year of publication.")
    venue: str = Field(description="Journal, conference, or repository name.")
    venue_type: VenueType = Field(
        description="Publication venue classification." + make_type_annotations(VenueType)
    )
    language: str = Field(description="Language of publication (e.g., 'English', 'German').")
    funding_source: Optional[str] = Field(default=None, description="Funding source as reported. NR if absent.")
    self_authored_flag: bool = Field(
        default=False,
        description="Y if any review author appears in author list."
    )
