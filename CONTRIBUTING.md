# Contributing to KMeans Engine

Thank you for your interest in contributing to KMeans Engine! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Conventions](#commit-message-conventions)
- [Branch Naming](#branch-naming)
- [Pull Request Process](#pull-request-process)
- [Project Phases](#project-phases)
- [Testing](#testing)
- [Questions and Support](#questions-and-support)

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Docker Desktop 4.20+ installed and running
- Git 2.30+ installed
- A GitHub account

### Setting Up Your Development Environment

1. **Fork the repository**
   ```bash
   # Fork the repository on GitHub, then clone your fork
   git clone https://github.com/yourusername/kmeans-engine.git
   cd kmeans-engine
   ```

2. **Add the upstream remote**
   ```bash
   git remote add upstream https://github.com/originalusername/kmeans-engine.git
   ```

3. **Create a virtual environment (optional for local development)**
   ```bash
   # Python virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows

   # Node.js environment is handled by package.json in frontend/
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

5. **Start the development environment**
   ```bash
   start.bat        # Windows
   docker-compose up # Linux/Mac
   ```

6. **Verify the setup**
   - Open http://localhost:3000 in your browser
   - Open http://localhost:8000/docs to see the API documentation

## Development Environment

### Running the Application

```bash
# Start all services
start.bat          # Windows
docker-compose up  # Linux/Mac

# Stop all services
stop.bat           # Windows
docker-compose down # Linux/Mac

# View logs
docker-compose logs -f

# Rebuild services (after code changes)
docker-compose up --build -d
```

### Working with the Codebase

The project is organized as follows:

```
backend/          # Python FastAPI application
  app/           # Application modules
  tests/         # Backend tests
  requirements.txt # Python dependencies

frontend/        # Next.js React application
  app/          # Next.js app directory
  components/   # React components
  package.json  # Node.js dependencies
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Run all tests
npm run test:all
```

## Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black default)
- Use type hints for function signatures
- Write descriptive docstrings for functions and classes

Example:
```python
def cluster_data(data: pd.DataFrame, n_clusters: int) -> Dict[str, Any]:
    """
    Cluster data using K-Means algorithm.

    Args:
        data: Input dataframe to cluster
        n_clusters: Number of clusters to create

    Returns:
        Dictionary containing cluster labels and centroids
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(data)
    return {"labels": labels, "centroids": kmeans.cluster_centers_}
```

### JavaScript/TypeScript (Frontend)

- Use 2 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use functional components with hooks
- Use TypeScript for type safety
- Follow [React best practices](https://react.dev/learn/thinking-in-react)

Example:
```typescript
interface ClusterData {
  labels: number[];
  centroids: number[][];
}

function ClusterChart({ data }: { data: ClusterData }) {
  // Component implementation
}
```

### CSS

- Use Tailwind CSS utility classes
- Follow mobile-first responsive design
- Use semantic class names when needed
- Keep styles scoped to components

## Commit Message Conventions

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)

### Examples

```
feat(backend): add K-Means clustering endpoint

- Implement /api/cluster endpoint with K-Means++ algorithm
- Add input validation for n_clusters parameter
- Return cluster labels and centroids in JSON format

Fixes #123

fix(frontend): resolve chart rendering issue on Safari

- Use canvas-based rendering for better browser compatibility
- Add fallback for unsupported features
- Update chart library to latest version

Closes #145

docs(readme): update installation instructions

- Add Docker Desktop version requirement
- Clarify Windows vs Linux/Mac commands
- Add troubleshooting link

docs(01-03): update project structure documentation

- Reflect new directory organization
- Add architecture diagram
- Update environment setup steps
```

### Commit Messages with Phase/Plan Reference

When working on specific phase/plan tasks, include the reference:

```
feat(01-03): create FastAPI Hello World endpoint

- Add /health endpoint for service health check
- Return JSON response with service status
- Include timestamp in response
```

## Branch Naming

Use the following branch naming conventions:

- `feature/<description>` - New features
- `bugfix/<description>` - Bug fixes
- `docs/<description>` - Documentation updates
- `refactor/<description>` - Code refactoring
- `test/<description>` - Test additions or updates
- `chore/<description>` - Maintenance tasks

Examples:
```
feature/clustering-endpoint
bugfix/data-upload-validation
docs/api-documentation
refactor/user-model
```

### Creating a Branch

```bash
# Create and checkout a new branch
git checkout -b feature/your-feature-name

# Or create and checkout in two steps
git branch feature/your-feature-name
git checkout feature/your-feature-name
```

### Keeping Your Branch Updated

```bash
# Fetch latest changes from upstream
git fetch upstream

# Merge upstream changes into your branch
git merge upstream/main

# Or rebase your branch on top of upstream/main
git rebase upstream/main
```

## Pull Request Process

### Before Creating a Pull Request

1. **Ensure your code is up to date**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests and linting**
   ```bash
   # Backend
   cd backend
   pytest
   flake8

   # Frontend
   cd frontend
   npm test
   npm run lint
   ```

3. **Update documentation** if needed

4. **Squash commits** if you have many small commits
   ```bash
   git rebase -i HEAD~<number_of_commits>
   ```

### Creating a Pull Request

1. Push your branch to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a pull request on GitHub
   - Go to https://github.com/originalusername/kmeans-engine/pulls
   - Click "New Pull Request"
   - Select your branch from the dropdown
   - Fill in the PR template

3. **PR Template**
   ```markdown
   ## Description
   Brief description of the changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No new warnings generated
   - [ ] All tests pass
   ```

### Pull Request Review

- Be responsive to review feedback
- Address all review comments
- Update your branch as needed
- Request review again after changes

## Project Phases

This project follows a structured development plan organized into phases. See [`.planning/ROADMAP.md`](.planning/ROADMAP.md) for the complete roadmap.

### Current Phase Planning

- Phase plans are in `.planning/phases/XX-phase-name/`
- Each phase has multiple plans (e.g., 01-01, 01-02, 01-03)
- Plans are executed sequentially within each phase
- Each plan has a summary document (SUMMARY.md)

### Phase Reference

When working on specific phases, reference the phase number and plan number:

```
feat(01-03): create Git repository initialization

- Initialize Git with .gitignore
- Add project documentation files
- Create initial baseline commit
```

## Testing

### Backend Tests

```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest -k test_cluster    # Run specific tests
pytest --coverage         # Run with coverage
```

### Frontend Tests

```bash
cd frontend
npm test                  # Run all tests
npm test -- --watch       # Watch mode
npm test -- --coverage    # With coverage
```

### Integration Tests

```bash
# Run all tests across the project
npm run test:all
```

### Writing Tests

- Write tests for new features
- Aim for high test coverage
- Use descriptive test names
- Test edge cases and error conditions

Example:
```python
def test_cluster_data_with_valid_input():
    """Test clustering with valid input data."""
    data = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [5, 4, 3, 2, 1]})
    result = cluster_data(data, n_clusters=2)
    assert "labels" in result
    assert "centroids" in result
    assert len(result["labels"]) == len(data)
```

## Questions and Support

If you have questions:

1. Check existing documentation
2. Search existing issues
3. Read the project roadmap in [`.planning/ROADMAP.md`](.planning/ROADMAP.md)
4. Create a new issue if needed

### Issue Templates

When creating issues, use the appropriate template:

- **Bug Report**: For reporting bugs
- **Feature Request**: For suggesting new features
- **Documentation**: For documentation issues
- **Question**: For general questions

## Code of Conduct

Be respectful and constructive in all interactions:
- Welcome new contributors
- Provide helpful feedback
- Assume good intentions
- Focus on what is best for the community

---

Thank you for contributing to KMeans Engine!
