"""
URL configuration for expense_tracker project.
"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('expenses.urls')),
]
