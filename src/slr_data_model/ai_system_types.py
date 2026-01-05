from dataclasses import Field

from .descriptive_enum import DescriptiveEnum
from pydantic import Field

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

class AgentRoleType(DescriptiveEnum):
    """Specialized role or function of an agent within the system."""
    MONOLITHIC = "monolithic", "Single agent handling all tasks without role specialization"
    ORCHESTRATOR = "orchestrator", "Decomposes task, manages task distribution and coordinates other agents"
    CODER = "coder", "Generates, modifies, or debugs code"
    PLANNER = "planner", "Creates plans and breaks down complex tasks into subtasks"
    SUMMARIZER = "summarizer", "Condenses and summarizes information"
    RETRIEVER = "retriever", "Searches and retrieves relevant information from knowledge sources"
    OTHER = "other", "Specialized role not covered by standard categories"

class AgentCollaborationType(DescriptiveEnum):
    """Agent interaction paradigm defining how agents align or conflict in their objectives."""
    COOPERATION = "cooperation", "Agents align individual objectives with shared collective goals"
    COMPETITION = "competition", "Agents prioritize their own objectives which may conflict with others"
    COOPETITION = "coopetition", "Hybrid model where agents collaborate on shared tasks while competing on others"

class OrganizationalStructureType(DescriptiveEnum):
    """Organizational structure defining control and communication patterns between agents."""
    DISTRIBUTED = "distributed", "Agents coordinate as peers without central authority"
    CENTRALIZED = "centralized", "Single central agent controlling subordinate agents"
    HIERARCHICAL = "hierarchical", "Multiple levels of hierarchical nesting with manager agents overseeing subordinate agents"
    LINEAR = "linear", "Sequential chain of agents where each agent passes the task to the next."

# class BehaviourStrategyType(DescriptiveEnum):
#     """Strategy for determining agent behavior in multi-agent systems."""
#     RULE_BASED = "rule-based", "Agent behavior determined by predefined rules and conditions"
#     ROLE_BASED = "role-based", "Agent behavior and task assignment based on specialized roles"