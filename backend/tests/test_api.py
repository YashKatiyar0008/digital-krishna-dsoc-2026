"""Tests for the sanitized Digital Krishna DSOC API."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint() -> None:
    """The root endpoint should describe the public API."""

    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Digital Krishna AI Public API"
    assert body["status"] == "running"
    assert body["documentation"] == "/docs"


def test_health_endpoint() -> None:
    """The health endpoint should confirm that the API is available."""

    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"
    assert body["service"] == "digital-krishna-guidance-api"
    assert body["version"] == "1.0.0"


def test_english_academic_guidance() -> None:
    """Academic input should return structured English guidance."""

    response = client.post(
        "/api/guidance",
        json={
            "message": "I am worried about my studies and cannot focus.",
            "language": "en",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["category"] == "Academic stress"
    assert body["language"] == "en"
    assert body["acknowledgement"]
    assert body["explanation"]
    assert body["reflection_question"]
    assert len(body["practical_steps"]) >= 1

    # The sanitized public demo must not claim an unverified verse.
    assert body["scripture"]["status"] == "none"
    assert body["scripture"]["reference"] is None


def test_hindi_guidance() -> None:
    """The API should return a Hindi response when requested."""

    response = client.post(
        "/api/guidance",
        json={
            "message": "मुझे अपनी पढ़ाई और भविष्य की चिंता है।",
            "language": "hi",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["language"] == "hi"
    assert body["acknowledgement"]
    assert body["explanation"]
    assert len(body["practical_steps"]) == 3


def test_hinglish_guidance() -> None:
    """The API should support a Hinglish response."""

    response = client.post(
        "/api/guidance",
        json={
            "message": "Mujhe career aur future ko lekar chinta hai.",
            "language": "hinglish",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["language"] == "hinglish"
    assert body["category"] == "Career uncertainty"
    assert len(body["practical_steps"]) == 3


def test_safety_language_adds_support_note() -> None:
    """Urgent-safety language should add a support message."""

    response = client.post(
        "/api/guidance",
        json={
            "message": "I am not safe and need urgent help.",
            "language": "en",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["safety_note"] is not None
    assert "trusted adult" in body["safety_note"]
    assert "emergency service" in body["safety_note"]


def test_short_message_is_rejected() -> None:
    """Messages below the minimum length should be rejected."""

    response = client.post(
        "/api/guidance",
        json={
            "message": "hi",
            "language": "en",
        },
    )

    assert response.status_code == 422


def test_unsupported_language_is_rejected() -> None:
    """Unsupported language codes should fail validation."""

    response = client.post(
        "/api/guidance",
        json={
            "message": "I need guidance about my future.",
            "language": "fr",
        },
    )

    assert response.status_code == 422


def test_response_does_not_expose_sensitive_fields() -> None:
    """Public API responses must not expose credentials."""

    response = client.post(
        "/api/guidance",
        json={
            "message": "I am confused about an important decision.",
            "language": "en",
        },
    )

    assert response.status_code == 200

    response_text = response.text.lower()

    forbidden_terms = [
        "api_key",
        "password",
        "secret_key",
        "access_token",
        "private_endpoint",
    ]

    for term in forbidden_terms:
        assert term not in response_text
