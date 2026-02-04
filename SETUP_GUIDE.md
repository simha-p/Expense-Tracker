# 🚀 Setup & Deployment Guide

How to deploy your own instance of the Expense Tracker app.

---

## 📋 Prerequisites

- GitHub account (free)
- Streamlit account (free)
- Render account (free)
- Git installed on your computer
- Python 3.9+ installed

---

## 🔧 Part 1: Clone & Setup Locally

### **1.1 Clone the Repository**

```bash
git clone https://github.com/simha-p/Expense-Tracker.git
cd Expense-Tracker
```

### **1.2 Setup Frontend (Streamlit)**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements-streamlit.txt

# Run locally
streamlit run streamlit_app.py
```

Visit: http://localhost:8501

### **1.3 Setup Backend (Django)**

**In a new terminal:**

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Visit: http://localhost:8000/api/expenses/

### **1.4 Connect Frontend to Backend**

Update `frontend_streamlit.py` line 12:
```python
API_URL = "http://localhost:8000/api"
```

Now the Streamlit app will use your local Django server.

---

## 🌐 Part 2: Deploy Backend to Render

### **2.1 Prepare Your Repository**

```bash
# Make sure all files are committed
git add .
git commit -m "Expense Tracker application"
git push origin main
```

### **2.2 Create Render Account & Web Service**

1. Go to **https://render.com**
2. Sign up with GitHub
3. Click **"New +" → "Web Service"**
4. Select your **Expense-Tracker** repository
5. Fill in:
   - **Name:** `expense-tracker` (or any name)
   - **Environment:** Docker
   - **Region:** Choose closest to you
   - **Branch:** main
6. Click **"Create Web Service"**

### **2.3 Add Environment Variables**

While creating service or in **Settings → Environment**:

```
DEBUG=False
SECRET_KEY=YOUR_SECRET_KEY_HERE
ALLOWED_HOSTS=yourdomain.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://*.streamlit.app
```

To generate SECRET_KEY, run locally:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### **2.4 Create PostgreSQL Database**

1. In Render dashboard, click **"New +" → "PostgreSQL"**
2. Fill in:
   - **Name:** `expense-tracker-db`
   - **Database:** `expense_tracker`
   - **User:** `postgres`
3. Click **"Create Database"**
4. Copy the **Internal Database URL**

### **2.5 Connect Database to Web Service**

1. Go to your Web Service settings
2. Add environment variable:
   ```
   DATABASE_URL=postgres://user:password@host:port/database
   ```
3. (Use the URL copied above)

### **2.6 Manual Redeploy**

1. Go to Web Service
2. Click **"Manual Deploy"** button
3. Wait for build to complete
4. Check **Logs** tab for any errors

### **2.7 Verify Backend is Working**

Visit: `https://your-service-name.onrender.com/`

Should show:
```json
{"status": "ok", "message": "Expense Tracker API is running"}
```

---

## 💻 Part 3: Deploy Frontend to Streamlit Cloud

### **3.1 Create Streamlit Cloud Account**

1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**

### **3.2 Deploy App**

1. Select your repository: `Expense-Tracker`
2. Select branch: `main`
3. Main file path: `streamlit_app.py`
4. Click **"Deploy"**

Streamlit will build and deploy. Takes 2-5 minutes.

### **3.3 Add Secrets**

1. Once deployed, click **gear icon** (Settings) in top right
2. Go to **"Secrets"**
3. Add:
   ```
   API_URL = "https://your-service-name.onrender.com/api"
   ```
4. Click **"Save"**

App will automatically reload.

### **3.4 Your Live App URL**

Your app is now live at:
```
https://your-username-expense-tracker.streamlit.app/
```

---

## ✅ Verification Checklist

- [ ] Backend API responds to `GET /` with JSON
- [ ] Backend API responds to `GET /api/expenses/` with list
- [ ] Streamlit app loads without errors
- [ ] Streamlit app shows "💰 Expense Tracker" title
- [ ] Can add expense in sidebar
- [ ] Expense appears in table
- [ ] Metrics update correctly
- [ ] Charts display
- [ ] Filters work

---

## 🔧 Configuration Details

### **Django Settings (backend/expense_tracker/settings.py)**

Key settings to understand:

```python
# Database
DATABASE_URL=postgres://...  # From Render

# Security
DEBUG=False  # Production mode
SECRET_KEY=...  # Generate random key
ALLOWED_HOSTS=[...]  # Django can serve these domains
CSRF_COOKIE_SECURE=True  # HTTPS only

# API
CORS_ALLOWED_ORIGINS=[...]  # Allow Streamlit Cloud domains
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,  # Items per page
}

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Handle CORS
    'django.middleware.security.SecurityMiddleware',
    ...
]
```

### **Streamlit Config (.streamlit/config.toml)**

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
headless = true
enableXsrfProtection = true
```

---

## 🆘 Troubleshooting

### **Backend Won't Start**
```
# Check logs in Render dashboard
# Common issues:
# 1. Missing environment variables
# 2. Database connection string invalid
# 3. Docker build failed
```

### **Frontend Can't Connect to API**
```
# Check Streamlit logs:
# 1. Is API_URL secret set correctly?
# 2. Is backend domain correct?
# 3. Check API_URL format: https://domain.onrender.com/api
```

### **Port Conflicts (Local Development)**
```bash
# If port 8000 is in use:
python manage.py runserver 8001

# If port 8501 is in use:
streamlit run streamlit_app.py --server.port 8502
```

### **Database Migrations Failed**
```bash
# Reset migrations
python manage.py migrate expenses zero
python manage.py migrate
```

### **CORS Errors in Browser Console**
```
# Error: "Access to XMLHttpRequest blocked by CORS policy"
# Solution: Check CORS_ALLOWED_ORIGINS in Django settings
# Make sure Streamlit domain is included
```

---

## 🔐 Security Best Practices

### **For Production:**

1. **Never commit secrets to Git**
   - Use environment variables
   - Use .gitignore for .env files

2. **Use HTTPS everywhere**
   - Render provides free SSL certificates
   - Always use `https://` URLs

3. **Set DEBUG=False**
   - Never expose error details to users
   - Required for production

4. **Use strong SECRET_KEY**
   - Use Python secrets module
   - 32+ character random string

5. **Configure CORS properly**
   - Only allow your Streamlit domain
   - Not `*` (allow all)

6. **Use environment variables**
   - Never hardcode credentials
   - Use Render secrets manager

---

## 📊 Monitoring

### **Render Dashboard**
- **Logs** - See application output
- **Metrics** - CPU, memory, request counts
- **Deploys** - History of deployments
- **Environment** - View/edit variables

### **Streamlit Cloud Dashboard**
- **App status** - Running, sleeping, crashed
- **Logs** - Execution logs and errors
- **App analytics** - Views, sessions, errors

### **Database Monitoring**
- Size and growth
- Connection count
- Query performance

---

## 🔄 Continuous Deployment

### **Auto-Deploy on Git Push**

Both Streamlit Cloud and Render auto-deploy when you push to `main`:

```bash
# Make changes locally
git add .
git commit -m "Update expenses app"
git push origin main

# Within 30 seconds:
# - Render detects push
# - Builds Docker image
# - Deploys new container
# - Runs migrations
# - App is live with new code

# Same for Streamlit Cloud
# - Detects push
# - Re-runs app code
# - New version live in 2-5 minutes
```

---

## 📈 Scaling Tips

### **If You Outgrow Free Tier:**

1. **Upgrade Streamlit Cloud**
   - $5/month for more resources
   - https://streamlit.io/cloud

2. **Upgrade Render**
   - $7+/month for guaranteed resources
   - Better uptime and performance

3. **Add Caching**
   - Reduce API calls
   - Improve response time

4. **Add CDN**
   - CloudFlare for static assets
   - Faster delivery globally

5. **Optimize Database**
   - Add indexes on frequently queried columns
   - Archive old data

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Render Deployment Guide](https://render.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 🎓 Learning Objectives

By following this guide, you'll learn:

✅ Full-stack application development  
✅ API design and implementation  
✅ Cloud deployment strategies  
✅ Database configuration  
✅ Environment variable management  
✅ CORS and security concepts  
✅ Docker containerization  
✅ CI/CD pipelines  
✅ Monitoring and logging  

---

## 📞 Support

If you get stuck:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) for common issues
3. Check logs in Render/Streamlit dashboards
4. Read error messages carefully (usually have helpful hints)

---

**Version:** 1.0  
**Last Updated:** February 4, 2026  
**Status:** Ready for deployment
