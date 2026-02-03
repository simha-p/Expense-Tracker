import streamlit as st
import requests
from datetime import datetime
import json
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-msg {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = []

def load_expenses():
    """Fetch expenses from Django API"""
    try:
        response = requests.get(f"{API_URL}/expenses/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error loading expenses: {e}")
        return []

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
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            return True, "Expense added successfully!"
        else:
            return False, f"Error: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_total_expenses():
    """Get total expenses from API"""
    try:
        response = requests.get(f"{API_URL}/expenses/total/")
        if response.status_code == 200:
            return response.json().get("total", 0)
        return 0
    except:
        return 0

def get_categories():
    """Get available categories from API"""
    try:
        response = requests.get(f"{API_URL}/expenses/categories/")
        if response.status_code == 200:
            return response.json().get("categories", [])
        return ["Food", "Transport", "Entertainment", "Utilities", "Other"]
    except:
        return ["Food", "Transport", "Entertainment", "Utilities", "Other"]

# Main Page
st.title("💰 Expense Tracker")
st.markdown("Track your expenses easily and efficiently")

# Sidebar - Add Expense Form
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
        
        categories = get_categories()
        category = st.selectbox("Category", categories)
        
        date = st.date_input("Date", value=datetime.now().date())
        
        submit = st.form_submit_button("Add Expense", use_container_width=True)
        
        if submit:
            if not description:
                st.error("Please enter a description")
            elif amount <= 0:
                st.error("Amount must be greater than 0")
            else:
                # Generate idempotency key
                idempotency_key = f"{description}_{amount}_{date}"
                success, message = add_expense(
                    description, amount, category, str(date), idempotency_key
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

# Main Content
col1, col2, col3 = st.columns(3)

# Fetch total and count
total = get_total_expenses()
expenses = load_expenses()

with col1:
    st.metric("Total Expenses", f"${total:.2f}", delta=None)

with col2:
    st.metric("Number of Expenses", len(expenses), delta=None)

with col3:
    if expenses:
        avg = total / len(expenses) if expenses else 0
        st.metric("Average Expense", f"${avg:.2f}", delta=None)
    else:
        st.metric("Average Expense", "$0.00", delta=None)

st.divider()

# Filters and Sorting
col1, col2 = st.columns(2)

with col1:
    categories = get_categories()
    selected_category = st.multiselect(
        "Filter by Category",
        categories,
        default=categories
    )

with col2:
    sort_order = st.radio(
        "Sort by Date",
        ["Newest First", "Oldest First"],
        horizontal=True
    )

# Filter and sort expenses
filtered_expenses = [
    exp for exp in expenses
    if exp.get("category") in selected_category
]

if sort_order == "Oldest First":
    filtered_expenses.sort(key=lambda x: x.get("date", ""))
else:
    filtered_expenses.sort(key=lambda x: x.get("date", ""), reverse=True)

# Display Expenses Table
st.subheader("📊 Your Expenses")

if filtered_expenses:
    # Display as table
    st.write("| Date | Description | Category | Amount |")
    st.write("|------|-------------|----------|--------|")
    for exp in filtered_expenses:
        date = exp.get("date", "")
        desc = exp.get("description", "")
        cat = exp.get("category", "")
        amt = f"${exp.get('amount', 0):.2f}"
        st.write(f"| {date} | {desc} | {cat} | {amt} |")
    
    # Category breakdown
    st.subheader("📈 Spending by Category")
    
    category_totals = {}
    for exp in filtered_expenses:
        cat = exp.get("category", "Other")
        category_totals[cat] = category_totals.get(cat, 0) + exp.get("amount", 0)
    
    if category_totals:
        st.write("| Category | Amount |")
        st.write("|----------|--------|")
        for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            st.write(f"| {cat} | ${amt:.2f} |")
else:
    st.info("📭 No expenses found. Start by adding one in the sidebar!")

# Footer
st.divider()
st.caption(f"Connected to API: {API_URL}")
st.caption("Built with Streamlit • Expense Tracker v1.0")
pip install -r requirements-streamlit.txt
