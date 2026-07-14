"""
AI System Data Model

This module provides Pydantic models for representing AI systems,
including their architecture, capabilities, and validation methods.
Aligned with the OSF preregistration extraction schema.
"""
from .descriptive_enum import DescriptiveEnum
from .context_engineering import ContextEngineering
from .ai_system import (
    AISystem,
    StudyExtraction,
    StudyCharacterization,
    LLMIntervention,
    SystemArchitecture,
    AIAgent,
    GenAIModel,
    ToolUse,
    TriggerType,
    FinetuningDatasetType,
    FinetuningMethodType,
    ModelFamilyType,
    OpenWeightType,
    ArchitecturalPatternType,
    AgenticArchitectureType,
    IntegrationType,
    ResearchType,
    ValidationStatusType,
    MultiAgentCoordinationStrategy,
    Orchestration,
    HumanIntegration,
    HumanOversightType,
    OrchestrationPatternType,
    CPSIntegrationType,
    ResearchMaturityType,
    ResearchMethodologyType,
    EvaluationMetricType,
    IndustryParadigmType,
    ScalabilityAssessmentType,
    FeedbackAndLearningType,
    InteractionModalityType,
)
from .context_engineering import (
    ContextEngineering,
    MemoryType,
    MemoryScopeType,
    RetrievalStrategyType,
    PromptEngineeringTechniquesType,
)
from .ai_system_types import (
    ParadigmType,
    AgentRoleType,
    ModalityType,
    ExternalToolsType,
    AgentCollaborationType,
    OrganizationalStructureType,
)
from .validation import (
    ValidationMethodType,
    EvaluationAndOutcomes,
    ReportedOutcomes,
    StudyDesignType,
    ComparatorType,
    FailureAttributionType,
)
from .domain import DomainType
from .bibliographic import BibliographicMetadata, VenueType
from .strategic_planning import (
    StrategicPlanningScope,
    SubdomainType,
    PlanningTaskType,
    PlanningHorizonTier,
    TheoreticalFrameworkType,
)
from .or_substrate import ORSubstrate, FormalizationLevel
from .gap_indicators import (
    GapIndicators,
    HITLType,
    DomainKnowledgeType,
    EvaluationFrameworkType,
)
from .quality_appraisal import (
    QualityAppraisal,
    StudyTypeCategory,
    QAScore,
    VenueTier,
    ExtractionProvenance,
)
from .retrieval_traceability import RetrievalTraceability, SourceDatabase


__all__ = [
    # Top-level extraction model (OSF prereg aligned)
    "StudyExtraction",
    "StudyCharacterization",
    "LLMIntervention",
    # Bibliographic
    "BibliographicMetadata",
    "VenueType",
    # Strategic planning
    "StrategicPlanningScope",
    "SubdomainType",
    "PlanningTaskType",
    "PlanningHorizonTier",
    "TheoreticalFrameworkType",
    # OR substrate
    "ORSubstrate",
    "FormalizationLevel",
    # Gap indicators
    "GapIndicators",
    "HITLType",
    "DomainKnowledgeType",
    "EvaluationFrameworkType",
    # Quality appraisal
    "QualityAppraisal",
    "StudyTypeCategory",
    "QAScore",
    "VenueTier",
    "ExtractionProvenance",
    # Retrieval traceability
    "RetrievalTraceability",
    "SourceDatabase",
    # AI system (legacy + extended)
    "AISystem",
    "SystemArchitecture",
    "AIAgent",
    "GenAIModel",
    "ToolUse",
    "TriggerType",
    "FinetuningDatasetType",
    "FinetuningMethodType",
    "ModelFamilyType",
    "OpenWeightType",
    "ArchitecturalPatternType",
    "AgenticArchitectureType",
    "IntegrationType",
    "ResearchType",
    "ValidationStatusType",
    "MultiAgentCoordinationStrategy",
    "Orchestration",
    "HumanIntegration",
    "HumanOversightType",
    "OrchestrationPatternType",
    "CPSIntegrationType",
    "ResearchMaturityType",
    "ResearchMethodologyType",
    "EvaluationMetricType",
    "IndustryParadigmType",
    "ScalabilityAssessmentType",
    "FeedbackAndLearningType",
    "InteractionModalityType",
    # Context Engineering
    "ContextEngineering",
    "MemoryType",
    "MemoryScopeType",
    "RetrievalStrategyType",
    "PromptEngineeringTechniquesType",
    # Types
    "ParadigmType",
    "AgentRoleType",
    "ModalityType",
    "ExternalToolsType",
    "AgentCollaborationType",
    "OrganizationalStructureType",
    # Validation
    "ValidationMethodType",
    "EvaluationAndOutcomes",
    "ReportedOutcomes",
    "StudyDesignType",
    "ComparatorType",
    "FailureAttributionType",
    # Domain
    "DomainType",
    # Base
    "DescriptiveEnum",
]
