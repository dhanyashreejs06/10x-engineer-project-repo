# PromptLab

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-lightgreen)

## Project Overview and Purpose

PromptLab is a comprehensive AI Prompt Engineering Platform designed to assist AI engineers in storing, organizing, and managing their prompts efficiently. It offers a structured workspace similar to "Postman for Prompts" with features to manage different versions and associated metadata.

## Features List

- **Prompt Management API Endpoints**:
  - ✅ Create, read, update, and delete prompts
  - 📋 Support for hierarchical prompt organization in future iterations
  - ✅ In-memory storage, with plans for database integration

## Prerequisites and Installation

Ensure you have Python 3.10+ installed. Set up the project using the following commands:

```bash
git clone <your-repo-url>
cd promptlab
python -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
```

## Quick Start Guide

To run the server:

```bash
cd backend
python main.py
# Open http://localhost:8000 in your browser
```

## API Endpoint Summary with Examples

| Method | Path                                | Description                              | Example Command                                                    |
|--------|-------------------------------------|------------------------------------------|-------------------------------------------------------------------|
| GET    | `/health`                           | Health check endpoint                    | `curl -X GET http://localhost:8000/health`                         |
| GET    | `/prompts`                          | Retrieve all prompts                     | `curl -X GET http://localhost:8000/prompts`                        |
| GET    | `/prompts/{prompt_id}`              | Retrieve a specific prompt by ID         | `curl -X GET http://localhost:8000/prompts/1`                      |
| POST   | `/prompts`                          | Create a new prompt                      | `curl -X POST -d '{\"title\": \"New Prompt\"}' http://localhost:8000/prompts` |
| PUT    | `/prompts/{prompt_id}`              | Update an existing prompt by ID          | `curl -X PUT -d '{\"title\": \"Updated\"}' http://localhost:8000/prompts/1`  |
| PATCH  | `/prompts/{prompt_id}`              | Partially update a prompt by ID          | `curl -X PATCH ...` (Replace with appropriate data)                |
| DELETE | `/prompts/{prompt_id}`              | Delete a specific prompt by ID           | `curl -X DELETE http://localhost:8000/prompts/1`                   |
| GET    | `/collections`                      | Retrieve all collections                 | `curl -X GET http://localhost:8000/collections`                    |
| GET    | `/collections/{collection_id}`      | Retrieve a specific collection by ID     | `curl -X GET http://localhost:8000/collections/1`                  |
| POST   | `/collections`                      | Create a new collection                  | `curl -X POST -d '{\"name\": \"New Collection\"}' http://localhost:8000/collections` |
| DELETE | `/collections/{collection_id}`      | Delete a specific collection by ID       | `curl -X DELETE http://localhost:8000/collections/1`               |

## Development Setup

To set up a development environment:

1. Ensure Python 3.10+ is installed.
2. Clone the repository and navigate to the `backend` directory.
3. Install the required packages using `pip install -r requirements.txt`.

## Running Tests

Run tests using:

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app
```

## Project Structure

```
promptlab/
├── README.md                  # Project documentation
├── .continue/                 # AI prompt continuation files
│   ├── rules/                 # Custom coding instructions
│   │   └── custom-coding-instructions.md
│   └── prompts/               # Prompt creation guidelines
│       ├── create-api-docs.md
│       ├── add-docstrings.md
│       └── create-feature-spec.md
├── .devcontainer/             # VSCode dev container configuration
│   ├── setup.sh
│   └── devcontainer.json
├── backend/
│   ├── app/                   # Core backend application
│   │   ├── __init__.py        # Initialization script for package
│   │   ├── api.py             # API endpoints for FastAPI
│   │   ├── models.py          # Pydantic models for data validation
│   │   ├── storage.py         # In-memory data storage logic
│   │   └── utils.py           # Utility functions and business logic
│   ├── main.py                # Main application entry point
│   ├── requirements.txt       # Dependencies and package requirements
│   ├── tests/                 # Unit and integration tests
│   │   ├── __init__.py        # Initialization for tests package
│   │   ├── conftest.py        # Fixtures and test setup
│   │   └── test_api.py        # Test cases for API endpoints
│   └── .pytest_cache/         # Cache directory for pytest
├── docs/
│   ├── .gitkeep               # Placeholder for version control
│   └── API_REFERENCE.md       # Detailed breakdown of API
├── frontend/
│   └── .gitkeep               # Placeholder for future frontend
├── specs/                     # Specifications and technical requirements
│   ├── .gitkeep               # Placeholder for version control
│   ├── prompt-versions.md     # Document on prompt versions
│   └── tagging-system.md      # Document on tagging system
└── PROJECT_BRIEF.md           # Brief of the project requirements
```

## Documentation Links

- [API Reference](docs/API_REFERENCE.md)
- [Prompt Versions Specification](specs/prompt-versions.md)
- [Tagging System Specification](specs/tagging-system.md)

## Roadmap

- **Near-Term Goals**:
  - Implement a system for hierarchical prompt organization.
  - Transition storage from in-memory to a robust database solution.
  - Write comprehensive tests.  <!-- New addition -->
  - Implement new features with TDD.  <!-- New addition -->
  - Set up CI/CD and Docker.  <!-- New addition -->

- **Long-Term Aspirations**:
  - Develop a user-friendly, comprehensive frontend interface.
  - Integrate real-time prompt evaluation with AI models to enhance development feedback.
  - Expand user roles and permissions for better collaboration.
  - Create a React frontend.  <!-- New addition -->
  - Connect it to the backend.  <!-- New addition -->
  - Polish the user experience.  <!-- New addition -->

## Contributing Guidelines

To contribute to PromptLab:

1. Fork the repository.
2. Create a new branch for a feature or bugfix.
3. Submit a pull request with a clear description and documentation of your changes.

### Summary

PromptLab streamlines prompt management with CRUD operations, collection management, and search capabilities, ensuring a sound and modern tech stack with Python and FastAPI. We welcome contributions to further enhance its capabilities.