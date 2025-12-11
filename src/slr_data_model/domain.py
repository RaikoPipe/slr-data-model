from .descriptive_enum import DescriptiveEnum


class DomainType(DescriptiveEnum):
    """Domain classification for production and logistics papers based on SCOR model + extensions"""

    # SCOR: Plan
    PRODUCTION_PLANNING = "production_planning" , "production planning, program planning, PPC, capacity planning"
    SUPPLY_CHAIN_PLANNING = "supply_chain_planning" , "SCM, supply chain planning"
    DEMAND_PLANNING = "demand_planning" , "demand forecasting, prediction, market demand"

    # SCOR: Source
    SOURCING = "sourcing" , "resource allocation, resource planning"

    # SCOR: Make
    PRODUCTION_SCHEDULING = "production_scheduling" , "job scheduling, shop floor scheduling, job shop, flow shop"
    PRODUCTION_CONTROL = "production_control" , "production control, line balancing"
    QUALITY_MANAGEMENT = "quality_management" , "QC, QA, quality control, quality assurance"
    MAINTENANCE = "maintenance" , "maintenance planning/scheduling, predictive/preventive maintenance"

    # SCOR: Deliver
    LOGISTICS_PLANNING = "logistics_planning" , "logistics planning, route optimization, delivery scheduling"
    WAREHOUSE_MANAGEMENT = "warehouse_management" , "warehouse management, stock management/control"
    INVENTORY_MANAGEMENT = "inventory_management" , "inventory management/control"

    # SCOR: Return (none in search terms)

    # Cross-cutting / Support domains
    OPTIMIZATION = "optimization" , "general optimization, optimization modeling, material flow optimization"
    SIMULATION = "simulation" , "simulation modeling, discrete event, agent-based simulation, what-if analysis"
    DIGITAL_TWIN = "digital_twin" , "digital twin, predictive analytics"
    SUSTAINABILITY = "sustainability" ," environmental planning, lifecycle assessment, green manufacturing"
    WORKFORCE_PLANNING = "workforce_planning" , "workforce planning"


# class Domain(BaseModel):
#     """Domain represents the specific area or field of application for an AI system.
#     It defines the context in which the AI operates, including the relevant knowledge,
#     terminology, and tasks associated with that domain."""
#     name: Set[DomainType] = Field(description="The name of the domain.")
