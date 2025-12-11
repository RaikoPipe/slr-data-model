from enum import Enum
from typing import Set

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """Memory storage mechanisms."""
    CONVERSATION_HISTORY = "conversation-history"
    VECTOR_DATABASE = "vector-database"
    KNOWLEDGE_GRAPH = "knowledge-graph"
    EXTERNAL_DATABASE = "external-database"
    STATE_TRACKING = "state-tracking"

class MemoryScope(str, Enum):
    """Temporal scope of memory."""
    SHORT_TERM = "short-term"
    LONG_TERM = "long-term"

class RetrievalStrategy(str, Enum):
    """How information is retrieved from memory."""
    SEMANTIC_SEARCH = "semantic-search"
    QUERY_DECOMPOSITION = "query-decomposition"
    RERANKING = "reranking"
    GRAPH_TRAVERSAL = "graph-traversal"

class Memory(BaseModel):
    """Memory system configuration for agent."""

    has_memory: bool = Field(
        description="Whether agent uses any explicit memory system beyond base model"
    )

    memory_types: Set[MemoryType] = Field(
        default_factory=set,
        description="Types of memory storage used. Empty if no memory system."
    )

    memory_scopes: Set[MemoryScope] = Field(
        default_factory=set,
        description="Temporal scopes of memory usage. Empty if no memory system."
    )

    retrieval_strategies: Set[RetrievalStrategy] = Field(
        default_factory=set,
        description="Methods for retrieving information. Empty if no retrieval mechanism."
    )

    shared_across_agents: bool = Field(
        default=False,
        description="Whether memory is shared between multiple agents"
    )