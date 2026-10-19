from pydantic import BaseModel, Field, computed_field

from .bibliographic import BibliographicMetadata, VenueType
from .study_characterization import StudyCharacterization, ResearchType, ValidationStatusType
from .strategic_planning import (
    StrategicPlanningScope,
    SubdomainType,
    PlanningTaskType,
    PlanningHorizonTier,
    TheoreticalFrameworkType,
)
from .llm_intervention import (
    LLMIntervention,
    ModelFamilyType,
    OpenWeightType,
    FineTuningType,
    AgenticArchitectureType,
    IntegrationType,
)
from .or_substrate import ORSubstrate, FormalizationLevel
from .evaluation import (
    EvaluationAndOutcomes,
    ReportedMetric,
    ComparatorType,
    StudyDesignType,
)
from .gap_indicators import (
    GapIndicators,
    HITLType,
    DomainKnowledgeType,
    EvaluationFrameworkType,
)
from .quality_appraisal import QualityAppraisal, StudyTypeCategory, CATEGORY_BY_VALIDATION_STATUS
from .retrieval import RetrievalTraceability
from .provenance import ExtractionMetaData, ProvenanceTag, VerificationStatus


class StudyExtraction(BaseModel):
    """Top-level study extraction record aligned with the v5.0 extractor instructions.

    Composes all field groups into a single study-level record.
    """
    study_id: str = Field(
        description="Unique identifier for the study within the review (e.g., OSF record ID)."
    )
    bibliographic_metadata: BibliographicMetadata = Field(
        description="Bibliographic metadata (imported from search-stage records, R1 spot-checks 10%; not LLM-extracted)."
    )
    study_characterization: StudyCharacterization = Field(
        description="Study characterization (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    strategic_planning_scope: StrategicPlanningScope = Field(
        description="Strategic planning scope (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    llm_intervention: LLMIntervention = Field(
        description="LLM/AI intervention details (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    or_substrate: ORSubstrate = Field(
        description="OR/optimization substrate (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    evaluation_and_outcomes: EvaluationAndOutcomes = Field(
        description="Evaluation and outcomes (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    retrieval_traceability: RetrievalTraceability = Field(
        description="Retrieval traceability (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    gap_indicators: GapIndicators = Field(
        description="Gap indicators (interpretive: LLM-extracted, R1 + R2 each verify 100%, blind)."
    )
    quality_appraisal: QualityAppraisal = Field(
        description="Quality appraisal (interpretive: LLM-extracted, R1 + R2 each verify 100%, blind)."
    )
    extraction_metadata: ExtractionMetaData = Field(
        description="Provenance and verification metadata (§7, §8)."
    )

    @computed_field(description="§3.9 study-type category, derived from validation status. Auto-computed, do not supply.")
    @property
    def study_type_category(self) -> StudyTypeCategory:
        return CATEGORY_BY_VALIDATION_STATUS[self.study_characterization.validation_status]
