# Contributing to YatraAI

We love contributions from the community! This document provides guidelines and instructions for contributing to YatraAI.

## Code of Conduct

Be respectful, inclusive, and constructive. We follow the principle of treating others as we'd like to be treated.

## Getting Started

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/YatraAI.git
   cd YatraAI
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

5. **Create .env file**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key and other settings
   ```

6. **Initialize database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Development Workflow

### Before You Start

- Check [existing issues](../../issues) to avoid duplicates
- Read the [README.md](README.md) for project overview
- Familiarize yourself with the project structure

### Making Changes

1. **Create descriptive commit messages**
   ```
   feat(itinerary): add AI-powered suggestions
   fix(ui): resolve mobile layout issue
   docs(readme): update installation steps
   style(css): improve button styling
   refactor(api): optimize database queries
   test(models): add comprehensive tests
   ```

2. **Keep commits focused**
   - One feature/fix per commit
   - Make commits atomic and logical

3. **Write clean code**
   - Follow PEP 8 guidelines
   - Use meaningful variable and function names
   - Add comments for complex logic

4. **Test your changes locally**
   ```bash
   # Run migrations
   python manage.py migrate

   # Run tests
   python manage.py test

   # Check code quality
   black --check apps/ config/
   flake8 apps/ config/ --max-line-length=100

   # Run development server
   python manage.py runserver
   ```

## Code Style

### Python

- **Formatter**: Black (automatically formats code)
  ```bash
  black apps/ config/
  ```

- **Linter**: Flake8 (checks code quality)
  ```bash
  flake8 apps/ config/ --max-line-length=100
  ```

- **Import Sorting**: isort
  ```bash
  isort apps/ config/
  ```

### HTML/CSS/JavaScript

- Use 2-space indentation
- Use meaningful class and ID names
- Follow BEM naming convention for CSS classes
- Use descriptive variable names in JavaScript

### Docstrings

All functions and classes should have docstrings:

```python
def generate_itinerary(destination, duration, interests):
    """
    Generate a personalized travel itinerary.
    
    Args:
        destination (str): Travel destination
        duration (int): Number of days
        interests (list): User interests
        
    Returns:
        dict: Generated itinerary with details
        
    Raises:
        ValueError: If arguments are invalid
    """
    pass
```

## Git Workflow

### Branch Naming Convention

```
feature/description      # New feature
fix/description         # Bug fix
docs/description        # Documentation
style/description       # Styling changes
refactor/description    # Code refactoring
test/description        # Test additions
```

### Commit Message Format

```
<type>(<scope>): <description>

<body> (optional)

<footer> (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature change
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, etc.

**Example:**
```
feat(api): add endpoint for hidden gems

- Implement GET /api/v1/locations/hidden-gems/
- Add filtering by region and season
- Include location ratings and descriptions

Closes #123
```

## Testing

### Writing Tests

- Write tests for new features
- Aim for at least 80% code coverage
- Use descriptive test names starting with `test_`

```python
def test_generate_itinerary_with_valid_parameters():
    """Test itinerary generation with valid inputs."""
    result = generate_itinerary(
        destination="Kathmandu",
        duration=7,
        interests=["culture", "nature"]
    )
    assert result is not None
    assert len(result["itinerary"]) == 7
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test apps.itinerary.tests

# Run with coverage
pytest --cov=apps

# Run specific test class
python manage.py test apps.itinerary.tests.TestItineraryGeneration
```

## Making a Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**
   - Go to the [main repository](../../)
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template:
     - Clear title and description
     - Reference related issues (#123)
     - List changes made
     - Mention any breaking changes

3. **Address Review Comments**
   - Make requested changes
   - Push updates (don't force push)
   - Mark conversations as resolved

4. **Get Approved & Merged**
   - Wait for CI/CD to pass
   - Get approval from maintainers
   - Merge when ready

## Reporting Issues

### Bug Reports

Include:
- Clear, descriptive title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/error logs if applicable
- Environment info (OS, Python version, etc.)

### Feature Requests

Include:
- Clear description of the feature
- Why it would be useful
- Possible implementation approach
- Examples or use cases

## Documentation

- Keep docs updated with code changes
- Write clear, beginner-friendly explanations
- Use code examples
- Include images/diagrams for complex concepts
- Update README if adding new features

## Questions?

- Check [Issues](../../issues) for similar questions
- Create a new discussion for questions
- Email: support@yatraai.com

## Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Project commit history
- Release notes

Thank you for contributing to YatraAI! 🙏
