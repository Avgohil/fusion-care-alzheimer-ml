import streamlit as st
import pandas as pd
import numpy as np
import joblib
import random

# --- Load model & features ---
model = joblib.load('models/prakriti_model_robust.pkl')
feature_columns = joblib.load("models/stage1_input_features_clean.pkl")

# --- Fix for DataFrame issue ---
if isinstance(feature_columns, pd.DataFrame):
    feature_columns = feature_columns.columns.tolist()
elif isinstance(feature_columns, (np.ndarray, pd.Series)):
    feature_columns = feature_columns.flatten().tolist()
elif isinstance(feature_columns, dict):
    feature_columns = list(feature_columns.keys())

# --- Label mapping ---
label_mapping = {0: "Vata", 1: "Pitta", 2: "Kapha"}

# --- Question Pool ---
question_pool = [
    {"question": "How would you describe your body frame?", "feature": "Body_Frame",
     "options": ["Thin, light", "Medium, muscular", "Heavy, broad"]},
    {"question": "How would you describe your skin texture?", "feature": "Skin_Texture",
     "options": ["Dry, rough, cold", "Warm, oily, reddish", "Smooth, moist, thick"]},
    {"question": "What best describes your hair type?", "feature": "Hair_Type",
     "options": ["Dry, frizzy, brittle", "Soft, oily, reddish/brown", "Thick, strong, oily"]},
    {"question": "How do you usually feel during sleep?", "feature": "Sleep_Pattern",
     "options": ["Light, interrupted", "Moderate", "Deep, prolonged"]},
    {"question": "How would you describe your appetite?", "feature": "Appetite",
     "options": ["Irregular", "Strong, frequent hunger", "Slow, steady"]},
    {"question": "What best describes your digestion?", "feature": "Digestion",
     "options": ["Variable, bloating", "Fast, prone to acidity", "Slow, sluggish"]},
    {"question": "Which best describes your psychological tendencies?", "feature": "Mindset_Emotion",
     "options": ["Fear, anxiety", "Anger, irritability", "Calm, possessive"]},
    {"question": "How would you characterize your energy levels?", "feature": "Energy_Levels",
     "options": ["Variable, bursts of energy", "High but gets tired fast", "Steady, consistent"]},
    {"question": "Which best describes your body weight tendency?", "feature": "Weight_Tendency",
     "options": ["Underweight", "Normal weight", "Tendency to gain weight"]},
    {"question": "How would you describe your speech and behavior pace?", "feature": "Speech_Pace",
     "options": ["Fast", "Measured", "Slow"]},
    {"question": "How would you describe your eyes?", "feature": "Eyes",
     "options": ["Sharp, intense, reddish", "Large, calm, watery", "Small, dry, dull"]},
    {"question": "How is your body temperature?", "feature": "Body_Temperature",
     "options": ["Warm", "Cool", "Cold"]},
    {"question": "How do you react to weather?", "feature": "Weather_Sensitivity",
     "options": ["Dislikes heat", "Dislikes cold, wind", "Dislikes damp, cold"]},
    {"question": "How is your memory?", "feature": "Memory",
     "options": ["Sharp memory, good retention", "Quick grasp, poor retention", "Slow learning, excellent retention"]},
    {"question": "How are your motion tendencies?", "feature": "Motion_Tendencies",
     "options": ["Purposeful, active", "Moderate", "Slow, lazy"]},
    {"question": "How is your stool/urination?", "feature": "Elimination_Stool",
     "options": ["Loose, frequent", "Dry, hard, constipation", "Well-formed, slow"]},
    {"question": "How many hours of sleep do you need?", "feature": "Sleep_Requirement",
     "options": ["4–6 hours", "6–7 hours", "8–10 hours"]},
    {"question": "How fast does hunger onset occur?", "feature": "Hunger_Onset",
     "options": ["Sharp, quick hunger", "Irregular", "Mild, slow hunger"]},
    {"question": "How would you describe your speech voice?", "feature": "Speech_Voice",
     "options": ["Sharp, loud", "Fast, low pitch", "Slow, melodious"]},
    {"question": "How would you describe your sweating?", "feature": "Sweating",
     "options": ["Profuse, with odor", "Moderate, little odor", "Less"]},
]

MAX_QUESTIONS = 10

# --- Reset Quiz ---
def reset_quiz():
    st.session_state['quiz_questions'] = random.sample(question_pool, MAX_QUESTIONS)
    st.session_state['quiz_answers'] = {}
    st.session_state['submitted'] = False

# --- Main App ---
def main():
    st.title("🌿 Short Ayurvedic Prakriti Assessment")

    if 'quiz_questions' not in st.session_state:
        reset_quiz()

    if st.button("🌀 New Assessment"):
        reset_quiz()
        st.experimental_rerun()

    for idx, q in enumerate(st.session_state['quiz_questions']):
        response = st.radio(f"Q{idx+1}. {q['question']}", q["options"], key=f'q{idx}')
        st.session_state['quiz_answers'][q["feature"]] = response

    if st.button("✅ Submit and Predict"):
        if len(st.session_state['quiz_answers']) < len(st.session_state['quiz_questions']):
            st.warning("Please answer all questions before submitting!")
            return
        st.session_state['submitted'] = True

    if st.session_state.get('submitted', False):
        st.subheader("📝 Your Responses")
        st.write(st.session_state['quiz_answers'])

        # One-hot encoding
        input_one_hot = pd.DataFrame(np.zeros((1, len(feature_columns))), columns=feature_columns)
        for feat, val in st.session_state['quiz_answers'].items():
            col_name = f"{feat}_{val}"
            if col_name in input_one_hot.columns:
                input_one_hot.at[0, col_name] = 1
            else:
                st.warning(f"Feature '{col_name}' not in model features, skipping.")

        pred = model.predict(input_one_hot)[0]
        proba = model.predict_proba(input_one_hot)[0]

        # Map to labels
        confidence = {label_mapping[i]: float(round(p, 3)) for i, p in enumerate(proba)}
        dominant = max(confidence, key=confidence.get)

        # Show results
        st.subheader("📊 Prakriti Scores")
        st.json(confidence)

        st.subheader("🌟 Dominant Prakriti Type")
        st.success(f"Your dominant Prakriti is **{dominant}** (ML Model Prediction)")
        st.caption("This prediction is made by a machine learning model trained on Ayurvedic data and is generally more accurate.")

        # Recommendations
        recommendations = {
            "Vata": {
                "Diet": "Warm, moist foods; soups, cooked grains, healthy oils.",
                "Lifestyle": "Regular routines, restful sleep, gentle exercise.",
                "Supplements": "Ashwagandha, sesame oil massage."
            },
            "Pitta": {
                "Diet": "Cooling foods; fruits, vegetables, whole grains.",
                "Lifestyle": "Mindfulness, avoid overheating, relaxation.",
                "Supplements": "Brahmi, Aloe Vera."
            },
            "Kapha": {
                "Diet": "Light, warm, dry foods with spices.",
                "Lifestyle": "Regular vigorous exercise.",
                "Supplements": "Ginger, turmeric."
            }
        }
        rec = recommendations.get(dominant, {})
        for key, val in rec.items():
            st.markdown(f"**{key}:** {val}")


if __name__ == "__main__":
    main()


