"""
SLR Data Model — v5.0 Extraction Schema

Pydantic models for LLM-based decision support for the strategic planning
horizon in manufacturing and logistics (SLR extraction schema, v5.0).

Tiers:
- Bibliographic metadata (imported from search-stage records, R1 spot-checks 10%)
- Descriptive fields (LLM pre-fill, R1 verifies 100%)
- Interpretive fields (LLM-extracted, R1 + R2 each verify 100%, blind)
"""
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations, reasoning_field

# Tier 1: Bibliographic metadata
from .bibliographic import BibliographicMetadata, VenueType

# Tier 2: Descriptive fields
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
    ArchitecturalPatternType,
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
from .retrieval import RetrievalTraceability, RetrievalSource

# Tier 3: Interpretive fields
from .gap_indicators import (
    GapIndicators,
    HITLType,
    DomainKnowledgeType,
    EvaluationFrameworkType,
)
from .quality_appraisal import (
    QualityAppraisal,
    AppraisalAnswer,
    StudyTypeCategory,
    CATEGORY_BY_VALIDATION_STATUS,
)

# Metadata (§7, §8)
from .provenance import ExtractionMetaData, ProvenanceTag, ReviewerRole, VerificationStatus, FieldVerdict

# Top-level record
from .study_extraction import StudyExtraction

__all__ = [
    # Top-level extraction model
    "StudyExtraction",
    # Bibliographic
    "BibliographicMetadata",
    "VenueType",
    # Study characterization
    "StudyCharacterization",
    "ResearchType",
    "ValidationStatusType",
    # Strategic planning
    "StrategicPlanningScope",
    "SubdomainType",
    "PlanningTaskType",
    "PlanningHorizonTier",
    "TheoreticalFrameworkType",
    # LLM intervention
    "LLMIntervention",
    "ModelFamilyType",
    "OpenWeightType",
    "FineTuningType",
    "ArchitecturalPatternType",
    "AgenticArchitectureType",
    "IntegrationType",
    # OR substrate
    "ORSubstrate",
    "FormalizationLevel",
    # Evaluation
    "EvaluationAndOutcomes",
    "ReportedMetric",
    "ComparatorType",
    "StudyDesignType",
    # Retrieval traceability
    "RetrievalTraceability",
    "RetrievalSource",
    # Gap indicators
    "GapIndicators",
    "HITLType",
    "DomainKnowledgeType",
    "EvaluationFrameworkType",
    # Quality appraisal
    "QualityAppraisal",
    "AppraisalAnswer",
    "StudyTypeCategory",
    "CATEGORY_BY_VALIDATION_STATUS",
    # Provenance
    "ExtractionMetaData",
    "ProvenanceTag",
    "ReviewerRole",
    "VerificationStatus",
    "FieldVerdict",
    # Base
    "DescriptiveEnum",
    "make_type_annotations",
    "reasoning_field",
]