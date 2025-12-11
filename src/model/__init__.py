"""
AI System Data Model

This module provides Pydantic models for representing AI systems,
including their architecture, capabilities, and validation methods.
"""

from .ai_system import (
    AISystem,
    AgentArchitecture,
    AIAgent,
    GenAIModel,
    ModelCapabilities,
    ToolUse,
    ContextEngineeringTechniques,
    AutonomyLevel,
    FinetuningDataset,
    OrchestrationPattern,
    GenerativeAIParadigm,
)
from .memory import Memory, MemoryType, MemoryScope, RetrievalStrategy
from .ai_system_types import (
    ParadigmType,
    AgentRoleType,
    ReasoningCapabilitiesType,
    CapabilityAcquisitionType,
    ModalityType,
    ExternalToolsType,
    CollaborationMechanismType,
    CollaborationStructureType,
    CollaborationStrategyType,
)
from .validation import ValidationMethod, ReportedOutcomes
from .domain import Domain, DomainType
from .descriptive_enum import DescriptiveEnum

__all__ = [
    # Main system
    "AISystem",
    "AgentArchitecture",
    "AIAgent",
    "GenAIModel",
    "ModelCapabilities",
    "ToolUse",
    "ContextEngineeringTechniques",
    "AutonomyLevel",
    "FinetuningDataset",
    "OrchestrationPattern",
    "GenerativeAIParadigm",
    # Memory
    "Memory",
    "MemoryType",
    "MemoryScope",
    "RetrievalStrategy",
    # Types
    "ParadigmType",
    "AgentRoleType",
    "ReasoningCapabilitiesType",
    "CapabilityAcquisitionType",
    "ModalityType",
    "ExternalToolsType",
    "CollaborationMechanismType",
    "CollaborationStructureType",
    "CollaborationStrategyType",
    # Validation
    "ValidationMethod",
    "ReportedOutcomes",
    # Domain
    "Domain",
    "DomainType",
    # Base
    "DescriptiveEnum",
]
