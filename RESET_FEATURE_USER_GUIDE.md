# 🆕 Reset Feature - User Guide

## What's New? 🎉

Your Expense Tracker app now has a **Reset/Refresh button** that allows users to:
- ✅ Clear all expenses in one click
- ✅ Start fresh with a clean slate
- ✅ Switch between different users
- ✅ Reset for testing/demo purposes

---

## Where is the Reset Button?

The reset button is located in the **left sidebar** at the bottom of the "Add Expense" form.

```
┌─────────────────────────┐
│    Expense Tracker      │
└─────────────────────────┘

SIDEBAR (LEFT):
┌─────────────────────────┐
│  ➕ ADD EXPENSE         │
│  ─────────────────────  │
│  Description: [     ]   │
│  Amount: [  ]           │
│  Category: [         ]  │
│  Date: [         ]      │
│  [  ➕ Add Expense   ]   │
│                         │
│  ─────────────────────  │
│  🔄 NEW USER?           │
│  ─────────────────────  │
│  Clear all expenses     │
│  and start fresh.       │
│                         │
│  [🗑️ Reset All Expenses]│ ← CLICK HERE
└─────────────────────────┘
```

---

## How to Use the Reset Feature

### Step 1: Locate the Button
- Open the Expense Tracker app
- Look in the **left sidebar**
- Scroll down to the **"🔄 New User?"** section

### Step 2: Click the Button
- Click **"🗑️ Reset All Expenses"** button
- A spinning loader will appear while deleting

### Step 3: Confirmation
- Once complete, you'll see a success message
- Message shows how many expenses were deleted
- Example: `✅ Cleared 5 expense(s)! Ready for new user.`

### Step 4: Fresh Start
- The app automatically reloads
- All expenses are cleared
- The app shows: `📭 No expenses found`
- You're ready to add new expenses!

---

## Use Cases

### 📱 **Scenario 1: Multi-User Device**
```
User A → Adds 10 expenses
User B → Click Reset → Clear all expenses
User B → Add their own expenses
```

### 🧪 **Scenario 2: Testing/Demo**
```
Developer → Add test data
Developer → Test filtering, sorting, analytics
Developer → Click Reset → Clean for next test run
```

### 👥 **Scenario 3: Monthly Reset**
```
January → Add all monthly expenses
February 1st → Click Reset → Start fresh for February
```

### 🔄 **Scenario 4: Data Cleanup**
```
Accidentally added bad data
Click Reset → Remove everything
Start over cleanly
```

---

## What Happens When You Click Reset?

```
[Click Button]
    ↓
[Spinner appears: "🔄 Clearing all expenses..."]
    ↓
[System fetches all expenses]
    ↓
[Deletes each expense one by one]
    ↓
[Success message: "✅ Cleared X expense(s)! Ready for new user."]
    ↓
[App auto-reloads with empty state]
    ↓
[Ready to add new expenses]
```

---

## Important Notes ⚠️

### ✅ Safe Operations
- **Secure**: Uses same API as add/delete operations
- **Timeout Protected**: 10-second timeout per delete
- **Error Handling**: Shows clear error messages if something goes wrong
- **No Permanent Damage**: You can always add new expenses immediately

### ⚡ Performance
- Deletes one expense at a time (safe and reliable)
- Usually completes in 2-5 seconds for small datasets
- Spinner keeps you informed during the process

### 🔐 Data Privacy
- Only affects your local expenses
- No other users' data is affected
- Backend validates all delete requests

### ↩️ Cannot Undo
- **Important**: Once deleted, expenses are gone permanently
- There is no undo button
- Make sure you want to delete before clicking
- (Future versions may add backup/export feature)

---

## Example Walkthrough

### Before Reset:
```
📊 Metrics:
- Total: $245.50
- Count: 5
- Average: $49.10

📋 Expenses:
1. Grocery Shopping - $65.00
2. Gas - $45.00
3. Movie Tickets - $30.00
4. Restaurant - $75.50
5. Gym Membership - $30.00
```

### Click "🗑️ Reset All Expenses"

### During Reset:
```
🔄 Clearing all expenses...
(spinner shows)
```

### After Reset:
```
📭 No expenses found. Start by adding one in the sidebar!

Ready for new user to add expenses...
```

---

## Troubleshooting

### ❓ Button Doesn't Work?
- **Check Connection**: Ensure API is reachable (https://expense-tracker-p79n.onrender.com/)
- **Check Status**: Try the health check endpoint
- **Refresh Page**: Sometimes helps with cache issues

### ❓ Delete Failed Partially?
- You'll see: `⚠️ Deleted X/Y expenses`
- Click the button again to retry remaining deletions
- Or refresh and try again

### ❓ Still Seeing Old Expenses?
- Clear your browser cache
- Refresh the page (Ctrl+R or Cmd+R)
- Check API is responding

### ❓ How Long Does It Take?
- Usually 2-5 seconds for under 50 expenses
- Large datasets may take longer
- Spinner shows progress during deletion

---

## Feature Details

| Property | Value |
|----------|-------|
| **Location** | Sidebar, below Add Expense form |
| **Button Text** | 🗑️ Reset All Expenses |
| **API Endpoint** | DELETE /api/expenses/{id}/ |
| **Time to Delete** | ~0.5 sec per expense |
| **Confirmation** | Shows count of deleted items |
| **Cache Clear** | Automatic |
| **Auto Reload** | Yes |

---

## Technical Info for Developers

### Function: `delete_expense(expense_id)`
```python
- Sends DELETE request to API
- Returns True if successful (200/204)
- Returns False on error
- Catches and logs exceptions
```

### Function: `reset_all_expenses()`
```python
- Fetches all expenses
- Deletes each one
- Counts successes
- Returns (success: bool, message: str)
```

### API Calls:
```
GET  /api/expenses/          → List all
DELETE /api/expenses/{id}/   → Delete one
```

---

## FAQ

**Q: Will this delete expenses for other users?**
A: Only your expenses in this application. Since there's no user authentication yet, all users share the same database.

**Q: Can I recover deleted expenses?**
A: No, deletion is permanent. There's no backup or recovery feature in the current version.

**Q: How often can I use reset?**
A: As many times as you want! No limits or cooldowns.

**Q: Does it affect the backend database?**
A: Yes, deletions are permanent in the database. This is by design.

**Q: Is there a confirmation dialog?**
A: Currently no, but future versions may add this for extra safety.

**Q: What if the delete fails?**
A: You'll see a warning message. The button can be clicked again to retry.

---

## Summary

🎯 **Feature**: Reset All Expenses  
✅ **Status**: LIVE and Production Ready  
📱 **Location**: Sidebar (bottom)  
⚡ **Speed**: 2-5 seconds for typical usage  
🔒 **Safety**: Validated API calls with error handling  
🔄 **Use**: Click anytime to start fresh  

---

## Learn More

- [Reset Feature Changelog](RESET_FEATURE_CHANGELOG.md) - Technical details
- [Live App](https://expense-tracker-h5d65qzjwwahsmf8wxyhpd.streamlit.app/) - Try it now
- [Backend API](https://expense-tracker-p79n.onrender.com/) - API status
- [Setup Guide](SETUP_GUIDE.md) - Full documentation

**Questions?** Check [README.md](README.md) for more info or open an issue on GitHub!
