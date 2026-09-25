import os

from fastapi.testclient import TestClient

from backend import main as backend_main


client = TestClient(backend_main.app)


class FakePrompt:
    @classmethod
    def from_messages(cls, *args, **kwargs):
        return cls()

    def __or__(self, other):
        return FakeChain()


class FakeChain:
    def __or__(self, other):
        return self

    def invoke(self, payload):
        return {
            "caption": "Healthy and balanced 7-day meal plan",
            "sugar_guidelines": "Keep portions steady and prefer low-GI grains.",
            "days": [
                {
                    "day": "Day 1",
                    "breakfast": "Ragi dosa with sambar",
                    "lunch": "Brown rice and vegetable curd bowl",
                    "dinner": "Grilled tofu with greens",
                    "focus": "Fiber and steady energy",
                }
            ],
        }


class FakeLLM:
    def __init__(self, *args, **kwargs):
        pass

    def __ror__(self, other):
        return FakeChain()


class FakeParser:
    def __init__(self, *args, **kwargs):
        pass

    def get_format_instructions(self):
        return "Return valid JSON"

    def __ror__(self, other):
        return FakeChain()


def test_generate_plan_success(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(backend_main, "ChatOpenAI", FakeLLM)
    monkeypatch.setattr(backend_main, "ChatPromptTemplate", FakePrompt)
    monkeypatch.setattr(backend_main, "JsonOutputParser", FakeParser)

    response = client.post(
        "/api/generate",
        json={
            "cuisine": "South Indian",
            "diet": "Diabetic Friendly",
            "goal": "Sugar Patient",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["caption"] == "Healthy and balanced 7-day meal plan"
    assert payload["days"][0]["day"] == "Day 1"
    assert len(payload["days"]) == 1


def test_generate_plan_missing_api_key(monkeypatch):
    monkeypatch.setattr(backend_main.os, "getenv", lambda key: None)

    response = client.post(
        "/api/generate",
        json={
            "cuisine": "South Indian",
            "diet": "Vegetarian",
            "goal": "Weight Loss",
        },
    )

    assert response.status_code == 400
    assert "OPENAI_API_KEY" in response.json()["detail"]


def test_generate_plan_invalid_payload():
    response = client.post(
        "/api/generate",
        json={"cuisine": "South Indian"},
    )

    assert response.status_code == 422


def test_download_pdf_returns_text_response():
    payload = [
        {
            "day": "Day 1",
            "breakfast": "Ragi dosa",
            "lunch": "Brown rice bowl",
            "dinner": "Tofu curry",
            "focus": "Low GI and balanced protein",
        }
    ]

    response = client.post("/api/download-pdf", json=payload)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/octet-stream")
    assert "Day 1" in response.text
    assert "Ragi dosa" in response.text


def test_generate_plan_handles_ai_exception(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def raise_error(*args, **kwargs):
        raise RuntimeError("OpenAI service unavailable")

    monkeypatch.setattr(backend_main, "ChatOpenAI", raise_error)

    response = client.post(
        "/api/generate",
        json={
            "cuisine": "South Indian",
            "diet": "Diabetic Friendly",
            "goal": "Sugar Patient",
        },
    )

    assert response.status_code == 500
    assert "OpenAI service unavailable" in response.json()["detail"]


def test_download_pdf_with_empty_list():
    response = client.post("/api/download-pdf", json=[])

    assert response.status_code == 200
    assert "--- 7-DAY REGIONAL NUTRITION STRATEGY ---" in response.text


def test_generate_plan_rejects_non_json_body():
    response = client.post(
        "/api/generate",
        data="not-json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
