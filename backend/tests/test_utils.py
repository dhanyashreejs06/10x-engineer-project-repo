import pytest
from datetime import datetime
from app.models import Prompt
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables
)


def make_prompt(title: str, description: str = None,
                collection_id: str = None, created_at: datetime = None) -> Prompt:
    p = Prompt(title=title, content="Default content here",
               description=description, collection_id=collection_id)
    if created_at:
        p.created_at = created_at
    return p


class TestSortPromptsByDate:
    def test_happy_path(self):
        prompts = [
            make_prompt("First", created_at=datetime(2023, 1, 1)),
            make_prompt("Second", created_at=datetime(2023, 1, 2)),
        ]
        sorted_prompts = sort_prompts_by_date(prompts)
        assert sorted_prompts[0].title == "Second"

    def test_empty_list(self):
        assert sort_prompts_by_date([]) == []

    def test_edge_case_same_date(self):
        prompts = [
            make_prompt("First", created_at=datetime(2023, 1, 1)),
            make_prompt("Second", created_at=datetime(2023, 1, 1)),
        ]
        sorted_prompts = sort_prompts_by_date(prompts)
        assert len(sorted_prompts) == 2


class TestFilterPromptsByCollection:
    def test_happy_path(self):
        prompts = [
            make_prompt("First", collection_id='col1'),
            make_prompt("Second", collection_id='col2'),
        ]
        filtered_prompts = filter_prompts_by_collection(prompts, 'col1')
        assert len(filtered_prompts) == 1
        assert filtered_prompts[0].title == "First"

    def test_empty_list(self):
        assert filter_prompts_by_collection([], 'col1') == []

    def test_no_results(self):
        prompts = [
            make_prompt("First", collection_id='col1'),
        ]
        filtered_prompts = filter_prompts_by_collection(prompts, 'col2')
        assert filtered_prompts == []


class TestSearchPrompts:
    def test_happy_path(self):
        prompts = [
            make_prompt("Title", "A description containing the word example"),
            make_prompt("Another", "No keyword here"),
        ]
        results = search_prompts(prompts, 'example')
        assert len(results) == 1
        assert results[0].title == "Title"

    def test_empty_list(self):
        assert search_prompts([], 'example') == []

    def test_case_insensitivity(self):
        prompts = [
            make_prompt("Title", "example"),
        ]
        results = search_prompts(prompts, 'EXAMPLE')
        assert len(results) == 1

    def test_no_matches(self):
        prompts = [
            make_prompt("Title", "A description"),
        ]
        results = search_prompts(prompts, 'absent')
        assert results == []


class TestValidatePromptContent:
    def test_happy_path(self):
        assert validate_prompt_content('This is a valid prompt.')

    def test_empty_string(self):
        assert not validate_prompt_content('')

    def test_whitespace_string(self):
        assert not validate_prompt_content('    ')

    def test_minimum_length_boundary(self):
        assert not validate_prompt_content('123456789')  # 9 chars
        assert validate_prompt_content('1234567890')    # 10 chars


class TestExtractVariables:
    def test_happy_path(self):
        content = 'Hello, {{name}}! Welcome to {{place}}.'
        variables = extract_variables(content)
        assert variables == ['name', 'place']

    def test_no_variables(self):
        content = 'Hello, World!'
        variables = extract_variables(content)
        assert variables == []

    def test_edge_case_empty_string(self):
        assert extract_variables('') == []

    def test_partial_template(self):
        content = 'Hello, {{name}! Welcome to {{place}}.'
        variables = extract_variables(content)
        assert variables == ['place']
