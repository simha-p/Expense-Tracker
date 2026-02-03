# Quick Start Guide - Expense Tracker

This guide will get you up and running with the Expense Tracker application in minutes.

## Prerequisites

Before starting, ensure you have:
- **Python 3.8+** - Download from [python.org](https://www.python.org/)
- **Node.js 14+** - Download from [nodejs.org](https://nodejs.org/)
- **Git** - Download from [git-scm.com](https://git-scm.com/) (optional, for cloning)

Verify installation:
```bash
python --version
node --version
npm --version
```

## Installation Steps

### Step 1: Backend Setup (Django API)

#### 1a. Navigate to backend directory
```bash
cd backend
```

#### 1b. Create virtual environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 1c. Install Python dependencies
```bash
pip install -r requirements.txt
```

You should see packages like:
- Django==4.2.7
- djangorestframework==3.14.0
- django-cors-headers==4.3.1

#### 1d. Initialize database
```bash
python manage.py migrate
```

This creates the SQLite database with expense tables.

#### 1e. (Optional) Load sample data
```bash
python manage.py shell < sample_data.py
```

This will populate the database with 10 sample expenses for testing.

#### 1f. (Optional) Create admin user for Django Admin
```bash
python manage.py createsuperuser
```

Follow the prompts to create a username and password. You can then access Django admin at http://localhost:8000/admin/

#### 1g. Start Django server
```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

✅ **Backend is running!** Access API at: http://localhost:8000/api/

### Step 2: Frontend Setup (React UI)

#### 2a. Open a NEW terminal/command prompt

**Keep the Django server running in the first terminal!**

#### 2b. Navigate to frontend directory
```bash
cd frontend
```

#### 2c. Install Node dependencies
```bash
npm install
```

This will download React and other packages (takes 1-2 minutes on first run).

#### 2d. Start React development server
```bash
npm start
```

The app will automatically open at http://localhost:3000

You should see:
- Expense form on the left
- Expense list on the right
- Summary showing totals

## Testing the Application

### 1. Add an Expense
- Fill out the form on the left:
  - **Amount**: 250
  - **Category**: Food
  - **Description**: Lunch
  - **Date**: Pick a date
- Click "Add Expense"
- See it appear in the table below

### 2. Test Duplicate Prevention
- Try clicking "Add Expense" again immediately
- The form should show loading state
- Only ONE expense should be created (idempotency works!)

### 3. Test Filters
- Use the "Category" dropdown to filter expenses
- Change to "Food" to see only food expenses
- Change to "All Categories" to see all

### 4. Test Sorting
- Click the sorting dropdown
- Select "Oldest First"
- See expenses reorder
- Change back to "Newest First"

### 5. Refresh and Verify
- Press F5 to refresh the page
- All data persists! (It's stored in the database)

### 6. Test Error Handling
- Try adding an expense with:
  - **Amount**: -100 (negative)
  - Should see error: "Amount must be greater than zero"

## API Endpoints (Backend)

Test these directly in your browser or with curl:

### Get All Expenses
```
http://localhost:8000/api/expenses/
```

### Get Expenses by Category
```
http://localhost:8000/api/expenses/?category=food
```

### Get Total
```
http://localhost:8000/api/expenses/total/
```

### Get Categories
```
http://localhost:8000/api/expenses/categories/
```

## Troubleshooting

### Problem: "Port 8000 already in use"
```bash
# Use a different port
python manage.py runserver 8001
```
Then update frontend `.env` to:
```
REACT_APP_API_URL=http://localhost:8001/api
```

### Problem: "Port 3000 already in use"
```bash
PORT=3001 npm start
```

### Problem: "ModuleNotFoundError: No module named 'django'"
- Make sure virtual environment is activated
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### Problem: "Cannot GET /api/expenses"
- Backend server is not running (see Step 1g)
- Backend is running on different port
- Check `CORS_ALLOWED_ORIGINS` in `backend/expense_tracker/settings.py`

### Problem: "CORS error in console"
- Make sure backend is running
- Check frontend `.env` has correct API URL
- Default should be: `REACT_APP_API_URL=http://localhost:8000/api`

### Problem: "Database locked"
```bash
# Delete old database and recreate
rm backend/db.sqlite3
python manage.py migrate
```

### Problem: npm modules not installing
```bash
# Clear cache and retry
npm cache clean --force
npm install
```

## File Structure Reference

```
expense-tracker/
├── backend/
│   ├── manage.py          ← Run Django commands here
│   ├── db.sqlite3         ← Your data (created after migrate)
│   ├── requirements.txt   ← Python dependencies
│   ├── sample_data.py     ← Sample data loader
│   └── expense_tracker/
│       ├── settings.py    ← Django configuration
│       └── urls.py        ← URL routing
│   └── expenses/
│       ├── models.py      ← Database models
│       ├── views.py       ← API views
│       └── serializers.py ← API serializers
│
├── frontend/
│   ├── package.json       ← npm dependencies
│   ├── .env               ← Environment config
│   └── src/
│       ├── App.js         ← Main component
│       └── components/    ← UI components
│
└── README.md              ← Full documentation
```

## Next Steps

1. **Explore the code**:
   - Backend API: `backend/expenses/views.py`
   - Frontend: `frontend/src/App.js`

2. **Customize**:
   - Change app title in `frontend/src/App.js`
   - Add more categories in `backend/expenses/models.py`
   - Modify styling in `frontend/src/index.css`

3. **Deploy** (see README.md for full deployment guide):
   - Backend: Heroku, Railway, Render, etc.
   - Frontend: Vercel, Netlify, GitHub Pages, etc.

4. **Extend features**:
   - Add user authentication
   - Implement bulk export
   - Add charts and reports
   - Mobile app with React Native

## Support

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **React Docs**: https://react.dev/
- **Issue**: Check backend logs and browser DevTools (F12)

## Key Concepts

### Idempotency
The API prevents duplicate charges even if you:
- Click submit twice
- Refresh page after submission
- Experience network issues

This is achieved using `Idempotency-Key` header.

### Data Persistence
- Data is stored in `db.sqlite3`
- Survives page refreshes, server restarts
- Can be backed up like any file

### API Communication
- Frontend sends requests to: `http://localhost:8000/api/`
- Backend processes and returns JSON
- CORS headers allow cross-origin requests

## Development Tips

### Print Debug Info
Add to any Python view:
```python
print("Debug:", something)  # Check terminal
```

Add to any JS component:
```js
console.log("Debug:", something);  // Check browser console (F12)
```

### Database Shell
```bash
python manage.py dbshell
.tables        # List tables
SELECT * FROM expenses_expense;  # Query expenses
.exit          # Exit
```

### Django Admin
- URL: http://localhost:8000/admin/
- Login with superuser credentials
- Browse/edit expenses visually

## Performance Notes

- First page load: 3-5 seconds (React compilation)
- Subsequent loads: < 1 second
- Data is cached in browser session
- Refresh forces reload from server

## Security Reminder

⚠️ **Development Mode Settings:**
- `DEBUG=True` (shows errors, not for production)
- `SECRET_KEY` is visible (change in production)
- CORS allows all origins (restrict in production)

See README.md for production security checklist.

---

**You're all set!** 🎉

Start with Step 1 (Backend), then Step 2 (Frontend), and test the application.

If stuck, check the troubleshooting section or review the full README.md.
