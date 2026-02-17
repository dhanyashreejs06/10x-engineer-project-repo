"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """Handles in-memory storage for prompts and collections.

    Attributes:
        _prompts: A dictionary to store prompts by their unique IDs.
        _collections: A dictionary to store collections by their unique IDs.
    """
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Add a new prompt to storage.
        
        Args:
            prompt (Prompt): The prompt instance to store.
            
        Returns:
            Prompt: The stored prompt instance.
            
        Example:
            >>> new_prompt = Prompt(id='123', title='Example')
            >>> storage.create_prompt(new_prompt)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a stored prompt by its ID.
        
        Args:
            prompt_id (str): The unique identifier for the prompt.
            
        Returns:
            Optional[Prompt]: The prompt instance if found, None otherwise.
            
        Example:
            >>> prompt = storage.get_prompt('123')
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Get a list of all stored prompts.

        Returns:
            List[Prompt]: A list of all prompt instances stored.
            
        Example:
            >>> all_prompts = storage.get_all_prompts()
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update a stored prompt by its ID.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt (Prompt): The new prompt data.
            
        Returns:
            Optional[Prompt]: The updated prompt instance if found, None otherwise.
            
        Example:
            >>> updated_prompt = Prompt(id='123', title='Updated')
            >>> storage.update_prompt('123', updated_prompt)
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Remove a stored prompt by its ID.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.
            
        Returns:
            bool: True if the prompt was deleted, False if not found.
            
        Example:
            >>> storage.delete_prompt('123')
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Add a new collection to storage.
        
        Args:
            collection (Collection): The collection instance to store.
            
        Returns:
            Collection: The stored collection instance.
            
        Example:
            >>> new_collection = Collection(id='col1', title='Examples')
            >>> storage.create_collection(new_collection)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a stored collection by its ID.
        
        Args:
            collection_id (str): The unique identifier for the collection.
            
        Returns:
            Optional[Collection]: The collection instance if found, None otherwise.
            
        Example:
            >>> collection = storage.get_collection('col1')
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Get a list of all stored collections.

        Returns:
            List[Collection]: A list of all collection instances stored.
            
        Example:
            >>> all_collections = storage.get_all_collections()
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Remove a stored collection by its ID.

        Args:
            collection_id (str): The unique identifier of the collection to delete.
            
        Returns:
            bool: True if the collection was deleted, False if not found.
            
        Example:
            >>> storage.delete_collection('col1')
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Get a list of prompts belonging to a specific collection.
        
        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            List[Prompt]: A list of prompts that belong to the specified collection.
            
        Example:
            >>> prompts_in_col = storage.get_prompts_by_collection('col1')
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all stored prompts and collections, resetting the storage.
        
        Example:
            >>> storage.clear()
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
