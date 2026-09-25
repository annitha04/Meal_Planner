import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_app_exists():
    assert (ROOT / "frontend" / "app.py").exists()


def test_frontend_file_contains_main_ui_elements():
    app_text = (ROOT / "frontend" / "app.py").read_text(encoding="utf-8")
    assert "st.sidebar.selectbox" in app_text
    assert "Generate Fresh Meal Plan" in app_text
    assert "st.tabs" in app_text


def test_frontend_file_is_not_empty():
    app_file = ROOT / "frontend" / "app.py"
    assert app_file.stat().st_size > 0
