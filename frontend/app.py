import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Vibrant AI Regional Nutrition Studio",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Aesthetic CSS Injection
st.markdown("""
<style>
    /* Main Theme Overrides */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Force Dataframe Text Wrapping and Auto Scaling */
    [data-testid="stTable"] td, [data-testid="stDataframe"] td {
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    
    /* Hero Banner Styling */
    .hero-container {
        background: linear-gradient(120deg, #10B981 0%, #059669 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.25);
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        margin-bottom: 5px !important;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.1rem !important;
        opacity: 0.95;
        font-weight: 400;
    }

    /* Metric Card Styling */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #10B981;
        margin-bottom: 15px;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #212529;
    }

    /* Content Card Box Styling */
    .info-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    /* Custom Button Enhancements */
    .stButton>button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🥗 Vibrant AI Regional Nutrition Studio</div>
    <div class="hero-subtitle">Hyper-personalized Indian regional meal plans for Diabetes, Gym Goals, Women's Health & Specialized Diets</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Options
st.sidebar.markdown("### 🎯 **Customize Your Plan**")
st.sidebar.markdown("---")

cuisine = st.sidebar.selectbox(
    "🍛 Cuisine Style",
    [
        "South Indian (Tamil Nadu)",
        "Kerala Special (Malabar)",
        "Andhra & Telangana (Spicy & High Protein)",
        "Karnataka (Udupi & Malnad Style)",
        "Chettinad Healthy",
        "North Indian (Punjabi Style)",
        "North Indian (Gujarati & Rajasthani Thali)",
        "Mughlai Vegetarian",
        "Kashmiri Pandith Vegetarian",
        "Bengali Plant-Based (Sattvic & Fish-Free)",
        "Maharashtrian (Konkan & Desh)",
        "Odia Pure Vegetarian",
        "Indo-Mediterranean Fusion",
        "Pan-Indian High-Fiber Protein Mix"
    ]
)

diet = st.sidebar.selectbox(
    "🥦 Dietary Preference",
    [
        "Strict Vegetarian",
        "High Protein Vegetarian",
        "Diabetic Friendly (Low Carb & Low GI)",
        "Vegan (100% Plant-Based)",
        "Jain Vegetarian (No Onion/Garlic/Root Veg)",
        "Sattvic (Pure & Mindful)",
        "Eggitarian"
    ]
)

goal = st.sidebar.selectbox(
    "🎯 Primary Health Goal",
    [
        "Sugar Patient (Diabetic / Pre-Diabetic Glucose Control)",
        "Weight Loss & Desk Stamina",
        "Fat Burn & Metabolism",
        "Gym Practitioner (Muscle Building & High Protein)",
        "Menopause Care (Bone Health, Hormone & Phytoestrogen Balance)",
        "PCOS / PCOD Management & Hormone Balance",
        "Heart Health & Cholesterol Control"
    ]
)

st.sidebar.markdown("---")

generate_btn = st.sidebar.button("🚀 Generate Fresh Meal Plan", use_container_width=True, type="primary")

# Backend API Interaction
if generate_btn:
    with st.spinner("✨ AI Dietitian is analyzing low-GI nutrition & regional diabetic profiles..."):
        try:
            response = requests.post(
                "http://localhost:8000/api/generate",
                json={"cuisine": cuisine, "diet": diet, "goal": goal}
            )
            
            if response.status_code == 200:
                st.session_state["meal_data"] = response.json()
                st.session_state["selected_cuisine"] = cuisine
                st.session_state["selected_diet"] = diet
                st.session_state["selected_goal"] = goal
                st.balloons()
            else:
                st.error(f"Error {response.status_code}: {response.text}")
                
        except Exception as e:
            st.error(f"⚠️ Could not connect to FastAPI backend: {e}")

# Display Interactive Dashboard
if "meal_data" in st.session_state:
    data = st.session_state["meal_data"]
    
    # Active Plan Summary Badges
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Cuisine Profile</div>
            <div class="metric-value">{st.session_state.get('selected_cuisine', 'Custom')}</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Dietary Focus</div>
            <div class="metric-value">{st.session_state.get('selected_diet', 'Custom')}</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Target Health Goal</div>
            <div class="metric-value">{st.session_state.get('selected_goal', 'Custom')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Main View Organized in Tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 7-Day Meal Plan", 
        "🩸 Sugar Control & Dietitian Notes", 
        "📲 Social Media Caption"
    ])
    
    with tab1:
        st.markdown("#### 📅 **Your Custom Weekly Meal Plan**")
        df = pd.DataFrame(data["days"])
        
        # Table Display with Full Text Visibility & Large Dynamic Columns
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "day": st.column_config.TextColumn("Day", width="small"),
                "breakfast": st.column_config.TextColumn("🍳 Breakfast", width="large"),
                "lunch": st.column_config.TextColumn("🥗 Lunch", width="large"),
                "dinner": st.column_config.TextColumn("🍲 Dinner", width="large"),
                "focus": st.column_config.TextColumn("💡 Nutritional Focus", width="large"),
            },
            hide_index=True
        )
        
        st.write("")
        
        # Download Section
        d_col1, d_col2 = st.columns([1, 3])
        with d_col1:
            if st.button("📥 Prepare Download Package", use_container_width=True):
                try:
                    res = requests.post(
                        "http://localhost:8000/api/download-pdf",
                        json=data["days"]
                    )
                    if res.status_code == 200:
                        st.download_button(
                            label="💾 Save Plan as (.txt)",
                            data=res.content,
                            file_name="7_day_regional_nutrition_plan.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Download failed: {e}")

    with tab2:
        st.markdown("#### 🩺 **Clinical Nutrition Guidelines & Glucose Tips**")
        sugar_notes = data.get("sugar_guidelines", "Maintain consistent meal timings, prioritize whole grains with a low Glycemic Index (GI), and avoid refined sugars.")
        st.info(sugar_notes)

    with tab3:
        st.markdown("#### 💬 **LinkedIn & Social Media Strategy**")
        st.markdown(f'<div class="info-box">{data["caption"]}</div>', unsafe_allow_html=True)
else:
    st.info("👈 Select your desired cuisine, diet, and health goal from the sidebar and click **Generate Fresh Meal Plan** to build your strategy!")