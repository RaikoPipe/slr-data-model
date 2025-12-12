from enum import Enum
from typing import Set
from . import DescriptiveEnum
from .annotation_helper import make_type_annotations
from pydantic import BaseModel, Field


class MemoryType(DescriptiveEnum):
    """Memory storage mechanisms."""
    CONVERSATION_HISTORY = "conversation-history", "Stores past interactions to maintain context."
    VECTOR_DATABASE = "vector-database", "Uses vector embeddings for semantic search and retrieval."
    KNOWLEDGE_GRAPH = "knowledge-graph", "Represents information as interconnected entities and relationships."
    EXTERNAL_DATABASE = "external-database", "Integrates with external databases for persistent storage."
    STATE_TRACKING = "state-tracking", "Maintains state information relevant to tasks or processes."

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

class Memory(BaseModel):
    """Memory system configuration for agent."""

    has_memory: bool = Field(
        description="Whether agent uses any explicit memory system beyond base model"
    )

    memory_types: Set[MemoryType] = Field(
        default_factory=set,
        description="Types of memory storage used. Empty if no memory system." + make_type_annotations(MemoryType)
    )

    memory_scopes: Set[MemoryScopeType] = Field(
        default_factory=set,
        description="Temporal scopes of memory usage. Empty if no memory system." + make_type_annotations(MemoryScopeType)
    )

    retrieval_strategies: Set[RetrievalStrategyType] = Field(
        default_factory=set,
        description="Methods for retrieving information. Empty if no retrieval mechanism." + make_type_annotations(RetrievalStrategyType)
    )

    shared_across_agents: bool = Field(
        default=False,
        description="Whether memory is shared between multiple agents"
    )