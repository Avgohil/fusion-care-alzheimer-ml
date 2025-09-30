from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Prakriti Classification API", version="1.0")

# Load model and encoder
model = joblib.load("model/prakriti_model_robust.pkl")
encoder = joblib.load("model/prakriti_encoder.pkl")

# Label mapping
label_map = {0: 'Kapha', 1: 'Pitta', 2: 'Vata'}

# Recommendation bank
recommendation_bank = {
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

# Input schema
class UserInput(BaseModel):
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

@app.post("/predict_prakriti")
def predict_prakriti(input_data: UserInput):
    user_df = pd.DataFrame([input_data.dict()])
    user_encoded = encoder.transform(user_df)
    user_encoded_df = pd.DataFrame(user_encoded, columns=encoder.get_feature_names_out())

    # Prediction
    probs = model.predict_proba(user_encoded_df)[0]
    prakriti_score = {label_map[i]: int(prob * 100) for i, prob in enumerate(probs)}

    # Dosha logic
    sorted_doshas = sorted(prakriti_score.items(), key=lambda x: x[1], reverse=True)
    top1, top2 = sorted_doshas[0], sorted_doshas[1]
    diff = top1[1] - top2[1]

    if top1[1] >= 60 and diff >= 20:
        verdict = f"🧬 Dominant Prakriti: {top1[0]}"
        recommendations = recommendation_bank[top1[0]]  # Single dosha recos
    else:
        verdict = f"⚖️ Mix Prakriti: {top1[0]} - {top2[0]}"
        recommendations = {
            "Diet": f"{recommendation_bank[top1[0]]['Diet']} Also consider: {recommendation_bank[top2[0]]['Diet']}",
            "Yoga": f"{recommendation_bank[top1[0]]['Yoga']} Also try: {recommendation_bank[top2[0]]['Yoga']}",
            "Sleep": f"{recommendation_bank[top1[0]]['Sleep']} + {recommendation_bank[top2[0]]['Sleep']}",
            "Stress": f"{recommendation_bank[top1[0]]['Stress']} / {recommendation_bank[top2[0]]['Stress']}"
        }

    return {
        "Prakriti_Score": prakriti_score,
        "Verdict": verdict,
        "Recommendations": recommendations
    }
