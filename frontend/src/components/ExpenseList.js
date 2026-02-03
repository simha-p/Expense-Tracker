import React from 'react';

function ExpenseList({ expenses }) {
  if (!expenses || expenses.length === 0) {
    return (
      <div className="empty-state">
        <p>📭 No expenses found. Start adding expenses to track your spending!</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getCategoryLabel = (category) => {
    const labels = {
      'food': 'Food',
      'transport': 'Transport',
      'entertainment': 'Entertainment',
      'utilities': 'Utilities',
      'shopping': 'Shopping',
      'health': 'Health',
      'other': 'Other'
    };
    return labels[category] || category;
  };

  return (
    <div className="expenses-list">
      <table className="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Description</th>
            <th style={{ textAlign: 'right' }}>Amount</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense) => (
            <tr key={expense.id}>
              <td className="date">{formatDate(expense.date)}</td>
              <td>
                <span className="category">{getCategoryLabel(expense.category)}</span>
              </td>
              <td>{expense.description}</td>
              <td style={{ textAlign: 'right' }}>
                <span className="amount">₹{parseFloat(expense.amount).toFixed(2)}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ExpenseList;
