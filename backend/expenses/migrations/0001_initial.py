"""
Initial migration for expenses app.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idempotency_key', models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('food', 'Food'), ('transport', 'Transport'), ('entertainment', 'Entertainment'), ('utilities', 'Utilities'), ('shopping', 'Shopping'), ('health', 'Health'), ('other', 'Other')], default='other', max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='expense',
            index=models.Index(fields=['category'], name='expenses_ex_categor_idx'),
        ),
        migrations.AddIndex(
            model_name='expense',
            index=models.Index(fields=['-date'], name='expenses_ex_date_idx'),
        ),
    ]
