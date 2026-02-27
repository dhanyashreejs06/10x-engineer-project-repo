"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check the health status of the application.

    Returns:
        HealthResponse: An object containing the status and version of the application.

    Example:
        >>> response = health_check()
        >>> print(response.status)
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tag: Optional[str] = None
):
    """Retrieve a list of prompts, optionally filtering by collection ID, search query, and tag.

    Args:
        collection_id (Optional[str]): The ID of the collection to filter prompts. Defaults to None.
        search (Optional[str]): A search term to filter the prompt list. Defaults to None.
        tag (Optional[str]): A tag to filter the prompt list. Defaults to None.

    Returns:
        PromptList: A list of prompts with the total count.

    Example:
        >>> prompts = list_prompts(collection_id="123", search="greeting", tag="python")
        >>> for prompt in prompts.prompts:
        ...     print(prompt.title)
    """
    prompts = storage.get_all_prompts()

    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)

    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)

    # Filter by tag if specified
    if tag:
        prompts = [p for p in prompts if tag in p.tags]

    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)

    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to retrieve.

    Returns:
        Prompt: The prompt object if found.

    Raises:
        HTTPException: If the prompt is not found, raises a 404 error.
    """
    prompt = storage.get_prompt(prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Args:
        prompt_data (PromptCreate): Data required to create a new prompt.

    Returns:
        Prompt: The created prompt object.

    Raises:
        HTTPException: If the specified collection is not found, raises a 400 error.

    Example:
        >>> prompt_data = PromptCreate(title="New Prompt", content="Example content")
        >>> new_prompt = create_prompt(prompt_data)
        >>> print(new_prompt.id)
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Update an existing prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): Data to update the prompt.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or specified collection is not found, raises a 404/400 error.

    Example:
        >>> updated_data = PromptUpdate(title="Updated Title")
        >>> updated_prompt = update_prompt("abc-123", updated_data)
        >>> print(updated_prompt.title)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        tags=prompt_data.tags,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Partially update a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptPatch): Data for partial update.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or specified collection is not found, raises a 404/400 error.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Extract only the fields that were actually sent in the request
    updated_fields = prompt_data.model_dump(exclude_unset=True)

    # Validate collection if it's being updated
    if 'collection_id' in updated_fields:
        collection = storage.get_collection(updated_fields['collection_id'])
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Merge existing fields with updated fields
    updated_prompt = Prompt(
        id=existing.id,
        title=updated_fields.get('title', existing.title),
        content=updated_fields.get('content', existing.content),
        description=updated_fields.get('description', existing.description),
        collection_id=updated_fields.get('collection_id', existing.collection_id),
        tags=updated_fields.get('tags', existing.tags),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Returns:
        None: Successfully returns None when the prompt is deleted.

    Raises:
        HTTPException: If the prompt is not found, raises a 404 error.

    Example:
        >>> delete_prompt("abc-123")
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Retrieve a list of all collections.

    Returns:
        CollectionList: A list containing all collections and the total number of collections.

    Example:
        >>> collections_list = list_collections()
        >>> print(collections_list.total)
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by its ID.

    Args:
        collection_id (str): The ID of the collection to retrieve.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: If the collection is not found, raises a 404 error.

    Example:
        >>> collection = get_collection("123")
        >>> print(collection.name)
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection_data (CollectionCreate): The data required to create a new collection.

    Returns:
        Collection: The created collection object.

    Example:
        >>> new_collection_data = CollectionCreate(name="New Collection")
        >>> new_collection = create_collection(new_collection_data)
        >>> print(new_collection.id)
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection by its ID and handle related prompts.

    Args:
        collection_id (str): The ID of the collection to delete.

    Returns:
        None

    Raises:
        HTTPException: If the collection is not found, raises a 404 error.
    """
    if not storage.get_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    # Delete all prompts belonging to this collection
    prompts = storage.get_all_prompts()
    for prompt in prompts:
        if prompt.collection_id == collection_id:
            storage.delete_prompt(prompt.id)

    storage.delete_collection(collection_id)

    return None