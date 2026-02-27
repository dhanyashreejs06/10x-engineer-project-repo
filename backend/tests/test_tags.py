"""TDD Tests for Tagging System Feature

Tests are written first (TDD approach) to verify the tagging feature.
Feature: prompts can have a list of string tags.
- Tags can be set when creating/updating a prompt
- Prompts can be filtered by tag via GET /prompts?tag=<tag_name>
"""

import pytest


class TestTagsOnCreate:
    """Tags can be set when creating a prompt."""

    def test_create_prompt_with_tags(self, client):
        payload = {
            "title": "Tagged Prompt",
            "content": "Some content for this prompt",
            "tags": ["python", "review"]
        }
        response = client.post("/prompts", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "tags" in data
        assert "python" in data["tags"]
        assert "review" in data["tags"]

    def test_create_prompt_without_tags_defaults_to_empty_list(self, client):
        payload = {"title": "No Tags", "content": "Content without tags here"}
        response = client.post("/prompts", json=payload)
        assert response.status_code == 201
        assert response.json()["tags"] == []

    def test_create_prompt_with_empty_tags_list(self, client):
        payload = {"title": "Empty Tags", "content": "Content here", "tags": []}
        response = client.post("/prompts", json=payload)
        assert response.status_code == 201
        assert response.json()["tags"] == []

    def test_create_prompt_tags_stored_as_list(self, client):
        payload = {"title": "Tagged", "content": "Some content here", "tags": ["ai"]}
        data = client.post("/prompts", json=payload).json()
        assert isinstance(data["tags"], list)

    def test_create_prompt_duplicate_tags_handled(self, client):
        payload = {"title": "Dups", "content": "Content here", "tags": ["ai", "ai", "ml"]}
        data = client.post("/prompts", json=payload).json()
        assert "ai" in data["tags"]
        assert "ml" in data["tags"]


class TestTagsOnUpdate:
    """Tags can be updated via PUT and PATCH."""

    def test_put_update_tags(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        updated = {
            "title": "Updated Title",
            "content": "Updated content here",
            "tags": ["updated", "tags"]
        }
        response = client.put(f"/prompts/{prompt_id}", json=updated)
        assert response.status_code == 200
        assert "updated" in response.json()["tags"]
        assert "tags" in response.json()["tags"]

    def test_patch_update_tags_partially(self, client, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"tags": ["partial", "update"]})
        assert response.status_code == 200
        assert response.json()["tags"] == ["partial", "update"]

    def test_patch_clear_tags_with_empty_list(self, client):
        payload = {"title": "Tagged", "content": "Content here", "tags": ["ai"]}
        prompt_id = client.post("/prompts", json=payload).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"tags": []})
        assert response.status_code == 200
        assert response.json()["tags"] == []

    def test_patch_without_tags_preserves_existing(self, client):
        payload = {"title": "Tagged", "content": "Content here", "tags": ["ai", "ml"]}
        prompt_id = client.post("/prompts", json=payload).json()["id"]
        # PATCH only title — tags should remain unchanged
        response = client.patch(f"/prompts/{prompt_id}", json={"title": "New Title"})
        assert response.status_code == 200
        assert "ai" in response.json()["tags"]
        assert "ml" in response.json()["tags"]


class TestTagsOnGet:
    """GET /prompts?tag= filters prompts by tag."""

    def test_filter_by_tag_returns_matching(self, client):
        client.post("/prompts", json={"title": "AI Prompt", "content": "Content", "tags": ["ai"]})
        client.post("/prompts", json={"title": "SQL Prompt", "content": "Content", "tags": ["sql"]})
        data = client.get("/prompts?tag=ai").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "AI Prompt"

    def test_filter_by_tag_no_match(self, client):
        client.post("/prompts", json={"title": "Prompt", "content": "Content", "tags": ["python"]})
        data = client.get("/prompts?tag=javascript").json()
        assert data["total"] == 0

    def test_filter_by_tag_returns_multiple_matches(self, client):
        client.post("/prompts", json={"title": "P1", "content": "Content", "tags": ["ai", "ml"]})
        client.post("/prompts", json={"title": "P2", "content": "Content", "tags": ["ai"]})
        client.post("/prompts", json={"title": "P3", "content": "Content", "tags": ["sql"]})
        data = client.get("/prompts?tag=ai").json()
        assert data["total"] == 2

    def test_no_tag_param_returns_all(self, client):
        client.post("/prompts", json={"title": "P1", "content": "Content", "tags": ["ai"]})
        client.post("/prompts", json={"title": "P2", "content": "Content"})
        data = client.get("/prompts").json()
        assert data["total"] == 2

    def test_tag_filter_combined_with_search(self, client):
        client.post("/prompts", json={"title": "Code Review", "content": "Content", "tags": ["python"]})
        client.post("/prompts", json={"title": "Code Generator", "content": "Content", "tags": ["java"]})
        data = client.get("/prompts?tag=python&search=code").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Code Review"

    def test_all_returned_prompts_contain_filtered_tag(self, client):
        client.post("/prompts", json={"title": "P1", "content": "Content", "tags": ["ai"]})
        client.post("/prompts", json={"title": "P2", "content": "Content", "tags": ["ai", "ml"]})
        client.post("/prompts", json={"title": "P3", "content": "Content", "tags": ["sql"]})
        data = client.get("/prompts?tag=ai").json()
        assert all("ai" in p["tags"] for p in data["prompts"])


class TestTagsInResponses:
    """Tags are included in all prompt responses."""

    def test_tags_included_in_single_prompt_response(self, client):
        payload = {"title": "Tagged", "content": "Content", "tags": ["review"]}
        prompt_id = client.post("/prompts", json=payload).json()["id"]
        data = client.get(f"/prompts/{prompt_id}").json()
        assert "tags" in data
        assert "review" in data["tags"]

    def test_tags_included_in_list_prompts_response(self, client):
        payload = {"title": "Tagged", "content": "Content", "tags": ["ml"]}
        client.post("/prompts", json=payload)
        prompts = client.get("/prompts").json()["prompts"]
        assert "tags" in prompts[0]
        assert "ml" in prompts[0]["tags"]

    def test_prompt_with_no_tags_shows_empty_list_in_response(self, client):
        payload = {"title": "No Tags", "content": "Content here no tags"}
        client.post("/prompts", json=payload)
        prompts = client.get("/prompts").json()["prompts"]
        assert prompts[0]["tags"] == []