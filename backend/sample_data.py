#!/usr/bin/env python
"""
Script to populate the database with sample expense data.
Run with: python manage.py shell < sample_data.py
"""

from decimal import Decimal
from datetime import date, timedelta
from expenses.models import Expense

# Clear existing expenses (optional)
# Expense.objects.all().delete()

today = date.today()

sample_expenses = [
    {
        'amount': Decimal('250.50'),
        'category': 'food',
        'description': 'Groceries from Super Mart',
        'date': today - timedelta(days=5)
    },
    {
        'amount': Decimal('50.00'),
        'category': 'transport',
        'description': 'Uber to office',
        'date': today - timedelta(days=4)
    },
    {
        'amount': Decimal('800.00'),
        'category': 'utilities',
        'description': 'Monthly electricity bill',
        'date': today - timedelta(days=3)
    },
    {
        'amount': Decimal('150.00'),
        'category': 'entertainment',
        'description': 'Movie tickets and popcorn',
        'date': today - timedelta(days=3)
    },
    {
        'amount': Decimal('200.00'),
        'category': 'shopping',
        'description': 'New shirt and shoes',
        'date': today - timedelta(days=2)
    },
    {
        'amount': Decimal('75.00'),
        'category': 'food',
        'description': 'Lunch at restaurant',
        'date': today - timedelta(days=2)
    },
    {
        'amount': Decimal('100.00'),
        'category': 'health',
        'description': 'Pharmacy - medicines',
        'date': today - timedelta(days=1)
    },
    {
        'amount': Decimal('30.00'),
        'category': 'transport',
        'description': 'Bike taxi',
        'date': today - timedelta(days=1)
    },
    {
        'amount': Decimal('500.00'),
        'category': 'other',
        'description': 'Haircut and salon',
        'date': today
    },
    {
        'amount': Decimal('120.00'),
        'category': 'food',
        'description': 'Coffee and snacks',
        'date': today
    },
]

print("Creating sample expenses...")
for exp_data in sample_expenses:
    expense, created = Expense.objects.get_or_create(
        description=exp_data['description'],
        date=exp_data['date'],
        defaults={
            'amount': exp_data['amount'],
            'category': exp_data['category']
        }
    )
    if created:
        print(f"✓ Created: {exp_data['category']}: ₹{exp_data['amount']} - {exp_data['description']}")
    else:
        print(f"✗ Already exists: {exp_data['description']}")

print("\nDone! Sample data loaded successfully.")
print(f"Total expenses: {Expense.objects.count()}")
