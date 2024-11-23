# Contributing to Network Traffic Anomaly Detection

First off, thank you for considering contributing to this project! It's people like you that make this tool better for everyone.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Process](#development-process)
4. [Pull Request Process](#pull-request-process)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Issue Reporting](#issue-reporting)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/network-traffic-anomaly-detection.git
cd network-traffic-anomaly-detection
```

3. Set up development environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Development Process

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

2. Make your changes
3. Test your changes thoroughly
4. Commit your changes:
```bash
git add .
git commit -m "Description of changes"
```

### Branch Naming Convention
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test-related changes
- `refactor/` - Code refactoring

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation if you're introducing new features
3. Ensure all tests pass
4. Update the version numbers if applicable
5. Submit a pull request to the `develop` branch

### PR Title Format
```
[TYPE] Brief description

Types:
- FEATURE: New functionality
- FIX: Bug fix
- DOCS: Documentation
- TEST: Testing
- REFACTOR: Code refactoring
```

## Coding Standards

### Python Style Guide
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example
```python
def analyze_traffic_pattern(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze network traffic patterns for anomalies.

    Args:
        data (pd.DataFrame): Input traffic data

    Returns:
        Dict[str, Any]: Analysis results
    """
    # Implementation
```

### JavaScript Style Guide
- Use ES6+ features
- Follow Airbnb JavaScript Style Guide
- Use meaningful variable and function names
- Add JSDoc comments for functions

## Testing Guidelines

### Python Tests
1. Write unit tests using pytest
2. Maintain test coverage above 80%
3. Place tests in the `tests/` directory
4. Name test files with `test_` prefix

```python
def test_anomaly_detection():
    """Test anomaly detection functionality."""
    detector = NetworkAnomalyDetector()
    result = detector.detect_anomalies(sample_data)
    assert result is not None
```

### JavaScript Tests
1. Write tests using Jest
2. Test all UI interactions
3. Mock API calls appropriately

## Documentation

### Code Documentation
- Add docstrings to all Python functions/classes
- Use JSDoc for JavaScript functions
- Keep documentation up to date with code changes

### Project Documentation
- Update README.md for major changes
- Maintain API documentation
- Update wiki pages when needed

## Issue Reporting

### Bug Reports
Include:
1. Description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. System information
6. Screenshots if applicable

### Feature Requests
Include:
1. Clear description of the feature
2. Rationale for the feature
3. Possible implementation approach
4. Examples of similar features elsewhere

## Review Process

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is considered
- [ ] Error handling is appropriate

### Security Considerations
- Review for security implications
- No sensitive data in code/comments
- Proper input validation
- Secure default configurations

## Version Control

### Commit Messages
```
[TYPE] Brief description

Detailed description of changes
Why the change was made
Any breaking changes

Types:
- FEAT: New feature
- FIX: Bug fix
- DOCS: Documentation
- STYLE: Code style
- REFACTOR: Code refactoring
- TEST: Testing
- CHORE: Maintenance
```

## Getting Help

If you need help:
1. Check existing documentation
2. Search through issues
3. Ask in discussions
4. Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License. 