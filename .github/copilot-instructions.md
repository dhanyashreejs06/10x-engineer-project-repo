---
description: Coding assistant
---

# PromptLab Coding Standards

## PROJECT CONTEXT
- Framework: FastAPI (Python 3.10+)
- Validation: Pydantic V2 (NEVER use V1 methods)
- Storage: In-memory dict-based (swappable for database)
- Architecture: Layered (api.py → models.py → storage.py, utils.py)

## CODE QUALITY STANDARDS

### Documentation (MANDATORY)
- Every function MUST have Google-style docstrings
- Include: Description, Args (with types), Returns (with type), Example
- Every class MUST have Attributes section
- Type hints REQUIRED on all function signatures

Example:
```python
def get_prompt(prompt_id: str) -> Optional[Prompt]:
    """Retrieve a prompt by its ID.
    
    Args:
        prompt_id: UUID string of the prompt.
        
    Returns:
        Prompt: The prompt object if found, None otherwise.
        
    Example:
        >>> prompt = get_prompt("abc-123")
    """
```

### Pydantic V2 Usage (CRITICAL)
✅ CORRECT: 
- model.model_dump()
- model.model_dump(exclude_unset=True)
- Model.model_validate(data)

❌ WRONG (deprecated V1):
- model.dict()
- model.parse_obj(data)
- model.schema()

### Python Style
- Follow PEP 8
- Max line length: 100 characters
- f-strings for formatting (not .format() or %)
- Descriptive variable names (no single letters except loops)
- List comprehensions when readable

## ARCHITECTURAL RULES

### Separation of Concerns
- api.py: HTTP handling ONLY (routes, status codes, validation)
- models.py: Pydantic models ONLY
- storage.py: Data persistence ONLY (CRUD operations)
- utils.py: Business logic ONLY (pure functions, no side effects)

❌ NEVER put business logic in api.py
❌ NEVER access storage._prompts or storage._collections directly

### Storage Pattern
✅ ALWAYS use storage methods:
```python
prompt = storage.get_prompt(id)
storage.create_prompt(prompt)
storage.delete_prompt(id)
```

## API ENDPOINT PATTERNS

### Resource Validation (MANDATORY)
✅ ALWAYS check resource exists:
```python
existing = storage.get_prompt(prompt_id)
if not existing:
    raise HTTPException(status_code=404, detail="Prompt not found")
```

❌ NEVER assume resource exists:
```python
prompt = storage.get_prompt(prompt_id)
return prompt  # Could be None!
```

### Foreign Key Validation
✅ ALWAYS validate related resources:
```python
if prompt_data.collection_id:
    collection = storage.get_collection(prompt_data.collection_id)
    if not collection:
        raise HTTPException(status_code=400, detail="Collection not found")
```

### Timestamp Management
✅ ALWAYS update timestamps on PUT/PATCH:
```python
updated_prompt = Prompt(
    id=existing.id,
    created_at=existing.created_at,  # Preserve
    updated_at=get_current_time(),   # NEW
    ...
)
```

### PATCH Endpoints
✅ ALWAYS use exclude_unset=True:
```python
updated_fields = patch_data.model_dump(exclude_unset=True)
title = updated_fields.get('title', existing.title)
```

### CASCADE DELETE
✅ ALWAYS clean up child resources:
```python
# Delete children FIRST
for prompt in storage.get_all_prompts():
    if prompt.collection_id == collection_id:
        storage.delete_prompt(prompt.id)

# Then delete parent
storage.delete_collection(collection_id)
```

## ERROR HANDLING

### Status Codes
- 200: Success (GET, PUT, PATCH)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Invalid input/reference
- 404: Resource not found
- 422: Validation error (Pydantic auto)

### Error Messages
✅ ALWAYS include helpful details:
```python
raise HTTPException(status_code=404, detail="Prompt not found")
raise HTTPException(status_code=400, detail="Collection not found")
```

❌ NEVER use generic messages:
```python
raise HTTPException(status_code=404, detail="Not found")
```

### Guard Clauses
✅ PREFER early returns:
```python
if not prompt:
    raise HTTPException(404, "Prompt not found")

return prompt  # Happy path
```

❌ AVOID deep nesting:
```python
if prompt:
    if prompt.id:
        if prompt.content:
            return prompt
```

## TESTING RULES

### Coverage
- Minimum 80% coverage
- EVERY endpoint: happy path + error cases
- ALWAYS clear storage between tests

### Test Structure
```python
def test_get_prompt_success(client, sample_prompt):
def test_get_prompt_not_found(client):
def test_create_prompt_invalid_collection(client):
```

### Cleanup
```python
@pytest.fixture(autouse=True)
def clear_storage():
    storage.clear()
    yield
    storage.clear()
```

## NAMING CONVENTIONS

- Files: `snake_case.py`
- Tests: `test_<module>.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

## CRITICAL MISTAKES TO AVOID

❌ Using Pydantic V1 methods (dict, parse_obj)
❌ Not validating resource exists
❌ Forgetting timestamp updates
❌ Not handling CASCADE deletes
❌ Skipping docstrings
❌ Missing type hints
❌ Using datetime.now() (use datetime.utcnow())
❌ Business logic in api.py
❌ Accessing storage internals
❌ Not clearing storage in tests
❌ Generic error messages

## WHEN WRITING CODE

1. Check if resource exists before operating on it
2. Validate foreign keys (collection_id)
3. Update timestamps on modifications
4. Use Pydantic V2 methods (model_dump)
5. Add comprehensive docstrings
6. Include type hints
7. Write tests (happy + error paths)
8. Clear storage in test fixtures
9. Return helpful error messages
10. Follow layered architecture
```

