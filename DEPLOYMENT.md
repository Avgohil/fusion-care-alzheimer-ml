# 🚀 Care Catalyst - Deployment Guide

## Complete Deployment Documentation for Ayurvedic-AI Healthcare Platform

**Project**: Early Alzheimer Detection using Fusion of Ayurveda + Modern Science + ML  
**Team**: Care Catalyst  
**Tech Stack**: FastAPI, Scikit-learn, Plotly, Docker  

---

## 📋 Table of Contents

1. [🔧 Prerequisites](#prerequisites)
2. [🐳 Docker Deployment](#docker-deployment)
3. [🚂 Railway Deployment](#railway-deployment)
4. [🟣 Heroku Deployment](#heroku-deployment)
5. [☁️ AWS Deployment](#aws-deployment)
6. [💻 Local Development](#local-development)
7. [🔍 Health Checks](#health-checks)
8. [🐛 Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.9+ (Recommended: 3.11)
- **Memory**: Minimum 1GB RAM (Recommended: 2GB+)
- **Storage**: 500MB+ free space
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### Required Files Checklist
- ✅ `main.py` - Main FastAPI application
- ✅ `requirements.txt` - Core dependencies
- ✅ `Dockerfile` - Container configuration
- ✅ `Procfile` - Heroku process file
- ✅ `railway.json` - Railway configuration
- ✅ Model files (`*.pkl`) in correct directories

---

## 🐳 Docker Deployment

### 🔨 Build and Run

```bash
# 1. Clone repository
git clone <your-repo-url>
cd Alzheimer-Ayurveda-ML

# 2. Build Docker image
docker build -t care-catalyst .

# 3. Run container
docker run -p 8000:8000 care-catalyst

# 4. Access application
open http://localhost:8000
```

### 🔧 Advanced Docker Options

```bash
# Run with environment variables
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=info \
  care-catalyst

# Run with volume mounts (for development)
docker run -p 8000:8000 \
  -v $(pwd):/app \
  -e PYTHONPATH=/app \
  care-catalyst

# Run in background
docker run -d -p 8000:8000 --name care-catalyst-app care-catalyst
```

### 🏥 Health Check
```bash
# Check container health
docker ps
curl http://localhost:8000/health
```

---

## 🚂 Railway Deployment

### 📦 One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### 🔧 Manual Railway Setup

1. **Create Railway Account**: [railway.app](https://railway.app)

2. **Connect Repository**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   railway init
   railway up
   ```

3. **Configure Environment**:
   ```bash
   # Set environment variables
   railway variables set ENVIRONMENT=production
   railway variables set PORT=8000
   ```

4. **Custom Domain** (Optional):
   - Go to Railway dashboard
   - Settings → Domains → Add custom domain

### 📋 Railway Configuration Files

**`railway.json`**: ✅ Already configured
```json
{
  \"build\": {\"builder\": \"NIXPACKS\"},
  \"deploy\": {
    \"startCommand\": \"uvicorn main:app --host 0.0.0.0 --port $PORT\",
    \"restartPolicyType\": \"ON_FAILURE\"
  }
}
```

**`requirements_railway.txt`**: ✅ Optimized for Railway

---

## 🟣 Heroku Deployment

### 🚀 Quick Deploy

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### 🔧 Manual Heroku Setup

1. **Install Heroku CLI**: [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create and Deploy**:
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create care-catalyst-app
   
   # Set buildpack
   heroku buildpacks:set heroku/python
   
   # Deploy
   git push heroku main
   ```

3. **Configure Environment**:
   ```bash
   # Set config vars
   heroku config:set ENVIRONMENT=production
   heroku config:set PYTHONPATH=/app
   ```

4. **Scale App**:
   ```bash
   # Ensure app is running
   heroku ps:scale web=1
   
   # Check logs
   heroku logs --tail
   ```

### 📋 Heroku Configuration Files

**`Procfile`**: ✅ Already configured
```
web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
```

**`runtime.txt`**: Specifies Python version
```
python-3.11.0
```

---

## ☁️ AWS Deployment

### 🔧 AWS Elastic Beanstalk

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy**:
   ```bash
   # Initialize Elastic Beanstalk
   eb init care-catalyst
   
   # Create environment
   eb create production
   
   # Deploy
   eb deploy
   ```

3. **Application Configuration**:
   ```python
   # Create application.py (EB entry point)
   from main import app
   application = app
   
   if __name__ == \"__main__\":
       application.run()
   ```

### 🔧 AWS Lambda (Serverless)

1. **Install Mangum**:
   ```bash
   pip install mangum
   ```

2. **Create Lambda Handler**:
   ```python
   # lambda_handler.py
   from mangum import Mangum
   from main import app
   
   handler = Mangum(app)
   ```

3. **Deploy with SAM**:
   ```yaml
   # template.yaml
   AWSTemplateFormatVersion: '2010-09-09'
   Transform: AWS::Serverless-2016-10-31
   
   Resources:
     CareCatalystFunction:
       Type: AWS::Serverless::Function
       Properties:
         CodeUri: .
         Handler: lambda_handler.handler
         Runtime: python3.11
   ```

---

## 💻 Local Development

### 🔧 Setup Development Environment

1. **Clone Repository**:
   ```bash
   git clone <your-repo-url>
   cd Alzheimer-Ayurveda-ML
   ```

2. **Create Virtual Environment**:
   ```bash
   # Windows
   python -m venv care_catalyst_env
   care_catalyst_env\\Scripts\\activate
   
   # macOS/Linux
   python3 -m venv care_catalyst_env
   source care_catalyst_env/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**:
   ```bash
   # Development mode (auto-reload)
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Production mode
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### 🔧 Development Tools

```bash
# Install development dependencies
pip install pytest black flake8 mypy

# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .

# Run tests
pytest
```

---

## 🔍 Health Checks

### 🏥 Application Health Endpoints

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed system info
curl http://localhost:8000/info

# API documentation
curl http://localhost:8000/docs
```

### 🔧 Monitoring Commands

```bash
# Check process status
ps aux | grep uvicorn

# Monitor system resources
htop

# Check port usage
netstat -tlnp | grep :8000

# View application logs
tail -f logs/app.log
```

---

## 🐛 Troubleshooting

### 🔧 Common Issues & Solutions

#### ❌ Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

#### ❌ Module Not Found Errors
```bash
# Verify Python path
export PYTHONPATH=\"${PYTHONPATH}:$(pwd)\"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### ❌ Model File Not Found
```bash
# Check model file paths
ls -la model/
ls -la stage_1_prakriti_classification/models/
ls -la stage_2_alzheimer_risk_prediction/models/

# Update model paths in main.py if needed
```

#### ❌ Memory Issues
```bash
# Reduce worker count
uvicorn main:app --workers 1

# Monitor memory usage
free -h
docker stats (for containers)
```

### 🔧 Platform-Specific Issues

#### Railway Issues
- Check build logs in Railway dashboard
- Verify `railway.json` configuration
- Ensure all model files are committed to git

#### Heroku Issues
- Check slug size: `heroku apps:info`
- Verify Procfile syntax
- Check dyno logs: `heroku logs --tail`

#### Docker Issues
- Rebuild image: `docker build --no-cache -t care-catalyst .`
- Check container logs: `docker logs <container-id>`
- Verify file permissions in container

---

## 📊 Performance Optimization

### 🚀 Production Optimizations

1. **Enable Gunicorn** (for production):
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Add Caching**:
   ```python
   # Add to main.py
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def cached_prediction(features):
       return model.predict(features)
   ```

3. **Database Connection Pooling**:
   ```python
   # For future database integration
   from sqlalchemy.pool import StaticPool
   ```

---

## 🔒 Security Considerations

### 🛡️ Production Security

1. **Environment Variables**:
   ```bash
   # Never commit secrets to git
   export SECRET_KEY=\"your-secret-key\"
   export DATABASE_URL=\"your-db-url\"
   ```

2. **API Rate Limiting**:
   ```python
   # Add to main.py
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   ```

3. **HTTPS Configuration**:
   ```python
   # Add SSL redirect
   from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
   app.add_middleware(HTTPSRedirectMiddleware)
   ```

---

## 📞 Support & Resources

### 🆘 Getting Help

- **Issues**: Create GitHub issue with detailed error logs
- **Documentation**: Check FastAPI docs for advanced configuration
- **Community**: Join healthcare AI communities for support

### 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Railway Documentation](https://docs.railway.app/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [Docker Documentation](https://docs.docker.com/)

---

## 🎯 Deployment Checklist

Before deploying to production:

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Model files accessible
- [ ] Health checks working
- [ ] Logs properly configured
- [ ] Security headers added
- [ ] Performance optimized
- [ ] Monitoring setup
- [ ] Backup strategy in place
- [ ] Documentation updated

---

**🌟 Care Catalyst Team**  
*Bridging Ancient Ayurvedic Wisdom with Modern AI Technology*

---

> **⚠️ Disclaimer**: This application is for research and educational purposes only. Not intended for clinical diagnosis. Always consult qualified healthcare professionals.
