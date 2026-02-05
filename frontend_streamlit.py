import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import os

# ============================================================================
# CONFIGURATION
# ============================================================================
API_URL = st.secrets.get("API_URL") if hasattr(st, "secrets") and st.secrets else os.getenv("API_URL")
if not API_URL:
    API_URL = "https://expense-tracker-p79n.onrender.com/api"

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 Expense Tracker")
st.markdown("Track your expenses easily and efficiently")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data(ttl=60)
def load_expenses_cached():
    """Fetch expenses from Django API"""
    try:
        url = f"{API_URL}/expenses/"
        response = requests.get(url, timeout=10, headers={"Accept": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            # Handle paginated response
            if isinstance(data, dict) and "results" in data:
                return data["results"]
            # Handle direct list response
            elif isinstance(data, list):
                return data
            else:
                return []
        else:
            return []
    except Exception as e:
        st.error(f"❌ Cannot load expenses: {str(e)}")
        return []

def load_expenses():
    """Load expenses with caching"""
    return load_expenses_cached()

def add_expense(description, amount, category, date, idempotency_key):
    """Add expense via Django API"""
    try:
        payload = {
            "description": description,
            "amount": float(amount),
            "category": category,
            "date": date
        }
        headers = {"Idempotency-Key": idempotency_key}
        
        response = requests.post(
            f"{API_URL}/expenses/",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            return True, "✅ Expense added successfully!"
        else:
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_msg = str(error_data)
                else:
                    error_msg = str(error_data)
            except:
                error_msg = response.text
            return False, f"❌ Error {response.status_code}: {error_msg}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def delete_expense(expense_id):
    """Delete a single expense via Django API"""
    try:
        response = requests.delete(
            f"{API_URL}/expenses/{expense_id}/",
            timeout=10
        )
        return response.status_code in [200, 204]
    except Exception as e:
        st.error(f"❌ Error deleting expense: {str(e)}")
        return False

def reset_all_expenses():
    """Delete all expenses for a fresh start"""
    try:
        # Get all expenses
        expenses = load_expenses_cached()
        
        if not expenses:
            return True, "✅ No expenses to clear!"
        
        # Delete each expense
        deleted_count = 0
        for exp in expenses:
            if delete_expense(exp.get("id")):
                deleted_count += 1
        
        if deleted_count == len(expenses):
            return True, f"✅ Cleared {deleted_count} expense(s)! Ready for new user."
        else:
            return False, f"⚠️ Deleted {deleted_count}/{len(expenses)} expenses"
    except Exception as e:
        return False, f"❌ Error resetting expenses: {str(e)}"

# ============================================================================
# SIDEBAR - ADD EXPENSE FORM
# ============================================================================

with st.sidebar:
    st.header("➕ Add Expense")
    
    with st.form("expense_form"):
        description = st.text_input(
            "Description",
            placeholder="e.g., Grocery shopping",
            max_chars=200
        )
        
        amount = st.number_input(
            "Amount ($)",
            min_value=0.01,
            step=0.01,
            format="%.2f"
        )
        
        category = st.selectbox(
            "Category",
            ["food", "transport", "entertainment", "utilities", "shopping", "health", "other"]
        )
        
        date = st.date_input(
            "Date",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )
        
        submitted = st.form_submit_button("➕ Add Expense", use_container_width=True)
        
        if submitted:
            if not description or amount <= 0:
                st.error("❌ Please fill in all fields correctly")
            else:
                idempotency_key = f"{description}-{amount}-{date}"
                success, message = add_expense(description, amount, category, str(date), idempotency_key)
                
                if success:
                    st.success(message)
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(message)
    
    # ====================================================================
    # NEW USER / RESET SECTION
    # ====================================================================
    
    st.divider()
    st.header("🔄 New User?")
    st.markdown("Clear all expenses and start fresh with a clean slate.")
    
    if st.button("🗑️ Reset All Expenses", use_container_width=True, type="secondary"):
        with st.spinner("🔄 Clearing all expenses..."):
            success, message = reset_all_expenses()
            
            if success:
                st.success(message)
                st.cache_data.clear()
                st.rerun()
            else:
                st.error(message)

# ============================================================================
# MAIN CONTENT - METRICS & DATA
# ============================================================================

# Load expenses
expenses = load_expenses()

if expenses:
    # Calculate metrics
    total = sum(float(e.get("amount", 0)) for e in expenses)
    count = len(expenses)
    avg = total / count if count > 0 else 0
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Expenses", f"${total:.2f}")
    with col2:
        st.metric("Number of Expenses", count)
    with col3:
        st.metric("Average Expense", f"${avg:.2f}")
    
    st.divider()
    
    # ====================================================================
    # FILTERS
    # ====================================================================
    
    col1, col2 = st.columns(2)
    
    with col1:
        categories = ["All"] + sorted(list(set(e.get("category", "Other") for e in expenses)))
        selected_category = st.multiselect(
            "Filter by Category",
            categories,
            default=["All"]
        )
    
    with col2:
        sort_order = st.radio(
            "Sort by Date",
            ["Newest First", "Oldest First"],
            horizontal=True
        )
    
    # ====================================================================
    # FILTER AND SORT
    # ====================================================================
    
    if "All" in selected_category:
        filtered_expenses = expenses
    else:
        filtered_expenses = [
            exp for exp in expenses
            if exp.get("category") in selected_category
        ]
    
    if sort_order == "Oldest First":
        filtered_expenses.sort(key=lambda x: x.get("date", ""))
    else:
        filtered_expenses.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    # ====================================================================
    # DISPLAY TABLE
    # ====================================================================
    
    st.subheader("📊 Your Expenses")
    
    if filtered_expenses:
        # Create DataFrame for better display
        df = pd.DataFrame([
            {
                "Date": e.get("date", ""),
                "Description": e.get("description", ""),
                "Category": e.get("category", ""),
                "Amount": f"${float(e.get('amount', 0)):.2f}"
            }
            for e in filtered_expenses
        ])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No expenses found for the selected filters")
    
    # ====================================================================
    # CHARTS
    # ====================================================================
    
    st.subheader("📈 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Spending by Category**")
        category_totals = {}
        for exp in filtered_expenses:
            cat = exp.get("category", "Other")
            amt = float(exp.get("amount", 0))
            category_totals[cat] = category_totals.get(cat, 0) + amt
        
        if category_totals:
            st.bar_chart(category_totals)
        else:
            st.info("No data to display")
    
    with col2:
        st.write("**Recent Expenses**")
        recent = sorted(expenses, key=lambda x: x.get("date", ""), reverse=True)[:5]
        
        for exp in recent:
            with st.container():
                col_desc, col_cat, col_amt = st.columns([2, 1, 1])
                with col_desc:
                    st.caption(f"📝 {exp.get('description', 'N/A')}")
                with col_cat:
                    st.caption(f"🏷️ {exp.get('category', 'N/A')}")
                with col_amt:
                    st.caption(f"💵 ${float(exp.get('amount', 0)):.2f}")

else:
    st.info("📭 No expenses found. Start by adding one in the sidebar!")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"🔗 API: {API_URL}")
with col2:
    st.caption("✨ Built with Streamlit")
with col3:
    st.caption("v1.0 • Expense Tracker")
