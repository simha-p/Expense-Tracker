"""
Serializers for the expenses app.
"""
from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model."""
    
    class Meta:
        model = Expense
        fields = [
            'id',
            'amount',
            'category',
            'description',
            'date',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_amount(self, value):
        """Ensure amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate_description(self, value):
        """Ensure description is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value.strip()
    
    def validate(self, data):
        """Validate the entire object."""
        if not data.get('date'):
            raise serializers.ValidationError({'date': 'Date is required.'})
        if not data.get('category'):
            raise serializers.ValidationError({'category': 'Category is required.'})
        return data
