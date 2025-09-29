# Care Catalyst - Heroku Deployment Guide

## 🚀 Deploy to Heroku - Complete Guide

### Prerequisites
1. Heroku account (free tier available)
2. Git installed
3. Heroku CLI installed

### Step 1: Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or use package manager:
# Windows (with Chocolatey): choco install heroku-cli
# macOS (with Homebrew): brew tap heroku/brew && brew install heroku
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Prepare for Deployment
Your project is already prepared with:
- ✅ `Dockerfile` 
- ✅ `requirements_prod.txt`
- ✅ Health checks
- ✅ Production-ready code

### Step 4: Create Heroku App
```bash
# Navigate to your project
cd e:\Alzheimer-Ayurveda-ML

# Initialize git (if not already)
git init

# Create Heroku app
heroku create your-app-name-here

# Or let Heroku generate name:
heroku create
```

### Step 5: Set Environment Variables
```bash
heroku config:set PRAKRITI_API_URL=https://your-app-name.herokuapp.com
heroku config:set RISK_API_URL=https://your-app-name.herokuapp.com  
heroku config:set PORT=8000
```

### Step 6: Deploy Using Git
```bash
# Add all files
git add .

# Commit
git commit -m "Deploy Care Catalyst to Heroku"

# Push to Heroku
git push heroku main
```

### Step 7: Scale Your App
```bash
# Make sure at least one dyno is running
heroku ps:scale web=1
```

### Step 8: Open Your App
```bash
heroku open
```

## 🔧 Heroku-Specific Files

### Option A: Use Docker (Recommended)
Heroku will automatically detect your `Dockerfile` and use it.

### Option B: Use Buildpack
If you prefer buildpack over Docker, you'll need:

1. **Procfile** (create this file):
```
web: python deploy.py
```

2. **runtime.txt** (specify Python version):
```
python-3.11.1
```

## 🌟 Production URLs
After deployment, your app will be available at:
- **Web Interface**: https://your-app-name.herokuapp.com
- **Prakriti API**: https://your-app-name.herokuapp.com:8001/docs
- **Risk API**: https://your-app-name.herokuapp.com:8002/docs

## 🛠️ Troubleshooting

### Common Issues:
1. **Port Issues**: Heroku assigns dynamic ports
2. **File Paths**: Use relative paths
3. **Memory Limits**: Free tier has 512MB limit

### View Logs:
```bash
heroku logs --tail
```

### Restart App:
```bash
heroku restart
```

## 💰 Cost Information
- **Free Tier**: 550-1000 free hours/month
- **Hobby Tier**: $7/month - no sleep, custom domains
- **Production**: $25+/month - more memory & features

## 🚀 Quick Deploy Commands
```bash
# Complete deployment in 5 commands:
cd e:\Alzheimer-Ayurveda-ML
git init
heroku create care-catalyst-ayurveda
git add .
git commit -m "Deploy Care Catalyst"
git push heroku main
heroku open
```

## 📱 Alternative: One-Click Deploy
You can also use Heroku's web interface:
1. Connect GitHub repository
2. Enable automatic deploys
3. Deploy branch