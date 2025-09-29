# Care Catalyst - Deployment Guide

## 🚀 Production Deployment

### Prerequisites
- Python 3.8+
- All model files (.pkl) in the `model/` directory
- Required packages from requirements.txt

### Quick Deploy Commands

#### Local Production Server
```bash
# Install dependencies
pip install -r requirements.txt

# Start all services
python deploy.py
```

#### Docker Deployment
```bash
# Build image
docker build -t care-catalyst .

# Run container
docker run -p 8000:8000 care-catalyst
```

#### Cloud Deployment (AWS/GCP/Azure)
```bash
# For cloud platforms
gunicorn -w 4 -k uvicorn.workers.UvicornWorker deploy:app --bind 0.0.0.0:8000
```

### Service URLs
- **Main Web Interface**: http://localhost:8000
- **Prakriti API**: http://localhost:8001/docs
- **Risk Assessment API**: http://localhost:8002/docs

### Environment Variables
```bash
export PRAKRITI_API_URL=http://localhost:8001
export RISK_API_URL=http://localhost:8002
export WEB_PORT=8000
```

### Health Check
- **Status**: GET `/health`
- **Prakriti**: POST `/predict_prakriti`
- **Risk**: POST `/predict_risk`

## 📦 Files Structure for Deployment
```
care-catalyst/
├── deploy.py              # Main deployment script
├── Dockerfile             # Docker configuration  
├── requirements.txt       # Dependencies
├── model/                 # ML model files
├── apis/                  # API endpoints
├── web_interface.py       # Web UI
└── README.md             # Documentation
```

## 🌟 Features Ready for Production
✅ Unified health assessment workflow  
✅ Web interface with form validation  
✅ REST APIs with proper error handling  
✅ ML model integration  
✅ Ayurvedic + Modern recommendations  
✅ Responsive design  

## 🔧 Monitoring & Logs
- All APIs include request logging
- Health checks available
- Error tracking enabled
- Performance metrics ready