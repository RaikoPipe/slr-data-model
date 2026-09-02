from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations


QADimensionScore = Annotated[int, Field(ge=1, le=3)]


class QualityAppraisal(BaseModel):
    """Three-dimension quality appraisal rubric per §3.9.

    Each dimension scored 1-3 independently before summing. Composite range: 3-9.
    Sources scoring <= 4 are dual-verified by R2.
    """
    methodological_transparency: QADimensionScore = Field(
        description="Methodological transparency: 1 = method description insufficient to replicate; "
                    "2 = key steps described but gaps remain; 3 = fully replicable."
    )
    methodological_transparency_rationale: str = Field(
        description="Free-text justification for the methodological transparency score, citing the source."
    )
    empirical_grounding: QADimensionScore = Field(
        description="Empirical grounding: 1 = conceptual or framework-only; "
                    "2 = prototype or limited evaluation; 3 = implemented + quantitative evaluation."
    )
    empirical_grounding_rationale: str = Field(
        description="Free-text justification for the empirical grounding score, citing the source."
    )
    venue_tier_dimension: QADimensionScore = Field(
        description="Venue tier dimension: 1 = preprint; 2 = Q3-Q4 journal or conference; 3 = Q1-Q2 journal."
    )
    venue_tier_rationale: str = Field(
        description="Free-text justification for the venue tier score (venue name and Scimago quartile)."
    )
    composite_score: int = Field(
        default=0,
        description="Sum of the three dimension scores. Range 3-9. Auto-computed, do not supply.",
        exclude=True,
    )

    @model_validator(mode="after")
    def compute_composite(self):
        """Composite score must equal the sum of the three independently scored dimensions."""
        computed = self.methodological_transparency + self.empirical_grounding + self.venue_tier_dimension
        object.__setattr__(self, "composite_score", computed)
        return self

    @property
    def needs_dual_verification(self) -> bool:
        """Sources scoring <= 4 are dual-verified by R2 per §3.9."""
        return self.composite_score <= 4