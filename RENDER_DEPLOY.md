# 🚀 QUICK DEPLOY TO RENDER (5 Minutes)

## ⚡ Fast Deployment Steps:

### 1. Push to GitHub (if not already)
```bash
git add .
git commit -m "Ready for Render deployment"
git push
```

### 2. Deploy on Render
1. Go to **https://render.com**
2. Click **"Get Started for Free"** (or Sign In)
3. Connect your **GitHub** account
4. Click **"New +"** → Select **"Web Service"**
5. Find and select your repo: `fusion-care-alzheimer-ml`

### 3. Configure (Copy these settings):
- **Name**: `care-catalyst` (or anything you like)
- **Region**: Choose closest to you
- **Branch**: `main` (or your branch name)
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn care_catalyst_fast:app --host 0.0.0.0 --port $PORT`
- **Plan**: **Free**

### 4. Click **"Create Web Service"**

⏱️ **Deployment takes 3-5 minutes**

---

## 🎯 After Deployment:

Your app will be live at:
```
https://care-catalyst-XXXX.onrender.com
```

- API Docs: `https://your-app.onrender.com/docs`
- UI: `https://your-app.onrender.com/`

---

## ⚠️ Important for Demo:

**First load takes 30-60 seconds** (free tier spins down after inactivity)

**Before your pitch:**
1. Open the URL 2 minutes early to wake it up
2. Keep the browser tab open
3. Test the assessment flow once

---

## 🆘 Troubleshooting:

**If deployment fails:**
- Check the Render logs
- Ensure all files committed to GitHub
- Verify `requirements.txt` exists

**Need help?** Render has live chat support!
