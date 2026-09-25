from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv
from pathlib import Path
import io

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Locate and load .env directly from root folder
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

app = FastAPI(title="AI Content Engine API")

class MealPlanRequest(BaseModel):
    cuisine: str
    diet: str
    goal: str

class DayPlan(BaseModel):
    day: str = Field(description="Day identifier e.g., Day 1")
    breakfast: str = Field(description="Breakfast dish details")
    lunch: str = Field(description="Lunch meal details")
    dinner: str = Field(description="Dinner meal details")
    focus: str = Field(description="Key nutritional focus")

class MealPlanResponse(BaseModel):
    caption: str = Field(description="Engaging social media post caption with hashtags")
    sugar_guidelines: str = Field(description="Diabetic & health guidance notes")
    days: List[DayPlan] = Field(description="List of 7 daily meal plans")

@app.post("/api/generate", response_model=MealPlanResponse)
async def generate_plan(request: MealPlanRequest):
    load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        raise HTTPException(
            status_code=400, 
            detail="OPENAI_API_KEY is missing from your .env file."
        )

    try:
        # Initialize LangChain model
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=openai_key
        )

        parser = JsonOutputParser(pydantic_object=MealPlanResponse)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert clinical dietitian specializing in Indian Diabetology, Gym Nutrition, and Regional Culinary Therapeutics."),
            ("user", """
            Create a DISTINCT, realistic 7-day meal plan based on these user choices:
            - CUISINE: {cuisine}
            - DIET TYPE: {diet}
            - HEALTH GOAL: {goal}

            SPECIAL CLINICAL RULES FOR SUGAR PATIENTS / DIABETICS:
            - Emphasize Low Glycemic Index (GI) grains (e.g., Foxtail Millet, Ragi, Brown/Red Rice, Bajra).
            - Avoid refined flour (Maida), white rice overconsumption, and added sugars.
            - Pair complex carbs with fiber and lean plant protein.

            {format_instructions}
            """)
        ])

        chain = prompt | llm | parser

        data = chain.invoke({
            "cuisine": request.cuisine,
            "diet": request.diet,
            "goal": request.goal,
            "format_instructions": parser.get_format_instructions()
        })

        return data

    except Exception as e:
        print(f"❌ LangChain/OpenAI Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/download-pdf")
async def generate_pdf(days: List[DayPlan]):
    buffer = io.StringIO()
    buffer.write("--- 7-DAY REGIONAL NUTRITION STRATEGY ---\n\n")
    for d in days:
        buffer.write(f"{d.day}:\n")
        buffer.write(f"  🍳 Breakfast: {d.breakfast}\n")
        buffer.write(f"  🥗 Lunch: {d.lunch}\n")
        buffer.write(f"  🍲 Dinner: {d.dinner}\n")
        buffer.write(f"  💡 Focus: {d.focus}\n\n")
        
    return Response(
        content=buffer.getvalue().encode('utf-8'),
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=meal_plan.txt"}
    )