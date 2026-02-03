import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import './index.css';
import ExpenseForm from './components/ExpenseForm';
import ExpenseList from './components/ExpenseList';
import Alert from './components/Alert';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [filters, setFilters] = useState({
    category: 'all',
    sort: 'date_desc'
  });
  const [categories, setCategories] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const abortControllerRef = useRef(null);

  // Fetch categories on mount
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get(`${API_BASE}/expenses/categories/`);
        setCategories(response.data);
      } catch (err) {
        console.error('Failed to fetch categories:', err);
      }
    };
    fetchCategories();
  }, []);

  // Fetch expenses when filters change
  useEffect(() => {
    fetchExpenses();
  }, [filters]);

  const fetchExpenses = useCallback(async () => {
    // Cancel previous request if still pending
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams();
      if (filters.category !== 'all') {
        params.append('category', filters.category);
      }
      params.append('sort', filters.sort);

      const response = await axios.get(`${API_BASE}/expenses/`, {
        params,
        signal: abortControllerRef.current.signal
      });
      
      setExpenses(response.data.results || response.data);
      
      // Fetch total
      const totalResponse = await axios.get(`${API_BASE}/expenses/total/`, {
        params,
        signal: abortControllerRef.current.signal
      });
      setTotal(parseFloat(totalResponse.data.total));
      setTotalCount(totalResponse.data.count);
    } catch (err) {
      if (err.name !== 'CanceledError') {
        setError('Failed to load expenses. Please try again.');
        console.error('Error fetching expenses:', err);
      }
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const handleAddExpense = async (expenseData) => {
    setError(null);
    setSuccess(null);

    try {
      // Generate idempotency key to handle retries
      const idempotencyKey = `expense-${Date.now()}-${Math.random()}`;
      
      const response = await axios.post(`${API_BASE}/expenses/`, expenseData, {
        headers: {
          'Idempotency-Key': idempotencyKey
        }
      });

      setSuccess('Expense added successfully!');
      
      // Refresh the list
      await fetchExpenses();

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
      
      return true;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.amount?.[0] ||
                          err.response?.data?.description?.[0] ||
                          err.response?.data?.date?.[0] ||
                          'Failed to add expense. Please try again.';
      setError(errorMessage);
      console.error('Error adding expense:', err);
      return false;
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1>💰 Expense Tracker</h1>
          <p>Track and manage your personal expenses</p>
        </div>
      </header>

      <div className="container">
        {error && <Alert type="error" message={error} onClose={() => setError(null)} />}
        {success && <Alert type="success" message={success} onClose={() => setSuccess(null)} />}

        <div className="content">
          <div className="card">
            <ExpenseForm onSubmit={handleAddExpense} />
          </div>

          <div className="card">
            <h2>Expenses</h2>
            
            <div className="filters">
              <select
                name="category"
                value={filters.category}
                onChange={handleFilterChange}
              >
                <option value="all">All Categories</option>
                {categories.map(cat => (
                  <option key={cat.value} value={cat.value}>
                    {cat.label}
                  </option>
                ))}
              </select>

              <select
                name="sort"
                value={filters.sort}
                onChange={handleFilterChange}
              >
                <option value="date_desc">Newest First</option>
                <option value="date_asc">Oldest First</option>
              </select>
            </div>

            <div className="summary">
              <div className="summary-row">
                <span className="summary-label">Total Expenses:</span>
                <span className="summary-value">₹{total.toFixed(2)}</span>
              </div>
              <div className="summary-row">
                <span className="summary-label">Count:</span>
                <span>{totalCount}</span>
              </div>
            </div>

            {loading ? (
              <div className="loading">
                <div className="spinner"></div>
                <p>Loading expenses...</p>
              </div>
            ) : (
              <ExpenseList expenses={expenses} />
            )}
          </div>
        </div>
      </div>

      <footer className="footer">
        <p>© 2024 Personal Expense Tracker | Built with Django & React</p>
      </footer>
    </div>
  );
}

export default App;
