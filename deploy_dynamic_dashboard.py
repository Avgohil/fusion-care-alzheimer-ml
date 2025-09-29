# 🚂 RAILWAY DEPLOYMENT - Dynamic Assessment Dashboard
# Enhanced version of your heroku_app.py with dynamic visualizations

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from typing import List
import asyncio

# Initialize FastAPI app
app = FastAPI(title="Care Catalyst - Dynamic Assessment Dashboard", version="2.0.0")

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
# VISUALIZATION FUNCTIONS (from your notebook)
# ========================================

def get_risk_color(score, parameter_type='standard'):
    """Return color based on risk level"""
    if parameter_type == 'cognitive' or parameter_type == 'physical':
        # Higher is better for these parameters
        if score >= 70: return '#2ecc71'  # Green - Good
        elif score >= 40: return '#f39c12'  # Orange - Moderate
        else: return '#e74c3c'  # Red - Poor
    elif parameter_type == 'constitution':
        # For constitution, balanced (lower) is better
        if score <= 40: return '#2ecc71'  # Green - Balanced
        elif score <= 65: return '#f39c12'  # Orange - Moderate imbalance
        else: return '#e74c3c'  # Red - High imbalance
    elif parameter_type == 'stress':
        # For stress, lower is better
        if score <= 30: return '#2ecc71'  # Green - Low stress
        elif score <= 60: return '#f39c12'  # Orange - Moderate stress
        else: return '#e74c3c'  # Red - High stress

# Color palette
colors = {
    'success': '#2ecc71',
    'warning': '#f39c12', 
    'danger': '#e74c3c',
    'primary': '#3498db',
    'dark': '#2c3e50'
}

def create_risk_gauge(assessment_data):
    """Create a clean risk level gauge - perfect for form results"""
    
    risk_score = assessment_data['overall_risk_score']
    risk_category = assessment_data['risk_category']
    
    # Determine gauge color
    if risk_score <= 30:
        gauge_color = colors['success']
        status_text = "Low Risk ✅"
    elif risk_score <= 60:
        gauge_color = colors['warning']
        status_text = "Moderate Risk ⚠️"
    else:
        gauge_color = colors['danger']
        status_text = "High Risk ❗"
    
    # Create simple gauge
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
    
    # Add status text
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
    """Create clean constitution balance chart"""
    
    # Constitution data
    constitutions = ['Vata', 'Pitta', 'Kapha']
    scores = [
        assessment_data['vata_score'], 
        assessment_data['pitta_score'], 
        assessment_data['kapha_score']
    ]
    
    # Get colors based on balance level
    bar_colors = [get_risk_color(score, 'constitution') for score in scores]
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=constitutions,
            y=scores,
            marker_color=bar_colors,
            text=[f'{score}%' for score in scores],
            textposition='auto',
            hovertemplate='<b>%{x} Constitution</b><br>' +
                         'Imbalance Level: %{y}%<br>' +
                         '<i>Lower is better (more balanced)</i><extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Ayurvedic Constitution Balance",
            x=0.5,
            font=dict(size=16)
        ),
        xaxis_title="Constitution Type",
        yaxis_title="Imbalance Level (%)",
        yaxis_range=[0, 100],
        height=350,
        font=dict(family="Arial", size=12),
        margin=dict(l=50, r=50, t=80, b=50),
        paper_bgcolor='white'
    )
    
    # Add dominant constitution annotation
    dominant_idx = scores.index(max(scores))
    dominant_constitution = constitutions[dominant_idx]
    
    fig.add_annotation(
        text=f"Dominant: <b>{dominant_constitution}</b>",
        x=dominant_idx, y=scores[dominant_idx] + 5,
        font=dict(size=14, color=bar_colors[dominant_idx]),
        showarrow=True,
        arrowhead=2,
        arrowcolor=bar_colors[dominant_idx]
    )
    
    return fig

def create_health_radar(assessment_data):
    """Create compact radar chart for health overview"""
    
    # Parameters for radar chart
    parameters = [
        'Sleep Quality', 'Digestion', 'Energy Levels', 'Stress Management',
        'Memory', 'Attention', 'Processing Speed', 'Executive Function'
    ]
    
    # Normalize scores (invert stress for better visualization)
    scores = [
        assessment_data['sleep_quality'],
        assessment_data['digestion_score'],
        assessment_data['energy_levels'],
        100 - assessment_data['stress_level'],  # Invert stress
        assessment_data['memory_score'],
        assessment_data['attention_score'],
        assessment_data['processing_speed'],
        assessment_data['executive_function']
    ]
    
    # Determine overall color based on average score
    avg_score = np.mean(scores)
    radar_color = get_risk_color(avg_score, 'physical')
    
    # Convert hex color to RGB for transparency
    def hex_to_rgba(hex_color, alpha=0.3):
        """Convert hex color to rgba format"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f'rgba({r},{g},{b},{alpha})'
    
    fig = go.Figure()
    
    # Add user's scores
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=parameters,
        fill='toself',
        fillcolor=hex_to_rgba(radar_color, 0.3),  # Use proper rgba format
        line=dict(color=radar_color, width=3),
        marker=dict(size=6, color=radar_color),
        name='Your Results',
        hovertemplate='<b>%{theta}</b><br>Score: %{r}%<extra></extra>'
    ))
    
    # Add target/ideal line
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
        title=dict(
            text="Health Overview - All Parameters",
            x=0.5,
            font=dict(size=16)
        ),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        paper_bgcolor='white'
    )
    
    return fig

def create_cognitive_summary(assessment_data):
    """Create clean cognitive health summary chart"""
    
    # Cognitive parameters
    cognitive_params = ['Memory', 'Attention', 'Processing Speed', 'Executive Function']
    cognitive_scores = [
        assessment_data['memory_score'],
        assessment_data['attention_score'], 
        assessment_data['processing_speed'],
        assessment_data['executive_function']
    ]
    
    # Get colors for each cognitive parameter
    cognitive_colors = [get_risk_color(score, 'cognitive') for score in cognitive_scores]
    
    # Create horizontal bar chart for better readability
    fig = go.Figure(data=[
        go.Bar(
            y=cognitive_params,
            x=cognitive_scores,
            orientation='h',
            marker_color=cognitive_colors,
            text=[f'{score}%' for score in cognitive_scores],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>' +
                         'Score: %{x}%<br>' +
                         '<i>Higher is better</i><extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Cognitive Health Assessment",
            x=0.5,
            font=dict(size=16)
        ),
        xaxis_title="Score (%)",
        xaxis_range=[0, 100],
        height=300,
        font=dict(family="Arial", size=12),
        margin=dict(l=120, r=50, t=80, b=50),
        paper_bgcolor='white'
    )
    
    # Add average line
    avg_cognitive = np.mean(cognitive_scores)
    fig.add_vline(
        x=avg_cognitive, 
        line_dash="dash", 
        line_color=get_risk_color(avg_cognitive, 'cognitive'),
        annotation_text=f"Average: {avg_cognitive:.0f}%",
        annotation_position="top"
    )
    
    return fig

def create_compact_result_summary(assessment_data):
    """Create a single, compact chart perfect for form results"""
    
    # Create 2x2 subplot layout
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Overall Risk', 'Constitution Balance', 'Physical Health', 'Cognitive Health'),
        specs=[
            [{"type": "indicator"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "bar"}]
        ],
        horizontal_spacing=0.15,
        vertical_spacing=0.2
    )
    
    # 1. Risk Gauge (Row 1, Col 1)
    risk_score = assessment_data['overall_risk_score']
    gauge_color = get_risk_color(risk_score, 'physical')
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': gauge_color, 'thickness': 0.3},
            'steps': [
                {'range': [0, 30], 'color': 'rgba(46, 204, 113, 0.2)'},
                {'range': [30, 60], 'color': 'rgba(243, 156, 18, 0.2)'},
                {'range': [60, 100], 'color': 'rgba(231, 76, 60, 0.2)'}
            ],
        }
    ), row=1, col=1)
    
    # 2. Constitution (Row 1, Col 2)
    constitution_names = ['Vata', 'Pitta', 'Kapha']
    constitution_scores = [assessment_data['vata_score'], assessment_data['pitta_score'], assessment_data['kapha_score']]
    constitution_colors = [get_risk_color(score, 'constitution') for score in constitution_scores]
    
    fig.add_trace(go.Bar(
        x=constitution_names,
        y=constitution_scores,
        marker_color=constitution_colors,
        text=[f'{s}%' for s in constitution_scores],
        textposition='auto',
        showlegend=False
    ), row=1, col=2)
    
    # 3. Physical Health (Row 2, Col 1)
    physical_params = ['Sleep', 'Digestion', 'Energy']
    physical_scores = [assessment_data['sleep_quality'], assessment_data['digestion_score'], assessment_data['energy_levels']]
    physical_colors = [get_risk_color(score, 'physical') for score in physical_scores]
    
    fig.add_trace(go.Bar(
        x=physical_params,
        y=physical_scores,
        marker_color=physical_colors,
        text=[f'{s}%' for s in physical_scores],
        textposition='auto',
        showlegend=False
    ), row=2, col=1)
    
    # 4. Cognitive Health (Row 2, Col 2)
    cognitive_params = ['Memory', 'Attention', 'Executive']
    cognitive_scores = [assessment_data['memory_score'], assessment_data['attention_score'], assessment_data['executive_function']]
    cognitive_colors = [get_risk_color(score, 'cognitive') for score in cognitive_scores]
    
    fig.add_trace(go.Bar(
        x=cognitive_params,
        y=cognitive_scores,
        marker_color=cognitive_colors,
        text=[f'{s}%' for s in cognitive_scores],
        textposition='auto',
        showlegend=False
    ), row=2, col=2)
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Assessment Summary - {assessment_data['risk_category']}",
            x=0.5,
            font=dict(size=16)
        ),
        height=500,
        font=dict(family="Arial", size=10),
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50),
        paper_bgcolor='white'
    )
    
    # Update y-axes for bar charts
    fig.update_yaxes(range=[0, 100], row=1, col=2)
    fig.update_yaxes(range=[0, 100], row=2, col=1)
    fig.update_yaxes(range=[0, 100], row=2, col=2)
    
    return fig

# ========================================
# ENHANCED ROUTES WITH DYNAMIC CHARTS
# ========================================

@app.get("/", response_class=HTMLResponse)
async def get_main_page():
    """Main page with dynamic dashboard"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏥⚕️ Care Catalyst - Dynamic Assessment</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
            }
            .header {
                margin-bottom: 40px;
            }
            .btn {
                display: inline-block;
                padding: 15px 30px;
                margin: 10px;
                background: #2196F3;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }
            .feature-list {
                text-align: left;
                margin: 30px 0;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥⚕️ Care Catalyst</h1>
                <h2>Dynamic Assessment Dashboard</h2>
                <p>AI-powered Ayurvedic + Cognitive Health Analysis</p>
            </div>
            
            <div class="feature-list">
                <h3>✨ New Dynamic Features:</h3>
                <ul>
                    <li>🎯 Interactive risk assessment gauges</li>
                    <li>🏛️ Real-time constitution balance analysis</li>
                    <li>🕸️ Comprehensive health radar charts</li>
                    <li>🧠 Cognitive health visualization</li>
                    <li>📊 Dynamic dashboard with live updates</li>
                    <li>📱 Mobile-friendly responsive design</li>
                </ul>
            </div>
            
            <a href="/dashboard" class="btn">🚀 Launch Dynamic Dashboard</a>
            <a href="/assessment" class="btn">📝 Take Assessment</a>
            <a href="/docs" class="btn">📚 API Documentation</a>
        </div>
    </body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dynamic_dashboard():
    """Dynamic interactive dashboard"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏥⚕️ Dynamic Assessment Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
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
            .control-group {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .slider-container {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 10px;
            }
            .slider {
                flex: 1;
                margin: 0 10px;
            }
            .value-display {
                min-width: 40px;
                text-align: center;
                font-weight: bold;
                color: #333;
            }
            .chart-container {
                margin: 20px 0;
                border: 1px solid #ddd;
                border-radius: 10px;
                overflow: hidden;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            button {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                margin: 5px;
                background: #2196F3;
                color: white;
                transition: all 0.3s ease;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
                <div class="control-group">
                    <h3>🏛️ Ayurvedic Constitution</h3>
                    <div class="slider-container">
                        <label>Vata Score:</label>
                        <input type="range" id="vata" class="slider" min="0" max="100" value="75">
                        <span id="vata-value" class="value-display">75</span>
                    </div>
                    <div class="slider-container">
                        <label>Pitta Score:</label>
                        <input type="range" id="pitta" class="slider" min="0" max="100" value="45">
                        <span id="pitta-value" class="value-display">45</span>
                    </div>
                    <div class="slider-container">
                        <label>Kapha Score:</label>
                        <input type="range" id="kapha" class="slider" min="0" max="100" value="30">
                        <span id="kapha-value" class="value-display">30</span>
                    </div>
                </div>
                
                <div class="control-group">
                    <h3>💪 Physical Health</h3>
                    <div class="slider-container">
                        <label>Sleep Quality:</label>
                        <input type="range" id="sleep" class="slider" min="0" max="100" value="35">
                        <span id="sleep-value" class="value-display">35</span>
                    </div>
                    <div class="slider-container">
                        <label>Digestion:</label>
                        <input type="range" id="digestion" class="slider" min="0" max="100" value="60">
                        <span id="digestion-value" class="value-display">60</span>
                    </div>
                    <div class="slider-container">
                        <label>Energy Levels:</label>
                        <input type="range" id="energy" class="slider" min="0" max="100" value="40">
                        <span id="energy-value" class="value-display">40</span>
                    </div>
                    <div class="slider-container">
                        <label>Stress Level:</label>
                        <input type="range" id="stress" class="slider" min="0" max="100" value="80">
                        <span id="stress-value" class="value-display">80</span>
                    </div>
                </div>
                
                <div class="control-group">
                    <h3>🧠 Cognitive Health</h3>
                    <div class="slider-container">
                        <label>Memory:</label>
                        <input type="range" id="memory" class="slider" min="0" max="100" value="70">
                        <span id="memory-value" class="value-display">70</span>
                    </div>
                    <div class="slider-container">
                        <label>Attention:</label>
                        <input type="range" id="attention" class="slider" min="0" max="100" value="45">
                        <span id="attention-value" class="value-display">45</span>
                    </div>
                    <div class="slider-container">
                        <label>Processing Speed:</label>
                        <input type="range" id="processing" class="slider" min="0" max="100" value="55">
                        <span id="processing-value" class="value-display">55</span>
                    </div>
                    <div class="slider-container">
                        <label>Executive Function:</label>
                        <input type="range" id="executive" class="slider" min="0" max="100" value="40">
                        <span id="executive-value" class="value-display">40</span>
                    </div>
                </div>
                
                <div class="control-group">
                    <h3>⚙️ Controls</h3>
                    <button onclick="generateRandomData()">🎲 Random Data</button>
                    <button onclick="resetToDefault()">🔄 Reset</button>
                    <button onclick="saveAssessment()">💾 Save Assessment</button>
                    <label>
                        <input type="checkbox" id="auto-update" checked> Auto Update
                    </label>
                </div>
            </div>
            
            <div class="grid" id="charts-grid">
                <div id="risk-gauge-chart" class="chart-container"></div>
                <div id="constitution-chart" class="chart-container"></div>
                <div id="health-radar-chart" class="chart-container"></div>
                <div id="cognitive-chart" class="chart-container"></div>
                <div id="compact-chart" class="chart-container"></div>
            </div>
        </div>

        <script>
            // Slider management
            const sliders = ['vata', 'pitta', 'kapha', 'sleep', 'digestion', 'energy', 'stress', 'memory', 'attention', 'processing', 'executive'];
            
            sliders.forEach(sliderId => {
                const slider = document.getElementById(sliderId);
                const valueDisplay = document.getElementById(sliderId + '-value');
                
                slider.addEventListener('input', () => {
                    valueDisplay.textContent = slider.value;
                    if (document.getElementById('auto-update').checked) {
                        updateCharts();
                    }
                });
            });
            
            function generateRandomData() {
                sliders.forEach(sliderId => {
                    const slider = document.getElementById(sliderId);
                    const randomValue = Math.floor(Math.random() * 81) + 20;
                    slider.value = randomValue;
                    document.getElementById(sliderId + '-value').textContent = randomValue;
                });
                updateCharts();
            }
            
            function resetToDefault() {
                const defaults = {vata: 75, pitta: 45, kapha: 30, sleep: 35, digestion: 60, energy: 40, stress: 80, memory: 70, attention: 45, processing: 55, executive: 40};
                Object.entries(defaults).forEach(([key, value]) => {
                    document.getElementById(key).value = value;
                    document.getElementById(key + '-value').textContent = value;
                });
                updateCharts();
            }
            
            function getCurrentData() {
                return {
                    user_id: 'WEB_USER_' + Date.now(),
                    assessment_date: new Date().toISOString(),
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
                    executive_function: parseInt(document.getElementById('executive').value),
                    overall_risk_score: calculateOverallRisk(),
                    risk_category: getRiskCategory(),
                    dominant_constitution: getDominantConstitution()
                };
            }
            
            function calculateOverallRisk() {
                const vata = parseInt(document.getElementById('vata').value);
                const pitta = parseInt(document.getElementById('pitta').value);
                const kapha = parseInt(document.getElementById('kapha').value);
                const sleep = parseInt(document.getElementById('sleep').value);
                const digestion = parseInt(document.getElementById('digestion').value);
                const energy = parseInt(document.getElementById('energy').value);
                const stress = parseInt(document.getElementById('stress').value);
                const memory = parseInt(document.getElementById('memory').value);
                const attention = parseInt(document.getElementById('attention').value);
                const processing = parseInt(document.getElementById('processing').value);
                const executive = parseInt(document.getElementById('executive').value);
                
                const constitutionAvg = (vata + pitta + kapha) / 3;
                const physicalAvg = (sleep + digestion + energy + (100 - stress)) / 4;
                const cognitiveAvg = (memory + attention + processing + executive) / 4;
                
                const overallRisk = (constitutionAvg * 0.3) + ((100 - physicalAvg) * 0.4) + ((100 - cognitiveAvg) * 0.3);
                return Math.round(overallRisk);
            }
            
            function getRiskCategory() {
                const risk = calculateOverallRisk();
                if (risk <= 30) return 'Low Risk';
                else if (risk <= 60) return 'Moderate Risk';
                else return 'High Risk';
            }
            
            function getDominantConstitution() {
                const vata = parseInt(document.getElementById('vata').value);
                const pitta = parseInt(document.getElementById('pitta').value);
                const kapha = parseInt(document.getElementById('kapha').value);
                
                if (vata >= pitta && vata >= kapha) return 'Vata';
                else if (pitta >= kapha) return 'Pitta';
                else return 'Kapha';
            }
            
            async function updateCharts() {
                try {
                    const data = getCurrentData();
                    const response = await fetch('/api/charts/generate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (result.charts) {
                        Object.entries(result.charts).forEach(([chartType, chartHtml]) => {
                            if (chartType !== 'data' && chartHtml && typeof chartHtml === 'string') {
                                const container = document.getElementById(chartType + '-chart');
                                if (container) {
                                    container.innerHTML = chartHtml;
                                }
                            }
                        });
                    }
                    
                } catch (error) {
                    console.error('Update error:', error);
                }
            }
            
            async function saveAssessment() {
                try {
                    const data = getCurrentData();
                    const response = await fetch('/api/assessment/create', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    alert('Assessment saved successfully!');
                    
                } catch (error) {
                    console.error('Save error:', error);
                    alert('Error saving assessment');
                }
            }
            
            // Initial chart load
            updateCharts();
        </script>
    </body>
    </html>
    """

@app.post("/api/charts/generate")
async def generate_charts_api(assessment_data: dict):
    """Generate charts for given assessment data"""
    try:
        charts = {}
        
        # Generate all chart types
        risk_gauge = create_risk_gauge(assessment_data)
        constitution_chart = create_constitution_chart(assessment_data)
        health_radar = create_health_radar(assessment_data)
        cognitive_summary = create_cognitive_summary(assessment_data)
        compact_summary = create_compact_result_summary(assessment_data)
        
        # Convert to HTML
        charts['risk-gauge'] = pio.to_html(risk_gauge, include_plotlyjs='cdn', div_id='risk-gauge-chart')
        charts['constitution'] = pio.to_html(constitution_chart, include_plotlyjs='cdn', div_id='constitution-chart')
        charts['health-radar'] = pio.to_html(health_radar, include_plotlyjs='cdn', div_id='health-radar-chart')
        charts['cognitive'] = pio.to_html(cognitive_summary, include_plotlyjs='cdn', div_id='cognitive-chart')
        charts['compact'] = pio.to_html(compact_summary, include_plotlyjs='cdn', div_id='compact-chart')
        
        return {"status": "success", "charts": charts}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating charts: {str(e)}")

@app.post("/api/assessment/create")
async def create_assessment(assessment_data: dict):
    """Create new assessment"""
    try:
        # Generate charts
        charts_response = await generate_charts_api(assessment_data)
        
        # Broadcast to WebSocket connections if any
        if active_connections:
            message = json.dumps({
                "type": "new_assessment",
                "data": assessment_data,
                "timestamp": datetime.now().isoformat()
            })
            
            for connection in active_connections:
                try:
                    await connection.send_text(message)
                except:
                    pass  # Connection might be closed
        
        return {
            "status": "success",
            "assessment_id": f"ASSESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "data": assessment_data,
            "charts": charts_response["charts"] if charts_response else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating assessment: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
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
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)