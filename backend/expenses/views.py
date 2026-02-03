"""
Views for the expenses app.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Sum
from django.utils.decorators import method_decorator
from django.views.decorators.http import condition
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for Expense CRUD operations with idempotency support."""
    
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    http_method_names = ['get', 'post', 'head', 'options']
    
    def get_queryset(self):
        """
        Filter and sort expenses based on query parameters.
        Supports:
        - category: filter by category
        - sort=date_desc: sort by date (newest first)
        """
        queryset = Expense.objects.all()
        
        # Filter by category if provided
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        
        # Sort by date (newest first) by default, can be modified by sort parameter
        sort_param = self.request.query_params.get('sort', 'date_desc')
        if sort_param == 'date_asc':
            queryset = queryset.order_by('date', 'created_at')
        else:  # Default: date_desc
            queryset = queryset.order_by('-date', '-created_at')
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Create a new expense with idempotency support.
        Client can provide 'Idempotency-Key' header to ensure duplicate requests
        return the same expense.
        """
        idempotency_key = request.headers.get('Idempotency-Key')
        
        # If idempotency key is provided, check if this request was already processed
        if idempotency_key:
            try:
                existing_expense = Expense.objects.get(idempotency_key=idempotency_key)
                serializer = self.get_serializer(existing_expense)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                    headers={'X-Idempotency': 'True'}
                )
            except Expense.DoesNotExist:
                pass
        
        # Create new expense
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save with idempotency key if provided
        if idempotency_key:
            serializer.validated_data['idempotency_key'] = idempotency_key
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if idempotency_key:
            headers['X-Idempotency'] = 'False'
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=False, methods=['get'])
    def total(self, request):
        """Get the total sum of expenses in the current filtered view."""
        queryset = self.get_queryset()
        total = queryset.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        return Response({
            'total': str(total),
            'currency': '₹',
            'count': queryset.count()
        })
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get available categories."""
        categories = [{'value': value, 'label': label} 
                     for value, label in Expense.CATEGORY_CHOICES]
        return Response(categories)
