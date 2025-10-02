# Care Catalyst 🌿🧠

**Ayurvedic Constitution & Alzheimer's Risk Assessment Platform**

Care Catalyst is an innovative web application that combines traditional Ayurvedic medicine with modern AI/ML technology to provide personalized health assessments. The platform performs two-stage analysis: first determining your Ayurvedic constitution (Prakriti), then evaluating Alzheimer's disease risk factors.

![Care Catalyst Demo](assets/demo-screenshot.png)

## ✨ Features

### 🎯 Two-Stage Assessment Pipeline
1. **Stage 1: Ayurvedic Prakriti Classification**
   - Analyzes 20 physical and behavioral characteristics
   - Determines constitution: Vata (💨), Pitta (🔥), Kapha (🌿), or combinations
   - Provides personalized Ayurvedic recommendations

2. **Stage 2: Alzheimer's Risk Prediction**
   - Evaluates 18 health and lifestyle factors
   - Generates risk score (0-100) with Low/Medium/High classification
   - Combines Prakriti type with modern health indicators

### 🎨 Beautiful UI/UX
- **Glassmorphism Design**: Modern, translucent card-based interface
- **Smooth Animations**: Powered by Anime.js for fluid transitions
- **Multi-Step Form**: Progressive disclosure with visual progress indicators
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Real-time Validation**: Instant feedback on form inputs

### 📊 Interactive Results
- **Dynamic Risk Gauge**: Animated progress bars and risk visualization
- **Personalized Recommendations**: Both Ayurvedic and modern medical advice
- **Beautiful Charts**: Plotly-generated risk assessment charts
- **Downloadable Results**: Print-friendly results page

## 🏗️ Technical Architecture

### Backend (FastAPI)
```
care_catalyst_demo.py
├── /predict (POST) - Main assessment endpoint
├── / (GET) - Serves frontend
└── /static/* - Static file serving
```

### Frontend (Vanilla HTML/JS)
```
static/index.html
├── TailwindCSS - Styling framework
├── Anime.js - Animation library
└── Vanilla JavaScript - Form handling & API communication
```

### Data Flow
```
User Input → Stage 1 (Prakriti) → Stage 2 (Risk) → Results + Chart
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone/Download the project**
   ```bash
   cd Alzheimer-Ayurveda-ML
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python care_catalyst_demo.py
   ```

4. **Open your browser**
   ```
   http://localhost:8000
   ```

### Alternative: Using Uvicorn
```bash
uvicorn care_catalyst_demo:app --host 0.0.0.0 --port 8000
```

## 📋 Assessment Fields

### Ayurvedic Constitution (20 fields)
- **Physical**: Body frame, skin texture, hair type, eyes
- **Physiological**: Sleep pattern, appetite, digestion, sweating
- **Behavioral**: Speech, energy levels, memory, motion tendencies
- **Environmental**: Body temperature, weather sensitivity

### Health Assessment (18 fields)
- **Demographics**: Age, gender
- **Lifestyle**: Diet, sleep quality, stress level, physical activity
- **Cognitive**: Memory loss, confusion, language difficulty, decision making
- **Behavioral**: Repetition, social withdrawal, mood swings
- **Medical**: Blood pressure, blood sugar, BMI, family history, chronic conditions

## 🎨 UI Components

### Form Steps
1. **Step 1**: Basic Ayurvedic characteristics (Body frame, skin, hair, etc.)
2. **Step 2**: Additional constitution factors (Temperature, memory, emotions)
3. **Step 3**: Health & lifestyle assessment (Age, diet, symptoms)
4. **Step 4**: Final health details (Vitals, family history)

### Animations
- **Slide Transitions**: Smooth left/right slide between form steps
- **Fade Effects**: Gentle opacity transitions for results display
- **Progress Indicators**: Animated step completion states
- **Loading Animation**: Spinner with progressive text updates
- **Result Reveals**: Staggered animations for result cards

### Styling Features
- **Glassmorphism Cards**: Semi-transparent backgrounds with blur effects
- **Gradient Backgrounds**: Beautiful color gradients for visual appeal
- **Responsive Grid**: Auto-adjusting layouts for different screen sizes
- **Interactive Elements**: Hover effects and focus states
- **Color Coding**: Risk levels represented by colors (Green/Yellow/Red)

## 🔬 Assessment Logic

### Prakriti Classification
The demo version uses rule-based scoring:
- Analyzes key characteristics (body frame, skin, hair, etc.)
- Assigns points to each dosha based on responses
- Determines dominant constitution or mixed type
- Provides appropriate recommendations for the determined type

### Risk Score Calculation
```python
# Age factors
age > 65: +10 points
age > 55: +5 points

# Cognitive symptoms
memory_loss: 0-20 points
confusion: 0-15 points
language_difficulty: 0-10 points

# Lifestyle factors
poor_sleep: +5 points
high_stress: +5 points
low_activity: +5 points

# Health indicators
systolic_bp > 140: +8 points
blood_sugar > 126: +8 points
bmi > 30: +6 points

# Family history: +15 points
```

### Risk Levels
- **Low (0-40)**: "Healthy but monitor"
- **Medium (41-60)**: "Needs attention"
- **High (61-100)**: "High risk, take action"

## 📊 Chart Generation

The application generates interactive risk visualization using Plotly:
- **Gauge Chart**: Shows risk score on a 0-100 scale
- **Color Zones**: Green (low), Yellow (medium), Red (high)
- **Base64 Encoding**: Charts converted to images for frontend display

## 🎯 API Endpoints

### POST /predict
**Request Body:**
```json
{
  "Body_Frame": "Medium, muscular",
  "Skin_Texture": "Warm, oily, reddish",
  "age": 45,
  "gender": "Male",
  "systolic_bp": 120,
  "blood_sugar": 100,
  "bmi": 23.5,
  ...
}
```

**Response:**
```json
{
  "prakriti_result": "Pitta-Vata",
  "prakriti_scores": {"Vata": 35, "Pitta": 45, "Kapha": 20},
  "alzheimer_risk": "Low",
  "risk_score": 25,
  "verdict": "Healthy but monitor",
  "ayurveda_recommendations": "Shankhpushpi, Gotu Kola...",
  "allopathy_recommendations": "Annual wellness exam...",
  "chart": "data:image/png;base64,..."
}
```

## 🧪 Testing

Test the API endpoint:
```bash
python test_api.py
```

## 📁 Project Structure

```
Alzheimer-Ayurveda-ML/
├── care_catalyst_demo.py      # Main FastAPI application
├── care_catalyst_app.py       # Full version (requires ML models)
├── test_api.py               # API testing script
├── requirements.txt          # Python dependencies
├── static/
│   └── index.html           # Frontend application
├── model/                   # ML models (for full version)
│   ├── prakriti_model_robust.pkl
│   └── prakriti_encoder.pkl
└── README.md               # This file
```

## 🔧 Dependencies

```
fastapi==0.104.1      # Web framework
uvicorn==0.24.0       # ASGI server
pandas==2.1.3         # Data manipulation
scikit-learn==1.3.2   # ML library (for full version)
joblib==1.3.2         # Model serialization
pydantic==2.5.0       # Data validation
numpy==1.25.2         # Numerical computing
matplotlib==3.7.2     # Plotting library
plotly==5.17.0        # Interactive charts
kaleido==0.2.1        # Static image export
```

## 🌟 Key Features Breakdown

### Frontend Highlights
- **Progressive Enhancement**: Works without JavaScript (graceful degradation)
- **Accessibility**: ARIA labels and keyboard navigation support
- **Performance**: Optimized animations and minimal external dependencies
- **Mobile First**: Responsive design that works on all devices

### Backend Highlights
- **Fast Performance**: Async FastAPI with optimized endpoints
- **Error Handling**: Comprehensive error messages and validation
- **Scalable Architecture**: Modular design for easy extension
- **Documentation**: Auto-generated API docs at `/docs`

### Integration Points
- **Seamless Data Flow**: Form → API → Results without page refresh
- **Real-time Updates**: Live progress indicators during processing
- **Smooth UX**: No jarring transitions or loading states

## 🚀 Future Enhancements

1. **Database Integration**: Store user assessments and historical data
2. **User Accounts**: Personal profiles and assessment history
3. **Advanced Analytics**: Trend analysis and population insights
4. **Mobile App**: React Native or Flutter mobile application
5. **Multilingual Support**: Multiple language options
6. **Real ML Models**: Integration with actual trained models
7. **Telemedicine Integration**: Connect with healthcare providers
8. **Wearable Data**: Integration with fitness trackers and health devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please consult healthcare professionals for medical advice.

## 🙏 Acknowledgments

- **Ayurveda Community**: For traditional knowledge and practices
- **Open Source Libraries**: FastAPI, TailwindCSS, Anime.js, Plotly
- **Healthcare Research**: Studies on Alzheimer's risk factors

---

**Built with ❤️ by the Care Catalyst Team**

*Bridging ancient wisdom with modern technology for better health outcomes.*