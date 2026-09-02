from pydantic import BaseModel, Field

from .annotation_helper import make_type_annotations
from .descriptive_enum import DescriptiveEnum


class ProvenanceTag(DescriptiveEnum):
    """Provenance tag for extracted fields per §8."""
    HUMAN = "H", "Human extracted"
    LLM_VERIFIED = "L-V", "LLM extracted, human verified"
    LLM_CORRECTED = "L-C", "LLM extracted, human corrected"
    DUAL = "D", "Dual-reviewer extraction"


class VerificationStatus(DescriptiveEnum):
    """Verification status of an LLM-prefilled field per §7."""
    VERIFIED = "verified", "Claim located in source and confirmed"
    CORRECTED = "corrected", "Value overwritten; original logged in llm_raw"
    UNVERIFIABLE = "unverifiable", "Could not be verified against source; escalate"


class ExtractionMetaData(BaseModel):
    """Provenance and verification metadata (§7, §8).

    All maps are keyed by field path relative to the study record
    (e.g., 'strategic_planning_scope.planning_horizon_tier').
    """
    provenance: dict[str, ProvenanceTag] = Field(
        default_factory=dict,
        description="Provenance tag per extracted field." + make_type_annotations(ProvenanceTag)
    )
    verification: dict[str, VerificationStatus] = Field(
        default_factory=dict,
        description="Verification status per LLM-prefilled field."
        + make_type_annotations(VerificationStatus)
    )
    llm_raw: dict[str, str] = Field(
        default_factory=dict,
        description="Original LLM-extracted value for fields where verification status is 'corrected'."
    )
    notes: dict[str, str] = Field(
        default_factory=dict,
        description="Free-text notes per field: uncertainty flags ('?' suffix per §6), contradictions, escalation reasoning (§10)."
    )