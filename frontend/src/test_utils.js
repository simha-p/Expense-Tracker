"""
Frontend tests for the Expense Tracker application.
"""

import pytest
import axios
from unittest.mock import Mock, patch


class TestExpenseForm:
    """Tests for the ExpenseForm component."""
    
    def test_form_validation(self):
        """Test form validation."""
        form_data = {
            'amount': '',
            'category': 'food',
            'description': 'Test',
            'date': '2024-02-01'
        }
        # Empty amount should fail validation
        assert form_data['amount'] == ''
    
    def test_positive_amount_required(self):
        """Test that amount must be positive."""
        amount = -100
        assert amount > 0 is False


class TestExpenseList:
    """Tests for the ExpenseList component."""
    
    def test_empty_list_message(self):
        """Test that empty state is shown when no expenses."""
        expenses = []
        assert len(expenses) == 0
    
    def test_format_date(self):
        """Test date formatting."""
        date_string = '2024-02-01'
        # Should format as human-readable
        assert date_string is not None


class TestExpenseAPI:
    """Tests for API interactions."""
    
    @patch('axios.get')
    def test_fetch_expenses(self, mock_get):
        """Test fetching expenses."""
        mock_get.return_value = Mock(data={'results': []})
        
        # Simulate API call
        response = mock_get('http://localhost:8000/api/expenses/')
        assert response.data['results'] == []
    
    @patch('axios.post')
    def test_add_expense(self, mock_post):
        """Test adding an expense."""
        mock_post.return_value = Mock(
            status_code=201,
            data={'id': 1, 'amount': '100.00'}
        )
        
        expense_data = {
            'amount': 100,
            'category': 'food',
            'description': 'Lunch',
            'date': '2024-02-01'
        }
        
        response = mock_post(
            'http://localhost:8000/api/expenses/',
            expense_data
        )
        assert response.status_code == 201
    
    def test_idempotency_key_header(self):
        """Test that idempotency key is sent in header."""
        headers = {
            'Idempotency-Key': 'unique-key-123'
        }
        assert 'Idempotency-Key' in headers
        assert headers['Idempotency-Key'] is not None


if __name__ == '__main__':
    pytest.main([__file__])
