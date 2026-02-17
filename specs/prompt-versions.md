# Feature Specification: Prompt Versions

## 1. Overview
The "Prompt Versions" feature allows users to save and retrieve different versions of prompts they create, ensuring that they can evolve and refine their ideas over time. This functionality is valuable for users who want to keep track of iterations and changes, facilitating better content management and increased productivity.

## 2. User Stories

### Story 1
- **As a** user,
- **I want** to save a new version of a prompt,
- **So that** I can keep track of changes and revert if necessary.

  **Acceptance Criteria**:
  - User can save a prompt with a version tag.
  - User receives confirmation upon successful save.

### Story 2
- **As a** user,
- **I want** to view the list of all versions of a specific prompt,
- **So that** I can choose which one to revert to or edit.

  **Acceptance Criteria**:
  - User can request a list of prompt versions.
  - List includes version numbers, timestamps, and brief summaries.

### Story 3
- **As a** user,
- **I want** to revert to a previous version of a prompt,
- **So that** I can recover a version I prefer.

  **Acceptance Criteria**:
  - User can select a version and set it as the current prompt.
  - Confirmation message is shown after successful revert.

### Story 4
- **As a** user,
- **I want** to delete a specific version of a prompt,
- **So that** I can manage storage and keep only relevant versions.

  **Acceptance Criteria**:
  - System allows deletion of specified versions.
  - User is notified when a version is deleted.

### Story 5
- **As a** user,
- **I want** to edit a previous version and save it as a new version,
- **So that** I can create a new variant of a prompt from an old version.

  **Acceptance Criteria**:
  - User can load, edit, and save a version as new.
  - Notifications are provided on save success.

## 3. Data Model Changes
```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PromptVersion(BaseModel):
    prompt_id: int
    content: str
    version: int
    timestamp: datetime
    summary: Optional[str] = None

class Prompt(BaseModel):
    id: int
    title: str
    current_version: PromptVersion
    versions: List[PromptVersion]
```

## 4. New API Endpoints

### Save Prompt Version
- **Method**: POST
- **Path**: `/api/prompts/{prompt_id}/versions`
- **Request Body**:
  ```json
  {
      "content": "string",
      "summary": "string"
  }
  ```
- **Response**:
  ```json
  {
      "message": "Version saved successfully."
  }
  ```

### List Prompt Versions
- **Method**: GET
- **Path**: `/api/prompts/{prompt_id}/versions`
- **Response**:
  ```json
  [
      {
          "version": 1,
          "timestamp": "2023-10-08T11:12:00",
          "summary": "Initial version"
      }
  ]
  ```

### Revert to Prompt Version
- **Method**: PUT
- **Path**: `/api/prompts/{prompt_id}/versions/{version_id}/revert`
- **Response**:
  ```json
  {
      "message": "Reverted to version {version_id}."
  }
  ```

### Delete Prompt Version
- **Method**: DELETE
- **Path**: `/api/prompts/{prompt_id}/versions/{version_id}`
- **Response**:
  ```json
  {
      "message": "Version deleted successfully."
  }
  ```

## 5. Updated Existing Endpoints
Currently, no existing endpoints require updates for this feature.

## 6. Storage Changes
- Implement a new database table called `PromptVersions` to hold versioning details.
- Update existing storage mechanisms to maintain a list of prompt versions alongside each prompt.

## 7. Edge Cases
| Scenario                                              | Handling Method                                                         |
|-------------------------------------------------------|------------------------------------------------------------------------|
| User attempts to save without content                 | Prompt user for content entry, fail save operation.                    |
| User deletes the current active version               | Prevent deletion, offer alternative handling to switch active version. |
| User reverts to a non-existent version                | Return error message and suggest checking available versions.         |
| Large number of versions impacting performance        | Implement pagination for version lists.                                |

## 8. Implementation Order
1. Design and implement the `PromptVersion` and `Prompt` models.
2. Create the `PromptVersions` database table.
3. Develop the API endpoints for managing prompt versions.
4. Implement frontend UI for saving and viewing prompt versions.
5. Test the API endpoints with various edge cases.
6. Optimize pagination for large datasets.
7. Deploy the feature ensuring thorough documentation is provided.
