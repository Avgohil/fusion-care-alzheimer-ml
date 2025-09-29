#!/usr/bin/env python3
"""
Unified Care Catalyst Assistant
Combines Ayurveda Prakriti prediction and Alzheimer's risk assessment
"""

import requests
import json
from typing import Dict, Any, Optional
import pandas as pd

class CareCatalystAssistant:
    def __init__(self, prakriti_api_url="http://127.0.0.1:8001", risk_api_url="http://127.0.0.1:8002"):
        self.prakriti_api_url = prakriti_api_url
        self.risk_api_url = risk_api_url
    
    def predict_prakriti(self, prakriti_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Step 1: Call Prakriti Classification API
        """
        try:
            response = requests.post(
                f"{self.prakriti_api_url}/predict_prakriti",
                json=prakriti_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Prakriti API Error: {str(e)}"}
    
    def predict_risk(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Call Risk Prediction API
        """
        try:
            response = requests.post(
                f"{self.risk_api_url}/predict_risk",
                json=risk_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Risk API Error: {str(e)}"}
    
    def extract_dominant_prakriti(self, prakriti_result: Dict[str, Any]) -> str:
        """
        Extract the dominant prakriti type from the prakriti prediction result
        """
        if "error" in prakriti_result:
            return "Vata"  # Default fallback
        
        verdict = prakriti_result.get("Verdict", "")
        
        # Parse verdict to extract dominant dosha
        if "Dominant Prakriti:" in verdict:
            return verdict.split("Dominant Prakriti: ")[1].strip()
        elif "Mix Prakriti:" in verdict:
            # Return the mix format like "Vata-Pitta"
            mix_part = verdict.split("Mix Prakriti: ")[1].strip()
            return mix_part.replace(" - ", "-")
        else:
            # Fallback: find highest scoring dosha
            prakriti_scores = prakriti_result.get("Prakriti_Score", {})
            if prakriti_scores:
                return max(prakriti_scores, key=prakriti_scores.get)
            return "Vata"
    
    def merge_ayurveda_recommendations(self, prakriti_recs: Dict[str, str], risk_recs: str) -> Dict[str, str]:
        """
        Merge and deduplicate Ayurveda recommendations from both APIs
        """
        merged = {}
        
        # Start with prakriti recommendations
        for category, rec in prakriti_recs.items():
            merged[category] = rec
        
        # Add risk-specific recommendations
        if risk_recs and isinstance(risk_recs, str):
            merged["Cognitive_Health"] = risk_recs
        
        return merged
    
    def generate_unified_report(self, prakriti_data: Dict[str, str], risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: Generate comprehensive unified report
        """
        print("🧬 Step 1: Analyzing Ayurvedic Constitution (Prakriti)...")
        prakriti_result = self.predict_prakriti(prakriti_data)
        
        if "error" in prakriti_result:
            return {"error": f"Prakriti analysis failed: {prakriti_result['error']}"}
        
        # Extract dominant prakriti for risk analysis
        dominant_prakriti = self.extract_dominant_prakriti(prakriti_result)
        print(f"✅ Prakriti identified: {dominant_prakriti}")
        
        # Update risk data with prakriti result
        risk_data["prakriti_type"] = dominant_prakriti
        
        print("🧠 Step 2: Analyzing Cognitive Health & Risk Factors...")
        risk_result = self.predict_risk(risk_data)
        
        if "error" in risk_result:
            return {"error": f"Risk analysis failed: {risk_result['error']}"}
        
        print("📋 Step 3: Generating Unified Health Report...")
        
        # Merge Ayurveda recommendations
        prakriti_recs = prakriti_result.get("Recommendations", {})
        risk_ayurveda_recs = risk_result.get("Ayurveda Recommendations", "")
        combined_ayurveda_recs = self.merge_ayurveda_recommendations(prakriti_recs, risk_ayurveda_recs)
        
        # Generate unified report
        unified_report = {
            "🧬 Ayurvedic Analysis": {
                "Dominant_Prakriti": dominant_prakriti,
                "Dosha_Scores": prakriti_result.get("Prakriti_Score", {}),
                "Constitution_Verdict": prakriti_result.get("Verdict", "")
            },
            
            "🧠 Cognitive Health Assessment": {
                "Risk_Score": risk_result.get("Risk Score (out of 100)", 0),
                "Risk_Level": risk_result.get("Risk Level", "Unknown"),
                "Health_Verdict": risk_result.get("Verdict", "")
            },
            
            "🌿 Integrated Ayurvedic Recommendations": combined_ayurveda_recs,
            
            "🏥 Modern Medical Recommendations": risk_result.get("Allopathy Recommendations", ""),
            
            "📊 Summary": {
                "Constitution": dominant_prakriti,
                "Risk_Level": risk_result.get("Risk Level", "Unknown"),
                "Overall_Status": self.get_overall_status(
                    risk_result.get("Risk Level", "Unknown"),
                    dominant_prakriti
                )
            }
        }
        
        return unified_report
    
    def get_overall_status(self, risk_level: str, prakriti: str) -> str:
        """
        Generate overall health status summary
        """
        risk_msgs = {
            "Low": "Maintain current lifestyle",
            "Medium": "Moderate preventive care needed",
            "High": "Immediate attention recommended"
        }
        
        base_msg = risk_msgs.get(risk_level, "Monitor regularly")
        return f"{base_msg}. {prakriti} constitution-specific care advised."

def create_sample_data():
    """
    Create sample data for testing
    """
    prakriti_sample = {
        "Body_Frame": "Thin",
        "Skin_Texture": "Dry",
        "Hair_Type": "Curly",
        "Eyes": "Small",
        "Sleep_Pattern": "Light",
        "Appetite": "Variable",
        "Digestion": "Irregular",
        "Sweating": "Less",
        "Speech_Voice": "Fast",
        "Energy_Levels": "Variable",
        "Body_Temperature": "Cold",
        "Weather_Sensitivity": "Cold",
        "Memory": "Sharp but Forgetful",
        "Motion_Tendencies": "Quick and Restless",
        "Mindset_Emotion": "Anxious and Creative",
        "Elimination_Stool": "Dry and Hard",
        "Sleep_Requirement": "6-7 hours",
        "Hunger_Onset": "Variable",
        "Speech_Pace": "Fast",
        "Weight_Tendency": "Hard to Gain"
    }
    
    risk_sample = {
        "age": 68,
        "gender": "Male",
        "diet_type": "Balanced",
        "sleep_quality": "Poor",
        "stress_level": "High",
        "physical_activity": "Sedentary",
        "memory_loss": "Sometimes",
        "confusion": "Mild",
        "language_difficulty": "No",
        "decision_making": "Indecisive",
        "repetition_behavior": "Sometimes",
        "social_withdrawal": "Sometimes",
        "mood_swings": "Yes",
        "chronic_conditions": "Diabetes",
        "systolic_bp": 145,
        "blood_sugar": 135,
        "bmi": 28.5,
        "family_history": "Yes"
    }
    
    return prakriti_sample, risk_sample

def get_user_input():
    """
    Interactive function to collect user input
    """
    print("\n📝 PATIENT DATA COLLECTION")
    print("=" * 40)
    
    # Collect Prakriti data
    print("\n🧬 AYURVEDIC CONSTITUTION ASSESSMENT:")
    print("Enter your characteristics (press Enter for default values):")
    
    prakriti_data = {}
    prakriti_questions = {
        "Body_Frame": "Body frame (Thin/Medium/Heavy): ",
        "Skin_Texture": "Skin texture (Dry/Normal/Oily): ",
        "Hair_Type": "Hair type (Curly/Straight/Wavy): ",
        "Eyes": "Eye size (Small/Medium/Large): ",
        "Sleep_Pattern": "Sleep pattern (Light/Medium/Heavy): ",
        "Appetite": "Appetite (Variable/Regular/Strong): ",
        "Digestion": "Digestion (Irregular/Regular/Strong): ",
        "Sweating": "Sweating tendency (Less/Moderate/Profuse): ",
        "Speech_Voice": "Speech/Voice (Fast/Medium/Slow): ",
        "Energy_Levels": "Energy levels (Variable/Steady/High): ",
        "Body_Temperature": "Body temperature preference (Cold/Normal/Warm): ",
        "Weather_Sensitivity": "Weather sensitivity (Cold/Variable/Hot): ",
        "Memory": "Memory pattern (Sharp but Forgetful/Good/Excellent): ",
        "Motion_Tendencies": "Movement tendencies (Quick and Restless/Moderate/Slow and Steady): ",
        "Mindset_Emotion": "Mindset/Emotion (Anxious and Creative/Balanced/Calm and Stable): ",
        "Elimination_Stool": "Stool pattern (Dry and Hard/Normal/Soft): ",
        "Sleep_Requirement": "Sleep requirement (6-7 hours/7-8 hours/8+ hours): ",
        "Hunger_Onset": "Hunger pattern (Variable/Regular/Strong): ",
        "Speech_Pace": "Speech pace (Fast/Medium/Slow): ",
        "Weight_Tendency": "Weight tendency (Hard to Gain/Stable/Easy to Gain): "
    }
    
    for key, question in prakriti_questions.items():
        response = input(question).strip()
        if response:
            prakriti_data[key] = response
        else:
            # Use sample defaults
            defaults = create_sample_data()[0]
            prakriti_data[key] = defaults[key]
    
    # Collect Risk assessment data
    print("\n🧠 HEALTH & COGNITIVE ASSESSMENT:")
    risk_data = {}
    
    try:
        age = input("Age: ").strip()
        risk_data["age"] = int(age) if age else 68
        
        gender = input("Gender (Male/Female): ").strip()
        risk_data["gender"] = gender if gender in ["Male", "Female"] else "Male"
        
        risk_data["diet_type"] = input("Diet type (Balanced/Vegetarian/Junk/Mediterranean): ").strip() or "Balanced"
        risk_data["sleep_quality"] = input("Sleep quality (Good/Poor/Fair): ").strip() or "Good"
        risk_data["stress_level"] = input("Stress level (Low/Medium/High): ").strip() or "Low"
        risk_data["physical_activity"] = input("Physical activity (Active/Moderate/Sedentary): ").strip() or "Moderate"
        
        print("\nCognitive symptoms (answer: No/Mild/Sometimes/Yes):")
        risk_data["memory_loss"] = input("Memory loss: ").strip() or "No"
        risk_data["confusion"] = input("Confusion: ").strip() or "No"
        risk_data["language_difficulty"] = input("Language difficulty: ").strip() or "No"
        risk_data["decision_making"] = input("Decision making issues (Good/Indecisive/Poor): ").strip() or "Good"
        risk_data["repetition_behavior"] = input("Repetition behavior: ").strip() or "No"
        risk_data["social_withdrawal"] = input("Social withdrawal: ").strip() or "No"
        risk_data["mood_swings"] = input("Mood swings: ").strip() or "No"
        
        risk_data["chronic_conditions"] = input("Chronic conditions (None/Diabetes/BP/Both): ").strip() or "None"
        
        systolic_bp = input("Systolic BP: ").strip()
        risk_data["systolic_bp"] = int(systolic_bp) if systolic_bp else 120
        
        blood_sugar = input("Blood sugar level: ").strip()
        risk_data["blood_sugar"] = int(blood_sugar) if blood_sugar else 100
        
        bmi = input("BMI: ").strip()
        risk_data["bmi"] = float(bmi) if bmi else 23.0
        
        family_history = input("Family history of cognitive issues (Yes/No): ").strip()
        risk_data["family_history"] = family_history if family_history in ["Yes", "No"] else "No"
        
    except ValueError:
        print("⚠️ Invalid input detected, using default values where needed.")
        _, risk_defaults = create_sample_data()
        for key, default_val in risk_defaults.items():
            if key not in risk_data:
                risk_data[key] = default_val
    
    return prakriti_data, risk_data

def main():
    """
    Main function to demonstrate the unified assistant
    """
    print("🌿 Care Catalyst Unified Assistant 🧠")
    print("=" * 50)
    
    # Initialize assistant
    assistant = CareCatalystAssistant()
    
    # Choice for input method
    print("\nChoose input method:")
    print("1. Interactive input (enter your own data)")
    print("2. Use sample data (quick demo)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        prakriti_data, risk_data = get_user_input()
    else:
        print("Using sample data for quick demonstration...")
        prakriti_data, risk_data = create_sample_data()
    
    print("\n📝 Sample Patient Profile:")
    print(f"Age: {risk_data['age']}, Gender: {risk_data['gender']}")
    print(f"Constitution traits: {prakriti_data['Body_Frame']}, {prakriti_data['Skin_Texture']}, {prakriti_data['Energy_Levels']}")
    print(f"Health concerns: {risk_data['memory_loss']} memory loss, {risk_data['stress_level']} stress")
    
    # Generate unified report
    report = assistant.generate_unified_report(prakriti_data, risk_data)
    
    if "error" in report:
        print(f"\n❌ Error: {report['error']}")
        return
    
    # Display results
    print("\n" + "=" * 50)
    print("📋 UNIFIED HEALTH ASSESSMENT REPORT")
    print("=" * 50)
    
    # Ayurvedic Analysis
    ayurvedic = report["🧬 Ayurvedic Analysis"]
    print(f"\n🧬 AYURVEDIC CONSTITUTION:")
    print(f"   Dominant Prakriti: {ayurvedic['Dominant_Prakriti']}")
    print(f"   Dosha Scores: {ayurvedic['Dosha_Scores']}")
    print(f"   Verdict: {ayurvedic['Constitution_Verdict']}")
    
    # Cognitive Health
    cognitive = report["🧠 Cognitive Health Assessment"]
    print(f"\n🧠 COGNITIVE HEALTH RISK:")
    print(f"   Risk Score: {cognitive['Risk_Score']}/100")
    print(f"   Risk Level: {cognitive['Risk_Level']}")
    print(f"   Verdict: {cognitive['Health_Verdict']}")
    
    # Recommendations
    ayur_recs = report["🌿 Integrated Ayurvedic Recommendations"]
    print(f"\n🌿 AYURVEDIC RECOMMENDATIONS:")
    for category, recommendation in ayur_recs.items():
        print(f"   {category}: {recommendation}")
    
    print(f"\n🏥 MODERN MEDICAL RECOMMENDATIONS:")
    print(f"   {report['🏥 Modern Medical Recommendations']}")
    
    # Summary
    summary = report["📊 Summary"]
    print(f"\n📊 OVERALL SUMMARY:")
    print(f"   Constitution: {summary['Constitution']}")
    print(f"   Risk Level: {summary['Risk_Level']}")
    print(f"   Status: {summary['Overall_Status']}")
    
    print("\n" + "=" * 50)
    print("✅ Assessment Complete!")

if __name__ == "__main__":
    main()