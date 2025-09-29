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
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            /* Keyframe Animations */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-50px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes pulse {
                0%, 100% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.05);
                }
            }
            
            @keyframes floating {
                0%, 100% {
                    transform: translateY(0px);
                }
                50% {
                    transform: translateY(-10px);
                }
            }
            
            @keyframes gradient-shift {
                0% {
                    background-position: 0% 50%;
                }
                50% {
                    background-position: 100% 50%;
                }
                100% {
                    background-position: 0% 50%;
                }
            }
            
            @keyframes shimmer {
                0% {
                    transform: translateX(-100%);
                }
                100% {
                    transform: translateX(100%);
                }
            }
            
            body {
                font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                background-size: 400% 400%;
                animation: gradient-shift 15s ease infinite;
                color: #2d3748;
                line-height: 1.6;
                min-height: 100vh;
                padding: 20px 0;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 16px;
                box-shadow: 0 4px 25px rgba(0,0,0,0.08);
                overflow: hidden;
                border: 1px solid #e2e8f0;
                animation: fadeInUp 1s ease-out;
                transition: all 0.3s ease;
            }
            .container:hover {
                box-shadow: 0 8px 40px rgba(0,0,0,0.12);
                transform: translateY(-2px);
            }
            .medical-header {
                background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 50%, #2b6cb0 100%);
                background-size: 200% 200%;
                animation: gradient-shift 8s ease infinite;
                color: white;
                padding: 40px 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            .medical-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="medical" patternUnits="userSpaceOnUse" width="20" height="20"><circle cx="10" cy="10" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23medical)"/></svg>');
            }
            .medical-header h1 {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 10px;
                position: relative;
                z-index: 1;
                animation: slideInLeft 1s ease-out 0.3s both;
                transition: all 0.3s ease;
            }
            .medical-header h1:hover {
                animation: floating 2s ease-in-out infinite;
            }
            .medical-header p {
                font-size: 1.1rem;
                opacity: 0.9;
                position: relative;
                z-index: 1;
                animation: fadeInUp 1s ease-out 0.6s both;
            }
            .form-content {
                padding: 40px 30px;
                animation: fadeInUp 1s ease-out 0.4s both;
            }
            .section {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 25px;
                margin: 25px 0;
                position: relative;
                border-left: 4px solid #3182ce;
                animation: slideInLeft 0.8s ease-out both;
                transition: all 0.3s ease;
                transform-origin: left center;
            }
            .section:nth-child(odd) {
                animation-delay: 0.1s;
            }
            .section:nth-child(even) {
                animation-delay: 0.2s;
            }
            .section:hover {
                transform: translateX(5px);
                box-shadow: 0 5px 20px rgba(43, 108, 176, 0.15);
                border-left-width: 6px;
            }
            .section h3 {
                color: #2b6cb0;
                font-size: 1.3rem;
                font-weight: 600;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
            }
            .section h3::before {
                content: '🏥';
                margin-right: 10px;
                font-size: 1.2rem;
            }
            .form-group {
                margin: 18px 0;
                display: flex;
                flex-direction: column;
                animation: fadeInUp 0.6s ease-out both;
            }
            .form-group:nth-child(odd) {
                animation-delay: 0.05s;
            }
            .form-group:nth-child(even) {
                animation-delay: 0.1s;
            }
            label {
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 8px;
                font-size: 0.95rem;
                transition: color 0.3s ease;
            }
            .form-group:hover label {
                color: #2b6cb0;
            }
            input, select {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 1rem;
                background: #ffffff;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                font-family: inherit;
                position: relative;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #3182ce;
                box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
                background: #fbfcfd;
                transform: translateY(-2px);
            }
            input:hover, select:hover {
                border-color: #cbd5e0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            .submit-btn {
                background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 50%, #2b6cb0 100%);
                background-size: 200% 200%;
                color: white;
                padding: 16px 40px;
                border: none;
                border-radius: 12px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                margin: 30px auto;
                display: block;
                min-width: 200px;
                position: relative;
                overflow: hidden;
                animation: pulse 2s ease-in-out infinite;
            }
            .submit-btn::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                transition: left 0.6s ease;
            }
            .submit-btn::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                background: rgba(255,255,255,0.2);
                border-radius: 50%;
                transform: translate(-50%, -50%);
                transition: width 0.6s ease, height 0.6s ease;
            }
            .submit-btn:hover {
                background-size: 100% 100%;
                animation: gradient-shift 1.5s ease infinite;
                box-shadow: 0 12px 40px rgba(43, 108, 176, 0.4);
                transform: translateY(-3px) scale(1.02);
            }
            .submit-btn:hover::before {
                left: 100%;
            }
            .submit-btn:hover::after {
                width: 300px;
                height: 300px;
            }
            .submit-btn:active {
                transform: translateY(-1px) scale(0.98);
                box-shadow: 0 8px 25px rgba(43, 108, 176, 0.3);
            }
            .medical-badge {
                display: inline-block;
                background: linear-gradient(45deg, #e6fffa, #b2f5ea);
                color: #234e52;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 500;
                border: 1px solid #b2f5ea;
                margin-left: 10px;
                transition: all 0.3s ease;
                animation: fadeInUp 0.8s ease-out both;
            }
            .medical-badge:hover {
                background: linear-gradient(45deg, #b2f5ea, #81e6d9);
                transform: scale(1.05);
                box-shadow: 0 3px 10px rgba(178, 245, 234, 0.4);
            }
            .info-tooltip {
                color: #718096;
                font-size: 0.9rem;
                margin-top: 4px;
                font-style: italic;
                opacity: 0.7;
                animation: fadeInUp 1s ease-out 0.3s both;
                transition: all 0.3s ease;
            }
            .section:hover .info-tooltip {
                opacity: 1;
                transform: translateY(-2px);
            }
            
            /* Wizard Progress Bar Styles */
            .progress-container {
                padding: 30px;
                background: #ffffff;
                border-bottom: 1px solid #e2e8f0;
            }
            .progress-bar {
                display: flex;
                align-items: center;
                justify-content: center;
                max-width: 600px;
                margin: 0 auto;
            }
            .step {
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
                transition: all 0.3s ease;
            }
            .step-number {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: #e2e8f0;
                color: #718096;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                margin-bottom: 8px;
            }
            .step.active .step-number {
                background: #3182ce;
                color: white;
                animation: pulse 2s ease-in-out infinite;
            }
            .step.completed .step-number {
                background: #38a169;
                color: white;
            }
            .step-label {
                font-size: 0.85rem;
                color: #4a5568;
                text-align: center;
                min-width: 100px;
            }
            .step.active .step-label {
                color: #3182ce;
                font-weight: 600;
            }
            .step-line {
                height: 2px;
                width: 100px;
                background: #e2e8f0;
                margin: 0 20px;
                position: relative;
                top: -25px;
            }
            .step.completed + .step-line {
                background: #38a169;
            }
            
            /* Wizard Step Content */
            .wizard-step {
                display: none;
                animation: fadeInUp 0.6s ease-out;
            }
            .wizard-step.active {
                display: block;
            }
            .step-header {
                text-align: center;
                margin: 30px 0;
                padding: 0 20px;
            }
            .step-header h2 {
                color: #2d3748;
                font-size: 2rem;
                margin-bottom: 15px;
                animation: slideInLeft 0.8s ease-out;
            }
            .step-description {
                color: #4a5568;
                font-size: 1.1rem;
                line-height: 1.6;
                max-width: 600px;
                margin: 0 auto;
                animation: fadeInUp 0.8s ease-out 0.2s both;
            }
            
            /* Navigation Buttons */
            .wizard-navigation {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 30px;
                border-top: 1px solid #e2e8f0;
                background: #f8fafc;
            }
            .nav-btn {
                padding: 12px 30px;
                border: 2px solid #3182ce;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }
            .nav-btn.primary {
                background: #3182ce;
                color: white;
            }
            .nav-btn.primary:hover {
                background: #2c5282;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(49, 130, 206, 0.3);
            }
            .nav-btn.secondary {
                background: transparent;
                color: #3182ce;
            }
            .nav-btn.secondary:hover {
                background: #3182ce;
                color: white;
            }
            .nav-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            @media (max-width: 768px) {
                .container {
                    margin: 10px;
                    border-radius: 12px;
                }
                .medical-header {
                    padding: 30px 20px;
                }
                .medical-header h1 {
                    font-size: 2rem;
                }
                .form-content {
                    padding: 30px 20px;
                }
                .section {
                    padding: 20px;
                }
            }
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
            <div class="medical-header">
                <h1>� Care Catalyst Medical Platform</h1>
                <p>Advanced AI-Driven Health Assessment System</p>
                <p style="font-size: 0.95rem; opacity: 0.8;">Integrating Ayurvedic Principles with Modern Clinical Analysis</p>
            </div>
            
            <div class="form-content">
                <form method="post" action="/assess">
                    
                    <div class="section">
                        <h3>Constitutional Analysis <span class="medical-badge">Ayurvedic Profile</span></h3>
                        <p class="info-tooltip">Complete this section for personalized constitutional assessment based on traditional Ayurvedic principles</p>
                    
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
                    <h3>Clinical Assessment <span class="medical-badge">Cognitive Screening</span></h3>
                    <p class="info-tooltip">Comprehensive cognitive health evaluation following clinical assessment protocols</p>
                    
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
                
                <button type="submit" class="submit-btn" onclick="showLoading()">⚕️ Generate Comprehensive Medical Assessment</button>
                
                <!-- Loading Animation -->
                <div id="loading" style="display:none; text-align: center; margin: 20px 0;">
                    <div style="display: inline-block; animation: spin 1s linear infinite; font-size: 2rem;">⚕️</div>
                    <p style="margin-top: 10px; color: #2b6cb0; font-weight: 600;">Processing your medical assessment...</p>
                </div>
                
                <script>
                function showLoading() {
                    document.getElementById('loading').style.display = 'block';
                    document.querySelector('.submit-btn').style.display = 'none';
                }
                </script>
                
                <style>
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
                </style>
                </form>
            </div>
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