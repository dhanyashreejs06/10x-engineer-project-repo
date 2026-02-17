# PromptLab

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-lightgreen)

## Overview

PromptLab is an AI Prompt Engineering Platform designed to help AI engineers store, organize, and manage their prompts efficiently. It's like a "Postman for Prompts," providing a structured workspace to:

- Create, Read, Update, and Delete (CRUD) prompt templates.
- Organize prompts into collections.
- Search, filter, and sort through prompts with ease.

## Features

- **CRUD operations** for managing prompts and collections.
- Easy **search, filter, and sorting** functionalities.

## Prerequisites

- Python 3.10+
- pip

## Installation

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd promptlab
   ```

2. **Navigate to the backend directory and set up the environment:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

The API runs at: http://localhost:8000
API documentation is available at: http://localhost:8000/docs

## Quick Start Guide

To interact with the API, you can use `curl` commands. Here are some examples:

- **Check health:**
  ```bash
  curl -X GET http://localhost:8000/health
  ```

- **Get all prompts:**
  ```bash
  curl -X GET http://localhost:8000/prompts
  ```

- **Create a new prompt:**
  ```bash
  curl -X POST http://localhost:8000/prompts -H "Content-Type: application/json" -d '{"title": "New Prompt", "content": "Prompt content here"}'
  ```

## API Endpoint Summary

| Method | Path                 | Description           |
|--------|----------------------|-----------------------|
| GET    | `/health`            | Health check endpoint |
| GET    | `/prompts`           | Retrieve all prompts  |
| GET    | `/prompts/{id}`      | Retrieve a specific prompt by ID |
| POST   | `/prompts`           | Create a new prompt   |
| PUT    | `/prompts/{id}`      | Update an existing prompt by ID |
| PATCH  | `/prompts/{id}`      | Partially update a prompt by ID |
| DELETE | `/prompts/{id}`      | Delete a specific prompt by ID |
| GET    | `/collections`       | Retrieve all collections |
| GET    | `/collections/{id}`  | Retrieve a specific collection by ID |
| POST   | `/collections`       | Create a new collection |
| DELETE | `/collections/{id}`  | Delete a specific collection by ID |

## Development Setup

To set up a development environment, follow these steps:

1. Ensure you have Python 3.10+ installed.
2. Clone the repository and navigate to the `backend` directory.
3. Install required dependencies with `pip install -r requirements.txt`.

## Running Tests

Execute the following command to run tests:

```bash
cd backend
pytest tests/ -v
```

## Project Structure

```
promptlab/
├── README.md                    # Project documentation
├── backend/
│   ├── app/
│   │   ├── api.py              # API routes
│   │   ├── models.py           # Data models
│   │   ├── storage.py          # Storage logic
│   │   └── utils.py            # Utility functions
│   ├── tests/
│   │   └── test_api.py         # Test cases
│   └── main.py                 # Application entry point
└── requirements.txt            # Dependency list
```

## Contributing

We welcome contributions from the community! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

### Summary

PromptLab is designed to streamline prompt management with features like CRUD operations, collections, and robust search & filter capabilities. It's built with Python and FastAPI, ensuring a modern and efficient tech stack. Join us in enhancing PromptLab by contributing your expertise!