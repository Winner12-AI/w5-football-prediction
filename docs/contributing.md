# Contributing to W-5 Football Prediction Framework

Thank you for your interest in contributing to the W-5 project! This document provides guidelines for contributing to this research implementation.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in [GitHub Issues](https://github.com/Winner12-AI/w5-football-prediction/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Submitting Code

1. **Fork the repository** and create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   pytest tests/
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

5. **Push and create a Pull Request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/Winner12-AI/w5-football-prediction.git
cd w5-football-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov mypy black flake8

# Run tests
pytest tests/
```

## Code Style

We follow PEP 8 style guidelines. Key points:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black default)
- Use descriptive variable names
- Add docstrings to all functions and classes
- Type hints are encouraged

Format your code with Black:
```bash
black src/ examples/
```

Check with flake8:
```bash
flake8 src/ examples/
```

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
# Run tests with coverage
pytest --cov=src tests/
```

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update relevant documentation in `docs/`
- Include usage examples where appropriate

## What We Accept

✅ **We welcome contributions that:**
- Fix bugs or improve existing code
- Add new baseline models or evaluation metrics
- Improve documentation and examples
- Enhance code quality and test coverage
- Add support for new data sources (with proper licensing)

## What We Don't Accept

❌ **We cannot accept contributions that:**
- Include proprietary data without authorization
- Attempt to reverse-engineer commercial models
- Add gambling or betting functionality
- Violate ethical guidelines or licenses
- Include malicious code or security vulnerabilities

## Research Contributions

If your contribution involves new research:

1. Provide clear documentation of methodology
2. Include references to relevant papers
3. Ensure reproducibility with sample data
4. Consider publishing your findings separately

## Commercial Use

This project is open source (MIT License), but please note:

- The commercial product WINNER12 includes proprietary enhancements
- If you build commercial applications, please:
  - Properly attribute the W-5 framework
  - Comply with all applicable laws and regulations
  - Consider ethical implications

## Questions?

- **Research questions**: contact@manus.im
- **Technical issues**: [GitHub Issues](https://github.com/Winner12-AI/w5-football-prediction/issues)
- **Commercial inquiries**: [WINNER12 Website](https://winner12.ai)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping improve the W-5 framework! 🚀⚽

