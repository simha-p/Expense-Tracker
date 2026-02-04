"""
URL configuration for expense_tracker project.
"""
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return JsonResponse({'status': 'ok', 'message': 'Expense Tracker API is running'})

urlpatterns = [
    path('', health_check, name='health_check'),
    path('api/', include('expenses.urls')),
]
