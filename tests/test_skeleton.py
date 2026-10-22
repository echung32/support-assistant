"""Basic page and API contract checks for the skeleton."""

import re

from fastapi.testclient import TestClient
from pydantic_ai.models import override_allow_model_requests

from app.main import app


def test_page_loads_with_main_heading() -> None:
    with override_allow_model_requests(False), TestClient(app) as client:
        response = client.get('/')

    assert response.status_code == 200
    assert re.search(r'<h1\b', response.text)


def test_trace_accepts_sample_request_and_returns_declared_fields() -> None:
    with override_allow_model_requests(False), TestClient(app) as client:
        response = client.post(
            '/api/trace',
            json={'search_type': 'sample', 'query': '220113-I1-HT03'},
        )

    assert response.status_code == 200
    assert set(response.json()) == {
        'placeholder',
        'message',
        'sample',
        'inventory',
        'results',
        'validation_findings',
        'review_decisions',
        'evidence_sets',
    }
