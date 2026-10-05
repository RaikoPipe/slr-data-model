from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations
from .descriptive_enum import DescriptiveEnum


class SubdomainType(DescriptiveEnum):
    """Strategic planning subdomains scoped by the review per §3.3."""
    FACTORY_PLANNING = "factory-planning", "Factory planning per VDI 5200"
    SC_NETWORK_DESIGN = "SC-network-design", "Supply chain network design"
    LOGISTICS_DISTRIBUTION_NETWORK_DESIGN = "logistics-distribution-network-design", "Strategic logistics and distribution network design"
    TECHNOLOGY_SELECTION = "technology-selection", "Technology selection and investment appraisal"
    SITE_SELECTION = "site-selection", "Site selection and facility location"
    GPN_DESIGN = "GPN-design", "Global production network design"


class PlanningTaskType(DescriptiveEnum):
    """Controlled vocabulary for specific planning tasks (§5)."""
    REQUIREMENTS_ELICITATION = "requirements-elicitation", "Elicitation of planning requirements"
    LASTENHEFT_GENERATION = "Lastenheft-generation", "Generation of requirements specification (Lastenheft)"
    FACTORY_LAYOUT_PLANNING = "factory-layout-planning", "Factory or facility layout planning"
    CAPACITY_DIMENSIONING = "capacity-dimensioning", "Capacity dimensioning and planning"
    MATERIAL_FLOW_DESIGN = "material-flow-design", "Material flow design and optimization"
    SIMULATION_MODELING = "simulation-modeling", "Simulation modeling for planning"
    SC_NETWORK_CONFIGURATION = "SC-network-configuration", "Supply chain network configuration"
    FACILITY_LOCATION = "facility-location", "Facility location selection"
    MAKE_OR_BUY = "make-or-buy", "Make-or-buy decision"
    TECHNOLOGY_SCOUTING = "technology-scouting", "Technology scouting and identification"
    INVESTMENT_APPRAISAL = "investment-appraisal", "Investment appraisal and evaluation"
    SITE_SELECTION = "site-selection", "Site selection"
    GPN_CONFIGURATION = "GPN-configuration", "Global production network configuration"
    DISTRIBUTION_NETWORK_PLANNING = "distribution-network-planning", "Distribution network planning"
    LOGISTICS_NETWORK_PLANNING = "logistics-network-planning", "Logistics network planning"
    NORM_COMPLIANCE = "norm-compliance", "Norm and standards compliance checking"
    TENDER_EVALUATION = "tender-evaluation", "Tender and bid evaluation"
    OTHER = "other", "Other planning task not covered by standard categories (specify)"


class PlanningHorizonTier(DescriptiveEnum):
    """Planning horizon tiers addressed per §3.3 (multi-valued; NA is exclusive)."""
    NA = "NA", "No planning horizon addressed"
    STRATEGIC = "Strategic", "Strategic planning horizon (system configuration: what exists)"
    TACTICAL = "Tactical", "Tactical planning horizon (mid-term allocation of existing resources)"
    OPERATIONAL = "Operational", "Operational planning horizon (short-term scheduling and control)"


class TheoreticalFrameworkType(DescriptiveEnum):
    """Theoretical frameworks cited for strategic planning scope per §3.3."""
    VDI_5200 = "VDI-5200", "VDI 5200 factory planning guideline"
    SC_PLANNING_MATRIX = "SC-Planning-Matrix", "Supply Chain Planning Matrix (Fleischmann, Meyr, Wagner)"
    LANZA_ET_AL_2019 = "Lanza-et-al-2019", "Global production network design (Lanza et al., CIRP Annals 2019)"
    WIENDAHL_NYHUIS = "Wiendahl-Nyhuis", "Wiendahl-Nyhuis factory planning framework"
    MELO_NICKEL_SALDANHA_DA_GAMA_2009 = "Melo-Nickel-Saldanha-da-Gama-2009", "Strategic logistics/distribution network design framework (Melo, Nickel, Saldanha-da-Gama 2009)"
    OTHER = "other", "Other theoretical framework (specify)"
    NONE = "none", "No theoretical framework cited"


class StrategicPlanningScope(BaseModel):
    """Strategic planning scope (LLM pre-fill; R1 verifies 100% against source text)."""
    subdomain: list[SubdomainType] = Field(
        description="Strategic planning subdomain(s) addressed. If not stated explicitly, map by task description using Appendix A."
        + make_type_annotations(SubdomainType)
    )
    subdomain_mapping_rationale: Optional[str] = Field(
        default=None,
        description="Free-text explanation of how tasks were mapped to subdomain(s) per Appendix A; document tactical/strategic boundary cases (§6)."
    )
    planning_task_type: list[PlanningTaskType] = Field(
        description="Specific planning task(s) addressed, pick all applicable." + make_type_annotations(PlanningTaskType)
    )
    other_planning_task_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the planning task if 'other' was selected."
    )
    time_horizon_explicitly_stated: bool = Field(
        description="Whether the paper explicitly states a time horizon."
    )
    planning_horizon_tiers: list[PlanningHorizonTier] = Field(
        min_length=1,
        description="All planning horizon tiers the paper addresses, pick all applicable; 'NA' only if no tier is addressed."
        + make_type_annotations(PlanningHorizonTier)
    )
    planning_horizon_rationale: Optional[str] = Field(
        default=None,
        description="Free-text reasoning for the tier classification; quote the paper's horizon statement(s) per tier."
    )
    system_configuring_decision_stated: bool = Field(
        description="Whether the paper explicitly frames the decision as system-configuring (determining what exists, not how existing resources are used)."
    )
    system_configuring_decision_description: Optional[str] = Field(
        default=None,
        description="Free-text description of what the system-configuring decision determines (entities created, capacities set, locations chosen), as reported."
    )
    theoretical_framework_cited: list[TheoreticalFrameworkType] = Field(
        description="Theoretical framework(s) cited for strategic planning scope." + make_type_annotations(TheoreticalFrameworkType)
    )
    theoretical_framework_rationale: Optional[str] = Field(
        default=None,
        description="Free-text reasoning why no theoretical framework applies. Required if 'none' was selected, otherwise null."
    )
    other_theoretical_framework_specification: Optional[str] = Field(
        default=None,
        description="Free-text name and citation of the specific framework(s) utilized, not restricted to a controlled vocabulary. Required if 'other' was selected, otherwise null."
    )

    @model_validator(mode="after")
    def validate_conditional_fields(self):
        """Exclusive NA/none values and conditionally required free-text fields."""
        if len(self.planning_horizon_tiers) > 1 and PlanningHorizonTier.NA in self.planning_horizon_tiers:
            raise ValueError("planning_horizon_tiers: 'NA' cannot be combined with other values")
        frameworks = self.theoretical_framework_cited
        if len(frameworks) > 1 and TheoreticalFrameworkType.NONE in frameworks:
            raise ValueError("theoretical_framework_cited: 'none' cannot be combined with other values")
        for value, field_name in (
            (TheoreticalFrameworkType.NONE, "theoretical_framework_rationale"),
            (TheoreticalFrameworkType.OTHER, "other_theoretical_framework_specification"),
        ):
            filled = bool((getattr(self, field_name) or "").strip())
            if value in frameworks and not filled:
                raise ValueError(f"{field_name} is required when '{value.value}' is selected")
            if value not in frameworks and filled:
                raise ValueError(f"{field_name} must be null unless '{value.value}' is selected")
        return self