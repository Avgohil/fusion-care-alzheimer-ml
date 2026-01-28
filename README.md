# Care Catalyst 🌿🧠

**Ayurvedic Constitution & Alzheimer's Risk Assessment Platform**
## **Problem & Motivation**
Early detection of Alzheimer’s disease is difficult in South Asian settings due to limited access to advanced diagnostics, late clinical presentation, and low awareness of mild cognitive changes. Traditional Ayurvedic frameworks like Prakriti assessment capture subtle, constitution-specific risk patterns that are not reflected in routine clinical screening. Care Catalyst bridges this gap by combining Ayurvedic constitution profiling with modern health and lifestyle indicators into a unified, low-cost digital assessment pipeline. This prototype is designed as an accessible, culturally grounded starting point for future data-driven models and real-world clinical validation.

## 🌐 **Live Demo**
🚀 **Try the live application**: [https://fusion-care-alzheimer-ml-production.up.railway.app](https://fusion-care-alzheimer-ml-production.up.railway.app)
> **Note** :  The application backend and API logic are fully implemented in this repository.
The UI was handled by my teammates during the hackathon, while I focused on 
the two-stage ML pipeline and FastAPI backend. The live demo (previously on Railway) 
expired due to trial limits, but the API responses and test scripts are included 
in the assets folder for review.

📚 **API Documentation**: [https://fusion-care-alzheimer-ml-production.up.railway.app/docs](https://fusion-care-alzheimer-ml-production.up.railway.app/docs)

> **Note**: This repository contains the **ML Pipeline & Backend Implementation** that I led during our hackathon project. The complete Care Catalyst full-stack application was built collaboratively by our team during the hackathon, but this specific implementation focuses on the machine learning pipeline, data processing, and API development components. you can find complete project here ![Fusion-Care](https://github.com/Avgohil/Fusion_Care)

A modern web application that combines traditional Ayurvedic medicine with AI/ML technology to provide personalized health assessments through two-stage analysis.

![Care Catalyst](https://img.shields.io/badge/Healthcare-AI%20Powered-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

## 🏆 Hackathon Project Context

This implementation represents the **Machine Learning Pipeline & Backend Development** component of our Care Catalyst project, originally built during a hackathon. While the complete full-stack application was developed collaboratively by our team, this repository specifically showcases:

- **ML Model Development & Training** 🤖
- **Data Pipeline & Feature Engineering** 📊  
- **FastAPI Backend Architecture** 🚀
- **API Design & Integration** 🔗
- **Performance Optimization** ⚡

The full-stack version included additional components like advanced frontend frameworks, database integration, user authentication, and deployment infrastructure that were developed by other team members.

## ✨ Features

### 🎯 Two-Stage ML Assessment Pipeline
1. **Stage 1: Ayurvedic Prakriti Classification**
   - Analyzes 20 physical and behavioral characteristics
   - Determines constitution: Vata (💨), Pitta (🔥), Kapha (🌿), or combinations
   - Provides personalized Ayurvedic recommendations

2. **Stage 2: Alzheimer's Risk Prediction**
   - Evaluates 18 health and lifestyle factors
   - Generates risk score (0-100) with Low/Medium/High classification
   - Combines Prakriti type with modern health indicators

### 🎨 Beautiful UI/UX
- **Medical Blue Theme**: Professional healthcare application design
- **Glassmorphism Design**: Modern, translucent card-based interface
- **Smooth Animations**: Powered by Anime.js for fluid transitions
- **Multi-Step Form**: Progressive disclosure with visual progress indicators
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Real-time Validation**: Instant feedback on form inputs

### 📊 Interactive Results
- **Animated Risk Gauge**: CSS-based gauge with smooth animations
- **Personalized Recommendations**: Both Ayurvedic and modern medical advice
- **Beautiful Charts**: Real-time animated risk assessment visualizations
- **Print-friendly Results**: Professional results page

## 🎯 My Contribution & Technical Leadership

As the **ML Pipeline Lead** for this hackathon project, I was responsible for:

### 🤖 Machine Learning Development
- Designed and implemented the two-stage ML assessment pipeline
- Developed Ayurvedic Prakriti classification algorithm with 20+ features
- Built Alzheimer's risk prediction model with 18 health indicators
- Optimized model performance and accuracy

### ⚡ Backend Architecture & Optimization  
- Designed FastAPI backend with efficient API endpoints
- Implemented performance optimizations (reduced response time from 30s to <1s)
- Replaced heavy Plotly image generation with lightweight CSS-based charts
- Built robust data validation and error handling

### 📊 Data Engineering
- Created comprehensive data preprocessing pipelines
- Designed feature engineering for both Ayurvedic and modern health metrics
- Implemented data encoders and model serialization
- Ensured data quality and validation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Avgohil/fusion-care-alzheimer-ml.git
   cd care-catalyst
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python care_catalyst_fast.py
   ```

4. **Open your browser**
   ```
   http://localhost:8003
   ```

## 🏗️ Technical Architecture

### Backend (FastAPI)
```
care_catalyst_fast.py
├── /predict (POST) - Main assessment endpoint
├── / (GET) - Serves frontend
└── /static/* - Static file serving
```

### Frontend (Vanilla HTML/JS)
```
static/index_fast.html
├── TailwindCSS - Styling framework
├── Anime.js - Animation library
└── Vanilla JavaScript - Form handling & API communication
```

### Data Flow
```
User Input → Stage 1 (Prakriti) → Stage 2 (Risk) → Results + Chart
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

### Enhanced Features
- **Medical Blue Theme**: Professional healthcare colors
- **Animated Progress Bars**: Smooth risk score animations
- **CSS Gauge Charts**: Real-time animated risk visualization
- **Glassmorphism Cards**: Modern translucent design
- **Floating Particles**: Subtle background animations
- **Form Validation**: Real-time input feedback with animations

## 🔬 Assessment Logic

### Prakriti Classification
The system uses rule-based scoring:
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
  "chart_data": {...},
  "processing_time": "0.15s"
}
```

## 🧪 Testing

Test the API endpoint:
```bash
python test_api.py
```

## 📁 Project Structure

```
care-catalyst/
├── care_catalyst_fast.py      # Main FastAPI application
├── care_catalyst_demo.py      # Demo version with chart generation
├── test_api.py               # API testing script
├── requirements.txt          # Python dependencies
├── static/
│   └── index_fast.html       # Frontend application
├── model/                    # ML models (for full version)
│   ├── prakriti_model_robust.pkl
│   └── prakriti_encoder.pkl
└── README.md                # This file
```

## 🔧 Dependencies

```
fastapi==0.104.1      # Web framework
uvicorn==0.24.0       # ASGI server
pandas==2.1.3         # Data manipulation
numpy==1.25.2         # Numerical computing
plotly==5.17.0        # Interactive charts (optional)
pydantic==2.5.0       # Data validation
```

## 🌟 Key Features

### Performance Optimizations
- **Lightning Fast**: < 1 second response time
- **CSS-based Charts**: No image generation delays
- **Optimized Animations**: Smooth 60fps transitions
- **Minimal Dependencies**: Lightweight and efficient

### User Experience
- **Progressive Enhancement**: Works without JavaScript
- **Accessibility**: ARIA labels and keyboard navigation
- **Mobile First**: Responsive design for all devices
- **Professional Medical Design**: Healthcare industry standards

## 🚀 Deployment Options

### Local Development
```bash
python care_catalyst_fast.py
```

### Production with Uvicorn
```bash
uvicorn care_catalyst_fast:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "care_catalyst_fast:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational and research purposes. Please consult healthcare professionals for medical advice.

## 🙏 Acknowledgments

- **Ayurveda Community**: For traditional knowledge and practices
- **Open Source Libraries**: FastAPI, TailwindCSS, Anime.js, Plotly
- **Healthcare Research**: Studies on Alzheimer's risk factors

## 🔮 Future Enhancements

### 🔬 **Advanced Ayurvedic Integration**
- [ ] **Nadi Pariksha Integration**: Currently exploring pulse diagnosis (Nadi Pariksha) integration with IoT sensors for more accurate Prakriti assessment
- [ ] **Neuro-Imaging Analysis**: Research in progress to combine traditional Ayurvedic assessment with modern neuroimaging data for enhanced Alzheimer's prediction

### 📱 **Platform Enhancements**
- [ ] Database integration for user history
- [ ] User authentication system
- [ ] Mobile app (React Native/Flutter)
- [ ] Multi-language support
- [ ] Integration with wearable devices
- [ ] Telemedicine provider connections
- [ ] Advanced ML models with real training data

### 🧠 **AI/ML Research**
- [ ] Deep learning models for EEG/fMRI pattern recognition
- [ ] Computer vision for traditional diagnostic methods
- [ ] Real-time biometric data fusion algorithms

---

**Built with ❤️ for better health outcomes**

*Bridging ancient Ayurvedic wisdom with modern AI technology*

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review the API endpoints


