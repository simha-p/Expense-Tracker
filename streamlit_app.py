"""
Streamlit Expense Tracker App
Main entry point for Streamlit Cloud deployment
"""
import sys
from pathlib import Path

# Import the original streamlit app
if Path("frontend_streamlit.py").exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("frontend_streamlit", "frontend_streamlit.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["frontend_streamlit"] = module
    spec.loader.exec_module(module)
else:
    # Fallback - run the app directly
    exec(open("frontend_streamlit.py").read())
