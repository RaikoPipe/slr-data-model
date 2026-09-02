from typing import Optional

from pydantic import BaseModel, Field

from .annotation_helper import make_type_annotations
from .descriptive_enum import DescriptiveEnum


class VenueType(DescriptiveEnum):
    """Publication venue classification per §3.1 (Scimago quartiles at time of publication)."""
    JOURNAL_Q1 = "journal-q1", "Scimago Q1 journal at time of publication"
    JOURNAL_Q2 = "journal-q2", "Scimago Q2 journal at time of publication"
    JOURNAL_Q3 = "journal-q3", "Scimago Q3 journal at time of publication"
    JOURNAL_Q4 = "journal-q4", "Scimago Q4 journal at time of publication"
    CONFERENCE_PROCEEDINGS = "conference-proceedings", "Peer-reviewed conference proceedings"
    TIER_1_PREPRINT = "tier-1-preprint", "Tier 1 preprint with confirmed institutional affiliation"
    GREY_LITERATURE = "grey-literature", "Grey literature source"


class BibliographicMetadata(BaseModel):
    """Bibliographic metadata extracted from the source header/footer (Metadata-extraction directly from corpus dataset)."""
    doi: Optional[str] = Field(
        default=None,
        description="Digital Object Identifier as reported. NR if absent."
    )
    title: str = Field(
        description="Full title of the publication as reported."
    )
    authors: list[str] = Field(
        description="List of author names as reported, in publication order."
    )
    affiliations: list[str] = Field(
        description="Author affiliations as reported."
    )
    country: str = Field(
        description="Country of the corresponding author."
    )
    year: int = Field(
        description="Year of publication."
    )
    venue: str = Field(
        description="Journal, conference, or repository name as reported."
    )
    venue_type: VenueType = Field(
        description="Publication venue classification (Scimago quartile lookup for current year)."
        + make_type_annotations(VenueType)
    )
    language: str = Field(
        description="Language of publication (e.g., 'English', 'German')."
    )
    funding_source: Optional[str] = Field(
        default=None,
        description="Funding source as reported. NR if absent."
    )
    funding_description: Optional[str] = Field(
        default=None,
        description="Free-text elaboration of funding context: grant numbers, funder role, or statement of no funding, as reported."
    )
    self_authored_flag: bool = Field(
        description="Y if any review author appears in the author list."
    )