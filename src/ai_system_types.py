from enum import Enum
from src.descriptive_enum import DescriptiveEnum

class ModalityType(DescriptiveEnum):
    """Input/output modalities supported by the system."""
    TEXT = "text", "Textual input and output"
    IMAGE = "image", "Visual image processing"
    AUDIO = "audio", "Speech or sound processing"
    VIDEO = "video", "Video stream processing"

class ParadigmType(DescriptiveEnum):
    """AI system paradigm classification based on autonomy and reasoning capabilities."""
    GENERATIVE_AI = "generative-ai", "Simple LLM-based generation without autonomous decision-making or tool use"
    AI_AGENT = "ai-agent", "System with fixed workflows and deterministic decision logic (rule-based, planning graphs)"
    AGENTIC_AI = "agentic-ai", "Autonomous system with iterative reasoning (ReAct, CoT) and dynamic tool use"

class ExternalToolsType(DescriptiveEnum):
    """External tools and interfaces available to the agent."""
    API_CALL = "api-call", "Direct API calls to external services"
    MODEL_CONTEXT_PROTOCOL = "model-context-protocol", "MCP for standardized tool integration"
    FUNCTION_CALLING = "function-calling", "LLM native function/tool calling capabilities"
    DATABASE = "database", "Direct database queries (SQL, NoSQL)"
    KNOWLEDGE_BASE = "knowledge-base", "Structured knowledge repositories"
    EXTERNAL_MODELS = "external-models", "Calls to other AI models or specialized algorithms"

class CapabilityAcquisitionType(DescriptiveEnum):
    """Method by which the model acquires task-specific capabilities."""
    FINETUNING = "fine-tuning", "Model weights updated through supervised training on task-specific data"
    PROMPT_ENGINEERING = "prompt-engineering", "Capabilities acquired through carefully designed prompts without weight updates"

class ReasoningCapabilitiesType(DescriptiveEnum):
    """Reasoning approaches used by the agent for decision-making and task execution."""
    # Fixed/deterministic approaches (AI Agent)
    RULE_BASED = "rule-based", "If-then logic and decision trees with predefined rules"
    DETERMINISTIC_WORKFLOW = "deterministic-workflow", "Fixed sequence of steps without dynamic adaptation"
    PLANNING_GRAPH = "planning-graph", "Graph-based planning with predefined state transitions"

    # Iterative/adaptive approaches (Agentic AI)
    REACT = "react", "Reasoning and Acting framework with iterative observation-thought-action cycles"
    CHAIN_OF_THOUGHT = "chain-of-thought", "Step-by-step reasoning with intermediate thought processes"
    TREE_OF_THOUGHT = "tree-of-thought", "Explores multiple reasoning paths in a tree structure for complex problem-solving"

class AgentRoleType(DescriptiveEnum):
    """Specialized role or function of an agent within the system."""
    MONOLITHIC = "monolithic", "Single agent handling all tasks without role specialization"
    ORCHESTRATOR = "orchestrator", "Manages task distribution and coordinates other agents"
    CODER = "coder", "Generates, modifies, or debugs code"
    PLANNER = "planner", "Creates plans and breaks down complex tasks into subtasks"
    SUMMARIZER = "summarizer", "Condenses and summarizes information"
    RETRIEVER = "retriever", "Searches and retrieves relevant information from knowledge sources"
    OTHER = "other", "Specialized role not covered by standard categories"

class CollaborationMechanismType(DescriptiveEnum):
    """Agent interaction paradigm defining how agents align or conflict in their objectives."""
    COOPERATION = "cooperation", "Agents align individual objectives with shared collective goals"
    COMPETITION = "competition", "Agents prioritize their own objectives which may conflict with others"
    COOPETITION = "coopetition", "Hybrid model where agents collaborate on shared tasks while competing on others"

class CollaborationStructureType(DescriptiveEnum):
    """Organizational structure defining control and communication patterns between agents."""
    CENTRALIZED = "centralized", "Single central controller manages all agent coordination and decision-making"
    DISTRIBUTED = "distributed", "Agents coordinate as peers without central authority"
    HIERARCHICAL = "hierarchical", "Multi-level structure with manager agents overseeing worker agents"

class CollaborationStrategyType(DescriptiveEnum):
    """Strategy for determining agent behavior and task allocation in multi-agent systems."""
    RULE_BASED = "rule-based", "Agent behavior determined by predefined rules and conditions"
    ROLE_BASED = "role-based", "Agent behavior and task assignment based on specialized roles"
    MODEL_BASED = "model-based", "Agent behavior learned or optimized through models (RL, optimization)"