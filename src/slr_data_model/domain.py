from .descriptive_enum import DescriptiveEnum


class DomainType(DescriptiveEnum):
    """Domain classification for production and logistics papers based on SCOR model + extensions"""

    FACTORY_PLANNING = "factory_planning" , ""#"factory planning, facility layout, plant layout, production system design"
    PRODUCTION_PLANNING = "production_planning" , ""#"production planning, program planning, PPC, capacity planning"
    SUPPLY_CHAIN_PLANNING = "supply_chain_planning" , ""#"SCM, supply chain planning, supply chaim management"
    DEMAND_PLANNING = "demand_planning" , ""#"demand forecasting, prediction, market demand"
    PRODUCTION_SCHEDULING = "production_scheduling" , ""#"job scheduling, shop floor scheduling, job shop, flow shop"
    PRODUCTION_CONTROL = "production_control" , ""#"production control, line balancing"
    QUALITY_MANAGEMENT = "quality_management" , ""#"QC, QA, quality control, quality assurance"
    MAINTENANCE = "maintenance" , ""#"maintenance planning/scheduling, predictive/preventive maintenance"
    LOGISTICS_PLANNING = "logistics_planning" , ""#"logistics planning, route optimization, delivery scheduling"
    WAREHOUSE_MANAGEMENT = "warehouse_management" , ""#"warehouse management, stock management/control"
    INVENTORY_MANAGEMENT = "inventory_management" , ""#"inventory management/control"
    OPTIMIZATION = "optimization" , ""#"general optimization, optimization modeling, material flow optimization"
    SIMULATION = "simulation" , ""#"simulation modeling, discrete event, agent-based simulation, what-if analysis"
    TRANSPORTATION_MANAGEMENT = "transportation_management" , ""#"transportation management, fleet management"




