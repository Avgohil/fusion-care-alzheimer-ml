import requests
import json

# Test data for the API
test_data = {
    # Stage 1: Ayurvedic Prakriti fields
    "Body_Frame": "Medium, muscular",
    "Skin_Texture": "Warm, oily, reddish",
    "Hair_Type": "Soft, oily, reddish/brown",
    "Eyes": "Sharp, intense, reddish",
    "Sleep_Pattern": "Moderate",
    "Appetite": "Strong, frequent hunger",
    "Digestion": "Fast, prone to acidity",
    "Sweating": "Profuse, with odor",
    "Speech_Voice": "Sharp, loud",
    "Energy_Levels": "High, sustained",
    "Body_Temperature": "Warm/hot",
    "Weather_Sensitivity": "Dislikes heat/sun",
    "Memory": "Sharp, clear",
    "Motion_Tendencies": "Moderate, purposeful",
    "Mindset_Emotion": "Intense, irritable",
    "Elimination_Stool": "Regular, loose",
    "Sleep_Requirement": "Moderate sleep needs",
    "Hunger_Onset": "Gets hungry quickly",
    "Speech_Pace": "Moderate, clear",
    "Weight_Tendency": "Normal weight",
    
    # Stage 2: Health and Alzheimer's risk fields
    "age": 45,
    "gender": "Male",
    "diet_type": "Balanced",
    "sleep_quality": "Good",
    "stress_level": "Medium",
    "physical_activity": "High",
    "memory_loss": "None",
    "confusion": "None",
    "language_difficulty": "None",
    "decision_making": "Good",
    "repetition_behavior": "None",
    "social_withdrawal": "None",
    "mood_swings": "None",
    "chronic_conditions": "None",
    "systolic_bp": 120,
    "blood_sugar": 100,
    "bmi": 23.5,
    "family_history": "No"
}

def test_api():
    """Test the Care Catalyst API endpoint"""
    try:
        print("Testing Care Catalyst API...")
        print("=" * 50)
        
        # Send POST request to the API
        response = requests.post(
            "http://localhost:8000/predict",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ API Test Successful!")
            print("\n📊 Results:")
            print(f"Prakriti Result: {result['prakriti_result']}")
            print(f"Prakriti Scores: {result['prakriti_scores']}")
            print(f"Alzheimer Risk: {result['alzheimer_risk']}")
            print(f"Risk Score: {result['risk_score']}/100")
            print(f"Verdict: {result['verdict']}")
            print(f"Chart Generated: {'Yes' if result['chart'].startswith('data:image') else 'No'}")
            
            print("\n🌿 Ayurveda Recommendations:")
            print(result['ayurveda_recommendations'])
            
            print("\n🏥 Medical Recommendations:")
            print(result['allopathy_recommendations'])
            
            return True
        else:
            print(f"❌ API Test Failed! Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_api()