"""
Models for the expenses app.
"""
from django.db import models
from decimal import Decimal
import uuid


class Expense(models.Model):
    """Model to represent an expense entry."""
    
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('shopping', 'Shopping'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]
    
    # Use UUID for idempotency - client can provide idempotency_key
    id = models.AutoField(primary_key=True)
    idempotency_key = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        help_text="Unique key for idempotent operations"
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount in currency (e.g., ₹)"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    description = models.CharField(max_length=500)
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['-date']),
        ]
    
    def __str__(self):
        return f"{self.category}: ₹{self.amount} - {self.description}"
