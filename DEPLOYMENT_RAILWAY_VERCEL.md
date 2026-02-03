# Deployment Guide

## Deploy Backend to Railway

1. Go to https://railway.app
2. Sign up/Login with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your `expense-tracker` repository
5. Railway auto-detects Django and creates PostgreSQL database
6. Go to **Variables** tab and add:
   ```
   SECRET_KEY=<generate-a-random-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-vercel-domain.vercel.app
   ```
7. Click **Deploy**
8. Wait 2-3 minutes, copy your Railway URL (e.g., `https://expense-tracker-xyz.railway.app`)

## Deploy Frontend to Vercel

1. Go to https://vercel.com
2. Sign up/Login with GitHub
3. Click **Import Project** → Select your `expense-tracker` repo
4. **Framework:** Select "Create React App"
5. **Root Directory:** `frontend`
6. **Environment Variables:**
   - Key: `REACT_APP_API_URL`
   - Value: `https://your-railway-app.railway.app/api`
7. Click **Deploy**
8. Wait 1 minute - your app is live!

## Verify Deployment

1. Go to your Vercel domain
2. Add an expense
3. Check backend logs in Railway dashboard
4. Both should communicate seamlessly

## Troubleshooting

**CORS Error?**
- Update Railway's `CORS_ALLOWED_ORIGINS` with your Vercel domain

**Database not connecting?**
- Railway automatically sets `DATABASE_URL`
- Check Railway logs for PostgreSQL errors

**Frontend not loading?**
- Check Vercel logs
- Verify `REACT_APP_API_URL` matches Railway URL
