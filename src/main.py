from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Set
from memory import Memory

class ParadigmTypes(str, Enum):
    """Paradigm types available."""
    GENERATIVE_AI = "Generative AI"
    AI_AGENT = "AI Agent"
    AGENTIC_AI = "Agentic AI"

class GenerativeAIParadigm(BaseModel):
    reasoning: str = Field(description="Reasoning for choice of generative AI paradigm.")
    paradigm_type: ParadigmTypes = Field(description="Paradigm type.")

class ExternalToolsTypes(str, Enum):
    API_CALL = "API Call"
    MODEL_CONTEXT_PROTOCOL = "Model Context Protocol"
    FUNCTION_CALLING = "Function Calling"
    DATABASE = "Database"
    KNOWLEDGE_BASE = "Knowledge Base"
    EXTERNAL_MODELS = "External Models"

class ToolUse(BaseModel):
    choice_reasoning: str = Field(description="Reasoning over utilized tools in the LLM-based system of the presented paper.")
    external_tools : Set[ExternalToolsTypes] = Field(description=
                """Set of external tools that are utilized.""")

class CapabilityAcquisitionType(str, Enum):
    FINETUNING = 'fine-tuning'
    PROMPT_ENGINEERING = 'prompt-engineering'

class FinetuningDataset(str, Enum):
    """Finetuning dataset."""
    HUMAN_ANNOTATED_DATASET = "human annotated dataset"
    LLM_GENERATED_DATASET = "llm generated dataset"
    REAL_WORLD_DATASET = "real world dataset"

class ReasoningCapabilitiesTypes(str, Enum):
    """At the core of the agents intelligence lies the knowledge representation and reasoning module,
    which applies symbolic, statistical or hybrid logic to input data"""
    # AI agent

    RULE_BASED = "Rule Based" # rule based logic (if then decision trees)
    DETERMINISTIC_WORKFLOW = "Deterministic Workflow"
    PLANNING_GRAPH = "Planning Graph"

    """Iterative reasoning capabilities using frameworks allowing agents to break down a complex task into multiple
    reasoning stages, evaluate intermediate results, and re-plan actions dynamically. This enables the system to
    respond adaptively to uncertainty or partial failure"""
    # agentic AI
    REACT = "Re-Act"
    CHAIN_OF_THOUGHT = "Chain of Thought"
    TREE_OF_THOUGHT = "Tree of Thought"

class ModelCapabilities(BaseModel):
    capability_acquisition_method : CapabilityAcquisitionType = Field(description="")

class AgentRoleType(str, Enum):
    MONOLITHIC = "Monolithic"
    ORCHESTRATOR = "orchestrator"
    CODER = "coder"
    PLANNER = "planner"
    SUMMARIZER = "summarizer"
    RETRIEVER = "retriever"
    OTHER = "other"

class AIAgent(BaseModel):
    agent_reasoning_capabilities: ReasoningCapabilitiesTypes = Field(description="")
    agent_memory: Memory = Field(description="")
    agent_role: AgentRoleType = Field(description="")
    tools: ToolUse = Field(description="")

class AgentArchitecture(BaseModel):
    agents: List[AIAgent] = Field(description="")
    shared_memory: bool = Field(description="Agent shares his memory with other agents") # add validation: if not multi agent, this is false

class AISystem(BaseModel):
    agent_architecture: AgentArchitecture = Field(description="")

