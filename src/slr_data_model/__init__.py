"""
SLR Data Model — v5.0 Extraction Schema (schema version 0.9.0)

Pydantic models for LLM-based decision support for the strategic planning
horizon in manufacturing and logistics (SLR extraction schema, v5.0).

Tiers:
- Bibliographic metadata (imported from search-stage records, R1 spot-checks 10%)
- Descriptive fields (LLM pre-fill, R1 verifies 100%)
- Interpretive fields (LLM-extracted, R1 + R2 each verify 100%, blind)
"""
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations, reasoning_field
from .common import NR, NotReported, ReportedStr, UniqueList, YesNoUnclear

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
    SCPProcess,
    VDI5200Phase,
    TASK_SUBDOMAINS,
)
from .llm_intervention import (
    LLMIntervention,
    ModelFamilyType,
    OpenWeightType,
    FineTuningType,
    AgenticArchitectureType,
    IntegrationType,
    DeploymentType,
    ModalityType,
    PromptingTechnique,
    WorkflowPattern,
    AgentMemory,
)
from .or_substrate import ORSubstrate, FormalizationLevel, OptimizationParadigm, LLMORRole
from .evaluation import (
    EvaluationAndOutcomes,
    ReportedMetric,
    ComparatorType,
    StudyDesignType,
    EvaluationParadigm,
)
from .retrieval import RetrievalTraceability, RetrievalSource

# Tier 3: Interpretive fields
from .gap_indicators import (
    GapIndicators,
    HITLType,
    DomainKnowledgeType,
    EvaluationFrameworkType,
    KGModel,
    KGConstruction,
    KGUsage,
    AutomationStage,
    DecisionAutonomy,
)
from .quality_appraisal import (
    QualityAppraisal,
    PromptDisclosure,
    AppraisalAnswer,
    StudyTypeCategory,
    CATEGORY_BY_VALIDATION_STATUS,
)

# Metadata (§7, §8)
from .provenance import ExtractionMetaData, ProvenanceTag, ReviewerRole, VerificationStatus, FieldVerdict

# Top-level record
from .study_extraction import StudyExtraction, SCHEMA_VERSION, strict_json_schema

__all__ = [
    # Top-level extraction model
    "StudyExtraction",
    "SCHEMA_VERSION",
    "strict_json_schema",
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
    "SCPProcess",
    "VDI5200Phase",
    "TASK_SUBDOMAINS",
    # LLM intervention
    "LLMIntervention",
    "ModelFamilyType",
    "OpenWeightType",
    "FineTuningType",
    "AgenticArchitectureType",
    "IntegrationType",
    "DeploymentType",
    "ModalityType",
    "PromptingTechnique",
    "WorkflowPattern",
    "AgentMemory",
    # OR substrate
    "ORSubstrate",
    "FormalizationLevel",
    "OptimizationParadigm",
    "LLMORRole",
    # Evaluation
    "EvaluationAndOutcomes",
    "ReportedMetric",
    "ComparatorType",
    "StudyDesignType",
    "EvaluationParadigm",
    # Retrieval traceability
    "RetrievalTraceability",
    "RetrievalSource",
    # Gap indicators
    "GapIndicators",
    "HITLType",
    "DomainKnowledgeType",
    "EvaluationFrameworkType",
    "KGModel",
    "KGConstruction",
    "KGUsage",
    "AutomationStage",
    "DecisionAutonomy",
    # Quality appraisal
    "QualityAppraisal",
    "PromptDisclosure",
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
    "NR",
    "NotReported",
    "ReportedStr",
    "UniqueList",
    "YesNoUnclear",
]