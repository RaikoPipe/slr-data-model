"""
SLR Data Model — v3.0 Extraction Schema

Pydantic models for LLM-based decision support for the strategic planning
horizon in manufacturing and logistics (SLR extraction schema, v3.0).

Tiers:
- Bibliographic metadata (LLM-extracted, R1 spot-checks 10%)
- Descriptive fields (LLM pre-fill, R1 verifies 100%)
- Interpretive fields (R1 manual, dual-verified by R2)
"""
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations

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

# Tier 3: Interpretive fields
from .gap_indicators import (
    GapIndicators,
    HITLType,
    DomainKnowledgeType,
    EvaluationFrameworkType,
)
from .quality_appraisal import QualityAppraisal

# Metadata (§7, §8)
from .provenance import ExtractionMetaData, ProvenanceTag, VerificationStatus

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
    # Gap indicators
    "GapIndicators",
    "HITLType",
    "DomainKnowledgeType",
    "EvaluationFrameworkType",
    # Quality appraisal
    "QualityAppraisal",
    # Provenance
    "ExtractionMetaData",
    "ProvenanceTag",
    "VerificationStatus",
    # Base
    "DescriptiveEnum",
    "make_type_annotations",
]