from pydantic import BaseModel, Field
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations


class StudyTypeCategory(DescriptiveEnum):
    """Study-type categories for conditional quality appraisal."""
    A = "A", "Empirical: primary data collection with a defined evaluation protocol"
    B = "B", "Prototype/Design Science: implemented system demonstrated on illustrative cases without controlled evaluation"
    C = "C", "Conceptual/Framework only: architectures, taxonomies, or frameworks without implementation or empirical evaluation"


class QAScore(DescriptiveEnum):
    """Quality appraisal item score."""
    YES = "Yes", "Criterion fully met"
    PARTIALLY = "Partially", "Criterion partially met"
    NO = "No", "Criterion not met"


class VenueTier(DescriptiveEnum):
    """Venue quality tier for quality appraisal."""
    Q1_Q2_JOURNAL = "Q1-Q2-journal", "Scimago or JCR Q1-Q2 journal at time of publication"
    Q3_Q4_CONFERENCE = "Q3-Q4-conference", "Q3-Q4 journal or peer-reviewed conference proceedings"
    PREPRINT = "preprint", "Tier 1 preprint with institutional affiliation, no peer review"


class ExtractionProvenance(DescriptiveEnum):
    """Provenance tag for extracted fields."""
    HUMAN = "H", "Human extracted"
    LLM_VERIFIED = "L-V", "LLM extracted, human verified"
    LLM_CORRECTED = "L-C", "LLM extracted, human corrected"
    DUAL = "D", "Dual-reviewer extraction"


class QualityAppraisal(BaseModel):
    """Quality appraisal per the OSF prereg 4-item checklist."""
    study_type_category: StudyTypeCategory = Field(
        description="Study-type category determining conditional Q2 interpretation." + make_type_annotations(StudyTypeCategory)
    )
    q1_methodological_transparency: QAScore = Field(
        description="Q1: Is the method described with sufficient detail for independent replication?" + make_type_annotations(QAScore)
    )
    q2_empirical_grounding: QAScore = Field(
        description="Q2: Empirical or demonstration grounding. Interpreted conditionally by study type: "
                    "A: metrics defined and results reported with context; "
                    "B: artifact demonstrated on a case exercising core claims; "
                    "C: argumentation internally consistent and traceable." + make_type_annotations(QAScore)
    )
    q3_validity_limitation: QAScore = Field(
        description="Q3: Are boundaries of the contribution explicitly discussed (failure modes, scalability, external validity, domain assumptions)?" + make_type_annotations(QAScore)
    )
    q4_positioning: QAScore = Field(
        description="Q4: Is the contribution compared against existing solutions with explicit differentiation?" + make_type_annotations(QAScore)
    )
    venue_tier: VenueTier = Field(
        description="Venue quality tier." + make_type_annotations(VenueTier)
    )
    extraction_provenance: ExtractionProvenance = Field(
        description="Provenance of the extraction." + make_type_annotations(ExtractionProvenance)
    )
