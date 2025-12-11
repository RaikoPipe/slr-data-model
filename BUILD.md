# Building and Publishing Guide

This document explains how to build and publish the `slr-data-model` package.

## Prerequisites

```bash
pip install build twine
```

## Building the Package

### Build wheel and source distribution:

```bash
python -m build
```

This will create both:
- `dist/slr_data_model-{version}-py3-none-any.whl` (wheel)
- `dist/slr-data-model-{version}.tar.gz` (source distribution)

### Build only wheel:

```bash
python -m build --wheel
```

### Build only source distribution:

```bash
python -m build --sdist
```

## Installing Locally

### Install in development mode (editable):

```bash
pip install -e .
```

### Install with development dependencies:

```bash
pip install -e ".[dev]"
```

### Install from wheel:

```bash
pip install dist/slr_data_model-{version}-py3-none-any.whl
```

## Publishing to PyPI

### Test on TestPyPI first:

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ slr-data-model
```

### Publish to PyPI:

```bash
twine upload dist/*
```

## Version Management

Update the version in `pyproject.toml`:

```toml
[project]
version = "0.2.0"  # Update this
```

## Cleaning Build Artifacts

```bash
# Remove build artifacts
rm -rf build/ dist/ *.egg-info/

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

## Package Structure

```
slr-data-model/
├── src/
│   └── slr_data_model/       # Main package
│       ├── __init__.py
│       ├── ai_system.py
│       ├── ai_system_types.py
│       ├── descriptive_enum.py
│       ├── domain.py
│       ├── memory.py
│       └── validation.py
├── test/                     # Tests
│   ├── test.py
│   └── verify_model.py
├── pyproject.toml            # Package configuration
├── README.md                 # Package documentation
├── LICENSE                   # MIT License
├── requirements.txt          # Dependencies
├── MANIFEST.in              # Additional files to include
└── .gitignore               # Git ignore rules
```

## Import Structure

After installation, the package can be imported as:

```python
# Import the main package
import slr_data_model

# Import specific components
from slr_data_model import AISystem, AIAgent, GenAIModel
from slr_data_model import Memory, MemoryType, MemoryScope
from slr_data_model import ValidationMethod, DomainType
from slr_data_model import ParadigmType, ModalityType, AgentRoleType
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest test/test.py
```
