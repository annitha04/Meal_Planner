# Meal Planner

Meal Planner is an AI-powered nutrition assistant that generates personalized 7-day meal plans based on cuisine preference, dietary type, and health goals. It combines a FastAPI backend with a Streamlit frontend to provide a simple web experience for creating region-aware, health-conscious meal plans.

## Project Description

This project helps users create customized meal plans for goals such as:

- Diabetes and sugar control
- Weight loss and energy balance
- Fat burn and metabolism support
- Gym performance and muscle-building goals
- Hormonal and women's health support
- Heart health and cholesterol management

The app uses AI to generate meal suggestions tailored to Indian regional cuisines and low-GI nutrition principles. It also provides a simple summary of sugar guidelines and a downloadable plan output.

## Architecture

- Frontend: Streamlit web app
- Backend: FastAPI REST API
- AI Layer: LangChain + OpenAI model integration
- Data Handling: Pydantic models for structured meal plan responses

## Repository Structure

```text
Meal_Planner/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example (optional, if added later)
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── .gitignore
├── README.md
└── venv/
```

## Features

- Custom meal-plan generation based on cuisine, diet, and goal
- Indian regional meal customization
- Diabetes-friendly low-GI recommendations
- Structured weekly meal schedule
- AI-generated nutrition notes and social media caption
- Downloadable text plan output

## Tech Stack

- Python 3.11+
- FastAPI
- Streamlit
- LangChain
- OpenAI API
- Pydantic
- python-dotenv

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run the Application

### Start the backend

```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Start the frontend

```bash
cd frontend
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Then open:

- Frontend: http://127.0.0.1:8501
- Backend API: http://127.0.0.1:8000

## API Endpoint

### POST /api/generate

Request body:

```json
{
  "cuisine": "South Indian (Tamil Nadu)",
  "diet": "Diabetic Friendly (Low Carb & Low GI)",
  "goal": "Sugar Patient (Diabetic / Pre-Diabetic Glucose Control)"
}
```

## Notes

- This project is designed around diabetic-friendly and low-GI recommendations.
- The AI-generated plan is meant to support, not replace, professional medical or nutrition advice.
- Use with your own OpenAI API key for live generation.

## License

This project is for personal and educational use. Add a license if you plan to distribute it publicly.

## Author

Annitha
