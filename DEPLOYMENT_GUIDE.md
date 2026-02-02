# Free Deployment Guide - GitHub + Render

## Overview
- **Backend**: Deployed to Render (free tier)
- **Database**: SQLite (included)
- **Frontend**: Option to deploy to Vercel/Netlify (free)

## Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
# Initialize Git repo (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - ready for deployment"

# Add your GitHub repo as remote
git remote add origin https://github.com/YOUR_USERNAME/ai-code-generator.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy Backend to Render

1. **Go to** [render.com](https://render.com) → Sign up (free)
2. **Create a new service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select `ai-code-generator` repository
   - Render will auto-detect the Dockerfile

3. **Configuration:**
   - **Name**: `ai-code-generator-api` (or your choice)
   - **Environment**: Docker
   - **Plan**: Free
   - Leave other settings default

4. **Deploy:**
   - Click "Create Web Service"
   - Render deploys automatically (takes 2-3 minutes)
   - You'll get a URL like: `https://ai-code-generator-api.onrender.com`

5. **Test your API:**
   - Visit `https://your-url.onrender.com/docs` (Swagger UI)
   - Your API is live! ✅

### Step 3: (Optional) Deploy Frontend to Vercel

1. **Go to** [vercel.com](https://vercel.com) → Sign in with GitHub
2. **Import project** → Select your repository
3. **Settings:**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Install Command: `npm install`
   - Output Directory: `build`

4. **Add Environment Variable:**
   - Go to Settings → Environment Variables
   - `REACT_APP_API_URL` = `https://your-render-url.onrender.com`

5. **Deploy** → Done! Frontend gets live URL

### Step 4: Update Frontend API URL

Update your frontend to use the production API:

In `frontend/src/` files, replace `localhost:8000` with:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

## Important Notes

⚠️ **Free Tier Limits:**
- Render free tier: App goes to sleep after 15 mins of inactivity
- First request after sleep takes 30 seconds to wake up
- SQLite database persists between restarts
- Upgrade to paid ($7/month) for always-on service

⚠️ **Ollama Service:**
- Deployed backend won't have Ollama installed
- If you need Ollama on server, either:
  1. Install in Dockerfile (adds 4GB+ size)
  2. Keep local Ollama and connect via API

## Troubleshooting

**Backend won't deploy:**
- Check Render logs for errors
- Ensure `render.yaml` and `Dockerfile` are in root directory

**Frontend can't reach backend:**
- Verify API URL in frontend environment variables
- Check CORS settings in `backend/main.py`

**Database issues:**
- SQLite file is in `/tmp/` on Render (temporary)
- Consider migrating to PostgreSQL for production

## Next Steps

- Monitor your app at Render dashboard
- Set up email notifications for deployment status
- Consider upgrading to paid tier if you get users

---

**Your API is now online!** 🚀
