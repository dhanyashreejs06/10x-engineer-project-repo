from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a new unique identifier."""
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC time.

    Returns:
        datetime: The current datetime in UTC.

    Example:
        >>> current_time = get_current_time()
        >>> print(current_time)
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for a prompt with title, content, and optional description.
    
    Attributes:
        title (str): The title of the prompt with a maximum length of 200.
        content (str): The content of the prompt with no maximum length.
        description (Optional[str]): An optional description of the prompt with a maximum length of 500.
        collection_id (Optional[str]): The ID of the associated collection.
        tags (List[str]): A list of string tags for categorizing the prompt.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class PromptCreate(PromptBase):
    """Model for creating a new prompt, inheriting all fields from PromptBase."""
    pass


class PromptUpdate(PromptBase):
    """Model for updating a prompt, inheriting all fields from PromptBase."""
    pass


class PromptPatch(BaseModel):
    """Model for partially updating a prompt, allowing optional fields.
    
    Attributes:
        title (Optional[str]): An optional new title for the prompt with a maximum length of 200.
        content (Optional[str]): Optional new content for the prompt.
        description (Optional[str]): An optional new description with a maximum length of 500.
        collection_id (Optional[str]): An optional new collection ID.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: Optional[List[str]] = None


class Prompt(PromptBase):
    """Represents a fully detailed prompt model with a unique ID and timestamps.
    
    Attributes:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Timestamp of when the prompt was created.
        updated_at (datetime): Timestamp of the last update to the prompt.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for a collection with a name and description.
    
    Attributes:
        name (str): The name of the collection with a maximum length of 100.
        description (Optional[str]): An optional description of the collection with a maximum length of 500.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new collection, inheriting all fields from CollectionBase."""
    pass


class Collection(CollectionBase):
    """Represents a fully detailed collection model with a unique ID and timestamp.
    
    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp of when the collection was created.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model for a list of prompts.
    
    Attributes:
        prompts (List[Prompt]): A list of prompt instances.
        total (int): Total number of prompts available.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Response model for a list of collections.
    
    Attributes:
        collections (List[Collection]): A list of collection instances.
        total (int): Total number of collections available.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model representing the health status of the application.
    
    Attributes:
        status (str): The current status of the application.
        version (str): The application version.
    """
    status: str
    version: str