class RetrievalTypes(str, Enum):
    """Retrieval types available."""
    QUERY_CENTERED_RETRIEVAL = "Query Centered Retrieval" # focuses on improving query formulation and adaptation
    MEMORY_CENTERED_RETRIEVAL = "Memory Centered Retrieval" # enhancement of organization and ranking of memory candidates, including better indexing strategies and reranking methods
    EVENT_CENTERED_RETRIEVAL = "Event Centered Retrieval" #

class MemoryUtilization(str, Enum):
    QUERY_CENTERED_RETRIEVAL = "Query Centered Retrieval" # focuses on improving query formulation and adaptation
    MEMORY_CENTERED_RETRIEVAL = "Memory Centered Retrieval" # enhancement of organization and ranking of memory candidates, including better indexing strategies and reranking methods
    EVENT_CENTERED_RETRIEVAL = "Event Centered Retrieval" # retrieve memory based on temporal and causal structures
    COMPRESSION = "compression"

class MemoryManagement(str, Enum):
    """Management in long-term memory involves operations such as consolidation,
    indexing, updating, and forgetting of acquired experiences. Here, memory is instantiated in two forms:
    (1) accumulated dialogue histories from multi-turn conversations,
    and (2) long-term observations and decisions made by autonomous agents. These are often encoded by
    LLMs and stored in external memory repositories
    for future access, reuse. Memory in those tasks is
    routinely updated with new information and pruned
    to remove outdated or irrelevant content."""
    CONSOLIDATION = "consolidation" # process of turning short-term memory into long-term memory by summarization
    GRAPH_INDEXING = "graph indexing" # structuring memory representations to support efficient and accurate retrieval
    SIGNAL_INDEXING = "signal indexing"
    TIMELINE_INDEXING = "timeline indexing"
    UPDATING = "updating" # external memory creates new entries for unseen information
    FORGETING = "forgetting" # actively forgetting information when there is harmful content

class ContextualStructuredMemoryTypes(str, Enum):
    """Explicit memory organized into predefined, interpretable formats or schemata such as knowledge graphs, relational tables or ontologies,
which remain easily queryable
Structured
memory can be short-term, constructed at inference
for local reasoning, or long-term, storing curated
knowledge across sessions."""
    KNOWLEDGE_GRAPH = "knowledge graph"
    RELATIONAL_TABLES = "relational table"
    ONTOLOGY = "ontology"
    STATE_TRACKING = "state tracking" # mostly used for short term memory

class ContextualUnstructuredMemoryTypes(str, Enum):
    """Refers to an explicit, modality-general memory system
    Short-term memory refers to recent observations, like the current dialogue session context, while for  long-term memory
this refers to the persistent records of cross-session conversation dialogues and personal persistent knowl-
edge."""
    dialogue_history = "dialogue history"
    text = "text"


class ContextualMemory(BaseModel):
    contextual_structured_memory : ContextualStructuredMemoryTypes = Field()
    contextual_unstructured_memory: ContextualStructuredMemoryTypes = Field()

class ParametricMemoryTypes(str, Enum):
    """Parametric memory types available."""
    BASE_MODEL = "Base Model"
    LORA_FINETUNING = "Lora Fine-tuning"
    ADDITIONAL_PRETRAINING = "Additional Model Pre-training"

class MemoryTaxonomy(BaseModel):
    parametric_memory: ParametricMemoryTypes = Field("referring to the knowledge stored through the model's parameters")
    contextual_memory: ContextualMemory = Field(description="denotes explicit, external information that complements an LLM’s parameters and is categorized into unstructured and structured forms.")

class Memory(BaseModel):

    long_term_memory : MemoryTaxonomy = Field(description="contextual long-term (persistent) memory") # agentic trait
    short_term_memory : MemoryTaxonomy = Field(description="")

    # in the context of long term memory
    memory_management: MemoryManagement = Field(description="")
    memory_utilization: MemoryUtilization = Field(description="")