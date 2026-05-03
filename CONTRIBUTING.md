# Contributing to KB-AI

## Setup for Development

1. Fork the repository
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your API keys

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Testing

Run tests before committing:
```bash
cd tests
python test_evaluator.py
```

## Agent Development

When adding new agents:
1. Inherit from base agent pattern (see existing agents)
2. Return consistent JSON structure with confidence_score
3. Add error handling for API failures
4. Update decision_agent.py if new inputs needed

## Pull Request Process

1. Update README if adding features
2. Add tests for new functionality
3. Ensure all existing tests pass
4. Describe changes clearly in PR description

## Questions?

Contact team members:
- Akshara Sarode: asarode@iu.edu
- Arun Munagala: amunagal@iu.edu
- Anuj Prakash: anuprak@iu.edu
