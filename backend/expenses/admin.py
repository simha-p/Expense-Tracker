"""
Admin configuration for the expenses app.
"""
from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'category', 'description', 'date', 'created_at')
    list_filter = ('category', 'date', 'created_at')
    search_fields = ('description', 'category')
    readonly_fields = ('created_at', 'updated_at', 'idempotency_key')
    fieldsets = (
        ('Expense Details', {
            'fields': ('amount', 'category', 'description', 'date')
        }),
        ('System Fields', {
            'fields': ('idempotency_key', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
