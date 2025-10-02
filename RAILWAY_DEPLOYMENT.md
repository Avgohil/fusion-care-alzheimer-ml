# Railway Deployment Guide for Care Catalyst 🚀

## Quick Deploy to Railway

### Option 1: One-Click Deploy
1. Go to [Railway](https://railway.app)
2. Click "New Project" 
3. Select "Deploy from GitHub repo"
4. Connect your repository: `Avgohil/fusion-care-alzheimer-ml`
5. Railway will automatically detect and deploy!

### Option 2: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy from current directory
railway link
railway up
```

## Environment Variables (Optional)
No environment variables required! The app works out of the box.

## Deployment Configuration

### Files for Railway:
- ✅ `railway.json` - Railway configuration
- ✅ `runtime.txt` - Python version specification  
- ✅ `requirements.txt` - Dependencies
- ✅ `care_catalyst_fast.py` - Main application (PORT configured)

### App Configuration:
- **Start Command**: `python care_catalyst_fast.py`
- **Port**: Automatically configured via environment variable
- **Python Version**: 3.11.0
- **Framework**: FastAPI with Uvicorn

## Post-Deployment

### 1. Access Your App
Your app will be available at: `https://your-app-name.railway.app`

### 2. Test Endpoints
- **Home**: `https://your-app-name.railway.app/`
- **API**: `https://your-app-name.railway.app/predict`
- **Health**: `https://your-app-name.railway.app/docs`

### 3. Custom Domain (Optional)
1. Go to Railway dashboard
2. Click on your service
3. Go to "Settings" → "Domains"
4. Add your custom domain

## Troubleshooting

### Common Issues:
1. **Build Fails**: Check `requirements.txt` for correct dependencies
2. **App Crashes**: Check logs in Railway dashboard
3. **Port Issues**: Ensure `PORT` environment variable is used (already configured)

### Check Logs:
```bash
railway logs
```

### Restart Service:
```bash
railway restart
```

## Performance Tips

### For Better Performance:
- App uses optimized CSS charts (fast loading)
- Static files served efficiently
- Minimal dependencies for quick builds

### Resource Usage:
- **Memory**: ~100-200MB
- **Build Time**: ~2-3 minutes
- **Response Time**: <1 second

## Features Available:
✅ Ayurvedic Prakriti Classification  
✅ Alzheimer's Risk Assessment  
✅ Interactive Animated UI  
✅ Real-time Charts  
✅ Mobile Responsive  
✅ Professional Medical Theme  

## Support
- **Railway Docs**: https://docs.railway.app
- **GitHub Issues**: Create issue in repository
- **FastAPI Docs**: Available at `/docs` endpoint

Your Care Catalyst app will be live and ready for users! 🏥✨