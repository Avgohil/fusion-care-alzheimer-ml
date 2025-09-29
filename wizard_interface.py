"""
Enhanced Wizard-based Web Interface for Care Catalyst
Multi-step assessment with professional medical design
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import requests
import json

app = FastAPI(title="Care Catalyst Medical Wizard", version="2.0")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Multi-step wizard assessment form"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏥 Care Catalyst Medical Platform - Health Assessment Wizard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            /* Keyframe Animations */
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes slideInLeft {
                from { opacity: 0; transform: translateX(-50px); }
                to { opacity: 1; transform: translateX(0); }
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            @keyframes gradient-shift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            body {
                font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
                background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
                color: #1e293b;
                line-height: 1.6;
                min-height: 100vh;
            }
            
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: #ffffff;
                min-height: 100vh;
                box-shadow: 0 0 50px rgba(0,0,0,0.1);
                animation: fadeInUp 1s ease-out;
            }
            
            .medical-header {
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #1e40af 100%);
                background-size: 200% 200%;
                animation: gradient-shift 10s ease infinite;
                color: white;
                padding: 40px 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            
            .medical-header h1 {
                font-size: 2.8rem;
                font-weight: 800;
                margin-bottom: 10px;
                animation: slideInLeft 1s ease-out;
            }
            
            .medical-header p {
                font-size: 1.2rem;
                opacity: 0.95;
                animation: fadeInUp 1s ease-out 0.3s both;
            }
            
            /* Progress Bar Styles */
            .progress-container {
                padding: 40px 30px;
                background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                border-bottom: 1px solid #e2e8f0;
            }
            
            .progress-bar {
                display: flex;
                align-items: center;
                justify-content: center;
                max-width: 700px;
                margin: 0 auto;
            }
            
            .step {
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
                transition: all 0.4s ease;
            }
            
            .step-number {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: #e2e8f0;
                color: #64748b;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 1.3rem;
                transition: all 0.4s ease;
                margin-bottom: 12px;
                border: 3px solid transparent;
            }
            
            .step.active .step-number {
                background: #3b82f6;
                color: white;
                animation: pulse 2s ease-in-out infinite;
                border-color: #dbeafe;
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
            }
            
            .step.completed .step-number {
                background: #10b981;
                color: white;
                border-color: #d1fae5;
            }
            
            .step-label {
                font-size: 0.95rem;
                color: #64748b;
                text-align: center;
                min-width: 120px;
                font-weight: 500;
            }
            
            .step.active .step-label {
                color: #3b82f6;
                font-weight: 700;
            }
            
            .step-line {
                height: 3px;
                width: 120px;
                background: #e2e8f0;
                margin: 0 20px;
                position: relative;
                top: -30px;
                border-radius: 2px;
            }
            
            .step.completed + .step-line {
                background: #10b981;
            }
            
            /* Wizard Step Content */
            .wizard-step {
                display: none;
                padding: 50px 40px;
                animation: fadeInUp 0.8s ease-out;
            }
            
            .wizard-step.active {
                display: block;
            }
            
            .step-header {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .step-header h2 {
                color: #1e293b;
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 15px;
                animation: slideInLeft 0.8s ease-out;
            }
            
            .step-description {
                color: #475569;
                font-size: 1.2rem;
                line-height: 1.7;
                max-width: 700px;
                margin: 0 auto;
                animation: fadeInUp 0.8s ease-out 0.2s both;
            }
            
            .section {
                background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                border: 2px solid #e2e8f0;
                border-radius: 16px;
                padding: 35px;
                margin: 30px 0;
                border-left: 6px solid #3b82f6;
                animation: slideInLeft 0.8s ease-out both;
                transition: all 0.3s ease;
            }
            
            .section:hover {
                transform: translateX(5px);
                box-shadow: 0 8px 30px rgba(59, 130, 246, 0.15);
                border-left-width: 8px;
            }
            
            .section h3 {
                color: #1e40af;
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
            }
            
            .medical-badge {
                background: linear-gradient(45deg, #dbeafe, #bfdbfe);
                color: #1e40af;
                padding: 6px 16px;
                border-radius: 25px;
                font-size: 0.9rem;
                font-weight: 600;
                margin-left: 15px;
                border: 2px solid #93c5fd;
                animation: fadeInUp 0.8s ease-out both;
            }
            
            .info-tooltip {
                color: #64748b;
                font-size: 1rem;
                margin-bottom: 25px;
                font-style: italic;
                animation: fadeInUp 1s ease-out 0.3s both;
            }
            
            .form-group {
                margin: 20px 0;
                animation: fadeInUp 0.6s ease-out both;
            }
            
            .form-group label {
                font-weight: 600;
                color: #1e293b;
                margin-bottom: 8px;
                display: block;
                font-size: 1rem;
            }
            
            .form-group select,
            .form-group input {
                width: 100%;
                padding: 14px 18px;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                font-size: 1rem;
                background: #ffffff;
                transition: all 0.3s ease;
                font-family: inherit;
            }
            
            .form-group select:focus,
            .form-group input:focus {
                outline: none;
                border-color: #3b82f6;
                box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
                transform: translateY(-2px);
            }
            
            .form-group select:hover,
            .form-group input:hover {
                border-color: #cbd5e0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            }
            
            /* Navigation Buttons */
            .wizard-navigation {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 40px;
                background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                border-top: 2px solid #e2e8f0;
            }
            
            .nav-btn {
                padding: 16px 32px;
                border: 2px solid #3b82f6;
                border-radius: 12px;
                font-weight: 700;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                min-width: 140px;
                text-align: center;
            }
            
            .nav-btn.primary {
                background: #3b82f6;
                color: white;
            }
            
            .nav-btn.primary:hover {
                background: #2563eb;
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
            }
            
            .nav-btn.secondary {
                background: transparent;
                color: #3b82f6;
            }
            
            .nav-btn.secondary:hover {
                background: #3b82f6;
                color: white;
            }
            
            @media (max-width: 768px) {
                .progress-bar {
                    flex-direction: column;
                    gap: 20px;
                }
                .step-line {
                    width: 3px;
                    height: 40px;
                    top: 0;
                    margin: 10px 0;
                }
                .wizard-step {
                    padding: 30px 20px;
                }
                .step-header h2 {
                    font-size: 2rem;
                }
                .wizard-navigation {
                    flex-direction: column;
                    gap: 15px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="medical-header">
                <h1>🏥 Care Catalyst Medical Platform</h1>
                <p>Advanced AI-Driven Health Assessment System</p>
                <p style="font-size: 1rem; opacity: 0.9;">Step-by-Step Comprehensive Health Evaluation</p>
            </div>
            
            <!-- Progress Indicator -->
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="step active" data-step="1">
                        <div class="step-number">1</div>
                        <div class="step-label">Ayurvedic Analysis</div>
                    </div>
                    <div class="step-line"></div>
                    <div class="step" data-step="2">
                        <div class="step-number">2</div>
                        <div class="step-label">Clinical Assessment</div>
                    </div>
                    <div class="step-line"></div>
                    <div class="step" data-step="3">
                        <div class="step-number">3</div>
                        <div class="step-label">Medical Report</div>
                    </div>
                </div>
            </div>
            
            <form method="post" action="/assess" id="wizard-form">
                
                <!-- Step 1: Ayurvedic Constitutional Analysis -->
                <div class="wizard-step active" id="step-1">
                    <div class="step-header">
                        <h2>🌿 Ayurvedic Constitutional Analysis</h2>
                        <p class="step-description">
                            Discover your unique body constitution (Prakriti) based on traditional Ayurvedic principles. 
                            This analysis reveals your natural physical and mental characteristics that have been with you since birth.
                        </p>
                    </div>
                    
                    <div class="section">
                        <h3>Physical Constitution Assessment <span class="medical-badge">Prakriti Analysis</span></h3>
                        <p class="info-tooltip">Please answer based on your natural, lifelong characteristics</p>
                        
                        <div class="form-group">
                            <label>Body Frame:</label>
                            <select name="Body_Frame" required>
                                <option value="">Select your natural body frame...</option>
                                <option value="Thin">Thin (naturally slender, find it hard to gain weight)</option>
                                <option value="Medium">Medium (moderate build, balanced proportions)</option>
                                <option value="Heavy">Heavy (solid build, tendency to gain weight easily)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Skin Texture:</label>
                            <select name="Skin_Texture" required>
                                <option value="">Select your natural skin type...</option>
                                <option value="Dry">Dry (tends to be rough, flaky)</option>
                                <option value="Oily">Oily (tends to be greasy, shiny)</option>
                                <option value="Normal">Normal (balanced, neither too dry nor oily)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Hair Type:</label>
                            <select name="Hair_Type" required>
                                <option value="">Select your natural hair characteristics...</option>
                                <option value="Dry">Dry (brittle, frizzy, lacks luster)</option>
                                <option value="Oily">Oily (greasy, needs frequent washing)</option>
                                <option value="Normal">Normal (balanced texture and shine)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Eyes:</label>
                            <select name="Eyes" required>
                                <option value="">Select your eye characteristics...</option>
                                <option value="Small">Small (smaller in size)</option>
                                <option value="Medium">Medium (average size)</option>
                                <option value="Large">Large (prominent, expressive)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Sleep Pattern:</label>
                            <select name="Sleep_Pattern" required>
                                <option value="">Select your natural sleep tendency...</option>
                                <option value="Light">Light (easily disturbed, restless sleep)</option>
                                <option value="Sound">Sound (deep, uninterrupted sleep)</option>
                                <option value="Variable">Variable (sometimes light, sometimes deep)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Appetite:</label>
                            <select name="Appetite" required>
                                <option value="">Select your appetite pattern...</option>
                                <option value="Variable">Variable (irregular hunger patterns)</option>
                                <option value="Strong">Strong (regular, strong hunger)</option>
                                <option value="Low">Low (generally poor appetite)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Digestion:</label>
                            <select name="Digestion" required>
                                <option value="">Select your digestion pattern...</option>
                                <option value="Variable">Variable (sometimes good, sometimes poor)</option>
                                <option value="Strong">Strong (can digest most foods easily)</option>
                                <option value="Weak">Weak (sensitive stomach, digestive issues)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Sweating:</label>
                            <select name="Sweating" required>
                                <option value="">Select your sweating tendency...</option>
                                <option value="Minimal">Minimal (sweat very little)</option>
                                <option value="Profuse">Profuse (sweat heavily)</option>
                                <option value="Moderate">Moderate (average sweating)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Speech/Voice:</label>
                            <select name="Speech_Voice" required>
                                <option value="">Select your speech pattern...</option>
                                <option value="Fast">Fast (speak quickly)</option>
                                <option value="Slow">Slow (speak slowly)</option>
                                <option value="Moderate">Moderate (normal pace)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Energy Levels:</label>
                            <select name="Energy_Levels" required>
                                <option value="">Select your energy pattern...</option>
                                <option value="Variable">Variable (fluctuating energy)</option>
                                <option value="High">High (consistently energetic)</option>
                                <option value="Low">Low (generally tired)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Body Temperature:</label>
                            <select name="Body_Temperature" required>
                                <option value="">Select your temperature preference...</option>
                                <option value="Cold">Cold (always feel cold)</option>
                                <option value="Hot">Hot (always feel warm)</option>
                                <option value="Variable">Variable (sometimes cold, sometimes hot)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Weather Sensitivity:</label>
                            <select name="Weather_Sensitivity" required>
                                <option value="">Select your weather preference...</option>
                                <option value="Cold">Cold (prefer cold weather)</option>
                                <option value="Hot">Hot (prefer hot weather)</option>
                                <option value="Moderate">Moderate (comfortable in most weather)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Memory:</label>
                            <select name="Memory" required>
                                <option value="">Select your memory pattern...</option>
                                <option value="Poor">Poor (forgetful)</option>
                                <option value="Good">Good (remember most things)</option>
                                <option value="Variable">Variable (sometimes good, sometimes poor)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Motion Tendencies:</label>
                            <select name="Motion_Tendencies" required>
                                <option value="">Select your movement style...</option>
                                <option value="Quick">Quick (fast, restless movements)</option>
                                <option value="Slow">Slow (deliberate, steady movements)</option>
                                <option value="Moderate">Moderate (balanced movements)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Mindset/Emotion:</label>
                            <select name="Mindset_Emotion" required>
                                <option value="">Select your emotional tendency...</option>
                                <option value="Anxious">Anxious (worry often)</option>
                                <option value="Calm">Calm (generally peaceful)</option>
                                <option value="Irritable">Irritable (get angry easily)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Elimination/Stool:</label>
                            <select name="Elimination_Stool" required>
                                <option value="">Select your bowel pattern...</option>
                                <option value="Irregular">Irregular (constipation tendency)</option>
                                <option value="Regular">Regular (normal bowel movements)</option>
                                <option value="Loose">Loose (tendency for diarrhea)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Sleep Requirement:</label>
                            <select name="Sleep_Requirement" required>
                                <option value="">Select your sleep needs...</option>
                                <option value="Less">Less (need less than 6 hours)</option>
                                <option value="Average">Average (6-8 hours)</option>
                                <option value="More">More (need more than 8 hours)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Hunger Onset:</label>
                            <select name="Hunger_Onset" required>
                                <option value="">Select your hunger pattern...</option>
                                <option value="Irregular">Irregular (unpredictable hunger)</option>
                                <option value="Regular">Regular (predictable meal times)</option>
                                <option value="Strong">Strong (get very hungry)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Speech Pace:</label>
                            <select name="Speech_Pace" required>
                                <option value="">Select your speaking speed...</option>
                                <option value="Fast">Fast (speak rapidly)</option>
                                <option value="Slow">Slow (speak slowly)</option>
                                <option value="Moderate">Moderate (normal speed)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Weight Tendency:</label>
                            <select name="Weight_Tendency" required>
                                <option value="">Select your weight pattern...</option>
                                <option value="Hard to Gain">Hard to Gain (stay thin easily)</option>
                                <option value="Easy to Gain">Easy to Gain (gain weight easily)</option>
                                <option value="Stable">Stable (weight stays constant)</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <!-- Step 2: Clinical Cognitive Assessment -->
                <div class="wizard-step" id="step-2">
                    <div class="step-header">
                        <h2>🧠 Clinical Cognitive Assessment</h2>
                        <p class="step-description">
                            Comprehensive cognitive health evaluation using evidence-based screening methods. 
                            This assessment helps identify potential cognitive risks and provides personalized recommendations.
                        </p>
                    </div>
                    
                    <div class="section">
                        <h3>Memory & Cognitive Function <span class="medical-badge">Clinical Screening</span></h3>
                        <p class="info-tooltip">Please answer honestly about your current cognitive experiences</p>
                        
                        <div class="form-group">
                            <label>Age:</label>
                            <input type="number" name="age" min="18" max="100" required placeholder="Enter your age">
                        </div>

                        <div class="form-group">
                            <label>Gender:</label>
                            <select name="gender" required>
                                <option value="">Select gender...</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Memory Issues:</label>
                            <select name="memory_issues" required>
                                <option value="">Select your experience...</option>
                                <option value="No">No memory issues</option>
                                <option value="Mild">Mild forgetfulness (occasional)</option>
                                <option value="Moderate">Moderate memory problems</option>
                                <option value="Severe">Significant memory difficulties</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Confusion Episodes:</label>
                            <select name="confusion" required>
                                <option value="">Select frequency...</option>
                                <option value="No">Never confused</option>
                                <option value="Rarely">Rarely confused</option>
                                <option value="Sometimes">Sometimes confused</option>
                                <option value="Yes">Frequently confused</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Language Difficulties:</label>
                            <select name="language_difficulty" required>
                                <option value="">Select your experience...</option>
                                <option value="No">No language problems</option>
                                <option value="Mild">Mild difficulty finding words</option>
                                <option value="Yes">Notable language problems</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Decision Making Ability:</label>
                            <select name="decision_making" required>
                                <option value="">Select your ability...</option>
                                <option value="Good">Good decision making</option>
                                <option value="Indecisive">Sometimes indecisive</option>
                                <option value="Poor">Poor decision making</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Social Withdrawal:</label>
                            <select name="social_withdrawal" required>
                                <option value="">Select frequency...</option>
                                <option value="No">Socially active</option>
                                <option value="Sometimes">Sometimes avoid social situations</option>
                                <option value="Yes">Frequently avoid social activities</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Diet Type:</label>
                            <select name="diet_type" required>
                                <option value="">Select your diet preference...</option>
                                <option value="Vegetarian">Vegetarian</option>
                                <option value="Non-Vegetarian">Non-Vegetarian</option>
                                <option value="Vegan">Vegan</option>
                                <option value="Mixed">Mixed Diet</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Sleep Quality:</label>
                            <select name="sleep_quality" required>
                                <option value="">Select your sleep quality...</option>
                                <option value="Poor">Poor (restless, interrupted)</option>
                                <option value="Average">Average (decent sleep)</option>
                                <option value="Good">Good (deep, restful sleep)</option>
                                <option value="Excellent">Excellent (perfect sleep)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Stress Level:</label>
                            <select name="stress_level" required>
                                <option value="">Select your stress level...</option>
                                <option value="Low">Low (minimal stress)</option>
                                <option value="Moderate">Moderate (manageable stress)</option>
                                <option value="High">High (significant stress)</option>
                                <option value="Very High">Very High (overwhelming stress)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Physical Activity:</label>
                            <select name="physical_activity" required>
                                <option value="">Select your activity level...</option>
                                <option value="Sedentary">Sedentary (little or no exercise)</option>
                                <option value="Light">Light (light exercise 1-3 days/week)</option>
                                <option value="Moderate">Moderate (moderate exercise 3-5 days/week)</option>
                                <option value="Active">Active (intense exercise 6-7 days/week)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Memory Loss:</label>
                            <select name="memory_loss" required>
                                <option value="">Select frequency...</option>
                                <option value="No">No memory loss</option>
                                <option value="Mild">Mild (occasional forgetfulness)</option>
                                <option value="Moderate">Moderate (noticeable memory issues)</option>
                                <option value="Severe">Severe (significant memory loss)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Repetitive Behavior:</label>
                            <select name="repetition_behavior" required>
                                <option value="">Select frequency...</option>
                                <option value="No">No repetitive behaviors</option>
                                <option value="Sometimes">Sometimes repeat actions/words</option>
                                <option value="Yes">Frequently repeat behaviors</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Mood Swings:</label>
                            <select name="mood_swings" required>
                                <option value="">Select frequency...</option>
                                <option value="No">Stable mood</option>
                                <option value="Mild">Mild mood changes</option>
                                <option value="Moderate">Moderate mood swings</option>
                                <option value="Severe">Severe mood swings</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Chronic Conditions:</label>
                            <select name="chronic_conditions" required>
                                <option value="">Select if you have any...</option>
                                <option value="None">No chronic conditions</option>
                                <option value="Diabetes">Diabetes</option>
                                <option value="Hypertension">High Blood Pressure</option>
                                <option value="Heart Disease">Heart Disease</option>
                                <option value="Multiple">Multiple conditions</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Systolic Blood Pressure:</label>
                            <input type="number" name="systolic_bp" min="80" max="200" required placeholder="Enter systolic BP (e.g., 120)">
                        </div>

                        <div class="form-group">
                            <label>Blood Sugar Level (mg/dL):</label>
                            <input type="number" name="blood_sugar" min="70" max="400" required placeholder="Enter blood sugar (e.g., 100)">
                        </div>

                        <div class="form-group">
                            <label>BMI (Body Mass Index):</label>
                            <input type="number" name="bmi" min="15" max="50" step="0.1" required placeholder="Enter BMI (e.g., 24.5)">
                        </div>

                        <div class="form-group">
                            <label>Family History of Alzheimer's:</label>
                            <select name="family_history" required>
                                <option value="">Select family history...</option>
                                <option value="No">No family history</option>
                                <option value="Yes">Yes, family member(s) had Alzheimer's</option>
                                <option value="Unknown">Unknown/Unsure</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <!-- Navigation -->
                <div class="wizard-navigation">
                    <button type="button" class="nav-btn secondary" id="prevBtn" onclick="changeStep(-1)" style="display:none;">
                        ← Previous Step
                    </button>
                    
                    <div style="flex-grow: 1;"></div>
                    
                    <button type="button" class="nav-btn primary" id="nextBtn" onclick="changeStep(1)">
                        Next Step →
                    </button>
                    
                    <button type="submit" class="nav-btn primary" id="submitBtn" style="display:none;">
                        🏥 Generate Medical Report
                    </button>
                </div>
                
            </form>
            
        </div>
        
        <script>
            let currentStep = 1;
            const totalSteps = 2;
            
            function changeStep(direction) {
                if (direction === 1 && currentStep < totalSteps) {
                    // Validate current step
                    if (validateStep(currentStep)) {
                        currentStep++;
                        updateWizard();
                    }
                } else if (direction === -1 && currentStep > 1) {
                    currentStep--;
                    updateWizard();
                }
            }
            
            function validateStep(step) {
                const currentStepEl = document.getElementById(`step-${step}`);
                const requiredFields = currentStepEl.querySelectorAll('[required]');
                
                for (let field of requiredFields) {
                    if (!field.value) {
                        field.focus();
                        field.style.borderColor = '#ef4444';
                        setTimeout(() => {
                            field.style.borderColor = '#e2e8f0';
                        }, 3000);
                        return false;
                    }
                }
                return true;
            }
            
            function updateWizard() {
                // Hide all steps
                document.querySelectorAll('.wizard-step').forEach(step => {
                    step.classList.remove('active');
                });
                
                // Show current step
                document.getElementById(`step-${currentStep}`).classList.add('active');
                
                // Update progress
                document.querySelectorAll('.step').forEach((step, index) => {
                    step.classList.remove('active', 'completed');
                    if (index + 1 < currentStep) {
                        step.classList.add('completed');
                    } else if (index + 1 === currentStep) {
                        step.classList.add('active');
                    }
                });
                
                // Update navigation buttons
                document.getElementById('prevBtn').style.display = currentStep > 1 ? 'block' : 'none';
                document.getElementById('nextBtn').style.display = currentStep < totalSteps ? 'block' : 'none';
                document.getElementById('submitBtn').style.display = currentStep === totalSteps ? 'block' : 'none';
            }
            
            // Add missing hidden fields for compatibility
            document.getElementById('wizard-form').addEventListener('submit', function() {
                // Add missing Ayurvedic fields with default values
                const hiddenFields = [
                    'Speech_Voice', 'Energy_Levels', 'Body_Temperature', 'Weather_Sensitivity',
                    'Memory', 'Motion_Tendencies', 'Mindset_Emotion', 'Elimination_Stool',
                    'Sleep_Requirement', 'Hunger_Onset', 'Speech_Pace', 'Weight_Tendency',
                    'repetition_behavior', 'mood_changes', 'family_history'
                ];
                
                hiddenFields.forEach(field => {
                    if (!this.querySelector(`[name="${field}"]`)) {
                        const input = document.createElement('input');
                        input.type = 'hidden';
                        input.name = field;
                        input.value = field.includes('memory') || field.includes('repetition') ? 'No' : 'Normal';
                        this.appendChild(input);
                    }
                });
                
                // Show loading
                document.querySelector('.wizard-navigation').innerHTML = 
                    '<div style="text-align: center; width: 100%;"><div style="display: inline-block; animation: spin 1s linear infinite; font-size: 3rem;">⚕️</div><p style="margin-top: 15px; color: #3b82f6; font-weight: 700; font-size: 1.2rem;">Processing your comprehensive medical assessment...</p></div>';
            });
        </script>
        
        <style>
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        </style>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)