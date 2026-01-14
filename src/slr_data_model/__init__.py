"""
AI System Data Model

This module provides Pydantic models for representing AI systems,
including their architecture, capabilities, and validation methods.
"""
from .descriptive_enum import DescriptiveEnum
from .context_engineering import ContextEngineering
from .ai_system import (
    AISystem,
    SystemArchitecture,
    AIAgent,
    GenAIModel,
    ToolUse,
    TriggerType,
    FinetuningDatasetType,
    MultiAgentCoordinationStrategy,
    OrchestrationPattern,
    HumanIntegration,
)
from .context_engineering import ContextEngineering, MemoryType, MemoryScopeType, RetrievalStrategyType, PromptEngineeringTechniquesType
from .ai_system_types import (
    ParadigmType,
    AgentRoleType,
    ModalityType,
    ExternalToolsType,
    AgentCollaborationType,
    OrganizationalStructureType,
)
from .validation import ValidationMethodType, ReportedOutcomes
from .domain import DomainType


__all__ = [
    # Main system
    "AISystem",
    "SystemArchitecture",
    "AIAgent",
    "GenAIModel",
    "ToolUse",
    "TriggerType",
    "FinetuningDatasetType",
    "MultiAgentCoordinationStrategy",
    "OrchestrationPattern",
    # Context Engineering
    "ContextEngineering",
    "MemoryType",
    "MemoryScopeType",
    "RetrievalStrategyType",
    "PromptEngineeringTechniquesType",
    # Types
    "ParadigmType",
    "AgentRoleType",
    "PromptEngineeringTechniquesType",
    "ModalityType",
    "ExternalToolsType",
    "AgentCollaborationType",
    "OrganizationalStructureType",
    # Validation
    "ValidationMethodType",
    "ReportedOutcomes",
    # Domain
    "DomainType",
    # Base
    "DescriptiveEnum",
]
