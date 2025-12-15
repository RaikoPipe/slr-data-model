"""
AI System Data Model

This module provides Pydantic models for representing AI systems,
including their architecture, capabilities, and validation methods.
"""
from .descriptive_enum import DescriptiveEnum
from .ai_system import (
    AISystem,
    SystemArchitecture,
    AIAgent,
    GenAIModel,
    ModelCapabilities,
    ToolUse,
    TriggerType,
    FinetuningDatasetType,
    InterAgentBehaviour,
)
from .memory import Memory, MemoryType, MemoryScopeType, RetrievalStrategyType
from .ai_system_types import (
    ParadigmType,
    AgentRoleType,
    ReasoningCapabilitiesType,
    CapabilityAcquisitionType,
    ModalityType,
    ExternalToolsType,
    TaskAlignmentType,
    OrganizationalStructureType,
    BehaviourStrategyType,
)
from .validation import ValidationMethodType, ReportedOutcomes
from .domain import DomainType


__all__ = [
    # Main system
    "AISystem",
    "SystemArchitecture",
    "AIAgent",
    "GenAIModel",
    "ModelCapabilities",
    "ToolUse",
    "TriggerType",
    "FinetuningDatasetType",
    "InterAgentBehaviour",
    # Memory
    "Memory",
    "MemoryType",
    "MemoryScopeType",
    "RetrievalStrategyType",
    # Types
    "ParadigmType",
    "AgentRoleType",
    "ReasoningCapabilitiesType",
    "CapabilityAcquisitionType",
    "ModalityType",
    "ExternalToolsType",
    "TaskAlignmentType",
    "OrganizationalStructureType",
    "BehaviourStrategyType",
    # Validation
    "ValidationMethodType",
    "ReportedOutcomes",
    # Domain
    "DomainType",
    # Base
    "DescriptiveEnum",
]
