# 🚀 Getting Started - Expense Tracker

**Start here!** This is the fastest way to get the application running.

## ⏱️ Time Required: 5 Minutes

## Step 1: Open Terminal/Command Prompt

Open 2 separate terminal windows/tabs

**Terminal 1** will run the backend  
**Terminal 2** will run the frontend

## Step 2: Start Backend (Terminal 1)

```bash
cd backend
python -m venv venv
```

Activate virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Then:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

✅ You should see:
```
Starting development server at http://127.0.0.1:8000/
```

**Keep this running!**

## Step 3: Start Frontend (Terminal 2)

```bash
cd frontend
npm install
npm start
```

✅ The browser will open automatically at http://localhost:3000

You should see the Expense Tracker app!

## Step 4: Test It! 🎉

1. **Fill the form** on the left side:
   - Amount: `150`
   - Category: `Food`
   - Description: `Lunch`
   - Date: `Today`

2. **Click "Add Expense"**

3. **See it appear** in the table!

4. **Try filtering**: Change category dropdown to "Food"

5. **Try sorting**: Click the sort dropdown to change order

## 🎯 That's it!

You now have:
- ✅ Backend API running on http://localhost:8000
- ✅ Frontend App running on http://localhost:3000
- ✅ Database storing expenses
- ✅ Full functionality working

## 📚 Next Steps

### Option A: Explore & Learn
- Click around the app
- Try adding more expenses
- Test the filters and sorting
- Refresh the page - data persists!

### Option B: Load Sample Data
```bash
# In a new terminal, in the backend folder:
cd backend
python manage.py shell < sample_data.py
```

Refresh your browser to see 10 sample expenses!

### Option C: Deploy to Production
See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Heroku (easiest)
- Railway (good value)
- AWS (more control)
- Vercel/Netlify (frontend)

### Option D: Develop & Extend
See [DEVELOPMENT.md](DEVELOPMENT.md) for:
- Code style guidelines
- How to add features
- How to run tests
- Security best practices

## 🔍 Quick Exploration

### Check the API
Open your browser and visit:
- http://localhost:8000/api/expenses/ - See all expenses (JSON)
- http://localhost:8000/api/expenses/categories/ - See available categories
- http://localhost:8000/api/expenses/total/ - See total amount

### Check the Database
```bash
# In backend terminal (with venv active):
python manage.py shell
>>> from expenses.models import Expense
>>> Expense.objects.all()  # See all expenses
>>> Expense.objects.count()  # How many expenses
>>> exit()
```

### Check Django Admin
```bash
# In backend terminal:
python manage.py createsuperuser
# Follow the prompts
```

Then visit: http://localhost:8000/admin/
Login and browse expenses visually!

## ❌ Troubleshooting

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
# Then update frontend .env file to use 8001
```

### "Port 3000 already in use"
```bash
PORT=3001 npm start
```

### "ModuleNotFoundError: No module named 'django'"
Make sure virtual environment is activated:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### "npm: command not found"
Install Node.js from https://nodejs.org/

### "Python not found"
Install Python from https://www.python.org/

### "Can't connect to backend"
1. Make sure backend is running (Terminal 1)
2. Check it's on http://localhost:8000
3. Check frontend `.env` file has `REACT_APP_API_URL=http://localhost:8000/api`

## 📖 Full Guides

- **QUICKSTART.md** - Detailed setup guide
- **README.md** - Complete documentation
- **DEPLOYMENT.md** - How to go live
- **DEVELOPMENT.md** - Development guidelines

## 💡 Pro Tips

1. **Test duplicate prevention**: Try clicking submit twice quickly
   - Only one expense should be created!

2. **Test data persistence**: Refresh the page (F5)
   - Your data is still there!

3. **Test filtering**: Add multiple categories, then filter
   - Watch the total update!

4. **Check browser console**: Open F12 Developer Tools
   - Network tab: See API calls
   - Console: See any JavaScript errors

5. **Check backend logs**: Look at Terminal 1
   - See what requests are coming in
   - See any errors

## 🎓 What You're Running

### Backend
- **Framework**: Django (Python web framework)
- **Database**: SQLite (file-based, zero-setup)
- **API**: Django REST Framework

### Frontend
- **Framework**: React (JavaScript UI library)
- **HTTP**: Axios (for API calls)
- **Styling**: Custom CSS

## 🔐 Security Notes

This is development mode:
- `DEBUG=True` (shows errors, not for production)
- `SECRET_KEY` is visible (change in production)
- CORS allows all origins (restrict in production)

See [DEPLOYMENT.md](DEPLOYMENT.md) for production checklist.

## 🚀 Next Level

After you're comfortable:

1. **Deploy to production** (10 minutes)
   - Use Heroku, Railway, or AWS
   - See [DEPLOYMENT.md](DEPLOYMENT.md)

2. **Add features** (1-2 hours each)
   - User authentication
   - Edit/delete expenses
   - Charts and reports
   - See [DEVELOPMENT.md](DEVELOPMENT.md)

3. **Contribute**
   - Fix bugs
   - Improve performance
   - Add tests
   - See [DEVELOPMENT.md](DEVELOPMENT.md)

## 🎉 Congratulations!

You now have a fully functional expense tracker running locally!

**Questions?** Check the relevant documentation:
- Setup issues? → [QUICKSTART.md](QUICKSTART.md)
- How features work? → [README.md](README.md)
- Want to deploy? → [DEPLOYMENT.md](DEPLOYMENT.md)
- Want to develop? → [DEVELOPMENT.md](DEVELOPMENT.md)

---

**Enjoy!** 🚀

Made with ❤️ using Django & React
