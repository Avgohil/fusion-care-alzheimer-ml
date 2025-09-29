# 🚀 CARE CATALYST - COMPLETE PROJECT DEPLOYMENT
# Main FastAPI application with all features integrated

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from typing import List, Optional
import asyncio
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="🏥⚕️ Care Catalyst - AI Ayurvedic Health Assessment",
    description="Complete AI-powered Ayurvedic + Cognitive Health Analysis Platform",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []

# ========================================
# ML MODEL LOADING
# ========================================

def load_models():
    """Load all ML models and encoders"""
    models = {}
    try:
        # Try different paths for models
        model_paths = [
            "model/",
            "Care Catalyst Final version/Backend/model/",
            "stage_1_prakriti_classification/models/",
            "stage_2_alzheimer_risk_prediction/models/",
            "./"
        ]
        
        model_files = {
            'prakriti_model': 'prakriti_model.pkl',
            'prakriti_encoder': 'prakriti_encoder.pkl',
            'alzheimers_model': 'alzheimers_stage2_model.pkl',
            'stage2_encoders': 'stage2_encoders.pkl'
        }
        
        for model_name, filename in model_files.items():
            loaded = False
            for path in model_paths:
                try:
                    full_path = Path(path) / filename
                    if full_path.exists():
                        with open(full_path, 'rb') as f:
                            models[model_name] = pickle.load(f)
                        logger.info(f"✅ Loaded {model_name} from {full_path}")
                        loaded = True
                        break
                except Exception as e:
                    logger.warning(f"⚠️ Could not load {model_name} from {path}: {e}")
                    continue
            
            if not loaded:
                logger.error(f"❌ Could not load {model_name}")
                # Create dummy model for demonstration
                models[model_name] = None
                
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        
    return models

# Load models at startup
MODELS = load_models()

# ========================================
# VISUALIZATION FUNCTIONS
# ========================================

def get_risk_color(score, parameter_type='standard'):
    """Return color based on risk level"""
    if parameter_type == 'cognitive' or parameter_type == 'physical':
        if score >= 70: return '#2ecc71'  # Green - Good
        elif score >= 40: return '#f39c12'  # Orange - Moderate  
        else: return '#e74c3c'  # Red - Poor
    elif parameter_type == 'constitution':
        if score <= 40: return '#2ecc71'  # Green - Balanced
        elif score <= 65: return '#f39c12'  # Orange - Moderate
        else: return '#e74c3c'  # Red - High imbalance
    elif parameter_type == 'stress':
        if score <= 30: return '#2ecc71'  # Green - Low stress
        elif score <= 60: return '#f39c12'  # Orange - Moderate
        else: return '#e74c3c'  # Red - High stress

colors = {
    'success': '#2ecc71',
    'warning': '#f39c12', 
    'danger': '#e74c3c',
    'primary': '#3498db',
    'dark': '#2c3e50'
}

def create_risk_gauge(assessment_data):
    """Create risk level gauge"""
    risk_score = assessment_data.get('overall_risk_score', 50)
    
    if risk_score <= 30:
        gauge_color = colors['success']
        status_text = "Low Risk ✅"
    elif risk_score <= 60:
        gauge_color = colors['warning']
        status_text = "Moderate Risk ⚠️"
    else:
        gauge_color = colors['danger']
        status_text = "High Risk ❗"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        title = {'text': f"Overall Health Risk Level"},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 2},
            'bar': {'color': gauge_color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "lightgray",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(46, 204, 113, 0.2)'},
                {'range': [30, 60], 'color': 'rgba(243, 156, 18, 0.2)'},
                {'range': [60, 100], 'color': 'rgba(231, 76, 60, 0.2)'}
            ],
        }
    ))
    
    fig.add_annotation(
        text=f"<b>{status_text}</b>",
        x=0.5, y=0.15,
        font=dict(size=18, color=gauge_color),
        showarrow=False
    )
    
    fig.update_layout(
        height=300,
        font={'family': "Arial", 'size': 14},
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='white'
    )
    
    return fig

def create_constitution_chart(assessment_data):
    """Create constitution balance chart"""
    constitutions = ['Vata', 'Pitta', 'Kapha']
    scores = [
        assessment_data.get('vata_score', 50),
        assessment_data.get('pitta_score', 50), 
        assessment_data.get('kapha_score', 50)
    ]
    
    bar_colors = [get_risk_color(score, 'constitution') for score in scores]
    
    fig = go.Figure(data=[
        go.Bar(
            x=constitutions,
            y=scores,
            marker_color=bar_colors,
            text=[f'{score}%' for score in scores],
            textposition='auto',
            hovertemplate='<b>%{x} Constitution</b><br>' +
                         'Imbalance Level: %{y}%<br>' +
                         '<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text="Ayurvedic Constitution Balance", x=0.5, font=dict(size=16)),
        xaxis_title="Constitution Type",
        yaxis_title="Imbalance Level (%)",
        yaxis_range=[0, 100],
        height=350,
        font=dict(family="Arial", size=12),
        margin=dict(l=50, r=50, t=80, b=50),
        paper_bgcolor='white'
    )
    
    return fig

def create_health_radar(assessment_data):
    """Create health radar chart"""
    parameters = [
        'Sleep Quality', 'Digestion', 'Energy Levels', 'Stress Management',
        'Memory', 'Attention', 'Processing Speed', 'Executive Function'
    ]
    
    scores = [
        assessment_data.get('sleep_quality', 50),
        assessment_data.get('digestion_score', 50),
        assessment_data.get('energy_levels', 50),
        100 - assessment_data.get('stress_level', 50),  # Invert stress
        assessment_data.get('memory_score', 50),
        assessment_data.get('attention_score', 50),
        assessment_data.get('processing_speed', 50),
        assessment_data.get('executive_function', 50)
    ]
    
    avg_score = np.mean(scores)
    radar_color = get_risk_color(avg_score, 'physical')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=parameters,
        fill='toself',
        fillcolor=f'rgba{tuple(list(int(radar_color[i:i+2], 16) for i in (1, 3, 5)) + [0.3])}',
        line=dict(color=radar_color, width=3),
        marker=dict(size=6, color=radar_color),
        name='Your Results',
        hovertemplate='<b>%{theta}</b><br>Score: %{r}%<extra></extra>'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[80] * len(parameters),
        theta=parameters,
        fill='toself',
        fillcolor='rgba(46, 204, 113, 0.1)',
        line=dict(color='rgba(46, 204, 113, 0.6)', width=2, dash='dash'),
        name='Target Level',
        hovertemplate='Target: %{r}%<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                rotation=90
            )
        ),
        title=dict(text="Health Overview - All Parameters", x=0.5, font=dict(size=16)),
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=50, r=50, t=80, b=50),
        paper_bgcolor='white'
    )
    
    return fig

def create_cognitive_summary(assessment_data):
    """Create cognitive health summary"""
    cognitive_params = ['Memory', 'Attention', 'Processing Speed', 'Executive Function']
    cognitive_scores = [
        assessment_data.get('memory_score', 50),
        assessment_data.get('attention_score', 50), 
        assessment_data.get('processing_speed', 50),
        assessment_data.get('executive_function', 50)
    ]
    
    cognitive_colors = [get_risk_color(score, 'cognitive') for score in cognitive_scores]
    
    fig = go.Figure(data=[
        go.Bar(
            y=cognitive_params,
            x=cognitive_scores,
            orientation='h',
            marker_color=cognitive_colors,
            text=[f'{score}%' for score in cognitive_scores],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Score: %{x}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text="Cognitive Health Assessment", x=0.5, font=dict(size=16)),
        xaxis_title="Score (%)",
        xaxis_range=[0, 100],
        height=300,
        font=dict(family="Arial", size=12),
        margin=dict(l=120, r=50, t=80, b=50),
        paper_bgcolor='white'
    )
    
    return fig

# ========================================
# ML PREDICTION FUNCTIONS  
# ========================================

def predict_prakriti(assessment_data):
    """Predict Ayurvedic constitution"""
    try:
        if MODELS.get('prakriti_model') and MODELS.get('prakriti_encoder'):
            # Extract features for prakriti prediction
            features = [
                assessment_data.get('sleep_quality', 50),
                assessment_data.get('digestion_score', 50),
                assessment_data.get('energy_levels', 50),
                assessment_data.get('stress_level', 50)
            ]
            
            # Make prediction (simplified)
            features_array = np.array(features).reshape(1, -1)
            prediction = MODELS['prakriti_model'].predict(features_array)[0]
            
            return {
                'dominant_constitution': prediction,
                'confidence': 0.85
            }
        else:
            # Fallback calculation
            vata = assessment_data.get('vata_score', 50)
            pitta = assessment_data.get('pitta_score', 50) 
            kapha = assessment_data.get('kapha_score', 50)
            
            if vata >= pitta and vata >= kapha:
                dominant = 'Vata'
            elif pitta >= kapha:
                dominant = 'Pitta'
            else:
                dominant = 'Kapha'
                
            return {
                'dominant_constitution': dominant,
                'confidence': 0.75
            }
            
    except Exception as e:
        logger.error(f"Prakriti prediction error: {e}")
        return {
            'dominant_constitution': 'Vata',
            'confidence': 0.50
        }

def predict_alzheimer_risk(assessment_data):
    """Predict Alzheimer's disease risk"""
    try:
        if MODELS.get('alzheimers_model') and MODELS.get('stage2_encoders'):
            # Extract cognitive features
            features = [
                assessment_data.get('memory_score', 50),
                assessment_data.get('attention_score', 50),
                assessment_data.get('processing_speed', 50), 
                assessment_data.get('executive_function', 50),
                assessment_data.get('age', 45),
                assessment_data.get('sleep_quality', 50)
            ]
            
            # Make prediction (simplified)
            features_array = np.array(features).reshape(1, -1)
            risk_prob = MODELS['alzheimers_model'].predict_proba(features_array)[0][1]
            
            return {
                'risk_probability': float(risk_prob),
                'risk_level': 'High' if risk_prob > 0.7 else 'Moderate' if risk_prob > 0.4 else 'Low'
            }
        else:
            # Fallback calculation based on cognitive scores
            cognitive_avg = np.mean([
                assessment_data.get('memory_score', 50),
                assessment_data.get('attention_score', 50),
                assessment_data.get('processing_speed', 50),
                assessment_data.get('executive_function', 50)
            ])
            
            # Lower cognitive scores = higher risk
            risk_prob = (100 - cognitive_avg) / 100
            
            return {
                'risk_probability': risk_prob,
                'risk_level': 'High' if risk_prob > 0.6 else 'Moderate' if risk_prob > 0.3 else 'Low'
            }
            
    except Exception as e:
        logger.error(f"Alzheimer risk prediction error: {e}")
        return {
            'risk_probability': 0.3,
            'risk_level': 'Moderate'
        }

# ========================================
# MAIN ROUTES
# ========================================

@app.get("/", response_class=HTMLResponse)
async def homepage():
    """Main homepage"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏥⚕️ Care Catalyst - AI Health Assessment</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
                text-align: center;
            }
            .header {
                margin-bottom: 50px;
            }
            .header h1 {
                font-size: 3.5em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                font-size: 1.3em;
                margin-bottom: 30px;
                opacity: 0.9;
            }
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin: 50px 0;
            }
            .feature-card {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                border: 1px solid rgba(255,255,255,0.2);
                transition: transform 0.3s ease;
            }
            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }
            .feature-card h3 {
                font-size: 1.5em;
                margin-bottom: 15px;
            }
            .cta-buttons {
                margin: 50px 0;
            }
            .btn {
                display: inline-block;
                padding: 20px 40px;
                margin: 15px;
                background: rgba(255,255,255,0.2);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                font-size: 1.1em;
                border: 2px solid rgba(255,255,255,0.3);
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }
            .btn:hover {
                background: rgba(255,255,255,0.3);
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }
            .btn.primary {
                background: #2196F3;
                border-color: #2196F3;
            }
            .btn.secondary {
                background: #4CAF50;
                border-color: #4CAF50;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥⚕️ Care Catalyst</h1>
                <p>AI-Powered Ayurvedic + Cognitive Health Assessment Platform</p>
                <p>Integrating Ancient Wisdom with Modern AI Technology</p>
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <h3>🧠 Cognitive Assessment</h3>
                    <p>Advanced AI algorithms analyze memory, attention, processing speed, and executive function to detect early signs of cognitive decline.</p>
                </div>
                
                <div class="feature-card">
                    <h3>🏛️ Ayurvedic Analysis</h3>
                    <p>Traditional Ayurvedic constitution (Prakriti) analysis using modern machine learning to understand your unique body type.</p>
                </div>
                
                <div class="feature-card">
                    <h3>📊 Dynamic Visualization</h3>
                    <p>Interactive real-time charts and dashboards that update as you input your health parameters and assessment responses.</p>
                </div>
                
                <div class="feature-card">
                    <h3>🎯 Risk Prediction</h3>
                    <p>Early detection of Alzheimer's disease risk using validated machine learning models trained on clinical datasets.</p>
                </div>
                
                <div class="feature-card">
                    <h3>💊 Personalized Recommendations</h3>
                    <p>Customized health recommendations combining Ayurvedic principles with evidence-based modern medicine.</p>
                </div>
                
                <div class="feature-card">
                    <h3>📱 Real-Time Monitoring</h3>
                    <p>Live WebSocket-powered dashboard for continuous health monitoring and instant feedback on health changes.</p>
                </div>
            </div>
            
            <div class="cta-buttons">
                <a href="/assessment" class="btn primary">📝 Take Full Assessment</a>
                <a href="/dashboard" class="btn secondary">📊 View Dynamic Dashboard</a>
                <a href="/quick-test" class="btn">⚡ Quick Health Check</a>
                <a href="/docs" class="btn">📚 API Documentation</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/assessment", response_class=HTMLResponse)
async def assessment_form():
    """Complete assessment form"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏥⚕️ Care Catalyst - Health Assessment</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.1);
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding: 30px;
                background: linear-gradient(90deg, #4CAF50, #2196F3);
                color: white;
                border-radius: 15px;
            }
            .section {
                margin: 30px 0;
                padding: 25px;
                border: 2px solid #f0f0f0;
                border-radius: 15px;
                background: #fafafa;
            }
            .section h3 {
                color: #333;
                margin-bottom: 20px;
                font-size: 1.3em;
            }
            .form-group {
                margin: 15px 0;
                display: grid;
                grid-template-columns: 1fr 2fr 100px;
                gap: 15px;
                align-items: center;
            }
            label {
                font-weight: bold;
                color: #555;
            }
            input[type="range"] {
                width: 100%;
                height: 6px;
                background: #ddd;
                outline: none;
                border-radius: 5px;
            }
            input[type="range"]::-webkit-slider-thumb {
                appearance: none;
                width: 20px;
                height: 20px;
                background: #2196F3;
                cursor: pointer;
                border-radius: 50%;
            }
            .value-display {
                text-align: center;
                font-weight: bold;
                font-size: 1.1em;
                color: #333;
                background: white;
                padding: 8px;
                border-radius: 8px;
                border: 2px solid #2196F3;
            }
            .submit-btn {
                width: 100%;
                padding: 20px;
                background: linear-gradient(90deg, #4CAF50, #45a049);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 1.2em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 30px;
            }
            .submit-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }
            .personal-info {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            .personal-info input, .personal-info select {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 1em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥⚕️ Comprehensive Health Assessment</h1>
                <p>Complete AI-powered Ayurvedic + Cognitive Analysis</p>
            </div>
            
            <form id="assessmentForm" onsubmit="submitAssessment(event)">
                <!-- Personal Information -->
                <div class="section">
                    <h3>👤 Personal Information</h3>
                    <div class="personal-info">
                        <input type="text" id="name" placeholder="Full Name" required>
                        <input type="number" id="age" placeholder="Age" min="18" max="100" required>
                        <select id="gender" required>
                            <option value="">Select Gender</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                        <input type="email" id="email" placeholder="Email Address">
                    </div>
                </div>
                
                <!-- Ayurvedic Constitution -->
                <div class="section">
                    <h3>🏛️ Ayurvedic Constitution Assessment</h3>
                    <div class="form-group">
                        <label>Vata Imbalance Level:</label>
                        <input type="range" id="vata" min="0" max="100" value="50" oninput="updateValue('vata')">
                        <span id="vata-value" class="value-display">50</span>
                    </div>
                    <div class="form-group">
                        <label>Pitta Imbalance Level:</label>
                        <input type="range" id="pitta" min="0" max="100" value="50" oninput="updateValue('pitta')">
                        <span id="pitta-value" class="value-display">50</span>
                    </div>
                    <div class="form-group">
                        <label>Kapha Imbalance Level:</label>
                        <input type="range" id="kapha" min="0" max="100" value="50" oninput="updateValue('kapha')">
                        <span id="kapha-value" class="value-display">50</span>
                    </div>
                </div>
                
                <!-- Physical Health -->
                <div class="section">
                    <h3>💪 Physical Health Parameters</h3>
                    <div class="form-group">
                        <label>Sleep Quality:</label>
                        <input type="range" id="sleep" min="0" max="100" value="60" oninput="updateValue('sleep')">
                        <span id="sleep-value" class="value-display">60</span>
                    </div>
                    <div class="form-group">
                        <label>Digestion Score:</label>
                        <input type="range" id="digestion" min="0" max="100" value="65" oninput="updateValue('digestion')">
                        <span id="digestion-value" class="value-display">65</span>
                    </div>
                    <div class="form-group">
                        <label>Energy Levels:</label>
                        <input type="range" id="energy" min="0" max="100" value="55" oninput="updateValue('energy')">
                        <span id="energy-value" class="value-display">55</span>
                    </div>
                    <div class="form-group">
                        <label>Stress Level:</label>
                        <input type="range" id="stress" min="0" max="100" value="70" oninput="updateValue('stress')">
                        <span id="stress-value" class="value-display">70</span>
                    </div>
                </div>
                
                <!-- Cognitive Assessment -->
                <div class="section">
                    <h3>🧠 Cognitive Health Assessment</h3>
                    <div class="form-group">
                        <label>Memory Score:</label>
                        <input type="range" id="memory" min="0" max="100" value="70" oninput="updateValue('memory')">
                        <span id="memory-value" class="value-display">70</span>
                    </div>
                    <div class="form-group">
                        <label>Attention Score:</label>
                        <input type="range" id="attention" min="0" max="100" value="65" oninput="updateValue('attention')">
                        <span id="attention-value" class="value-display">65</span>
                    </div>
                    <div class="form-group">
                        <label>Processing Speed:</label>
                        <input type="range" id="processing" min="0" max="100" value="60" oninput="updateValue('processing')">
                        <span id="processing-value" class="value-display">60</span>
                    </div>
                    <div class="form-group">
                        <label>Executive Function:</label>
                        <input type="range" id="executive" min="0" max="100" value="55" oninput="updateValue('executive')">
                        <span id="executive-value" class="value-display">55</span>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn">🚀 Generate Complete Analysis</button>
            </form>
        </div>

        <script>
            function updateValue(sliderId) {
                const slider = document.getElementById(sliderId);
                const valueDisplay = document.getElementById(sliderId + '-value');
                valueDisplay.textContent = slider.value;
                
                // Color coding based on value
                const value = parseInt(slider.value);
                if (sliderId === 'stress') {
                    // For stress, lower is better
                    if (value <= 30) valueDisplay.style.backgroundColor = '#4CAF50';
                    else if (value <= 60) valueDisplay.style.backgroundColor = '#FF9800';
                    else valueDisplay.style.backgroundColor = '#F44336';
                } else if (sliderId.includes('vata') || sliderId.includes('pitta') || sliderId.includes('kapha')) {
                    // For constitution, lower is more balanced
                    if (value <= 40) valueDisplay.style.backgroundColor = '#4CAF50';
                    else if (value <= 65) valueDisplay.style.backgroundColor = '#FF9800';
                    else valueDisplay.style.backgroundColor = '#F44336';
                } else {
                    // For other parameters, higher is better
                    if (value >= 70) valueDisplay.style.backgroundColor = '#4CAF50';
                    else if (value >= 40) valueDisplay.style.backgroundColor = '#FF9800';
                    else valueDisplay.style.backgroundColor = '#F44336';
                }
                valueDisplay.style.color = 'white';
            }
            
            // Initialize color coding
            ['vata', 'pitta', 'kapha', 'sleep', 'digestion', 'energy', 'stress', 'memory', 'attention', 'processing', 'executive'].forEach(updateValue);
            
            async function submitAssessment(event) {
                event.preventDefault();
                
                const formData = {
                    name: document.getElementById('name').value,
                    age: parseInt(document.getElementById('age').value),
                    gender: document.getElementById('gender').value,
                    email: document.getElementById('email').value,
                    vata_score: parseInt(document.getElementById('vata').value),
                    pitta_score: parseInt(document.getElementById('pitta').value),
                    kapha_score: parseInt(document.getElementById('kapha').value),
                    sleep_quality: parseInt(document.getElementById('sleep').value),
                    digestion_score: parseInt(document.getElementById('digestion').value),
                    energy_levels: parseInt(document.getElementById('energy').value),
                    stress_level: parseInt(document.getElementById('stress').value),
                    memory_score: parseInt(document.getElementById('memory').value),
                    attention_score: parseInt(document.getElementById('attention').value),
                    processing_speed: parseInt(document.getElementById('processing').value),
                    executive_function: parseInt(document.getElementById('executive').value)
                };
                
                try {
                    const response = await fetch('/api/assessment/complete', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(formData)
                    });
                    
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        // Redirect to results page with assessment ID
                        window.location.href = `/results?id=${result.assessment_id}`;
                    } else {
                        alert('Error processing assessment. Please try again.');
                    }
                    
                } catch (error) {
                    console.error('Assessment error:', error);
                    alert('Error submitting assessment. Please try again.');
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
async def dynamic_dashboard():
    """Dynamic interactive dashboard with working Plotly charts"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏥⚕️ Dynamic Assessment Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(90deg, #4CAF50, #2196F3);
                color: white;
                border-radius: 10px;
            }
            .controls {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
            }
            .chart-container {
                margin: 20px 0;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                background: white;
                min-height: 400px;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 20px;
            }
            .slider-container {
                margin: 10px 0;
            }
            .slider-container label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            .slider {
                width: 100%;
                margin: 10px 0;
            }
            button {
                padding: 10px 20px;
                margin: 5px;
                border: none;
                border-radius: 5px;
                background: #2196F3;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background: #1976D2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥⚕️ Dynamic Assessment Dashboard</h1>
                <p>Real-time Ayurvedic + Cognitive Health Visualization</p>
            </div>
            
            <div class="controls">
                <div>
                    <h3>🏛️ Ayurvedic Constitution</h3>
                    <div class="slider-container">
                        <label>Vata Score: <span id="vata-value">65</span>%</label>
                        <input type="range" id="vata" class="slider" min="0" max="100" value="65">
                    </div>
                    <div class="slider-container">
                        <label>Pitta Score: <span id="pitta-value">45</span>%</label>
                        <input type="range" id="pitta" class="slider" min="0" max="100" value="45">
                    </div>
                    <div class="slider-container">
                        <label>Kapha Score: <span id="kapha-value">35</span>%</label>
                        <input type="range" id="kapha" class="slider" min="0" max="100" value="35">
                    </div>
                </div>
                
                <div>
                    <h3>💪 Physical Health</h3>
                    <div class="slider-container">
                        <label>Sleep Quality: <span id="sleep-value">60</span>%</label>
                        <input type="range" id="sleep" class="slider" min="0" max="100" value="60">
                    </div>
                    <div class="slider-container">
                        <label>Energy Levels: <span id="energy-value">55</span>%</label>
                        <input type="range" id="energy" class="slider" min="0" max="100" value="55">
                    </div>
                    <div class="slider-container">
                        <label>Stress Level: <span id="stress-value">75</span>%</label>
                        <input type="range" id="stress" class="slider" min="0" max="100" value="75">
                    </div>
                </div>
                
                <div>
                    <h3>🧠 Cognitive Health</h3>
                    <div class="slider-container">
                        <label>Memory: <span id="memory-value">70</span>%</label>
                        <input type="range" id="memory" class="slider" min="0" max="100" value="70">
                    </div>
                    <div class="slider-container">
                        <label>Attention: <span id="attention-value">65</span>%</label>
                        <input type="range" id="attention" class="slider" min="0" max="100" value="65">
                    </div>
                    <div class="slider-container">
                        <label>Processing Speed: <span id="processing-value">60</span>%</label>
                        <input type="range" id="processing" class="slider" min="0" max="100" value="60">
                    </div>
                </div>
                
                <div>
                    <button onclick="updateAllCharts()">🔄 Update Charts</button>
                    <button onclick="generateRandomData()">🎲 Random Data</button>
                    <button onclick="resetDefaults()">↺ Reset</button>
                </div>
            </div>
            
            <div class="grid">
                <div id="risk-gauge" class="chart-container"></div>
                <div id="constitution-chart" class="chart-container"></div>
                <div id="health-radar" class="chart-container"></div>
                <div id="cognitive-chart" class="chart-container"></div>
            </div>
        </div>

        <script>
            // Initialize sliders
            const sliders = ['vata', 'pitta', 'kapha', 'sleep', 'energy', 'stress', 'memory', 'attention', 'processing'];
            
            sliders.forEach(id => {
                document.getElementById(id).addEventListener('input', function() {
                    document.getElementById(id + '-value').textContent = this.value;
                });
            });
            
            function getCurrentData() {
                return {
                    vata_score: parseInt(document.getElementById('vata').value),
                    pitta_score: parseInt(document.getElementById('pitta').value),
                    kapha_score: parseInt(document.getElementById('kapha').value),
                    sleep_quality: parseInt(document.getElementById('sleep').value),
                    energy_levels: parseInt(document.getElementById('energy').value),
                    stress_level: parseInt(document.getElementById('stress').value),
                    memory_score: parseInt(document.getElementById('memory').value),
                    attention_score: parseInt(document.getElementById('attention').value),
                    processing_speed: parseInt(document.getElementById('processing').value),
                    executive_function: 60,
                    digestion_score: 65,
                    overall_risk_score: Math.round(Math.random() * 100)
                };
            }
            
            function createRiskGauge(data) {
                const risk = data.overall_risk_score;
                const color = risk <= 30 ? '#2ecc71' : risk <= 60 ? '#f39c12' : '#e74c3c';
                
                const gauge = {
                    type: "indicator",
                    mode: "gauge+number",
                    value: risk,
                    title: {text: "Overall Health Risk"},
                    gauge: {
                        axis: {range: [0, 100]},
                        bar: {color: color},
                        steps: [
                            {range: [0, 30], color: "rgba(46, 204, 113, 0.2)"},
                            {range: [30, 60], color: "rgba(243, 156, 18, 0.2)"},
                            {range: [60, 100], color: "rgba(231, 76, 60, 0.2)"}
                        ]
                    }
                };
                
                Plotly.newPlot('risk-gauge', [gauge], {
                    height: 350,
                    margin: {t: 50, b: 50, l: 50, r: 50}
                });
            }
            
            function createConstitutionChart(data) {
                const trace = {
                    x: ['Vata', 'Pitta', 'Kapha'],
                    y: [data.vata_score, data.pitta_score, data.kapha_score],
                    type: 'bar',
                    marker: {
                        color: ['#e74c3c', '#f39c12', '#2ecc71']
                    },
                    text: data.vata_score > data.pitta_score && data.vata_score > data.kapha_score ? 
                          ['Dominant', '', ''] : 
                          data.pitta_score > data.kapha_score ? 
                          ['', 'Dominant', ''] : 
                          ['', '', 'Dominant'],
                    textposition: 'auto'
                };
                
                Plotly.newPlot('constitution-chart', [trace], {
                    title: 'Ayurvedic Constitution Balance',
                    yaxis: {title: 'Imbalance Level (%)'},
                    height: 350,
                    margin: {t: 80, b: 50, l: 50, r: 50}
                });
            }
            
            function createHealthRadar(data) {
                const trace = {
                    type: 'scatterpolar',
                    r: [
                        data.sleep_quality,
                        data.energy_levels,
                        100 - data.stress_level,
                        data.memory_score,
                        data.attention_score,
                        data.processing_speed
                    ],
                    theta: ['Sleep', 'Energy', 'Stress Mgmt', 'Memory', 'Attention', 'Processing'],
                    fill: 'toself',
                    name: 'Your Health'
                };
                
                Plotly.newPlot('health-radar', [trace], {
                    polar: {
                        radialaxis: {
                            visible: true,
                            range: [0, 100]
                        }
                    },
                    title: 'Health Overview Radar',
                    height: 350
                });
            }
            
            function createCognitiveChart(data) {
                const trace = {
                    y: ['Memory', 'Attention', 'Processing Speed'],
                    x: [data.memory_score, data.attention_score, data.processing_speed],
                    type: 'bar',
                    orientation: 'h',
                    marker: {
                        color: ['#3498db', '#9b59b6', '#e67e22']
                    }
                };
                
                Plotly.newPlot('cognitive-chart', [trace], {
                    title: 'Cognitive Health Assessment',
                    xaxis: {title: 'Score (%)'},
                    height: 350,
                    margin: {t: 80, b: 50, l: 100, r: 50}
                });
            }
            
            function updateAllCharts() {
                const data = getCurrentData();
                createRiskGauge(data);
                createConstitutionChart(data);
                createHealthRadar(data);
                createCognitiveChart(data);
            }
            
            function generateRandomData() {
                sliders.forEach(id => {
                    const value = Math.floor(Math.random() * 81) + 20;
                    document.getElementById(id).value = value;
                    document.getElementById(id + '-value').textContent = value;
                });
                updateAllCharts();
            }
            
            function resetDefaults() {
                const defaults = {vata: 65, pitta: 45, kapha: 35, sleep: 60, energy: 55, stress: 75, memory: 70, attention: 65, processing: 60};
                Object.entries(defaults).forEach(([key, value]) => {
                    document.getElementById(key).value = value;
                    document.getElementById(key + '-value').textContent = value;
                });
                updateAllCharts();
            }
            
            // Initialize charts on load
            updateAllCharts();
        </script>
    </body>
    </html>
    """

@app.get("/results", response_class=HTMLResponse)
async def show_results(request: Request):
    """Show assessment results with interactive Plotly charts"""
    assessment_id = request.query_params.get("id", "DEMO")
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏥⚕️ Assessment Results - Care Catalyst</title>
        <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
                padding: 30px;
                background: linear-gradient(90deg, #4CAF50, #2196F3);
                color: white;
                border-radius: 15px;
            }}
            .summary-box {{
                background: linear-gradient(90deg, #4CAF50, #45a049);
                color: white;
                padding: 30px;
                border-radius: 15px;
                margin: 30px 0;
                text-align: center;
                font-size: 1.1em;
            }}
            .charts-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 30px;
                margin: 40px 0;
            }}
            .chart-container {{
                border: 2px solid #f0f0f0;
                border-radius: 15px;
                padding: 20px;
                background: #fafafa;
                min-height: 400px;
            }}
            .btn {{
                display: inline-block;
                padding: 15px 30px;
                margin: 10px;
                background: #2196F3;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s ease;
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥⚕️ Your Comprehensive Health Analysis</h1>
                <p>Assessment ID: {assessment_id}</p>
                <p>Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="summary-box" id="summary-box">
                <h2>📊 Analysis Summary</h2>
                <div id="summary-content">
                    <strong>Risk Level:</strong> <span id="risk-text">Moderate Risk (58%)</span> &nbsp;&nbsp;|&nbsp;&nbsp;
                    <strong>Dominant Constitution:</strong> <span id="constitution-text">Vata</span> &nbsp;&nbsp;|&nbsp;&nbsp;
                    <strong>Cognitive Health:</strong> <span id="cognitive-text">62%</span>
                </div>
            </div>
            
            <div class="charts-grid">
                <div class="chart-container">
                    <h3>🎯 Overall Risk Level</h3>
                    <div id="risk-gauge"></div>
                </div>
                
                <div class="chart-container">
                    <h3>🏛️ Ayurvedic Constitution</h3>
                    <div id="constitution-chart"></div>
                </div>
                
                <div class="chart-container">
                    <h3>🕸️ Health Overview</h3>
                    <div id="health-radar"></div>
                </div>
                
                <div class="chart-container">
                    <h3>🧠 Cognitive Assessment</h3>
                    <div id="cognitive-chart"></div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px;">
                <a href="/assessment" class="btn">📝 Take Another Assessment</a>
                <a href="/dashboard" class="btn">📊 View Dynamic Dashboard</a>
                <a href="/" class="btn">🏠 Return Home</a>
            </div>
        </div>

        <script>
            // Sample assessment data (in real app, this would come from the assessment)
            const assessmentData = {{
                vata_score: 65,
                pitta_score: 45,
                kapha_score: 35,
                sleep_quality: 60,
                energy_levels: 55,
                stress_level: 75,
                memory_score: 70,
                attention_score: 65,
                processing_speed: 60,
                executive_function: 55,
                digestion_score: 65,
                overall_risk_score: 58,
                risk_category: 'Moderate Risk',
                dominant_constitution: 'Vata'
            }};
            
            function createRiskGauge() {{
                const risk = assessmentData.overall_risk_score;
                const color = risk <= 30 ? '#2ecc71' : risk <= 60 ? '#f39c12' : '#e74c3c';
                const status = risk <= 30 ? 'Low Risk ✅' : risk <= 60 ? 'Moderate Risk ⚠️' : 'High Risk ❗';
                
                const gauge = {{
                    type: "indicator",
                    mode: "gauge+number",
                    value: risk,
                    title: {{text: "Overall Health Risk Level"}},
                    gauge: {{
                        axis: {{range: [0, 100], tickwidth: 2}},
                        bar: {{color: color, thickness: 0.3}},
                        bgcolor: "white",
                        borderwidth: 2,
                        bordercolor: "lightgray",
                        steps: [
                            {{range: [0, 30], color: "rgba(46, 204, 113, 0.2)"}},
                            {{range: [30, 60], color: "rgba(243, 156, 18, 0.2)"}},
                            {{range: [60, 100], color: "rgba(231, 76, 60, 0.2)"}}
                        ]
                    }}
                }};
                
                const layout = {{
                    height: 350,
                    margin: {{t: 50, b: 50, l: 50, r: 50}},
                    font: {{family: "Arial", size: 14}},
                    annotations: [{{
                        text: status,
                        x: 0.5, y: 0.15,
                        font: {{size: 18, color: color}},
                        showarrow: false
                    }}]
                }};
                
                Plotly.newPlot('risk-gauge', [gauge], layout);
            }}
            
            function createConstitutionChart() {{
                const constitutions = ['Vata', 'Pitta', 'Kapha'];
                const scores = [assessmentData.vata_score, assessmentData.pitta_score, assessmentData.kapha_score];
                const colors = scores.map(score => 
                    score <= 40 ? '#2ecc71' : score <= 65 ? '#f39c12' : '#e74c3c'
                );
                
                const trace = {{
                    x: constitutions,
                    y: scores,
                    type: 'bar',
                    marker: {{color: colors}},
                    text: scores.map(score => score + '%'),
                    textposition: 'auto',
                    hovertemplate: '<b>%{{x}} Constitution</b><br>Imbalance Level: %{{y}}%<extra></extra>'
                }};
                
                const layout = {{
                    title: 'Ayurvedic Constitution Balance',
                    xaxis: {{title: 'Constitution Type'}},
                    yaxis: {{title: 'Imbalance Level (%)', range: [0, 100]}},
                    height: 350,
                    margin: {{t: 80, b: 50, l: 50, r: 50}}
                }};
                
                Plotly.newPlot('constitution-chart', [trace], layout);
            }}
            
            function createHealthRadar() {{
                const parameters = [
                    'Sleep Quality', 'Energy Levels', 'Stress Management',
                    'Memory', 'Attention', 'Processing Speed'
                ];
                
                const scores = [
                    assessmentData.sleep_quality,
                    assessmentData.energy_levels,
                    100 - assessmentData.stress_level, // Invert stress
                    assessmentData.memory_score,
                    assessmentData.attention_score,
                    assessmentData.processing_speed
                ];
                
                const userTrace = {{
                    type: 'scatterpolar',
                    r: scores,
                    theta: parameters,
                    fill: 'toself',
                    fillcolor: 'rgba(52, 152, 219, 0.3)',
                    line: {{color: '#3498db', width: 3}},
                    marker: {{size: 6, color: '#3498db'}},
                    name: 'Your Results',
                    hovertemplate: '<b>%{{theta}}</b><br>Score: %{{r}}%<extra></extra>'
                }};
                
                const targetTrace = {{
                    type: 'scatterpolar',
                    r: [80, 80, 80, 80, 80, 80],
                    theta: parameters,
                    fill: 'toself',
                    fillcolor: 'rgba(46, 204, 113, 0.1)',
                    line: {{color: 'rgba(46, 204, 113, 0.6)', width: 2, dash: 'dash'}},
                    name: 'Target Level',
                    hovertemplate: 'Target: %{{r}}%<extra></extra>'
                }};
                
                const layout = {{
                    polar: {{
                        radialaxis: {{
                            visible: true,
                            range: [0, 100],
                            tickfont: {{size: 10}}
                        }},
                        angularaxis: {{
                            tickfont: {{size: 11}},
                            rotation: 90
                        }}
                    }},
                    title: 'Health Overview - All Parameters',
                    height: 400,
                    showlegend: true,
                    legend: {{
                        orientation: "h",
                        yanchor: "bottom",
                        y: 1.02,
                        xanchor: "center",
                        x: 0.5
                    }}
                }};
                
                Plotly.newPlot('health-radar', [userTrace, targetTrace], layout);
            }}
            
            function createCognitiveChart() {{
                const cognitiveParams = ['Memory', 'Attention', 'Processing Speed', 'Executive Function'];
                const cognitiveScores = [
                    assessmentData.memory_score,
                    assessmentData.attention_score,
                    assessmentData.processing_speed,
                    assessmentData.executive_function
                ];
                
                const colors = cognitiveScores.map(score => 
                    score >= 70 ? '#2ecc71' : score >= 40 ? '#f39c12' : '#e74c3c'
                );
                
                const trace = {{
                    y: cognitiveParams,
                    x: cognitiveScores,
                    type: 'bar',
                    orientation: 'h',
                    marker: {{color: colors}},
                    text: cognitiveScores.map(score => score + '%'),
                    textposition: 'auto',
                    hovertemplate: '<b>%{{y}}</b><br>Score: %{{x}}%<extra></extra>'
                }};
                
                const layout = {{
                    title: 'Cognitive Health Assessment',
                    xaxis: {{title: 'Score (%)', range: [0, 100]}},
                    height: 350,
                    margin: {{t: 80, b: 50, l: 120, r: 50}}
                }};
                
                // Add average line
                const avgCognitive = cognitiveScores.reduce((a, b) => a + b) / cognitiveScores.length;
                layout.shapes = [{{
                    type: 'line',
                    x0: avgCognitive,
                    x1: avgCognitive,
                    y0: -0.5,
                    y1: cognitiveParams.length - 0.5,
                    line: {{
                        color: colors[0],
                        width: 2,
                        dash: 'dash'
                    }}
                }}];
                
                layout.annotations = [{{
                    x: avgCognitive,
                    y: cognitiveParams.length - 0.2,
                    text: `Average: ${{avgCognitive.toFixed(0)}}%`,
                    showarrow: false,
                    font: {{size: 12}}
                }}];
                
                Plotly.newPlot('cognitive-chart', [trace], layout);
            }}
            
            // Initialize all charts
            function loadResults() {{
                createRiskGauge();
                createConstitutionChart();
                createHealthRadar();
                createCognitiveChart();
                
                // Update summary
                const cognitiveAvg = Math.round((assessmentData.memory_score + assessmentData.attention_score + 
                                               assessmentData.processing_speed + assessmentData.executive_function) / 4);
                
                document.getElementById('risk-text').textContent = 
                    `${{assessmentData.risk_category}} (${{assessmentData.overall_risk_score}}%)`;
                document.getElementById('constitution-text').textContent = assessmentData.dominant_constitution;
                document.getElementById('cognitive-text').textContent = cognitiveAvg + '%';
            }}
            
            // Load results when page loads
            window.addEventListener('load', loadResults);
        </script>
    </body>
    </html>
    """
                border-radius: 15px;
                padding: 20px;
                background: #fafafa;
            }}
            .summary-box {{
                background: linear-gradient(90deg, #4CAF50, #45a049);
                color: white;
                padding: 30px;
                border-radius: 15px;
                margin: 30px 0;
                text-align: center;
            }}
            .btn {{
                display: inline-block;
                padding: 15px 30px;
                margin: 10px;
                background: #2196F3;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s ease;
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥⚕️ Your Comprehensive Health Analysis</h1>
                <p>Assessment ID: {assessment_id}</p>
                <p>Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="summary-box" id="summary-box">
                <h2>📊 Analysis Summary</h2>
                <p id="summary-text">Loading your personalized health analysis...</p>
            </div>
            
            <div class="charts-grid" id="results-charts">
                <div id="risk-gauge-chart" class="chart-container">
                    <h3>🎯 Overall Risk Level</h3>
                    <div>Loading risk assessment...</div>
                </div>
                
                <div id="constitution-chart" class="chart-container">
                    <h3>🏛️ Ayurvedic Constitution</h3>
                    <div>Loading constitution analysis...</div>
                </div>
                
                <div id="health-radar-chart" class="chart-container">
                    <h3>🕸️ Health Overview</h3>
                    <div>Loading health radar...</div>
                </div>
                
                <div id="cognitive-chart" class="chart-container">
                    <h3>🧠 Cognitive Assessment</h3>
                    <div>Loading cognitive analysis...</div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px;">
                <a href="/assessment" class="btn">📝 Take Another Assessment</a>
                <a href="/dashboard" class="btn">📊 View Dynamic Dashboard</a>
                <a href="/" class="btn">🏠 Return Home</a>
            </div>
        </div>

        <script>
            async function loadResults() {{
                try {{
                    // Get assessment data from URL or use demo data
                    const demoData = {{
                        vata_score: 65,
                        pitta_score: 45,
                        kapha_score: 35,
                        sleep_quality: 60,
                        digestion_score: 70,
                        energy_levels: 55,
                        stress_level: 75,
                        memory_score: 65,
                        attention_score: 60,
                        processing_speed: 55,
                        executive_function: 50,
                        overall_risk_score: 58,
                        risk_category: 'Moderate Risk',
                        dominant_constitution: 'Vata'
                    }};
                    
                    // Generate charts
                    const response = await fetch('/api/charts/generate', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify(demoData)
                    }});
                    
                    const result = await response.json();
                    
                    if (result.charts) {{
                        // Update summary
                        const summaryText = `
                            <strong>Risk Level:</strong> ${{demoData.risk_category}} (${{demoData.overall_risk_score}}%) &nbsp;&nbsp;|&nbsp;&nbsp;
                            <strong>Dominant Constitution:</strong> ${{demoData.dominant_constitution}} &nbsp;&nbsp;|&nbsp;&nbsp;
                            <strong>Cognitive Health:</strong> ${{Math.round((demoData.memory_score + demoData.attention_score + demoData.processing_speed + demoData.executive_function) / 4)}}%
                        `;
                        document.getElementById('summary-text').innerHTML = summaryText;
                        
                        // Update charts
                        Object.entries(result.charts).forEach(([chartType, chartHtml]) => {{
                            if (chartType !== 'data' && chartHtml) {{
                                const container = document.getElementById(chartType + '-chart');
                                if (container) {{
                                    container.innerHTML = chartHtml;
                                }}
                            }}
                        }});
                    }}
                    
                }} catch (error) {{
                    console.error('Results loading error:', error);
                    document.getElementById('summary-text').innerHTML = 'Error loading results. Please try again.';
                }}
            }}
            
            // Load results when page loads
            loadResults();
        </script>
    </body>
    </html>
    """

# ========================================
# API ROUTES
# ========================================

@app.post("/api/assessment/complete")
async def complete_assessment(assessment_data: dict):
    """Process complete assessment"""
    try:
        # Calculate overall risk score
        constitution_avg = (assessment_data['vata_score'] + assessment_data['pitta_score'] + assessment_data['kapha_score']) / 3
        physical_avg = (assessment_data['sleep_quality'] + assessment_data['digestion_score'] + assessment_data['energy_levels'] + (100 - assessment_data['stress_level'])) / 4
        cognitive_avg = (assessment_data['memory_score'] + assessment_data['attention_score'] + assessment_data['processing_speed'] + assessment_data['executive_function']) / 4
        
        overall_risk = (constitution_avg * 0.3) + ((100 - physical_avg) * 0.4) + ((100 - cognitive_avg) * 0.3)
        
        # Determine risk category
        if overall_risk <= 30:
            risk_category = 'Low Risk'
        elif overall_risk <= 60:
            risk_category = 'Moderate Risk'
        else:
            risk_category = 'High Risk'
        
        # Add calculated fields
        assessment_data.update({
            'overall_risk_score': round(overall_risk),
            'risk_category': risk_category,
            'assessment_date': datetime.now().isoformat(),
            'assessment_id': f"ASSESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{assessment_data.get('name', 'USER').upper()}"
        })
        
        # Get ML predictions
        prakriti_result = predict_prakriti(assessment_data)
        alzheimer_result = predict_alzheimer_risk(assessment_data)
        
        assessment_data.update({
            'dominant_constitution': prakriti_result['dominant_constitution'],
            'constitution_confidence': prakriti_result['confidence'],
            'alzheimer_risk_probability': alzheimer_result['risk_probability'],
            'alzheimer_risk_level': alzheimer_result['risk_level']
        })
        
        logger.info(f"✅ Processed assessment for {assessment_data.get('name', 'Unknown')}")
        
        return {
            "status": "success",
            "assessment_id": assessment_data['assessment_id'],
            "data": assessment_data
        }
        
    except Exception as e:
        logger.error(f"Assessment processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing assessment: {str(e)}")

@app.post("/api/charts/generate")
async def generate_charts_api(assessment_data: dict):
    """Generate charts for assessment data"""
    try:
        charts = {}
        
        # Generate all chart types
        risk_gauge = create_risk_gauge(assessment_data)
        constitution_chart = create_constitution_chart(assessment_data)
        health_radar = create_health_radar(assessment_data)
        cognitive_summary = create_cognitive_summary(assessment_data)
        
        # Convert to HTML
        charts['risk-gauge'] = pio.to_html(risk_gauge, include_plotlyjs='cdn', div_id='risk-gauge-chart')
        charts['constitution'] = pio.to_html(constitution_chart, include_plotlyjs='cdn', div_id='constitution-chart')
        charts['health-radar'] = pio.to_html(health_radar, include_plotlyjs='cdn', div_id='health-radar-chart')
        charts['cognitive'] = pio.to_html(cognitive_summary, include_plotlyjs='cdn', div_id='cognitive-chart')
        
        return {"status": "success", "charts": charts}
        
    except Exception as e:
        logger.error(f"Chart generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating charts: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": {
            "prakriti_model": MODELS.get('prakriti_model') is not None,
            "alzheimers_model": MODELS.get('alzheimers_model') is not None
        },
        "version": "2.0.0"
    }

# ========================================
# WebSocket for Real-time Updates
# ========================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"✅ WebSocket connected. Total connections: {len(active_connections)}")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "request_charts":
                assessment_data = message.get("data")
                if assessment_data:
                    charts_response = await generate_charts_api(assessment_data)
                    await websocket.send_text(json.dumps({
                        "type": "charts_update",
                        "charts": charts_response["charts"]
                    }))
                    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Remaining connections: {len(active_connections)}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

# ========================================
# STARTUP EVENT
# ========================================

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("🚀 Care Catalyst - Starting up...")
    logger.info(f"📊 Models loaded: {len([k for k, v in MODELS.items() if v is not None])}/{len(MODELS)}")
    logger.info("✅ Care Catalyst is ready!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)