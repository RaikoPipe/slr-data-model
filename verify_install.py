#!/usr/bin/env python3
"""
Verification script to test that slr-data-model is properly installed as an external package.

This script can be run from anywhere after installing the package:
  pip install slr-data-model
  python verify_install.py

Or in development mode:
  pip install -e .
  python verify_install.py
"""

import sys


def main():
    print("=" * 60)
    print("SLR Data Model - Installation Verification")
    print("=" * 60)

    # Test 1: Check if package can be imported
    print("\n1. Testing package import...")
    try:
        import slr_data_model
        print("   ✓ Package 'slr_data_model' imported successfully")
        print(f"   Location: {slr_data_model.__file__}")
    except ImportError as e:
        print(f"   ✗ Failed to import package: {e}")
        return False

    # Test 2: Check if main classes can be imported
    print("\n2. Testing main class imports...")
    try:
        from slr_data_model import (
            StudyExtraction,
            BibliographicMetadata,
            VenueType,
            StudyCharacterization,
            ResearchType,
            ValidationStatusType,
            StrategicPlanningScope,
            SubdomainType,
            PlanningTaskType,
            PlanningHorizonTier,
            TheoreticalFrameworkType,
            LLMIntervention,
            ModelFamilyType,
            OpenWeightType,
            FineTuningType,
            ArchitecturalPatternType,
            AgenticArchitectureType,
            IntegrationType,
            ORSubstrate,
            FormalizationLevel,
            EvaluationAndOutcomes,
            ReportedMetric,
            ComparatorType,
            StudyDesignType,
            GapIndicators,
            HITLType,
            DomainKnowledgeType,
            EvaluationFrameworkType,
            QualityAppraisal,
            ExtractionMetaData,
            ProvenanceTag,
            VerificationStatus,
            DescriptiveEnum,
        )
        print("   ✓ All main classes imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import classes: {e}")
        return False

    # Test 3: Schema generation
    print("\n3. Testing JSON schema generation...")
    try:
        schema = StudyExtraction.model_json_schema()
        required = [
            "study_id",
            "bibliographic_metadata",
            "study_characterization",
            "strategic_planning_scope",
            "llm_intervention",
            "or_substrate",
            "evaluation_and_outcomes",
            "gap_indicators",
            "quality_appraisal",
            "extraction_metadata",
        ]
        missing = [k for k in required if k not in schema.get("properties", {})]
        if missing:
            print(f"   ✗ Schema missing properties: {missing}")
            return False
        print("   ✓ JSON schema generated with all field groups")
    except Exception as e:
        print(f"   ✗ Schema generation failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ Installation verified successfully!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)