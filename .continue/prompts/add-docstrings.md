---
name: add-docstrings
description: Add Google-style docstrings to all functions and classes
invokable: true
---

Add comprehensive Google-style docstrings to every function and class in this file.
DO NOT change any existing code unless explicitly mentioned

For each function include:
- Brief description of what it does
- Args section listing each parameter with its type and description
- Returns section with return type and description
- Example section showing how to use it

For each class include:
- Brief description of what the class represents
- Attributes section describing all fields

Example format:
```python
def get_prompt(prompt_id: str) -> Optional[Prompt]:
    """Retrieve a prompt by its ID.
    
    Args:
        prompt_id: UUID string of the prompt to retrieve.
        
    Returns:
        Prompt: The prompt object if found, None otherwise.
        
    Example:
        >>> prompt = get_prompt("abc-123")
        >>> print(prompt.title)
    """
```

Analyze the existing code to write accurate descriptions.