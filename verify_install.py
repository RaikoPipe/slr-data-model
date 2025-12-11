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
            AISystem,
            AIAgent,
            GenAIModel,
            AgentArchitecture,
            AutonomyLevel,
            ParadigmType,
            ModalityType,
            Memory,
            MemoryType,
            ValidationMethod,
            DomainType,
        )
        print("   ✓ All main classes imported successfully")
        classes = [
            'AISystem', 'AIAgent', 'GenAIModel', 'AgentArchitecture',
            'AutonomyLevel', 'ParadigmType', 'ModalityType',
            'Memory', 'MemoryType', 'ValidationMethod', 'DomainType'
        ]
        print(f"   Classes available: {', '.join(classes)}")
    except ImportError as e:
        print(f"   ✗ Failed to import classes: {e}")
        print("\n   Note: Make sure pydantic is installed:")
        print("   pip install pydantic>=2.0.0")
        return False

    # Test 3: Check package metadata
    print("\n3. Checking package metadata...")
    try:
        import importlib.metadata
        metadata = importlib.metadata.metadata('slr-data-model')
        print(f"   ✓ Package name: {metadata['Name']}")
        print(f"   ✓ Version: {metadata['Version']}")
        print(f"   ✓ Summary: {metadata['Summary']}")
    except Exception as e:
        print(f"   ⚠ Could not read metadata: {e}")

    # Test 4: Verify module structure
    print("\n4. Verifying module structure...")
    try:
        expected_modules = [
            'slr_data_model.ai_system',
            'slr_data_model.ai_system_types',
            'slr_data_model.memory',
            'slr_data_model.validation',
            'slr_data_model.domain',
            'slr_data_model.descriptive_enum',
        ]
        for module in expected_modules:
            __import__(module)
        print(f"   ✓ All {len(expected_modules)} submodules found")
    except ImportError as e:
        print(f"   ✗ Module structure incomplete: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ ALL CHECKS PASSED!")
    print("=" * 60)
    print("\nThe package is properly installed and ready to use.")
    print("\nExample usage:")
    print("  from slr_data_model import AISystem, ParadigmType")
    print("  # ... create your AI system models ...")
    print("\nFor more examples, see: README.md")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
