"""
Web-based Care Catalyst Interface
Simple HTML form to collect patient data and display results
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json
from typing import Optional

app = FastAPI(title="Care Catalyst Web Interface", version="1.0")
templates = Jinja2Templates(directory="templates")

class CareCatalystWeb:
    def __init__(self, prakriti_api_url="http://127.0.0.1:8001", risk_api_url="http://127.0.0.1:8002"):
        self.prakriti_api_url = prakriti_api_url
        self.risk_api_url = risk_api_url

    def get_unified_assessment(self, prakriti_data, risk_data):
        """Unified assessment similar to the console version"""
        try:
            # Step 1: Prakriti prediction
            prakriti_response = requests.post(
                f"{self.prakriti_api_url}/predict_prakriti",
                json=prakriti_data
            )
            prakriti_result = prakriti_response.json()
            
            # Extract dominant prakriti
            verdict = prakriti_result.get("Verdict", "")
            if "Dominant Prakriti:" in verdict:
                dominant_prakriti = verdict.split("Dominant Prakriti: ")[1].strip()
            elif "Mix Prakriti:" in verdict:
                dominant_prakriti = verdict.split("Mix Prakriti: ")[1].strip().replace(" - ", "-")
            else:
                dominant_prakriti = "Vata"
            
            # Step 2: Risk prediction with prakriti
            risk_data["prakriti_type"] = dominant_prakriti
            risk_response = requests.post(
                f"{self.risk_api_url}/predict_risk",
                json=risk_data
            )
            risk_result = risk_response.json()
            
            return {
                "success": True,
                "prakriti": prakriti_result,
                "risk": risk_result,
                "dominant_prakriti": dominant_prakriti
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}

web_assistant = CareCatalystWeb()

@app.get("/", response_class=HTMLResponse)
async def home():
    """Main form page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌿 Care Catalyst - Ayurveda + AI Health Assessment 🧠</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                padding: 30px;
            }
            .header {
                text-align: center;
                color: #4a5568;
                margin-bottom: 30px;
            }
            .section {
                background: #f7fafc;
                padding: 20px;
                margin: 20px 0;
                border-radius: 10px;
                border-left: 5px solid #667eea;
            }
            .form-group {
                margin: 15px 0;
            }
            label {
                display: block;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 5px;
            }
            input, select {
                width: 100%;
                padding: 10px;
                border: 2px solid #e2e8f0;
                border-radius: 5px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            input:focus, select:focus {
                border-color: #667eea;
                outline: none;
            }
            .submit-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                margin-top: 20px;
                transition: transform 0.2s;
            }
            .submit-btn:hover {
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌿 Care Catalyst 🧠</h1>
                <h3>Ayurvedic Constitution + Cognitive Health Assessment</h3>
                <p>Combining Ancient Wisdom with Modern AI</p>
            </div>
            
            <form method="post" action="/assess">
                
                <div class="section">
                    <h3>🧬 Ayurvedic Constitution Assessment</h3>
                    
                    <div class="form-group">
                        <label>Body Frame:</label>
                        <select name="Body_Frame" required>
                            <option value="">Select...</option>
                            <option value="Thin">Thin</option>
                            <option value="Medium">Medium</option>
                            <option value="Heavy">Heavy</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Skin Texture:</label>
                        <select name="Skin_Texture" required>
                            <option value="">Select...</option>
                            <option value="Dry">Dry</option>
                            <option value="Normal">Normal</option>
                            <option value="Oily">Oily</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Hair Type:</label>
                        <select name="Hair_Type" required>
                            <option value="">Select...</option>
                            <option value="Curly">Curly</option>
                            <option value="Straight">Straight</option>
                            <option value="Wavy">Wavy</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Eyes:</label>
                        <select name="Eyes" required>
                            <option value="">Select...</option>
                            <option value="Small">Small</option>
                            <option value="Medium">Medium</option>
                            <option value="Large">Large</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Sleep Pattern:</label>
                        <select name="Sleep_Pattern" required>
                            <option value="">Select...</option>
                            <option value="Light">Light</option>
                            <option value="Medium">Medium</option>
                            <option value="Heavy">Heavy</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Appetite:</label>
                        <select name="Appetite" required>
                            <option value="">Select...</option>
                            <option value="Variable">Variable</option>
                            <option value="Regular">Regular</option>
                            <option value="Strong">Strong</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Digestion:</label>
                        <select name="Digestion" required>
                            <option value="">Select...</option>
                            <option value="Irregular">Irregular</option>
                            <option value="Regular">Regular</option>
                            <option value="Strong">Strong</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Sweating:</label>
                        <select name="Sweating" required>
                            <option value="">Select...</option>
                            <option value="Less">Less</option>
                            <option value="Moderate">Moderate</option>
                            <option value="Profuse">Profuse</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Speech/Voice:</label>
                        <select name="Speech_Voice" required>
                            <option value="">Select...</option>
                            <option value="Fast">Fast</option>
                            <option value="Medium">Medium</option>
                            <option value="Slow">Slow</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Energy Levels:</label>
                        <select name="Energy_Levels" required>
                            <option value="">Select...</option>
                            <option value="Variable">Variable</option>
                            <option value="Steady">Steady</option>
                            <option value="High">High</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Body Temperature Preference:</label>
                        <select name="Body_Temperature" required>
                            <option value="">Select...</option>
                            <option value="Cold">Cold</option>
                            <option value="Normal">Normal</option>
                            <option value="Warm">Warm</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Weather Sensitivity:</label>
                        <select name="Weather_Sensitivity" required>
                            <option value="">Select...</option>
                            <option value="Cold">Cold</option>
                            <option value="Variable">Variable</option>
                            <option value="Hot">Hot</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Memory:</label>
                        <select name="Memory" required>
                            <option value="">Select...</option>
                            <option value="Sharp but Forgetful">Sharp but Forgetful</option>
                            <option value="Good">Good</option>
                            <option value="Excellent">Excellent</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Motion Tendencies:</label>
                        <select name="Motion_Tendencies" required>
                            <option value="">Select...</option>
                            <option value="Quick and Restless">Quick and Restless</option>
                            <option value="Moderate">Moderate</option>
                            <option value="Slow and Steady">Slow and Steady</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Mindset/Emotion:</label>
                        <select name="Mindset_Emotion" required>
                            <option value="">Select...</option>
                            <option value="Anxious and Creative">Anxious and Creative</option>
                            <option value="Balanced">Balanced</option>
                            <option value="Calm and Stable">Calm and Stable</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Elimination/Stool:</label>
                        <select name="Elimination_Stool" required>
                            <option value="">Select...</option>
                            <option value="Dry and Hard">Dry and Hard</option>
                            <option value="Normal">Normal</option>
                            <option value="Soft">Soft</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Sleep Requirement:</label>
                        <select name="Sleep_Requirement" required>
                            <option value="">Select...</option>
                            <option value="6-7 hours">6-7 hours</option>
                            <option value="7-8 hours">7-8 hours</option>
                            <option value="8+ hours">8+ hours</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Hunger Onset:</label>
                        <select name="Hunger_Onset" required>
                            <option value="">Select...</option>
                            <option value="Variable">Variable</option>
                            <option value="Regular">Regular</option>
                            <option value="Strong">Strong</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Speech Pace:</label>
                        <select name="Speech_Pace" required>
                            <option value="">Select...</option>
                            <option value="Fast">Fast</option>
                            <option value="Medium">Medium</option>
                            <option value="Slow">Slow</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Weight Tendency:</label>
                        <select name="Weight_Tendency" required>
                            <option value="">Select...</option>
                            <option value="Hard to Gain">Hard to Gain</option>
                            <option value="Stable">Stable</option>
                            <option value="Easy to Gain">Easy to Gain</option>
                        </select>
                    </div>
                </div>
                
                <div class="section">
                    <h3>🧠 Health & Cognitive Assessment</h3>
                    
                    <div class="form-group">
                        <label>Age:</label>
                        <input type="number" name="age" required min="18" max="120" value="45">
                    </div>
                    
                    <div class="form-group">
                        <label>Gender:</label>
                        <select name="gender" required>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Diet Type:</label>
                        <select name="diet_type" required>
                            <option value="Balanced">Balanced</option>
                            <option value="Vegetarian">Vegetarian</option>
                            <option value="Junk">Junk</option>
                            <option value="Mediterranean">Mediterranean</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Sleep Quality:</label>
                        <select name="sleep_quality" required>
                            <option value="Good">Good</option>
                            <option value="Poor">Poor</option>
                            <option value="Fair">Fair</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Stress Level:</label>
                        <select name="stress_level" required>
                            <option value="Low">Low</option>
                            <option value="Medium">Medium</option>
                            <option value="High">High</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Physical Activity:</label>
                        <select name="physical_activity" required>
                            <option value="Active">Active</option>
                            <option value="Moderate">Moderate</option>
                            <option value="Sedentary">Sedentary</option>
                        </select>
                    </div>
                    
                    <h4>Cognitive Symptoms:</h4>
                    
                    <div class="form-group">
                        <label>Memory Loss:</label>
                        <select name="memory_loss" required>
                            <option value="No">No</option>
                            <option value="Mild">Mild</option>
                            <option value="Sometimes">Sometimes</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Confusion:</label>
                        <select name="confusion" required>
                            <option value="No">No</option>
                            <option value="Mild">Mild</option>
                            <option value="Sometimes">Sometimes</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Language Difficulty:</label>
                        <select name="language_difficulty" required>
                            <option value="No">No</option>
                            <option value="Mild">Mild</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Decision Making:</label>
                        <select name="decision_making" required>
                            <option value="Good">Good</option>
                            <option value="Indecisive">Indecisive</option>
                            <option value="Poor">Poor</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Repetition Behavior:</label>
                        <select name="repetition_behavior" required>
                            <option value="No">No</option>
                            <option value="Sometimes">Sometimes</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Social Withdrawal:</label>
                        <select name="social_withdrawal" required>
                            <option value="No">No</option>
                            <option value="Sometimes">Sometimes</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Mood Swings:</label>
                        <select name="mood_swings" required>
                            <option value="No">No</option>
                            <option value="Sometimes">Sometimes</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Chronic Conditions:</label>
                        <select name="chronic_conditions" required>
                            <option value="None">None</option>
                            <option value="Diabetes">Diabetes</option>
                            <option value="BP">BP</option>
                            <option value="Both">Both</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Systolic Blood Pressure:</label>
                        <input type="number" name="systolic_bp" required min="80" max="200" value="120">
                    </div>
                    
                    <div class="form-group">
                        <label>Blood Sugar Level:</label>
                        <input type="number" name="blood_sugar" required min="70" max="300" value="100">
                    </div>
                    
                    <div class="form-group">
                        <label>BMI (Body Mass Index):</label>
                        <input type="number" name="bmi" required min="15" max="50" step="0.1" value="23.0">
                    </div>
                    
                    <div class="form-group">
                        <label>Family History (Cognitive Issues):</label>
                        <select name="family_history" required>
                            <option value="No">No</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn">🔍 Generate Health Assessment</button>
            </form>
        </div>
        
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Care Catalyst Web Interface"}

@app.post("/assess")
async def assess_health(request: Request):
    """Process the form and return assessment results"""
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
    
    # Extract Risk data
    risk_data = {
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
    
    # Get unified assessment
    result = web_assistant.get_unified_assessment(prakriti_data, risk_data)
    
    if not result["success"]:
        return HTMLResponse(f"<h1>Error</h1><p>{result['error']}</p>")
    
    # Generate results HTML
    prakriti = result["prakriti"]
    risk = result["risk"]
    
    html_result = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌿 Your Health Assessment Results 🧠</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                padding: 30px;
            }}
            .header {{
                text-align: center;
                color: #4a5568;
                margin-bottom: 30px;
            }}
            .result-section {{
                background: #f7fafc;
                padding: 20px;
                margin: 20px 0;
                border-radius: 10px;
                border-left: 5px solid #667eea;
            }}
            .risk-high {{ border-left-color: #e53e3e; }}
            .risk-medium {{ border-left-color: #f6ad55; }}
            .risk-low {{ border-left-color: #48bb78; }}
            .score {{
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
                text-align: center;
                margin: 15px 0;
            }}
            .recommendation {{
                background: #e6fffa;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #38b2ac;
            }}
            .back-btn {{
                background: #667eea;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 20px;
                display: inline-block;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌿 Your Personalized Health Assessment 🧠</h1>
                <p>Combining Ayurvedic Wisdom with Modern AI</p>
            </div>
            
            <div class="result-section">
                <h3>🧬 Your Ayurvedic Constitution (Prakriti)</h3>
                <div class="score">{result["dominant_prakriti"]}</div>
                <p><strong>Dosha Scores:</strong> {prakriti.get("Prakriti_Score", {})}</p>
                <p><strong>Verdict:</strong> {prakriti.get("Verdict", "")}</p>
            </div>
            
            <div class="result-section risk-{risk.get('Risk Level', 'low').lower()}">
                <h3>🧠 Cognitive Health Risk Assessment</h3>
                <div class="score">{risk.get("Risk Score (out of 100)", 0)}/100</div>
                <p><strong>Risk Level:</strong> {risk.get("Risk Level", "")}</p>
                <p><strong>Assessment:</strong> {risk.get("Verdict", "")}</p>
            </div>
            
            <div class="result-section">
                <h3>🌿 Ayurvedic Recommendations</h3>
                <div class="recommendation">
                    <h4>Constitution-Based Care:</h4>
    """
    
    # Add Prakriti recommendations
    recs = prakriti.get("Recommendations", {})
    for category, rec in recs.items():
        html_result += f"<p><strong>{category}:</strong> {rec}</p>"
    
    # Add Risk-based Ayurvedic recommendations
    if risk.get("Ayurveda Recommendations"):
        html_result += f"<h4>Cognitive Health Support:</h4><p>{risk.get('Ayurveda Recommendations')}</p>"
    
    html_result += f"""
                </div>
            </div>
            
            <div class="result-section">
                <h3>🏥 Modern Medical Recommendations</h3>
                <div class="recommendation">
                    <p>{risk.get("Allopathy Recommendations", "Regular health monitoring advised.")}</p>
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="/" class="back-btn">🔄 Take Another Assessment</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)