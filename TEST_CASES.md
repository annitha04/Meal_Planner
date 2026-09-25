# Test Cases for Meal Planner Application

## Overview

This document contains the manual and automated test scenarios for the Meal Planner application. It includes functional, negative, edge-case, and UI validation checks for the backend API and Streamlit frontend.

## Scope

- Backend API validation in `backend/main.py`
- Frontend user interactions in `frontend/app.py`
- Data output generation and error handling
- Project-level regression checks

## Test Environment

- Python 3.11+
- FastAPI backend
- Streamlit frontend
- pytest for automated backend testing
- Playwright for browser-based UI smoke testing (optional/manual)

---

## Functional Test Cases

### TC-01: App loads successfully
- Title: Frontend homepage loads without errors
- Precondition: Frontend is running
- Steps:
  1. Open the Streamlit app in the browser
  2. Verify the page loads
  3. Confirm all sidebar controls are visible
- Expected Result:
  - Page renders without crashing
  - Cuisine dropdown, diet dropdown, goal dropdown, and Generate button appear

### TC-02: Generate meal plan with valid inputs
- Title: Valid request generates a 7-day meal plan
- Precondition: Backend is running and API key is configured
- Steps:
  1. Select a cuisine
  2. Select a diet
  3. Select a health goal
  4. Click the Generate button
- Expected Result:
  - Request succeeds
  - 7-day meal plan is displayed
  - Output includes breakfast, lunch, dinner, focus, sugar guidance, and caption

### TC-03: Generate plan for diabetic-friendly goal
- Title: Diabetic goal returns low-GI recommendations
- Precondition: User chooses a sugar-control goal
- Steps:
  1. Select a diabetic-friendly diet
  2. Choose “Sugar Patient” or similar health goal
  3. Generate the plan
- Expected Result:
  - Output emphasizes low-GI foods and avoids added sugar
  - Suggestions align with diabetes-friendly nutrition patterns

### TC-04: Generate plan for high-protein or gym-focused goal
- Title: Gym goal returns protein-rich recommendations
- Precondition: User chooses a gym or muscle-building goal
- Steps:
  1. Select “Gym Practitioner” or similar option
  2. Generate the plan
- Expected Result:
  - Meals include a higher-protein focus
  - Calorie balance and recovery support are reflected in suggestions

### TC-05: Generate plan for vegetarian diet
- Title: Vegetarian plan respects vegetarian restrictions
- Precondition: User selects “Strict Vegetarian” or other vegetarian option
- Steps:
  1. Select vegetarian diet
  2. Generate the plan
- Expected Result:
  - No non-vegetarian meals appear in the output

### TC-06: Generate plan for vegan diet
- Title: Vegan plan excludes animal-based items
- Steps:
  1. Select “Vegan”
  2. Generate the plan
- Expected Result:
  - No dairy, eggs, or other non-vegan items are suggested

### TC-07: Generate plan for Jain diet
- Title: Jain diet avoids restricted ingredients
- Steps:
  1. Choose “Jain Vegetarian”
  2. Generate the plan
- Expected Result:
  - No onion, garlic, or root vegetables are included in suggestions if applicable

### TC-08: Generate plan for multiple cuisines
- Title: Cuisine selection affects plan content
- Steps:
  1. Choose different cuisine styles such as South Indian, North Indian, Kerala, or Marathi
  2. Generate for each one
- Expected Result:
  - Output reflects the cuisine choice appropriately
  - Meal recommendations vary according to cuisine

---

## API Test Cases

### TC-09: API success response validation
- Title: Valid payload returns 200 OK
- Request:
  - POST to `/api/generate`
  - JSON payload contains cuisine, diet, and goal
- Expected Result:
  - Response status is 200
  - JSON contains `caption`, `sugar_guidelines`, and `days`

### TC-10: Missing API key
- Title: Missing `OPENAI_API_KEY` is blocked cleanly
- Precondition: `.env` file does not include the key
- Steps:
  1. Remove or unset `OPENAI_API_KEY`
  2. Send valid API request
- Expected Result:
  - Response status is 400
  - Error message mentions `OPENAI_API_KEY`

### TC-11: Invalid payload rejected
- Title: Missing required request fields returns validation error
- Steps:
  1. Send request with incomplete JSON
  2. Example: missing `diet` or `goal`
- Expected Result:
  - Response status is 422
  - Validation error is returned

### TC-12: Non-JSON request body rejected
- Title: Invalid content type or malformed body is rejected
- Steps:
  1. Send malformed or plain text body to `/api/generate`
- Expected Result:
  - Response status is 422 or 400
  - Request is rejected without server crash

### TC-13: AI failure handled gracefully
- Title: OpenAI service issues do not crash the API
- Precondition: Simulate a model or API failure
- Steps:
  1. Trigger request while AI service is unavailable
- Expected Result:
  - Response status is 500
  - Error message indicates the backend issue clearly

### TC-14: Download endpoint works
- Title: PDF/text output is returned successfully
- Steps:
  1. Call `/api/download-pdf` with valid day data
- Expected Result:
  - Response status is 200
  - File is returned as a downloadable attachment
  - Content includes meal details

### TC-15: Empty download list works gracefully
- Title: Empty day list is accepted without breaking output
- Steps:
  1. Call `/api/download-pdf` with an empty list
- Expected Result:
  - Response status is 200
  - Output still contains the header text

---

## Negative and Edge-Case Test Cases

### TC-16: Empty request body
- Title: Empty JSON object is rejected
- Steps:
  1. Send `{}` to the API
- Expected Result:
  - Validation error is raised
  - No server crash

### TC-17: Long input values
- Title: Very long form input does not break backend/frontend
- Steps:
  1. Enter large strings or extended meal descriptions
- Expected Result:
  - App remains stable
  - Response is still processed or rejected cleanly

### TC-18: Special characters input
- Title: Special characters do not cause errors
- Steps:
  1. Submit punctuation or symbols in diet or goal values
- Expected Result:
  - No crash
  - Response generation continues normally

### TC-19: Backend unavailable
- Title: Frontend handles offline backend
- Steps:
  1. Stop the FastAPI server
  2. Click Generate in the app
- Expected Result:
  - User sees a meaningful error message
  - App does not freeze

### TC-20: Browser refresh during processing
- Title: Refresh does not corrupt state
- Steps:
  1. Trigger generation
  2. Refresh the browser while it is loading
- Expected Result:
  - App recovers or resets without crashing

### TC-21: Null or invalid values in day data
- Title: Malformed plan item is handled safely
- Steps:
  1. Send a day object missing fields to download route
- Expected Result:
  - Response is either rejected or handled gracefully

---

## UI Test Cases

### TC-22: Sidebar options render correctly
- Title: User can access all input controls
- Steps:
  1. Open the app
  2. Review the sidebar
- Expected Result:
  - All dropdowns and the Generate button are visible and usable

### TC-23: Generate button shows loading state
- Title: Loading indicator appears during request
- Steps:
  1. Click Generate
- Expected Result:
  - Spinner or loading message appears while the backend processes

### TC-24: Output area updates after generation
- Title: Plan is displayed after request completes
- Steps:
  1. Click Generate
  2. Wait for backend response
- Expected Result:
  - Meal data appears in the interface
  - Plan summary and tabs are visible

### TC-25: Table/list formatting remains readable
- Title: Generated meal plan is legible
- Steps:
  1. Generate a long meal plan
- Expected Result:
  - Text wraps properly
  - No severe layout breakage or unreadable cells

### TC-26: Playwright browser smoke test
- Title: App loads in a real browser
- Steps:
  1. Start the frontend locally
  2. Open the site in Chromium via Playwright
  3. Check page title and key text
- Expected Result:
  - Browser page loads successfully
  - Expected UI elements are visible

---

## Automation Coverage

The automated suite currently includes:

- Valid generation test
- Missing API key test
- Invalid payload test
- Download endpoint test
- Empty list handling
- AI failure handling
- Frontend smoke validation for presence of key UI elements

---

## Exit Criteria

The feature is considered ready when:

- All critical functional flows pass
- API validation and errors behave correctly
- Frontend loads and displays the expected controls
- Edge-case scenarios do not crash the application
- Automated tests pass in CI

---

## Notes

- The backend should be tested with both real service calls and mock/failure conditions.
- Frontend tests should validate user-visible behavior rather than internal implementation details.
- All test results should be recorded before release or deployment.
