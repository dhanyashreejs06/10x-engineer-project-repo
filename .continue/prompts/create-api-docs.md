---
name: create-api-docs
description: Generate complete API reference
invokable: true
---

Create comprehensive API documentation in markdown format by analyzing backend/app/api.py.

For EVERY endpoint document:
- HTTP method and full path
- Description of what it does
- Path parameters (if any) in table format
- Query parameters (if any) in table format  
- Request body structure with JSON example (if applicable)
- Success response with status code and full JSON example
- All possible error responses (404, 400, 422) with when they occur

Also include:
- Overview section (base URL, content type, response format)
- Error response format explanation
- Authentication section (state "None" if not implemented)

Use realistic example data that matches the models in models.py.