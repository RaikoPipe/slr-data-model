from enum import Enum
from typing import Set
from wsgiref.validate import validator

from . import DescriptiveEnum
from .annotation_helper import make_type_annotations
from pydantic import BaseModel, Field, field_validator


class MemoryType(DescriptiveEnum):
    """Memory storage mechanisms."""
    CONVERSATION_HISTORY = "conversation-history", "Stores past interactions to maintain context."
    VECTOR_DATABASE = "vector-database", "Uses vector embeddings for semantic search and retrieval."
    KNOWLEDGE_GRAPH = "knowledge-graph", "Represents information as interconnected entities and relationships."
    EXTERNAL_DATABASE = "external-database", "Integrates with external databases for persistent storage."
    STATE_TRACKING = "state-tracking", "Maintains state information relevant to tasks or processes."
    PARAMETRIC_MEMORY = "parametric-memory", "Utilizes model parameters to store learned information."

class MemoryScopeType(DescriptiveEnum):
    """Temporal scope of memory."""
    SHORT_TERM = "short-term", "Temporary memory for immediate context."
    LONG_TERM = "long-term", "Persistent memory for extended knowledge retention."

class RetrievalStrategyType(DescriptiveEnum):
    """How information is retrieved from memory."""
    SEMANTIC_SEARCH = "semantic-search", "Retrieves information based on meaning and context."
    QUERY_DECOMPOSITION = "query-decomposition", "Breaks down complex queries into simpler sub-queries for retrieval."
    RERANKING = "reranking", "Ranks retrieved items based on relevance to the query."
    GRAPH_TRAVERSAL = "graph-traversal", "Navigates knowledge graphs to find related information."

class PromptInjectionStrategyType(DescriptiveEnum):
    """Strategies for injecting memory into prompts."""
    PREPENDING = "prepending", "Adding memory content at the beginning of the prompt."
    APPENDING = "appending", "Adding memory content at the end of the prompt."
    IN_TEXT_INJECTION = "in-text-injection", "Inserting memory content within the body of the prompt."
    DYNAMIC_INJECTION = "dynamic-injection", "Adapting memory injection based on context or query."

class PromptEngineeringTechniquesType(DescriptiveEnum):
    """Reasoning approaches used by the agent for decision-making and task execution."""
    # Fixed/deterministic approaches (AI Agent)
    ITERATIVE_REASONING = "iterative-reasoning", "Reasoning and Acting framework with iterative observation-thought-action cycles"
    CHAIN_OF_THOUGHT = "chain-of-thought", "Step-by-step reasoning with intermediate thought processes"
    TREE_OF_THOUGHT = "tree-of-thought", "Explores multiple reasoning paths in a tree structure for complex problem-solving"
    IN_CONTEXT_LEARNING = "in-context-learning", "Learning from examples provided in the input context without weight updates"
    RETRIEVAL_AUGMENTED_GENERATION = "retrieval-augmented-generation", "Incorporating retrieved information into generation tasks for enhanced responses"

class ContextEngineering(BaseModel):
    """Memory architecture for agent."""

    # memory_description: str = Field(description="Description of the memory system as reported in the paper.")

    # has_memory: bool = Field(
    #     description="Whether agent uses any explicit memory system beyond base model"
    # )

    memory_types: Set[MemoryType] = Field(
        default_factory=set,
        description="Types of memory storage used. Empty if no memory system." + make_type_annotations(MemoryType)
    )

    prompt_engineering_techniques: Set[PromptEngineeringTechniquesType] = Field(
        description="Reasoning approaches used (rule-based, ReAct, chain-of-thought, etc.). State at least one."+ make_type_annotations(PromptEngineeringTechniquesType)
    )

    retrieval_strategies: Set[RetrievalStrategyType] = Field(
        default_factory=set,
        description="Methods for retrieving information. Empty if no retrieval mechanism/RAG." + make_type_annotations(RetrievalStrategyType)
    )

    prompt_injection_strategy : Set[PromptInjectionStrategyType] = Field(
        default_factory=set,
        description="Techniques for injecting memory into prompts. Empty if no persistent memory system." + make_type_annotations(PromptInjectionStrategyType)
    )

    @field_validator("retrieval_strategies")
    def validate_retrieval_strategies(cls, v, values):
        if (not v or len(v) == 0) and (PromptEngineeringTechniquesType.RETRIEVAL_AUGMENTED_GENERATION in values.get("prompt_engineering_techniques", set())):
            raise ValueError("If RAG is used as a prompt engineering technique, at least one retrieval strategy must be specified.")
        return v