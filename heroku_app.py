"""
Heroku-optimized single-app deployment
Combines all APIs into one FastAPI app for Heroku deployment
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal
import joblib
import pandas as pd
import os

# Initialize main app
app = FastAPI(title="Care Catalyst - Complete Health Assessment", version="1.0")

# Load models for Prakriti prediction
try:
    import os
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in model directory: {os.listdir('model') if os.path.exists('model') else 'model directory not found'}")
    
    prakriti_model = joblib.load("model/prakriti_model_robust.pkl")
    prakriti_encoder = joblib.load("model/prakriti_encoder.pkl")
    models_loaded = True
    print("✅ Models loaded successfully!")
except Exception as e:
    models_loaded = False
    print(f"⚠️ Warning: Model loading failed: {str(e)}")
    print("Using mock responses instead.")

# Label mapping for Prakriti
label_map = {0: 'Kapha', 1: 'Pitta', 2: 'Vata'}

# Recommendation banks
prakriti_recommendations = {
    "Vata": {
        "Diet": "Eat warm, moist, and grounding foods like soups, cooked grains, and ghee.",
        "Yoga": "Slow, grounding yoga like Hatha or Yin. Avoid overstimulation.",
        "Sleep": "Stick to a fixed schedule, warm oil massage before bed.",
        "Stress": "Meditation, calming music, warm baths, and journaling."
    },
    "Pitta": {
        "Diet": "Eat cooling foods like cucumbers, coconut, dairy. Avoid spicy/oily items.",
        "Yoga": "Calming yoga like Moon Salutation and restorative poses.",
        "Sleep": "Sleep in a cool, dark room. Avoid late-night stimulation.",
        "Stress": "Practice pranayama (Sheetali), nature walks, and reduce competition."
    },
    "Kapha": {
        "Diet": "Favor light, dry, and spicy foods. Avoid heavy, oily meals.",
        "Yoga": "Dynamic, energizing yoga like Vinyasa or Power Yoga.",
        "Sleep": "Wake early. Avoid excessive napping or oversleeping.",
        "Stress": "Stimulate with new routines, breathwork, and active hobbies."
    }
}

AYURVEDA_REC = {
    'Vata': 'Brahmi, Ashwagandha, Abhyanga massage, warm diet',
    'Pitta': 'Shankhpushpi, Gotu Kola, cooling herbs, meditation',
    'Kapha': 'Triphala, Guggulu, Panchakarma, light diet'
}

ALLOPATHY_REC = {
    'Low': 'Annual wellness exam, cognitive screening',
    'Medium': 'Memory clinic referral, neurology consultation',
    'High': 'MRI brain scan, neuropsychological testing, therapy'
}

# Pydantic models
class PrakritiInput(BaseModel):
    Body_Frame: str
    Skin_Texture: str
    Hair_Type: str
    Eyes: str
    Sleep_Pattern: str
    Appetite: str
    Digestion: str
    Sweating: str
    Speech_Voice: str
    Energy_Levels: str
    Body_Temperature: str
    Weather_Sensitivity: str
    Memory: str
    Motion_Tendencies: str
    Mindset_Emotion: str
    Elimination_Stool: str
    Sleep_Requirement: str
    Hunger_Onset: str
    Speech_Pace: str
    Weight_Tendency: str

class RiskInput(BaseModel):
    prakriti_type: Literal["Vata", "Pitta", "Kapha", "Vata-Pitta", "Pitta-Kapha", "Vata-Kapha", "Tridoshic"]
    age: int
    gender: Literal["Male", "Female"]
    diet_type: str
    sleep_quality: str
    stress_level: str
    physical_activity: str
    memory_loss: str
    confusion: str
    language_difficulty: str
    decision_making: str
    repetition_behavior: str
    social_withdrawal: str
    mood_swings: str
    chronic_conditions: str
    systolic_bp: int
    blood_sugar: int
    bmi: float
    family_history: Literal["Yes", "No"]

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Care Catalyst", "models_loaded": models_loaded}

# Prakriti prediction endpoint
@app.post("/predict_prakriti")
def predict_prakriti(input_data: PrakritiInput):
    if not models_loaded:
        # Mock response for testing
        return {
            "Prakriti_Score": {"Vata": 60, "Pitta": 25, "Kapha": 15},
            "Verdict": "🧬 Dominant Prakriti: Vata",
            "Recommendations": prakriti_recommendations["Vata"]
        }
    
    try:
        user_df = pd.DataFrame([input_data.dict()])
        user_encoded = prakriti_encoder.transform(user_df)
        user_encoded_df = pd.DataFrame(user_encoded, columns=prakriti_encoder.get_feature_names_out())

        # Prediction
        probs = prakriti_model.predict_proba(user_encoded_df)[0]
        prakriti_score = {label_map[i]: int(prob * 100) for i, prob in enumerate(probs)}

        # Dosha logic
        sorted_doshas = sorted(prakriti_score.items(), key=lambda x: x[1], reverse=True)
        top1, top2 = sorted_doshas[0], sorted_doshas[1]
        diff = top1[1] - top2[1]

        if top1[1] >= 60 and diff >= 20:
            verdict = f"🧬 Dominant Prakriti: {top1[0]}"
            recommendations = prakriti_recommendations[top1[0]]
        else:
            verdict = f"⚖️ Mix Prakriti: {top1[0]} - {top2[0]}"
            recommendations = {
                "Diet": f"{prakriti_recommendations[top1[0]]['Diet']} Also consider: {prakriti_recommendations[top2[0]]['Diet']}",
                "Yoga": f"{prakriti_recommendations[top1[0]]['Yoga']} Also try: {prakriti_recommendations[top2[0]]['Yoga']}",
                "Sleep": f"{prakriti_recommendations[top1[0]]['Sleep']} + {prakriti_recommendations[top2[0]]['Sleep']}",
                "Stress": f"{prakriti_recommendations[top1[0]]['Stress']} / {prakriti_recommendations[top2[0]]['Stress']}"
            }

        return {
            "Prakriti_Score": prakriti_score,
            "Verdict": verdict,
            "Recommendations": recommendations
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

# Risk assessment functions
def calculate_risk_score(row):
    score = 0
    
    if row['age'] > 65:
        score += 10
    
    if row['memory_loss'] == 'Sometimes':
        score += 10
    elif row['memory_loss'] == 'Mild':
        score += 5
    elif row['memory_loss'] == 'Yes':
        score += 15
    
    if row['confusion'] == 'Mild':
        score += 5
    elif row['confusion'] == 'Sometimes':
        score += 7
    elif row['confusion'] == 'Yes':
        score += 10
    
    if row['language_difficulty'] == 'Mild':
        score += 5
    elif row['language_difficulty'] == 'Yes':
        score += 10
    
    if row['decision_making'] == 'Indecisive':
        score += 5
    elif row['decision_making'] == 'Poor':
        score += 10
    
    if row['repetition_behavior'] == 'Sometimes':
        score += 5
    elif row['repetition_behavior'] == 'Yes':
        score += 8
    
    if row['social_withdrawal'] == 'Sometimes':
        score += 5
    elif row['social_withdrawal'] == 'Yes':
        score += 7
    
    if row['mood_swings'] == 'Sometimes':
        score += 3
    elif row['mood_swings'] == 'Yes':
        score += 5
    
    if row['stress_level'] in ['Moderate', 'Medium']:
        score += 5
    elif row['stress_level'] == 'High':
        score += 8
    
    if row['sleep_quality'] == 'Poor':
        score += 7
    
    if row['physical_activity'] == 'Sedentary':
        score += 5
    
    if row['diet_type'] == 'Junk':
        score += 5
    
    if row['chronic_conditions'] in ['Diabetes', 'BP', 'Both']:
        score += 10
    
    if row['family_history'] == 'Yes':
        score += 10
    
    if row['systolic_bp'] > 140:
        score += 5
    
    if row['blood_sugar'] > 130:
        score += 5
    
    if row['bmi'] < 18 or row['bmi'] > 30:
        score += 5
    
    # Dosha weighting
    prakriti = row['prakriti_type']
    if '-' in prakriti:
        doshas = prakriti.split('-')
        weights = [1.1 if d == 'Vata' else 1.05 if d == 'Kapha' else 1.0 for d in doshas]
        score *= sum(weights) / len(weights)
    elif prakriti == 'Tridoshic':
        score *= 1.05
    elif prakriti == 'Vata':
        score *= 1.1
    elif prakriti == 'Kapha':
        score *= 1.05
    else:
        score *= 1.0
    
    score = min(score, 125)
    return round((score / 125) * 100, 2)

def get_risk_level(score):
    if score <= 40:
        return "Low"
    elif 41 <= score <= 60:
        return "Medium"
    else:
        return "High"

def get_verdict(score):
    if score <= 40:
        return "Healthy but monitor"
    elif 41 <= score <= 60:
        return "Needs attention"
    else:
        return "High risk, take action"

def get_recommendations(prakriti, risk_level):
    ayurveda = []
    
    if 'Vata' in prakriti:
        ayurveda.append(AYURVEDA_REC['Vata'])
    if 'Pitta' in prakriti:
        ayurveda.append(AYURVEDA_REC['Pitta'])
    if 'Kapha' in prakriti:
        ayurveda.append(AYURVEDA_REC['Kapha'])
    if prakriti == 'Tridoshic':
        ayurveda.append("Balanced diet, Nasya, lifestyle moderation, stress detox")
    
    return ", ".join(ayurveda), ALLOPATHY_REC[risk_level]

# Risk prediction endpoint
@app.post("/predict_risk")
def predict_risk(input_data: RiskInput):
    try:
        input_dict = input_data.dict()
        score = calculate_risk_score(input_dict)
        level = get_risk_level(score)
        verdict = get_verdict(score)
        ayurveda, allopathy = get_recommendations(input_dict['prakriti_type'], level)

        return {
            "Risk Score (out of 100)": score,
            "Risk Level": level,
            "Verdict": verdict,
            "Ayurveda Recommendations": ayurveda,
            "Allopathy Recommendations": allopathy
        }
    except Exception as e:
        return {"error": f"Risk assessment failed: {str(e)}"}

# Web interface endpoints
@app.get("/", response_class=HTMLResponse)
async def home():
    """Main assessment form"""
    with open("web_interface.py", "r", encoding="utf-8") as f:
        content = f.read()
        # Extract HTML content from the web_interface.py file
        start = content.find('html_content = """') + len('html_content = """')
        end = content.find('"""', start)
        html_content = content[start:end]
        return HTMLResponse(content=html_content)

@app.post("/assess")
async def assess_health(request: Request):
    """Process assessment form"""
    form_data = await request.form()
    
    # Extract Prakriti data
    prakriti_data = {
        "Body_Frame": form_data["Body_Frame"],
        "Skin_Texture": form_data["Skin_Texture"],
        "Hair_Type": form_data["Hair_Type"],
        "Eyes": form_data["Eyes"],
        "Sleep_Pattern": form_data["Sleep_Pattern"],
        "Appetite": form_data["Appetite"],
        "Digestion": form_data["Digestion"],
        "Sweating": form_data["Sweating"],
        "Speech_Voice": form_data["Speech_Voice"],
        "Energy_Levels": form_data["Energy_Levels"],
        "Body_Temperature": form_data["Body_Temperature"],
        "Weather_Sensitivity": form_data["Weather_Sensitivity"],
        "Memory": form_data["Memory"],
        "Motion_Tendencies": form_data["Motion_Tendencies"],
        "Mindset_Emotion": form_data["Mindset_Emotion"],
        "Elimination_Stool": form_data["Elimination_Stool"],
        "Sleep_Requirement": form_data["Sleep_Requirement"],
        "Hunger_Onset": form_data["Hunger_Onset"],
        "Speech_Pace": form_data["Speech_Pace"],
        "Weight_Tendency": form_data["Weight_Tendency"]
    }
    
    # Get prakriti prediction
    prakriti_input = PrakritiInput(**prakriti_data)
    prakriti_result = predict_prakriti(prakriti_input)
    
    # Extract dominant prakriti
    verdict = prakriti_result.get("Verdict", "")
    if "Dominant Prakriti:" in verdict:
        dominant_prakriti = verdict.split("Dominant Prakriti: ")[1].strip()
    elif "Mix Prakriti:" in verdict:
        dominant_prakriti = verdict.split("Mix Prakriti: ")[1].strip().replace(" - ", "-")
    else:
        dominant_prakriti = "Vata"
    
    # Extract Risk data
    risk_data = {
        "prakriti_type": dominant_prakriti,
        "age": int(form_data["age"]),
        "gender": form_data["gender"],
        "diet_type": form_data["diet_type"],
        "sleep_quality": form_data["sleep_quality"],
        "stress_level": form_data["stress_level"],
        "physical_activity": form_data["physical_activity"],
        "memory_loss": form_data["memory_loss"],
        "confusion": form_data["confusion"],
        "language_difficulty": form_data["language_difficulty"],
        "decision_making": form_data["decision_making"],
        "repetition_behavior": form_data["repetition_behavior"],
        "social_withdrawal": form_data["social_withdrawal"],
        "mood_swings": form_data["mood_swings"],
        "chronic_conditions": form_data["chronic_conditions"],
        "systolic_bp": int(form_data["systolic_bp"]),
        "blood_sugar": int(form_data["blood_sugar"]),
        "bmi": float(form_data["bmi"]),
        "family_history": form_data["family_history"]
    }
    
    # Get risk prediction
    risk_input = RiskInput(**risk_data)
    risk_result = predict_risk(risk_input)
    
    # Generate results HTML (simplified for Heroku)
    html_result = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medical Assessment Report - Care Catalyst</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; 
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                color: #2d3748;
                line-height: 1.6;
                padding: 20px 0;
            }}
            .container {{ 
                max-width: 900px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 16px; 
                box-shadow: 0 4px 25px rgba(0,0,0,0.08);
                overflow: hidden;
                border: 1px solid #e2e8f0;
            }}
            .medical-header {{
                background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .medical-header h1 {{
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 10px;
            }}
            .results-content {{
                padding: 40px 30px;
            }}
            .result-section {{ 
                background: #f8fafc; 
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 25px; 
                margin: 25px 0; 
                border-left: 4px solid #3182ce;
            }}
            .result-section h3 {{
                color: #2b6cb0;
                font-size: 1.3rem;
                font-weight: 600;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
            }}
            .score {{ 
                font-size: 3em; 
                font-weight: 700; 
                text-align: center; 
                margin: 20px 0;
                color: #2b6cb0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .back-btn {{ 
                background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
                color: white; 
                padding: 16px 30px; 
                text-decoration: none; 
                border-radius: 12px;
                font-weight: 600;
                display: inline-block;
                margin: 30px auto;
                transition: all 0.3s ease;
            }}
            .back-btn:hover {{
                background: linear-gradient(135deg, #2c5282 0%, #2b6cb0 100%);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(43, 108, 176, 0.3);
            }}
            .medical-badge {{
                background: #e6fffa;
                color: #234e52;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 500;
                margin-left: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="medical-header">
                <h1>� Medical Assessment Report</h1>
                <p>Comprehensive Health Analysis Results</p>
            </div>
            
            <div class="results-content">
            <div class="result-section">
                <h3>⚕️ Constitutional Analysis <span class="medical-badge">Ayurvedic Profile</span></h3>
                <div class="score">{dominant_prakriti}</div>
                <p><strong>Clinical Assessment:</strong> {prakriti_result.get("Verdict", "")}</p>
            </div>
            
            <div class="result-section">
                <h3>🧠 Cognitive Risk Analysis <span class="medical-badge">Clinical Screening</span></h3>
                <div class="score">{risk_result.get("Risk Score (out of 100)", 0)}/100</div>
                <p><strong>Risk Classification:</strong> {risk_result.get("Risk Level", "")}</p>
                <p><strong>Clinical Assessment:</strong> {risk_result.get("Verdict", "")}</p>
            </div>
            
            <div class="result-section">
                <h3>📋 Treatment Recommendations <span class="medical-badge">Integrated Approach</span></h3>
                <p><strong>Traditional Medicine:</strong> {risk_result.get("Ayurveda Recommendations", "")}</p>
                <p><strong>Modern Medicine:</strong> {risk_result.get("Allopathy Recommendations", "")}</p>
            </div>
            
            <div style="text-align: center; padding: 20px 0;">
                <a href="/" class="back-btn">⚕️ New Patient Assessment</a>
            </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_result)

# For Heroku
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)