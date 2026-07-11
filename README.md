<p align="center">
  <img src="assets/banner.svg" alt="Fusion Care banner" width="100%" />
</p>

<h1 align="center">🧠 Fusion Care</h1>

<h3 align="center">
AI-Powered Early Alzheimer's Disease Risk Assessment<br/>
using Ayurvedic Phenotyping &amp; Modern Clinical Intelligence
</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Machine-Learning-orange?style=for-the-badge" alt="Machine Learning"/>
  <img src="https://img.shields.io/badge/Healthcare-AI-blue?style=for-the-badge" alt="Healthcare AI"/>
  <img src="https://img.shields.io/badge/AAIC-2026-purple?style=for-the-badge" alt="AAIC 2026"/>
  <img src="https://img.shields.io/badge/Research-Repository-6f42c1?style=for-the-badge" alt="Research"/>
  <img src="https://img.shields.io/badge/Open-Source-2ea44f?style=for-the-badge" alt="Open Source"/>
</p>

---

## 🏆 Recognition

**Presented at the Alzheimer's Association International Conference (AAIC) 2026**

| | |
|---|---|
| **Presentation Type** | Virtual Poster |
| **Abstract Title** | *A Two-Stage AI/ML Framework Integrating Ayurvedic Phenotyping and Clinical Data for Early Alzheimer's Risk Detection* |

> 🖼️ *Suggested placement: crop the title block and abstract panel from the AAIC poster and insert it here as an image. Full-poster images are usually too dense to read at README width — a cropped section reads better.*

---

## 🌟 Overview

Fusion Care is a two-stage AI/ML framework for early Alzheimer's disease risk assessment. It integrates **Ayurvedic constitutional phenotyping (Prakriti)** with **modern clinical and lifestyle evaluation**, combining traditional diagnostic knowledge with evidence-based health assessment to produce personalized risk predictions and recommendations.

The architecture is designed to extend toward wearable sensors, digital biomarkers, EEG signals, neuroimaging, and digital Nadi (pulse) analytics as the research matures.

---

## ✨ Key Features

- 🧠 Two-stage AI/ML pipeline for early Alzheimer's disease risk assessment
- 🌿 Ayurvedic Prakriti phenotyping across 20 constitutional characteristics
- 🩺 Modern clinical, cognitive, and lifestyle assessment across 18 factors
- 🤖 Personalized recommendations combining Ayurveda and modern medicine
- ⚡ FastAPI backend with a sub-second prediction pipeline
- 🔬 Extensible architecture for wearables, EEG, neuroimaging, and digital biomarkers

---

## 👩‍💻 My Contribution

This repository contains the **AI/ML pipeline and FastAPI backend** that I designed and built: model development, feature engineering, data processing, API design, and performance optimization. The frontend interface was developed collaboratively with teammates during the original hackathon — this repository documents the ML and backend work specifically.

---

## 📚 Research Companion

This is the **implementation repository**. The accompanying research repository holds the scientific background:

- Literature review and research background
- AAIC 2026 poster
- Conference abstract
- References
- Future research roadmap

**Repository:** [Ayu-Allo Dementia Research](https://github.com/Avgohil/Ayu-Allo-Dementia-Research)

---

## 🏆 Hackathon Context

Fusion Care originated as the **Care Catalyst** hackathon project. This repository documents the machine learning pipeline and backend architecture I built — model development, data/feature engineering, FastAPI design, and performance work. The full-stack hackathon build additionally included a frontend (TailwindCSS + Anime.js), developed collaboratively by the team, along with deployment infrastructure that isn't part of this repository's scope.

---

## 🎯 Features

### Two-Stage ML Assessment Pipeline

**Stage 1 — Ayurvedic Prakriti Classification**
- Analyzes 20 physical and behavioral characteristics
- Determines constitution: Vata (💨), Pitta (🔥), Kapha (🌿), or a combination
- Produces personalized Ayurvedic recommendations

**Stage 2 — Alzheimer's Risk Prediction**
- Evaluates 18 health and lifestyle factors
- Generates a risk score (0–100) with Low / Medium / High classification
- Combines Prakriti type with modern clinical indicators

> 🖼️ *Suggested placement: screenshot of the multi-step assessment form (Stage 1 inputs) here.*

### Interface

- Multi-step form with progressive disclosure and visual progress indicators
- Glassmorphism, medical-blue themed design
- Animated CSS-based risk gauge (replaces earlier Plotly image generation)
- Responsive layout for desktop and mobile
- Real-time input validation

> 🖼️ *Suggested placement: screenshot of the animated risk gauge / results page here.*

---

## 🎯 Technical Leadership

As the ML and backend lead on this project, my work spanned three areas:

**Machine Learning**
- Designed the two-stage assessment pipeline (Prakriti classification → risk prediction)
- Built the Ayurvedic Prakriti classifier across 20+ features
- Built the Alzheimer's risk model across 18 health indicators

**Backend Architecture & Performance**
- Designed the FastAPI backend and its endpoints
- Reduced response time from ~30s to <1s by replacing server-side Plotly image generation with lightweight CSS-based charts
- Implemented data validation and error handling

**Data Engineering**
- Built preprocessing pipelines for both Ayurvedic and clinical inputs
- Designed feature engineering across both assessment stages
- Implemented data encoders and model serialization

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Avgohil/fusion-care-alzheimer-ml.git
cd fusion-care-alzheimer-ml

# Install dependencies
pip install -r requirements.txt

# Start the server
python care_catalyst_fast.py
```

Then open **http://localhost:8003**

---

## 🏗️ Technical Architecture

```mermaid
flowchart LR
    A[User Input] --> B[Stage 1: Prakriti Classification]
    B --> C[Stage 2: Alzheimer's Risk Prediction]
    C --> D[Results + Risk Gauge]

    subgraph Backend [FastAPI Backend]
        E["/predict — POST"]
        F["/ — GET (serves frontend)"]
        G["/static/* — static files"]
    end

    subgraph Frontend [Vanilla HTML / JS]
        H[TailwindCSS styling]
        I[Anime.js animations]
        J[Form handling + API calls]
    end

    A -.-> Backend
    Backend -.-> Frontend
```

**Backend (FastAPI):** `care_catalyst_fast.py` — `/predict` (POST, main assessment endpoint), `/` (GET, serves frontend), `/static/*` (static file serving)

**Frontend (Vanilla HTML/JS):** `static/index_fast.html` — TailwindCSS for styling, Anime.js for animation, vanilla JS for form handling and API communication

---

## 🔬 Assessment Logic

### Prakriti Classification

Rule-based scoring:
- Analyzes key characteristics (body frame, skin, hair, etc.)
- Assigns points to each dosha based on responses
- Determines the dominant constitution or mixed type
- Returns recommendations appropriate to the determined type

### Assessment Fields

**Ayurvedic Constitution (20 fields)**
- Physical: body frame, skin texture, hair type, eyes
- Physiological: sleep pattern, appetite, digestion, sweating
- Behavioral: speech, energy levels, memory, motion tendencies
- Environmental: body temperature, weather sensitivity

**Health Assessment (18 fields)**
- Demographics: age, gender
- Lifestyle: diet, sleep quality, stress level, physical activity
- Cognitive: memory loss, confusion, language difficulty, decision making
- Behavioral: repetition, social withdrawal, mood swings
- Medical: blood pressure, blood sugar, BMI, family history, chronic conditions

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

**Risk levels:** Low (0–40) — "Healthy but monitor" · Medium (41–60) — "Needs attention" · High (61–100) — "High risk, take action"

---

## 🎯 API

### `POST /predict`

**Request body**
```json
{
  "Body_Frame": "Medium, muscular",
  "Skin_Texture": "Warm, oily, reddish",
  "age": 45,
  "gender": "Male",
  "systolic_bp": 120,
  "blood_sugar": 100,
  "bmi": 23.5
}
```

**Response**
```json
{
  "prakriti_result": "Pitta-Vata",
  "prakriti_scores": {"Vata": 35, "Pitta": 45, "Kapha": 20},
  "alzheimer_risk": "Low",
  "risk_score": 25,
  "verdict": "Healthy but monitor",
  "ayurveda_recommendations": "Shankhpushpi, Gotu Kola...",
  "allopathy_recommendations": "Annual wellness exam...",
  "chart_data": {},
  "processing_time": "0.15s"
}
```

📚 Full interactive API docs are available at `/docs` when running locally.

---

## 🧪 Testing

```bash
python test_api.py
```

---

## 📁 Project Structure

```mermaid
flowchart TD
    Root["fusion-care-alzheimer-ml/"]
    Root --> A[care_catalyst_fast.py — main FastAPI app]
    Root --> B[care_catalyst_demo.py — demo version with chart generation]
    Root --> C[test_api.py — API testing script]
    Root --> D[requirements.txt — Python dependencies]
    Root --> E[static/]
    E --> E1[index_fast.html — frontend]
    Root --> F[model/]
    F --> F1[prakriti_model_robust.pkl]
    F --> F2[prakriti_encoder.pkl]
    Root --> G[README.md]
```

---

## 🔧 Dependencies

```
fastapi==0.104.1      # Web framework
uvicorn==0.24.0       # ASGI server
pandas==2.1.3         # Data manipulation
numpy==1.25.2         # Numerical computing
plotly==5.17.0        # Interactive charts (optional)
pydantic==2.5.0       # Data validation
```

---

## 🚀 Deployment

**Local development**
```bash
python care_catalyst_fast.py
```

**Production with Uvicorn**
```bash
uvicorn care_catalyst_fast:app --host 0.0.0.0 --port 8000
```

**Docker**
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "care_catalyst_fast:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔮 Future Roadmap

```mermaid
flowchart LR
    Now[Current: Rule-based Prakriti + Clinical Risk Model]
    Now --> A[Nadi Pariksha + IoT sensor integration]
    Now --> B[Neuroimaging fusion for risk prediction]
    Now --> C[EEG / fMRI pattern recognition]
    A --> D[Digital Nadi Analytics]
    B --> D
    C --> D
    D --> E[Explainable, clinically validated risk model]
```

**Advanced Ayurvedic integration**
- Nadi Pariksha (pulse diagnosis) integration with IoT sensors for more accurate Prakriti assessment
- Neuroimaging fusion with traditional Ayurvedic assessment for enhanced Alzheimer's prediction

**AI/ML research**
- Deep learning models for EEG/fMRI pattern recognition
- Computer vision for traditional diagnostic methods
- Real-time biometric data fusion

**Platform**
- Database integration for user history · authentication · mobile app · multi-language support · wearable device integration · telemedicine connections · expanded training data

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is for educational and research purposes. Please consult healthcare professionals for medical advice.

---

## 🙏 Acknowledgements

- **Ayurveda community** — for traditional knowledge and practices
- **Open source libraries** — FastAPI, TailwindCSS, Anime.js, Plotly
- **Healthcare research** — studies on Alzheimer's risk factors

---

<p align="center">
Built for better health outcomes — bridging Ayurvedic knowledge with modern AI.
</p>
