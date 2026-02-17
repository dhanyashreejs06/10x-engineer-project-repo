# API Reference for PromptLab

## Overview
- **Base URL**: `/`
- **Content Type**: `application/json`
- **Response Format**: JSON

## Authentication
- **Authentication**: None

---

## Endpoints

### Health Check

- **Method**: `GET`
- **Path**: `/health`
- **Description**: Check the health status of the application.

  **Response Example**
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

  **Potential Error Responses**: None

---

### List Prompts

- **Method**: `GET`
- **Path**: `/prompts`
- **Description**: Retrieve a list of prompts, optionally filtering by collection ID and search query.

  **Query Parameters**
  | Name | Type    | Description                                 |
  |------|---------|---------------------------------------------|
  | collection_id | string  | The ID of the collection to filter prompts. |
  | search        | string  | A search term to filter the prompt list.    |

  **Response Example**

  ```json
  {
    "prompts": [
      {"id": "uuid-1", "title": "Example Prompt", "content": "Hello World", "description": "A basic example", "collection_id": "col-1", "created_at": "2023-10-11T00:00:00Z", "updated_at": "2023-10-11T00:00:00Z"}
    ],
    "total": 1
  }
  ```

  **Potential Error Responses**: None

---

### Get Prompt by ID

- **Method**: `GET`
- **Path**: `/prompts/{prompt_id}`
- **Description**: Retrieve a prompt by its ID.

  **Path Parameters**
  | Name     | Type   | Description              |
  |----------|--------|--------------------------|
  | prompt_id | string | The ID of the prompt.     |

  **Response Example**

  ```json
  {"id": "uuid-1", "title": "Example Prompt", "content": "Hello World", "description": "A basic example", "collection_id": "col-1", "created_at": "2023-10-11T00:00:00Z", "updated_at": "2023-10-11T00:00:00Z"}
  ```

  **Potential Error Responses**
  - `404`: Prompt not found if the prompt ID does not exist.

---

### Create Prompt

- **Method**: `POST`
- **Path**: `/prompts`
- **Description**: Create a new prompt.

  **Request Body**

  ```json
  {
    "title": "New Prompt",
    "content": "Example content",
    "description": "An optional description",
    "collection_id": "col-1"
  }
  ```

  **Response Example** (201 Created)

  ```json
  {"id": "uuid-2", "title": "New Prompt", "content": "Example content", "description": "An optional description", "collection_id": "col-1", "created_at": "2023-10-11T00:00:00Z", "updated_at": "2023-10-11T00:00:00Z"}
  ```

  **Potential Error Responses**
  - `400`: Collection not found if the specified collection ID is invalid.

---

### Update Prompt

- **Method**: `PUT`
- **Path**: `/prompts/{prompt_id}`
- **Description**: Update an existing prompt by its ID.

  **Path Parameters**
  | Name     | Type   | Description          |
  |----------|--------|----------------------|
  | prompt_id | string | The ID of the prompt. |

  **Request Body**
  ```json
  {
    "title": "Updated Title",
    "content": "Updated Content"
  }
  ```

  **Response Example**
  ```json
  {"id": "uuid-1", "title": "Updated Title", "content": "Updated Content", "description": "An updated description", "collection_id": "col-1", "created_at": "2023-10-11T00:00:00Z", "updated_at": "2023-10-11T01:00:00Z"}
  ```

  **Potential Error Responses**
  - `404`: Prompt not found
  - `400`: Collection not found if the collection_id is invalid

---

### Partially Update Prompt

- **Method**: `PATCH`
- **Path**: `/prompts/{prompt_id}`
- **Description**: Partially update a prompt by its ID.

  **Path Parameters**
  | Name     | Type   | Description          |
  |----------|--------|----------------------|
  | prompt_id | string | The ID of the prompt. |

  **Request Body Example**

  ```json
  {
    "title": "Partially Updated Title"
  }
  ```

  **Response Example**
  ```json
  {"id": "uuid-1", "title": "Partially Updated Title", "content": "Updated Content", "description": "An updated description", "collection_id": "col-1", "created_at": "2023-10-11T00:00:00Z", "updated_at": "2023-10-11T01:00:00Z"}
  ```

  **Potential Error Responses**
  - `404`: Prompt not found
  - `400`: Collection not found if the collection_id is invalid

---

### Delete Prompt

- **Method**: `DELETE`
- **Path**: `/prompts/{prompt_id}`
- **Description**: Delete a prompt by its ID.

  **Path Parameters**
  | Name     | Type   | Description           |
  |----------|--------|-----------------------|
  | prompt_id | string | The ID of the prompt.  |

  **Response**: None (204 No Content)

  **Potential Error Responses**
  - `404`: Prompt not found

---

### List Collections

- **Method**: `GET`
- **Path**: `/collections`
- **Description**: Retrieve a list of all collections.

  **Response Example**
  ```json
  {
    "collections": [
      {"id": "col-1", "name": "Example Collection", "description": "A collection of examples", "created_at": "2023-10-10T00:00:00Z"}
    ],
    "total": 1
  }
  ```

  **Potential Error Responses**: None

---

### Get Collection by ID

- **Method**: `GET`
- **Path**: `/collections/{collection_id}`
- **Description**: Retrieve a collection by its ID.

  **Path Parameters**
  | Name          | Type   | Description                |
  |---------------|--------|----------------------------|
  | collection_id | string | The ID of the collection.  |

  **Response Example**
  ```json
  {"id": "col-1", "name": "Example Collection", "description": "A collection of examples", "created_at": "2023-10-10T00:00:00Z"}
  ```

  **Potential Error Responses**
  - `404`: Collection not found

---

### Create Collection

- **Method**: `POST`
- **Path**: `/collections`
- **Description**: Create a new collection.

  **Request Body**
  ```json
  {
    "name": "New Collection",
    "description": "A new collection description"
  }
  ```

  **Response Example** (201 Created)
  ```json
  {"id": "col-1", "name": "New Collection", "description": "A new collection description", "created_at": "2023-10-10T00:00:00Z"}
  ```

  **Potential Error Responses**: None

---

### Delete Collection

- **Method**: `DELETE`
- **Path**: `/collections/{collection_id}`
- **Description**: Delete a collection by its ID and handle related prompts.

  **Path Parameters**
  | Name          | Type   | Description                |
  |---------------|--------|----------------------------|
  | collection_id | string | The ID of the collection.  |

  **Response**: None (204 No Content)

  **Potential Error Responses**
  - `404`: Collection not found

---
---
## Error Response Format

All error responses are returned in the following structure:

```json
{
  "detail": "Error message here"
}
```

- **404 Not Found**: Indicates that a requested resource could not be found.
- **400 Bad Request**: Indicates a request error such as invalid input data.
