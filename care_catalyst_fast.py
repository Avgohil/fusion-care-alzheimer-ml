from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Literal, Optional
import os
import random
import time

app = FastAPI(title="Care Catalyst - Ayurveda & Alzheimer's Risk Assessment", version="1.0")

# For demo purposes, we'll simulate the models
# Label mapping for Stage 1
prakriti_label_map = {0: 'Kapha', 1: 'Pitta', 2: 'Vata'}

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

# Ayurveda and Allopathy recommendations for Stage 2
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

# Input schema for the complete assessment
class AssessmentInput(BaseModel):
    # Stage 1: Ayurvedic Prakriti fields (20 fields)
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
    
    # Stage 2: Health and Alzheimer's risk fields (18 fields)
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

def predict_prakriti_demo(input_data: dict):
    """Demo Stage 1: Predict Ayurvedic Prakriti using rule-based logic"""
    vata_score = 0
    pitta_score = 0
    kapha_score = 0
    
    # Rule-based scoring based on characteristics
    
    # Body Frame
    if input_data['Body_Frame'] == 'Thin, light':
        vata_score += 3
    elif input_data['Body_Frame'] == 'Medium, muscular':
        pitta_score += 3
    elif input_data['Body_Frame'] == 'Heavy, broad':
        kapha_score += 3
    
    # Skin Texture
    if input_data['Skin_Texture'] == 'Dry, rough, cold':
        vata_score += 3
    elif input_data['Skin_Texture'] == 'Warm, oily, reddish':
        pitta_score += 3
    elif input_data['Skin_Texture'] == 'Smooth, moist, thick':
        kapha_score += 3
    
    # Hair Type
    if input_data['Hair_Type'] == 'Dry, frizzy, brittle':
        vata_score += 3
    elif input_data['Hair_Type'] == 'Soft, oily, reddish/brown':
        pitta_score += 3
    elif input_data['Hair_Type'] == 'Thick, strong, oily':
        kapha_score += 3
    
    # Eyes
    if input_data['Eyes'] == 'Small, dry, dull':
        vata_score += 3
    elif input_data['Eyes'] == 'Sharp, intense, reddish':
        pitta_score += 3
    elif input_data['Eyes'] == 'Large, calm, watery':
        kapha_score += 3
    
    # Appetite
    if input_data['Appetite'] == 'Irregular':
        vata_score += 2
    elif input_data['Appetite'] == 'Strong, frequent hunger':
        pitta_score += 2
    elif input_data['Appetite'] == 'Slow, steady':
        kapha_score += 2
    
    # Add some variability
    vata_score += random.randint(0, 5)
    pitta_score += random.randint(0, 5)
    kapha_score += random.randint(0, 5)
    
    # Normalize scores
    total = vata_score + pitta_score + kapha_score
    if total == 0:
        total = 1
    
    prakriti_score = {
        'Vata': int((vata_score / total) * 100),
        'Pitta': int((pitta_score / total) * 100),
        'Kapha': int((kapha_score / total) * 100)
    }
    
    # Determine dominant prakriti
    sorted_doshas = sorted(prakriti_score.items(), key=lambda x: x[1], reverse=True)
    top1, top2 = sorted_doshas[0], sorted_doshas[1]
    diff = top1[1] - top2[1]
    
    if top1[1] >= 60 and diff >= 20:
        verdict = f"{top1[0]}"
        recommendations = prakriti_recommendations[top1[0]]
    else:
        verdict = f"{top1[0]}-{top2[0]}"
        # Combine recommendations for mixed prakriti
        recommendations = {
            "Diet": f"{prakriti_recommendations[top1[0]]['Diet']} Also consider: {prakriti_recommendations[top2[0]]['Diet']}",
            "Yoga": f"{prakriti_recommendations[top1[0]]['Yoga']} Also try: {prakriti_recommendations[top2[0]]['Yoga']}",
            "Sleep": f"{prakriti_recommendations[top1[0]]['Sleep']} + {prakriti_recommendations[top2[0]]['Sleep']}",
            "Stress": f"{prakriti_recommendations[top1[0]]['Stress']} / {prakriti_recommendations[top2[0]]['Stress']}"
        }
    
    return {
        "prakriti_type": verdict,
        "prakriti_scores": prakriti_score,
        "recommendations": recommendations
    }

def calculate_alzheimer_risk_score(input_data: dict):
    """Stage 2: Calculate Alzheimer's risk score"""
    score = 0
    
    # Age scoring
    if input_data['age'] > 65:
        score += 10
    elif input_data['age'] > 55:
        score += 5
    
    # Memory and cognitive symptoms
    if input_data['memory_loss'] == 'Sometimes':
        score += 10
    elif input_data['memory_loss'] == 'Mild':
        score += 15
    elif input_data['memory_loss'] == 'Severe':
        score += 20
    
    if input_data['confusion'] == 'Sometimes':
        score += 10
    elif input_data['confusion'] == 'Often':
        score += 15
    
    if input_data['language_difficulty'] == 'Mild':
        score += 5
    elif input_data['language_difficulty'] == 'Yes':
        score += 10
    
    if input_data['decision_making'] == 'Indecisive':
        score += 5
    elif input_data['decision_making'] == 'Poor':
        score += 10
    
    if input_data['repetition_behavior'] == 'Sometimes':
        score += 5
    elif input_data['repetition_behavior'] == 'Often':
        score += 10
    
    if input_data['social_withdrawal'] == 'Sometimes':
        score += 5
    elif input_data['social_withdrawal'] == 'Often':
        score += 10
    
    if input_data['mood_swings'] == 'Sometimes':
        score += 5
    elif input_data['mood_swings'] == 'Often':
        score += 10
    
    # Lifestyle factors
    if input_data['sleep_quality'] == 'Poor':
        score += 5
    
    if input_data['stress_level'] == 'High':
        score += 5
    
    if input_data['physical_activity'] == 'Low':
        score += 5
    
    # Health indicators
    if input_data['systolic_bp'] > 140:
        score += 8
    elif input_data['systolic_bp'] > 130:
        score += 4
    
    if input_data['blood_sugar'] > 126:
        score += 8
    elif input_data['blood_sugar'] > 100:
        score += 4
    
    if input_data['bmi'] > 30:
        score += 6
    elif input_data['bmi'] > 25:
        score += 3
    
    # Family history
    if input_data['family_history'] == 'Yes':
        score += 15
    
    # Chronic conditions
    if input_data['chronic_conditions'] != 'None':
        score += 5
    
    return min(score, 100)  # Cap at 100

def get_risk_level(score):
    """Convert score to risk level"""
    if score <= 40:
        return "Low"
    elif 41 <= score <= 60:
        return "Medium"
    else:
        return "High"

def get_verdict(score):
    """Get verdict based on risk score"""
    if score <= 40:
        return "Healthy but monitor"
    elif 41 <= score <= 60:
        return "Needs attention"
    else:
        return "High risk, take action"

def get_recommendations(prakriti, risk_level):
    """Get combined recommendations"""
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

def generate_fast_chart_data(risk_score):
    """Generate chart data for frontend rendering - no image generation"""
    # Determine color based on risk score
    if risk_score <= 40:
        color = "#10B981"  # Green
        bg_color = "#D1FAE5"  # Light green
        risk_text = "Low Risk"
    elif risk_score <= 60:
        color = "#F59E0B"  # Yellow
        bg_color = "#FEF3C7"  # Light yellow
        risk_text = "Medium Risk"
    else:
        color = "#EF4444"  # Red
        bg_color = "#FEE2E2"  # Light red
        risk_text = "High Risk"
    
    return {
        "score": risk_score,
        "percentage": risk_score,
        "color": color,
        "bg_color": bg_color,
        "risk_text": risk_text,
        "chart_type": "css_gauge"  # Signal to frontend to use CSS rendering
    }

@app.post("/predict")
async def predict_assessment(input_data: AssessmentInput):
    """Main endpoint that processes both stages and returns complete results"""
    try:
        start_time = time.time()
        input_dict = input_data.dict()
        
        # Stage 1: Predict Prakriti
        prakriti_result = predict_prakriti_demo(input_dict)
        
        # Add prakriti to input for Stage 2
        input_dict['prakriti_type'] = prakriti_result['prakriti_type']
        
        # Stage 2: Calculate Alzheimer's risk
        risk_score = calculate_alzheimer_risk_score(input_dict)
        risk_level = get_risk_level(risk_score)
        verdict = get_verdict(risk_score)
        
        # Get recommendations
        ayurveda_rec, allopathy_rec = get_recommendations(
            prakriti_result['prakriti_type'], 
            risk_level
        )
        
        # Generate fast chart data (no image generation)
        chart_data = generate_fast_chart_data(risk_score)
        
        processing_time = time.time() - start_time
        print(f"Processing completed in {processing_time:.2f} seconds")
        
        # Return complete response
        return {
            "prakriti_result": prakriti_result['prakriti_type'],
            "prakriti_scores": prakriti_result['prakriti_scores'],
            "prakriti_recommendations": prakriti_result['recommendations'],
            "alzheimer_risk": risk_level,
            "risk_score": risk_score,
            "verdict": verdict,
            "ayurveda_recommendations": ayurveda_rec,
            "allopathy_recommendations": allopathy_rec,
            "chart_data": chart_data,  # Fast chart data instead of image
            "processing_time": f"{processing_time:.2f}s"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing assessment: {str(e)}")

@app.get("/")
async def serve_frontend():
    """Serve the main HTML page"""
    return FileResponse("static/index_fast.html")

# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)