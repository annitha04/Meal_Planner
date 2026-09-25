import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.skip(reason="Requires browser app to be running locally on http://127.0.0.1:8501")
def test_streamlit_homepage_loads(page: Page):
    page.goto("http://127.0.0.1:8501")
    expect(page).to_have_title(re.compile("Vibrant AI Regional Nutrition Studio|Streamlit"), timeout=20000)
    expect(page.get_by_text("Customize Your Plan")).to_be_visible(timeout=20000)
    expect(page.get_by_role("button", name="Generate Fresh Meal Plan")).to_be_visible(timeout=20000)
