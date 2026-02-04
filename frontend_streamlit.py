import streamlit as st
import requests
from datetime import datetime
import json
import os
import pandas as pd
from functools import lru_cache
import time

# Configuration - Try Streamlit secrets first, then environment variables, then default
try:
    API_URL = st.secrets["API_URL"]
except (KeyError, AttributeError):
    API_URL = os.getenv("API_URL", "http://localhost:8000/api")

# Session management
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = 0
if "expenses_cache" not in st.session_state:
    st.session_state.expenses_cache = []

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

@st.cache_data(ttl=60)
def load_expenses_cached():
    """Fetch expenses from Django API"""
    try:
        response = requests.get(f"{API_URL}/expenses/", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.Timeout:
        st.error("⏱️ Backend timeout. Please try again.")
        return []
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Is it running?")
        return []
    except Exception as e:
        st.error(f"❌ Error loading expenses: {str(e)}")
        return []

def load_expenses():
    """Load expenses with user-triggered refresh option"""
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
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            return True, "Expense added successfully!"
        else:
            return False, f"Error: {response.json().get('detail', 'Unknown error')}"
    except Exception as e:
        return False, f"Error: {str(e)}"

@st.cache_data(ttl=60)
def get_total_expenses_cached():
    """Get total expenses from API"""
    try:
        response = requests.get(f"{API_URL}/expenses/total/", timeout=10)
        if response.status_code == 200:
            return response.json().get("total", 0)
        return 0
    except:
        return 0

def get_total_expenses():
    """Get total expenses"""
    return get_total_expenses_cached()

@st.cache_data(ttl=3600)
def get_categories_cached():
    """Get available categories from API"""
    try:
        response = requests.get(f"{API_URL}/expenses/categories/", timeout=10)
        if response.status_code == 200:
            return response.json().get("categories", [])
        return ["Food", "Transport", "Entertainment", "Utilities", "Other"]
    except:
        return ["Food", "Transport", "Entertainment", "Utilities", "Other"]

def get_categories():
    """Get categories"""
    return get_categories_cached()

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

# Main Content - Add Refresh Button
col1, col2, col3, col4 = st.columns(4)

with col4:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

cols = st.columns(3)

# Fetch total and count
total = get_total_expenses()
expenses = load_expenses()

with cols[0]:
    st.metric("Total Expenses", f"${total:.2f}", delta=None)

with cols[1]:
    st.metric("Number of Expenses", len(expenses), delta=None)

with cols[2]:
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
    # Convert to DataFrame for better display
    df_data = []
    for exp in filtered_expenses:
        df_data.append({
            "Date": exp.get("date", ""),
            "Description": exp.get("description", ""),
            "Category": exp.get("category", ""),
            "Amount": f"${exp.get('amount', 0):.2f}"
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Category breakdown
    st.subheader("📈 Spending by Category")
    
    category_totals = {}
    for exp in filtered_expenses:
        cat = exp.get("category", "Other")
        category_totals[cat] = category_totals.get(cat, 0) + exp.get("amount", 0)
    
    if category_totals:
        # Display as DataFrame
        df_categories = pd.DataFrame([
            {"Category": cat, "Amount": f"${amt:.2f}"}
            for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        ])
        st.dataframe(df_categories, use_container_width=True, hide_index=True)
        
        # Display as chart
        chart_data = {cat: amt for cat, amt in category_totals.items()}
        st.bar_chart(chart_data, use_container_width=True)
else:
    st.info("📭 No expenses found. Start by adding one in the sidebar!")

# Footer
st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption(f"🔗 API: {API_URL}")
with footer_col2:
    st.caption("✨ Built with Streamlit")
with footer_col3:
    st.caption("v1.0 • Expense Tracker")
