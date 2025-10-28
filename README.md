# 🧮 FastAPI Calculator Application

A modern web-based calculator built with FastAPI, featuring a RESTful API and web interface for performing basic arithmetic operations.

## ✨ Features

- **Basic Operations**: Addition, Subtraction, Multiplication, Division
- **Web Interface**: User-friendly HTML calculator
- **RESTful API**: JSON-based endpoints for programmatic access
- **Comprehensive Testing**: Unit, Integration, and End-to-End tests
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **Security Scanning**: Trivy vulnerability scanning

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: HTML, JavaScript
- **Testing**: pytest, Playwright
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Security**: Trivy scanner

---

# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. Docker Setup


## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

---

# 🚀 Running the Project

## Development Mode

- **Start the server**:

```bash
python main.py
```

The application will be available at `http://localhost:8000`

- **With virtual environment**:

```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows
python main.py
```

## Production Mode (Docker)

```bash
# Build the image
docker build -t calculator-app .

# Run the container
docker run -p 8000:8000 calculator-app
```

## Using Docker Compose

```bash
docker-compose up -d
```

---

# 📚 API Documentation

## Endpoints

### Addition
- **POST** `/add`
- **Request**: `{"a": 10, "b": 5}`
- **Response**: `{"result": 15}`

### Subtraction
- **POST** `/subtract`
- **Request**: `{"a": 10, "b": 5}`
- **Response**: `{"result": 5}`

### Multiplication
- **POST** `/multiply`
- **Request**: `{"a": 10, "b": 5}`
- **Response**: `{"result": 50}`

### Division
- **POST** `/divide`
- **Request**: `{"a": 10, "b": 2}`
- **Response**: `{"result": 5.0}`

### Error Handling
- **Division by Zero**: Returns `400` with `{"error": "Cannot divide by zero!"}`
- **Invalid Input**: Returns `400` with validation error details

## Example API Usage

```bash
# Addition
curl -X POST "http://localhost:8000/add" \
     -H "Content-Type: application/json" \
     -d '{"a": 10, "b": 5}'

# Division by zero
curl -X POST "http://localhost:8000/divide" \
     -H "Content-Type: application/json" \
     -d '{"a": 10, "b": 0}'
```

---

# 🧪 Testing

## Test Types

### Unit Tests
Test individual functions in isolation:
```bash
pytest tests/unit/ --cov=app --cov-report=html
```

### Integration Tests
Test API endpoints with TestClient:
```bash
pytest tests/integration/ --cov=app --cov-append
```

### End-to-End Tests
Test complete user workflows with Playwright:
```bash
pytest tests/e2e/ --cov=app --cov-append
```

## Running All Tests

```bash
# Run all tests with coverage
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# Run specific test categories
pytest -m "not e2e"  # Skip E2E tests
pytest -m "e2e"       # Only E2E tests
```

## Coverage Requirements

- **Unit Tests**: 100% coverage required
- **Integration Tests**: API endpoint coverage
- **E2E Tests**: User workflow validation

---

# 🏗️ Project Structure

```
module8_is601/
├── app/
│   └── operations/          # Calculator functions
│       └── __init__.py
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # API integration tests
│   ├── e2e/               # End-to-end tests
│   └── conftest.py        # Test fixtures
├── templates/
│   └── index.html         # Web interface
├── .github/workflows/     # CI/CD pipeline
├── main.py               # FastAPI application
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-container setup
├── requirements.txt     # Python dependencies
└── pytest.ini         # Test configuration
```

---

# 🔄 CI/CD Pipeline

## GitHub Actions Workflow

The project uses GitHub Actions for automated testing and deployment:

### Test Job
- **Python Setup**: Python 3.10
- **Dependencies**: Install requirements and Playwright
- **Test Execution**: Unit, Integration, and E2E tests
- **Coverage**: Generate coverage reports

### Security Job
- **Docker Build**: Build application image
- **Trivy Scan**: Vulnerability scanning
- **Severity**: CRITICAL and HIGH vulnerabilities block deployment

### Deploy Job
- **Docker Hub**: Push to registry
- **Multi-platform**: linux/amd64, linux/arm64
- **Tags**: latest and commit SHA

## Manual Deployment

```bash
# Build and push to Docker Hub
docker build -t yourusername/calculator-app .
docker push yourusername/calculator-app
```

---

# 🛡️ Security

## Vulnerability Scanning

The project uses Trivy for security scanning:

- **Automated**: Runs on every CI/CD pipeline
- **Severity Levels**: CRITICAL and HIGH vulnerabilities block deployment
- **Ignored CVEs**: Listed in `.trivyignore`

## Security Best Practices

- **Non-root User**: Application runs as `appuser`
- **Minimal Image**: Uses Python slim base image
- **Dependency Updates**: Regular security updates
- **Input Validation**: Pydantic models validate all inputs

---

# 🐛 Troubleshooting

## Common Issues

### Port Already in Use
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Docker Build Fails
```bash
# Clean Docker cache
docker system prune -a
```

### Tests Fail
```bash
# Install Playwright browsers
playwright install
```

### Permission Denied
```bash
# Fix file permissions
chmod +x scripts/*
```

## Error Messages

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Port 8000 already in use` | Kill existing process or use different port |
| `Docker permission denied` | Add user to docker group or use sudo |

---


# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- Install **Docker** to run this project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
