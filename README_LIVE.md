# 💰 Expense Tracker - Live Application

A modern, full-stack expense tracking application built with **Streamlit** (frontend) and **Django** (backend). Deploy for FREE on Streamlit Cloud and Render!

## 🚀 Live Demo

### **Frontend (Streamlit Cloud)**
👉 **[Open Expense Tracker App](https://expense-tracker-h5d65qzjwwahsmf8wxyhpd.streamlit.app/)**

### **Backend API (Render)**
👉 **[API Health Check](https://expense-tracker-p79n.onrender.com/)**

---

## ✨ Features

✅ **Add Expenses** - Record expenses with description, amount, category, and date  
✅ **View All Expenses** - See all expenses in a clean table format  
✅ **Filter by Category** - Filter expenses by food, transport, entertainment, utilities, shopping, health, and other  
✅ **Sort Options** - Sort by newest or oldest first  
✅ **Analytics Dashboard** - View total expenses, count, and average  
✅ **Charts & Graphs** - Visualize spending by category  
✅ **Recent Expenses** - Quick view of the 5 most recent expenses  
✅ **Idempotent Operations** - Duplicate-proof API requests  

---

## 🏗️ Architecture

### **Frontend Stack**
- **Streamlit 1.32.0** - Interactive web interface
- **Pandas 2.1.4** - Data manipulation
- **Requests 2.31.0** - HTTP client for API communication
- **Deployed on:** Streamlit Cloud (FREE tier)

### **Backend Stack**
- **Django 4.2.7** - Web framework
- **Django REST Framework** - REST API
- **PostgreSQL** - Database (FREE tier on Render)
- **Gunicorn** - WSGI application server
- **Docker** - Containerization
- **Deployed on:** Render (FREE tier)

### **Architecture Diagram**
```
┌─────────────────────────────────┐
│   Streamlit Cloud (Frontend)    │
│   expense-tracker-*.streamlit.app
│   ├─ streamlit_app.py           │
│   └─ frontend_streamlit.py       │
└──────────────┬──────────────────┘
               │ HTTPS API Calls
               │ /api/expenses/
               ▼
┌─────────────────────────────────┐
│  Render Web Service (Backend)   │
│  expense-tracker-p79n.onrender.com
│  ├─ Django REST API             │
│  ├─ PostgreSQL Database         │
│  └─ Gunicorn Server             │
└─────────────────────────────────┘
```

---

## 🎯 How to Use

### **Add an Expense**
1. Fill in the form in the left sidebar:
   - **Description** - What was the expense for?
   - **Amount** - How much did you spend?
   - **Category** - Pick from food, transport, entertainment, utilities, shopping, health, other
   - **Date** - When did you spend it?
2. Click **"➕ Add Expense"**
3. Your expense will appear in the table below

### **View & Filter**
1. All expenses appear in the main **"Your Expenses"** table
2. **Filter by Category** - Select one or multiple categories (or "All")
3. **Sort** - Choose "Newest First" or "Oldest First"

### **Analyze Spending**
1. **Top Metrics** show:
   - Total Expenses (sum of all)
   - Number of Expenses (count)
   - Average Expense (total ÷ count)
2. **Chart** shows spending breakdown by category
3. **Recent Expenses** shows your 5 latest transactions

---

## 📊 API Endpoints

### **GET /api/expenses/**
Fetch all expenses (supports pagination)
```bash
curl https://expense-tracker-p79n.onrender.com/api/expenses/
```

### **POST /api/expenses/**
Create a new expense
```bash
curl -X POST https://expense-tracker-p79n.onrender.com/api/expenses/ \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique-key-123" \
  -d '{
    "description": "Grocery shopping",
    "amount": 50.00,
    "category": "food",
    "date": "2026-02-04"
  }'
```

---

## 🔧 Tech Stack Summary

| Component | Technology | Tier |
|-----------|-----------|------|
| Frontend | Streamlit 1.32.0 | FREE (Streamlit Cloud) |
| Backend | Django 4.2.7 + DRF | FREE (Render) |
| Database | PostgreSQL 16 | FREE (Render 12GB) |
| Hosting | Docker Container | FREE (Render) |
| **Total Cost** | **$0/month** | ✅ |

---

## 📁 Project Structure

```
Expense-Tracker/
├── streamlit_app.py           # Streamlit entry point
├── frontend_streamlit.py       # Main Streamlit UI app
├── requirements-streamlit.txt  # Frontend dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── backend/
│   ├── manage.py
│   ├── Dockerfile             # Docker config for Render
│   ├── requirements.txt        # Backend dependencies
│   ├── expense_tracker/        # Django project settings
│   │   ├── settings.py         # Django config (CORS, DB, etc)
│   │   ├── urls.py             # Root URLs + health check
│   │   └── wsgi.py
│   └── expenses/               # Django app
│       ├── models.py           # Expense model
│       ├── views.py            # ViewSet & API logic
│       ├── serializers.py      # DRF serializers
│       └── urls.py             # API routes
├── render.yaml                 # Render deployment config
└── README_LIVE.md              # This file
```

---

## 🚀 Deployment Details

### **Streamlit Cloud (Frontend)**
- **URL:** https://expense-tracker-h5d65qzjwwahsmf8wxyhpd.streamlit.app/
- **Branch:** `main` (auto-deploys on push)
- **Secrets:** `API_URL` = Render backend URL
- **Status:** 🟢 Live & Running

### **Render (Backend + Database)**
- **Web Service:** https://expense-tracker-p79n.onrender.com/
- **Database:** PostgreSQL (Free 12GB tier)
- **Docker:** Auto-builds from Dockerfile
- **Environment Variables:**
  - `SECRET_KEY` = Django secret
  - `DEBUG` = False (production)
  - `ALLOWED_HOSTS` = expense-tracker-p79n.onrender.com
  - `CORS_ALLOWED_ORIGINS` = *.streamlit.app
  - `DATABASE_URL` = PostgreSQL connection string
- **Status:** 🟢 Live & Running

---

## 🔐 Security Features

✅ **CSRF Protection** - Django CSRF tokens enabled  
✅ **CORS Configured** - Only Streamlit Cloud can call the API  
✅ **Idempotent Operations** - Duplicate requests are rejected  
✅ **HTTPS Everywhere** - All connections encrypted  
✅ **Environment Variables** - Sensitive data in secrets, not code  
✅ **Debug Off** - Production mode (`DEBUG=False`)  

---

## 📱 Browser Compatibility

✅ Chrome/Edge (Latest)  
✅ Firefox (Latest)  
✅ Safari (Latest)  
✅ Mobile browsers (iPhone, Android)  

---

## 📝 Example Workflow

1. **Open the app:** https://expense-tracker-h5d65qzjwwahsmf8wxyhpd.streamlit.app/
2. **Add expense:**
   - Description: "Coffee at Starbucks"
   - Amount: 5.50
   - Category: food
   - Date: Today
   - Click ➕ Add Expense
3. **View results:**
   - Expense appears in table
   - Metrics update (Total, Count, Average)
   - Chart shows food category spending
4. **Filter & analyze:**
   - Select only "food" category
   - Sort by Newest First
   - View spending patterns

---

## 🛠️ For Developers

### **Clone & Run Locally**

```bash
# Clone repo
git clone https://github.com/simha-p/Expense-Tracker.git
cd Expense-Tracker

# Frontend
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py

# Backend (in another terminal)
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### **Deploy Your Own**

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

---

## 📚 Documentation

- [LIVE_DEPLOYMENT.md](LIVE_DEPLOYMENT.md) - How to access and use the live app
- [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) - What was built and how it works
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Deploy your own instance
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed technical architecture

---

## 🎓 Learning Resources

This project demonstrates:
- **Streamlit** - Building interactive web apps without JavaScript
- **Django REST Framework** - Building robust REST APIs
- **PostgreSQL** - Modern relational database
- **Docker** - Containerization for consistent deployments
- **CORS & Security** - Cross-origin requests and API security
- **Cloud Deployment** - Deploying to Streamlit Cloud and Render

---

## 📧 Support

If you have questions or find issues:
1. Check [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) for common issues
2. Review API logs in Render dashboard
3. Check Streamlit Cloud logs for frontend errors

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Credits

Built with:
- [Streamlit](https://streamlit.io/) - Frontend framework
- [Django](https://www.djangoproject.com/) - Backend framework
- [Render](https://render.com/) - Cloud hosting
- [Streamlit Cloud](https://streamlit.io/cloud) - Frontend hosting

---

## 🎉 Status

| Component | Status | Link |
|-----------|--------|------|
| Frontend | 🟢 Live | [Open App](https://expense-tracker-h5d65qzjwwahsmf8wxyhpd.streamlit.app/) |
| Backend API | 🟢 Live | [Health Check](https://expense-tracker-p79n.onrender.com/) |
| Database | 🟢 Active | PostgreSQL on Render |
| **Overall** | ✅ **READY FOR PRODUCTION** | |

---

**Last Updated:** February 4, 2026  
**Version:** 1.0  
**Deployment Status:** Live & Running 🚀
