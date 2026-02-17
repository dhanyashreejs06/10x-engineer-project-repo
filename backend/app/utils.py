"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    Args:
        prompts: A list of Prompt objects to sort.
        descending: Boolean flag to determine if sorting should be in descending order. Defaults to True.
        
    Returns:
        A list of Prompt objects sorted by creation date.
        
    Example:
        >>> sorted_prompts = sort_prompts_by_date(prompts, descending=True)
        >>> print(sorted_prompts[0].created_at)
    """
    # Adjust the sort to respect the 'descending' parameter
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by their collection ID.
    
    Args:
        prompts: A list of Prompt objects to filter.
        collection_id: The ID of the collection to filter prompts by.
        
    Returns:
        A list of Prompt objects that belong to the specified collection.
        
    Example:
        >>> filtered_prompts = filter_prompts_by_collection(prompts, 'collection-123')
        >>> print(len(filtered_prompts))
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search for prompts containing a query string in their title or description.
    
    Args:
        prompts: A list of Prompt objects to search through.
        query: A string to search for within the titles and descriptions of prompts.
        
    Returns:
        A list of Prompt objects where the title or description contains the query string.
        
    Example:
        >>> search_results = search_prompts(prompts, 'example')
        >>> print([prompt.title for prompt in search_results])
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate prompt content against specific criteria.
    
    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters

    Args:
        content: The content of the prompt as a string.
        
    Returns:
        A boolean indicating if the content is valid.
        
    Example:
        >>> is_valid = validate_prompt_content('This is a valid prompt.')
        >>> print(is_valid)
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are identified by the format {{variable_name}}.

    Args:
        content: The content of the prompt as a string.
        
    Returns:
        A list of strings representing variable names extracted from the content.
        
    Example:
        >>> variables = extract_variables('Hello, {{name}}!')
        >>> print(variables)
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
