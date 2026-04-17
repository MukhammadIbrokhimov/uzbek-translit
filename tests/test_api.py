"""Tests for the FastAPI service."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestHealth:
    def test_health_returns_ok(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert "version" in body


class TestTransliterateEndpoint:
    def test_latin_to_cyrillic(self, client: TestClient) -> None:
        response = client.post(
            "/transliterate",
            json={"text": "Assalomu alaykum", "direction": "cyrillic"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["result"] == "Ассалому алайкум"
        assert body["direction"] == "cyrillic"

    def test_cyrillic_to_latin(self, client: TestClient) -> None:
        response = client.post(
            "/transliterate",
            json={"text": "Ассалому алайкум", "direction": "latin"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["result"] == "Assalomu alaykum"
        assert body["direction"] == "latin"

    def test_invalid_direction_422(self, client: TestClient) -> None:
        # Pydantic Literal rejects any value outside cyrillic/latin
        response = client.post(
            "/transliterate",
            json={"text": "kitob", "direction": "klingon"},
        )
        assert response.status_code == 422

    def test_empty_text_422(self, client: TestClient) -> None:
        response = client.post(
            "/transliterate",
            json={"text": "", "direction": "cyrillic"},
        )
        assert response.status_code == 422

    def test_missing_field_422(self, client: TestClient) -> None:
        response = client.post("/transliterate", json={"text": "kitob"})
        assert response.status_code == 422

    def test_text_too_long_422(self, client: TestClient) -> None:
        response = client.post(
            "/transliterate",
            json={"text": "a" * 50_001, "direction": "cyrillic"},
        )
        assert response.status_code == 422


class TestDocs:
    def test_openapi_schema_available(self, client: TestClient) -> None:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "uzbek-translit"
        assert "/transliterate" in schema["paths"]
        assert "/health" in schema["paths"]

    def test_swagger_ui(self, client: TestClient) -> None:
        response = client.get("/docs")
        assert response.status_code == 200
