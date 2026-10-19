from typing import Optional

from pydantic import BaseModel, Field, computed_field, model_validator

from .annotation_helper import make_type_annotations
from .descriptive_enum import DescriptiveEnum


class ProvenanceTag(DescriptiveEnum):
    """Provenance tag for extracted fields per §8."""
    METADATA = "M", "Imported from search-stage metadata"
    HUMAN = "H", "Human extracted"
    LLM_VERIFIED = "L-V", "LLM extracted, human verified"
    LLM_CORRECTED = "L-C", "LLM extracted, human corrected"
    DUAL = "D", "Dual-reviewer extraction"


class ReviewerRole(DescriptiveEnum):
    """Reviewer roles per the extractor instructions."""
    R1 = "R1", "Primary researcher"
    R2 = "R2", "Fellow researcher"
    R3 = "R3", "Supervisor / adjudicator"


class VerificationStatus(DescriptiveEnum):
    """Verification status of an LLM-prefilled field per §7."""
    VERIFIED = "Y", "Claim located in source and confirmed"
    CORRECTED = "corrected", "Value overwritten; original logged in llm_raw"
    UNVERIFIABLE = "unverifiable", "Could not be verified against source; escalate"


class FieldVerdict(BaseModel):
    """One verifier's verdict on one field (§7). Interpretive fields carry blind R1 and R2 verdicts."""
    reviewer: ReviewerRole = Field(
        description="Verifier who recorded this verdict." + make_type_annotations(ReviewerRole)
    )
    status: VerificationStatus = Field(
        description="Verification outcome." + make_type_annotations(VerificationStatus)
    )
    corrected_value: Optional[str] = Field(
        default=None,
        description="The verifier's own value. Required if status is 'corrected', otherwise null."
    )
    reasoning: Optional[str] = Field(
        default=None,
        description="The verifier's own reasoning when correcting or flagging."
    )

    @model_validator(mode="after")
    def validate_corrected_value(self):
        """A corrected verdict must carry the verifier's own value."""
        corrected = self.status == VerificationStatus.CORRECTED
        if corrected and self.corrected_value is None:
            raise ValueError("corrected_value is required when status is 'corrected'")
        if not corrected and self.corrected_value is not None:
            raise ValueError("corrected_value must be null unless status is 'corrected'")
        return self


class ExtractionMetaData(BaseModel):
    """Provenance and verification metadata (§7, §8).

    All maps are keyed by field path relative to the study record
    (e.g., 'strategic_planning_scope.planning_horizon_tiers'); keys are checked against the real field paths
    on StudyExtraction, so typos are rejected (A8, v0.8.0 review).
    Per-field notes live in the record's `<field>_reasoning` columns (§4).
    """
    provenance: dict[str, ProvenanceTag] = Field(
        default_factory=dict,
        description="Provenance tag per extracted field." + make_type_annotations(ProvenanceTag)
    )
    verification: dict[str, list[FieldVerdict]] = Field(
        default_factory=dict,
        description="Verifier verdicts per LLM-prefilled field: one per verifier (R1 for descriptive fields; "
        "R1 and R2, recorded blind, for interpretive fields)."
    )
    llm_raw: dict[str, str] = Field(
        default_factory=dict,
        description="Original LLM-extracted value for fields that were corrected."
    )

    @computed_field(description="Verifier(s) per field, e.g. 'R1;R2' (§8). Derived from verification.")
    @property
    def verified_by(self) -> dict[str, str]:
        return {
            field: ";".join(dict.fromkeys(v.reviewer.value for v in verdicts))
            for field, verdicts in self.verification.items()
        }
