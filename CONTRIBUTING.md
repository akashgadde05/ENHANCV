# Contributing to Smart ATS Resume Builder

Thank you for your interest in contributing! Here's how you can help:

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ENHANCV.git`
3. Create a virtual environment: `python -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your `.env` file with your Groq API key

## Development Setup

```bash
# Install development dependencies
pip install -r requirements-minimal.txt

# Run tests
python test_complete_system.py

# Start development server
python run.py
```

## Making Changes

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test your changes: `python test_complete_system.py`
4. Commit your changes: `git commit -m "Add your feature"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Update tests when adding new features

## Reporting Issues

Please use the GitHub issue tracker to report bugs or request features.
Include:
- Python version
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior

## Questions?

Feel free to open an issue for questions or join our discussions!
