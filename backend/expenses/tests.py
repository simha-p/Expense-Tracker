"""
Tests for the expenses app.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import date
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from .models import Expense


class ExpenseModelTest(TestCase):
    """Test the Expense model."""
    
    def setUp(self):
        self.expense = Expense.objects.create(
            amount=Decimal('150.50'),
            category='food',
            description='Lunch',
            date=date(2024, 2, 1)
        )
    
    def test_expense_creation(self):
        """Test that an expense can be created."""
        self.assertEqual(self.expense.amount, Decimal('150.50'))
        self.assertEqual(self.expense.category, 'food')
        self.assertEqual(self.expense.description, 'Lunch')
    
    def test_expense_string_representation(self):
        """Test the string representation of an expense."""
        expected_str = "food: ₹150.50 - Lunch"
        self.assertEqual(str(self.expense), expected_str)
    
    def test_idempotency_key_unique(self):
        """Test that idempotency keys are unique."""
        expense1 = Expense.objects.create(
            amount=Decimal('100'),
            category='food',
            description='Test',
            date=date(2024, 2, 1),
            idempotency_key='unique-key-1'
        )
        
        with self.assertRaises(Exception):
            Expense.objects.create(
                amount=Decimal('200'),
                category='food',
                description='Test 2',
                date=date(2024, 2, 1),
                idempotency_key='unique-key-1'
            )


class ExpenseAPITest(TestCase):
    """Test the Expense API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test expenses
        Expense.objects.create(
            amount=Decimal('150.50'),
            category='food',
            description='Lunch',
            date=date(2024, 2, 1)
        )
        
        Expense.objects.create(
            amount=Decimal('50.00'),
            category='transport',
            description='Taxi',
            date=date(2024, 2, 2)
        )
    
    def test_list_expenses(self):
        """Test that expenses can be listed."""
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_by_category(self):
        """Test filtering expenses by category."""
        response = self.client.get('/api/expenses/?category=food')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category'], 'food')
    
    def test_sort_by_date_desc(self):
        """Test sorting expenses by date descending (newest first)."""
        response = self.client.get('/api/expenses/?sort=date_desc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['date'], '2024-02-02')  # Newest first
    
    def test_create_expense(self):
        """Test creating a new expense."""
        data = {
            'amount': '250.00',
            'category': 'food',
            'description': 'Dinner',
            'date': '2024-02-03'
        }
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], '250.00')
    
    def test_idempotency(self):
        """Test that idempotency keys prevent duplicates."""
        data = {
            'amount': '300.00',
            'category': 'food',
            'description': 'Breakfast',
            'date': '2024-02-04'
        }
        
        # First request
        response1 = self.client.post(
            '/api/expenses/',
            data,
            HTTP_IDEMPOTENCY_KEY='test-key-1'
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        expense_id_1 = response1.data['id']
        
        # Second request with same idempotency key
        response2 = self.client.post(
            '/api/expenses/',
            data,
            HTTP_IDEMPOTENCY_KEY='test-key-1'
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        expense_id_2 = response2.data['id']
        
        # Should return the same expense
        self.assertEqual(expense_id_1, expense_id_2)
        
        # Should only have one expense with this description
        expenses = Expense.objects.filter(description='Breakfast')
        self.assertEqual(expenses.count(), 1)
    
    def test_total_endpoint(self):
        """Test the total endpoint."""
        response = self.client.get('/api/expenses/total/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertEqual(float(response.data['total']), 200.50)
    
    def test_categories_endpoint(self):
        """Test the categories endpoint."""
        response = self.client.get('/api/expenses/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]['value'], 'food')
    
    def test_validation_negative_amount(self):
        """Test that negative amounts are rejected."""
        data = {
            'amount': '-100',
            'category': 'food',
            'description': 'Test',
            'date': '2024-02-01'
        }
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_validation_empty_description(self):
        """Test that empty description is rejected."""
        data = {
            'amount': '100',
            'category': 'food',
            'description': '',
            'date': '2024-02-01'
        }
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
