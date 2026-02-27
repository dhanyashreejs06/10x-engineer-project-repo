"""Comprehensive API tests for PromptLab

Covers all endpoints with happy paths, edge cases, and error scenarios.
Students: This file REPLACES/EXPANDS the original test_api.py
"""

import pytest
import time
from fastapi.testclient import TestClient


# ─── Health ─────────────────────────────────────────────────────────────────

class TestHealth:

    def test_health_check_returns_200(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_has_status_healthy(self, client: TestClient):
        data = client.get("/health").json()
        assert data["status"] == "healthy"

    def test_health_check_has_version(self, client: TestClient):
        data = client.get("/health").json()
        assert "version" in data
        assert isinstance(data["version"], str)


# ─── Prompts — CRUD ──────────────────────────────────────────────────────────

class TestCreatePrompt:

    def test_create_prompt_success(self, client, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]

    def test_create_prompt_returns_id(self, client, sample_prompt_data):
        data = client.post("/prompts", json=sample_prompt_data).json()
        assert "id" in data
        assert len(data["id"]) > 0

    def test_create_prompt_returns_timestamps(self, client, sample_prompt_data):
        data = client.post("/prompts", json=sample_prompt_data).json()
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_prompt_without_description(self, client):
        payload = {"title": "No Description", "content": "Some content here"}
        response = client.post("/prompts", json=payload)
        assert response.status_code == 201
        assert response.json()["description"] is None

    def test_create_prompt_missing_title_fails(self, client):
        response = client.post("/prompts", json={"content": "Some content"})
        assert response.status_code == 422

    def test_create_prompt_missing_content_fails(self, client):
        response = client.post("/prompts", json={"title": "My Prompt"})
        assert response.status_code == 422

    def test_create_prompt_empty_title_fails(self, client):
        response = client.post("/prompts", json={"title": "", "content": "Some content"})
        assert response.status_code == 422

    def test_create_prompt_title_too_long_fails(self, client):
        response = client.post("/prompts", json={
            "title": "x" * 201,
            "content": "Some content"
        })
        assert response.status_code == 422

    def test_create_prompt_description_too_long_fails(self, client):
        response = client.post("/prompts", json={
            "title": "Valid Title",
            "content": "Some content",
            "description": "x" * 501
        })
        assert response.status_code == 422

    def test_create_prompt_with_invalid_collection_fails(self, client, sample_prompt_data):
        payload = {**sample_prompt_data, "collection_id": "nonexistent-col"}
        response = client.post("/prompts", json=payload)
        assert response.status_code == 400
        assert "Collection not found" in response.json()["detail"]

    def test_create_prompt_with_valid_collection(self, client, sample_prompt_data, sample_collection_data):
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        payload = {**sample_prompt_data, "collection_id": col_id}
        response = client.post("/prompts", json=payload)
        assert response.status_code == 201
        assert response.json()["collection_id"] == col_id


class TestListPrompts:

    def test_list_prompts_empty(self, client):
        data = client.get("/prompts").json()
        assert data["prompts"] == []
        assert data["total"] == 0

    def test_list_prompts_returns_all(self, client, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        client.post("/prompts", json={**sample_prompt_data, "title": "Second"})
        data = client.get("/prompts").json()
        assert data["total"] == 2
        assert len(data["prompts"]) == 2

    def test_list_prompts_sorted_newest_first(self, client):
        client.post("/prompts", json={"title": "First", "content": "Content one here"})
        time.sleep(0.05)
        client.post("/prompts", json={"title": "Second", "content": "Content two here"})
        prompts = client.get("/prompts").json()["prompts"]
        assert prompts[0]["title"] == "Second"

    def test_list_prompts_filter_by_collection(self, client, sample_collection_data, sample_prompt_data):
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        client.post("/prompts", json={**sample_prompt_data, "collection_id": col_id})
        client.post("/prompts", json={**sample_prompt_data, "title": "No Collection"})
        data = client.get(f"/prompts?collection_id={col_id}").json()
        assert data["total"] == 1
        assert data["prompts"][0]["collection_id"] == col_id

    def test_list_prompts_search_by_title(self, client):
        client.post("/prompts", json={"title": "Code Review Helper", "content": "Review code here"})
        client.post("/prompts", json={"title": "Unrelated Prompt", "content": "Something else here"})
        data = client.get("/prompts?search=code").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Code Review Helper"

    def test_list_prompts_search_case_insensitive(self, client):
        client.post("/prompts", json={"title": "Python Helper", "content": "Help with python stuff"})
        data = client.get("/prompts?search=PYTHON").json()
        assert data["total"] == 1

    def test_list_prompts_search_no_results(self, client, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        data = client.get("/prompts?search=zzznomatch").json()
        assert data["total"] == 0

    def test_list_prompts_filter_and_search_combined(self, client, sample_collection_data):
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        client.post("/prompts", json={"title": "Code Review", "content": "Review some code", "collection_id": col_id})
        client.post("/prompts", json={"title": "Code Generator", "content": "Generate some code"})
        data = client.get(f"/prompts?collection_id={col_id}&search=code").json()
        assert data["total"] == 1


class TestGetPrompt:

    def test_get_prompt_success(self, client, sample_prompt_data):
        created_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.get(f"/prompts/{created_id}")
        assert response.status_code == 200
        assert response.json()["id"] == created_id

    def test_get_prompt_not_found_returns_404(self, client):
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404

    def test_get_prompt_not_found_error_message(self, client):
        data = client.get("/prompts/nonexistent-id").json()
        assert "not found" in data["detail"].lower()


class TestUpdatePrompt:

    def test_update_prompt_success(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        updated = {"title": "New Title", "content": "Updated content text here"}
        response = client.put(f"/prompts/{prompt_id}", json=updated)
        assert response.status_code == 200
        assert response.json()["title"] == "New Title"

    def test_update_prompt_updates_timestamp(self, client, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        original_updated_at = created["updated_at"]
        time.sleep(0.05)
        updated = {"title": "New Title", "content": "New content text here for update"}
        data = client.put(f"/prompts/{created['id']}", json=updated).json()
        assert data["updated_at"] != original_updated_at

    def test_update_prompt_preserves_created_at(self, client, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        updated = {"title": "New Title", "content": "New content here"}
        data = client.put(f"/prompts/{created['id']}", json=updated).json()
        assert data["created_at"] == created["created_at"]

    def test_update_prompt_not_found(self, client):
        response = client.put("/prompts/nonexistent", json={"title": "X", "content": "Y"})
        assert response.status_code == 404

    def test_update_prompt_invalid_collection_fails(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.put(f"/prompts/{prompt_id}", json={
            "title": "Updated", "content": "Content here", "collection_id": "bad-col"
        })
        assert response.status_code == 400


class TestPatchPrompt:

    def test_patch_title_only(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"title": "Patched Title"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched Title"
        # Content should be unchanged
        assert data["content"] == sample_prompt_data["content"]

    def test_patch_content_only(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"content": "Patched content text here"})
        assert response.status_code == 200
        assert response.json()["content"] == "Patched content text here"

    def test_patch_description_only(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"description": "New description here"})
        assert response.status_code == 200
        assert response.json()["description"] == "New description here"

    def test_patch_updates_timestamp(self, client, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        time.sleep(0.05)
        data = client.patch(f"/prompts/{created['id']}", json={"title": "Patched"}).json()
        assert data["updated_at"] != created["updated_at"]

    def test_patch_nonexistent_prompt_returns_404(self, client):
        response = client.patch("/prompts/nonexistent", json={"title": "X"})
        assert response.status_code == 404

    def test_patch_with_invalid_collection_fails(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"collection_id": "bad-col-id"})
        assert response.status_code == 400

    def test_patch_collection_id_to_valid_collection(self, client, sample_prompt_data, sample_collection_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"collection_id": col_id})
        assert response.status_code == 200
        assert response.json()["collection_id"] == col_id

    def test_patch_empty_body_preserves_all_fields(self, client, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        data = client.patch(f"/prompts/{created['id']}", json={}).json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]


class TestDeletePrompt:

    def test_delete_prompt_success(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204

    def test_delete_prompt_removes_it(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        client.delete(f"/prompts/{prompt_id}")
        assert client.get(f"/prompts/{prompt_id}").status_code == 404

    def test_delete_prompt_not_found(self, client):
        response = client.delete("/prompts/nonexistent")
        assert response.status_code == 404

    def test_delete_reduces_count(self, client, sample_prompt_data):
        id1 = client.post("/prompts", json=sample_prompt_data).json()["id"]
        client.post("/prompts", json={**sample_prompt_data, "title": "Second"})
        client.delete(f"/prompts/{id1}")
        assert client.get("/prompts").json()["total"] == 1


# ─── Collections ─────────────────────────────────────────────────────────────

class TestCreateCollection:

    def test_create_collection_success(self, client, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data

    def test_create_collection_returns_created_at(self, client, sample_collection_data):
        data = client.post("/collections", json=sample_collection_data).json()
        assert "created_at" in data

    def test_create_collection_missing_name_fails(self, client):
        response = client.post("/collections", json={"description": "No name"})
        assert response.status_code == 422

    def test_create_collection_empty_name_fails(self, client):
        response = client.post("/collections", json={"name": ""})
        assert response.status_code == 422

    def test_create_collection_name_too_long_fails(self, client):
        response = client.post("/collections", json={"name": "x" * 101})
        assert response.status_code == 422

    def test_create_collection_without_description(self, client):
        response = client.post("/collections", json={"name": "No Desc Collection"})
        assert response.status_code == 201
        assert response.json()["description"] is None


class TestListCollections:

    def test_list_collections_empty(self, client):
        data = client.get("/collections").json()
        assert data["collections"] == []
        assert data["total"] == 0

    def test_list_collections_returns_all(self, client, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        client.post("/collections", json={**sample_collection_data, "name": "Second"})
        data = client.get("/collections").json()
        assert data["total"] == 2


class TestGetCollection:

    def test_get_collection_success(self, client, sample_collection_data):
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        response = client.get(f"/collections/{col_id}")
        assert response.status_code == 200
        assert response.json()["id"] == col_id

    def test_get_collection_not_found(self, client):
        assert client.get("/collections/nonexistent").status_code == 404


class TestDeleteCollection:

    def test_delete_collection_success(self, client, sample_collection_data):
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        response = client.delete(f"/collections/{col_id}")
        assert response.status_code == 204

    def test_delete_collection_removes_it(self, client, sample_collection_data):
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        client.delete(f"/collections/{col_id}")
        assert client.get(f"/collections/{col_id}").status_code == 404

    def test_delete_collection_not_found(self, client):
        assert client.delete("/collections/nonexistent").status_code == 404

    def test_delete_collection_also_deletes_its_prompts(self, client, sample_collection_data, sample_prompt_data):
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        client.post("/prompts", json={**sample_prompt_data, "collection_id": col_id})
        client.delete(f"/collections/{col_id}")
        # Prompts belonging to deleted collection should be gone
        prompts = client.get("/prompts").json()["prompts"]
        assert all(p["collection_id"] != col_id for p in prompts)

    def test_delete_collection_leaves_unrelated_prompts(self, client, sample_collection_data, sample_prompt_data):
        col_id = client.post("/collections", json=sample_collection_data).json()["id"]
        # Prompt in the collection
        client.post("/prompts", json={**sample_prompt_data, "collection_id": col_id})
        # Prompt NOT in the collection
        client.post("/prompts", json={**sample_prompt_data, "title": "Unrelated"})
        client.delete(f"/collections/{col_id}")
        prompts = client.get("/prompts").json()["prompts"]
        assert len(prompts) == 1
        assert prompts[0]["title"] == "Unrelated"


# ─── Storage Layer ────────────────────────────────────────────────────────────

class TestStorage:
    """Direct tests of storage operations for edge cases."""

    def test_get_nonexistent_prompt_returns_none(self):
        from app.storage import Storage
        s = Storage()
        assert s.get_prompt("no-such-id") is None

    def test_update_nonexistent_prompt_returns_none(self):
        from app.storage import Storage
        from app.models import Prompt
        s = Storage()
        p = Prompt(title="X", content="Y")
        assert s.update_prompt("no-id", p) is None

    def test_delete_nonexistent_prompt_returns_false(self):
        from app.storage import Storage
        s = Storage()
        assert s.delete_prompt("no-id") is False

    def test_delete_existing_prompt_returns_true(self):
        from app.storage import Storage
        from app.models import Prompt
        s = Storage()
        p = Prompt(title="X", content="Y")
        s.create_prompt(p)
        assert s.delete_prompt(p.id) is True

    def test_get_nonexistent_collection_returns_none(self):
        from app.storage import Storage
        s = Storage()
        assert s.get_collection("no-such-id") is None

    def test_clear_empties_all_data(self):
        from app.storage import Storage
        from app.models import Prompt, Collection
        s = Storage()
        s.create_prompt(Prompt(title="A", content="B"))
        s.create_collection(Collection(name="C"))
        s.clear()
        assert s.get_all_prompts() == []
        assert s.get_all_collections() == []

    def test_get_prompts_by_collection(self):
        from app.storage import Storage
        from app.models import Prompt
        s = Storage()
        p1 = Prompt(title="A", content="Content A", collection_id="col-1")
        p2 = Prompt(title="B", content="Content B", collection_id="col-2")
        s.create_prompt(p1)
        s.create_prompt(p2)
        result = s.get_prompts_by_collection("col-1")
        assert len(result) == 1
        assert result[0].title == "A"