# Development Guidelines

Guidelines for contributing to and maintaining the Expense Tracker project.

## Code Style

### Python (Backend)

Follow PEP 8:
```bash
pip install black flake8
black backend/
flake8 backend/ --max-line-length=100
```

Example:
```python
# Good
def calculate_total(expenses):
    """Calculate sum of all expenses."""
    return sum(e.amount for e in expenses)

# Bad
def calc_tot(exp):
    return sum([e.amount for e in exp])
```

### JavaScript/React (Frontend)

Follow Standard JS / Airbnb style:
```bash
npm install --save-dev eslint prettier
npx eslint src/
npx prettier --write src/
```

Example:
```jsx
// Good
function ExpenseList({ expenses }) {
  return (
    <ul>
      {expenses.map((expense) => (
        <li key={expense.id}>{expense.description}</li>
      ))}
    </ul>
  );
}

// Bad
function ExpenseList({expenses}){return<ul>{expenses.map(e=><li key={e.id}>{e.description}</li>)}</ul>}
```

## Testing

### Backend Testing

```bash
cd backend
python manage.py test expenses
python manage.py test --verbosity=2
```

Write tests in `expenses/tests.py`:
```python
def test_expense_creation(self):
    expense = Expense.objects.create(
        amount=Decimal('100'),
        category='food',
        description='Test',
        date=date.today()
    )
    self.assertEqual(expense.amount, Decimal('100'))
```

### Frontend Testing

Create tests in `src/components/ComponentName.test.js`:
```bash
npm test
```

Example:
```jsx
import { render, screen } from '@testing-library/react';
import ExpenseForm from './ExpenseForm';

test('renders form fields', () => {
  render(<ExpenseForm onSubmit={jest.fn()} />);
  expect(screen.getByLabelText(/amount/i)).toBeInTheDocument();
});
```

## Git Workflow

### Branch Naming
```
feature/add-authentication
bugfix/fix-cors-error
docs/update-readme
refactor/clean-up-models
```

### Commit Messages
```
Good: "Add idempotency key support for expense creation"
Bad: "update"

Good: "Fix: Prevent negative amounts in form validation"
Bad: "Fix stuff"

Good: "Docs: Update deployment guide with Railway instructions"
Bad: "Doc changes"
```

### Pull Request Process
1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit
3. Push: `git push origin feature/my-feature`
4. Create PR with description
5. Request review
6. Make requested changes
7. Merge when approved

## Documentation

### Docstrings (Python)
```python
def create_expense(amount, category, description, date):
    """
    Create a new expense entry.
    
    Args:
        amount (Decimal): Expense amount (must be > 0)
        category (str): One of: food, transport, entertainment, etc.
        description (str): What the expense was for
        date (date): Date of the expense
    
    Returns:
        Expense: The created expense object
    
    Raises:
        ValueError: If amount is not positive
        ValidationError: If category not recognized
    """
    if amount <= 0:
        raise ValueError("Amount must be positive")
    # Implementation
```

### Comments (JavaScript)
```javascript
// Good: explains WHY
const idempotencyKey = `${Date.now()}-${Math.random()}`;  // Unique per request to prevent duplicates

// Bad: explains WHAT (code already shows this)
const idempotencyKey = `${Date.now()}-${Math.random()}`;  // Create idempotency key
```

### README Sections
- Feature list (what it does)
- Tech stack (versions)
- Installation (step-by-step)
- Usage (examples)
- API reference (endpoints)
- Deployment (options)
- Contributing (how to help)

## Performance Guidelines

### Backend
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for reverse relations
- Add database indexes for frequently filtered fields
- Cache expensive computations
- Limit query results with pagination

Example:
```python
# Bad: N+1 queries
expenses = Expense.objects.all()
for e in expenses:
    print(e.category)  # Each iteration queries database

# Good: Single query
expenses = Expense.objects.select_related('category').all()
```

### Frontend
- Lazy load components: `React.lazy()`
- Memoize expensive computations: `useMemo()`
- Avoid inline functions in render
- Use `useCallback()` for stable function references
- Cancel in-flight requests when component unmounts

Example:
```jsx
// Bad: Refetches on every render
const [data, setData] = useState(null);
useEffect(() => {
  fetch('/api/expenses').then(r => setData(r));  // No dependency array
});

// Good: Fetches once on mount
useEffect(() => {
  fetch('/api/expenses').then(r => setData(r));
}, []);  // Empty dependency array
```

## Security Best Practices

### Input Validation
- **Backend**: Always validate in serializers and views
- **Frontend**: Validate for UX, never trust client-side validation
- **Database**: Use constraints (UNIQUE, NOT NULL, CHECK)

### Authentication
- Never store passwords in plaintext
- Use Django's `make_password()` and `check_password()`
- Implement token-based auth (JWT recommended)
- Always use HTTPS in production

### CORS & CSRF
- Whitelist specific domains, not '*'
- Enable CSRF protection
- Use secure cookies (SECURE_COOKIE_SECURE)
- Implement SameSite attribute

### Secrets Management
```python
# Bad: Hardcoded secrets
SECRET_KEY = 'abc123'
DATABASE_PASSWORD = 'password123'

# Good: Environment variables
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
```

## Common Patterns

### Adding a New Feature

1. **Backend**:
   - Add model field if needed
   - Create migration: `python manage.py makemigrations`
   - Update serializer for validation
   - Add/update views
   - Write tests

2. **Frontend**:
   - Create component
   - Add form field if needed
   - Make API call
   - Handle loading/error states
   - Test user interactions

3. **Integration**:
   - Test end-to-end
   - Update documentation
   - Create PR with description

### Debugging

**Backend**:
```python
# Add to views.py
print("DEBUG:", variable_name)

# Or use pdb
import pdb; pdb.set_trace()

# Or use Django shell
python manage.py shell
>>> from expenses.models import Expense
>>> Expense.objects.all().values()
```

**Frontend**:
```javascript
// Browser console (F12)
console.log("DEBUG:", variableName);
console.error("ERROR:", error);

// React DevTools: Install extension in Chrome
// Network tab: Check API requests and responses
```

## Database Migrations

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Custom Migrations
```bash
python manage.py makemigrations expenses --name=add_tags --empty
```

Edit the generated file:
```python
from django.db import migrations, models

class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='expense',
            name='tags',
            field=models.CharField(max_length=255, default=''),
        ),
    ]
```

### Reversing Migrations (Development Only)
```bash
python manage.py migrate expenses 0002  # Go back to 0002
```

## API Versioning

Current version: v1 (implied)

Future versions:
```
/api/v1/expenses/     # Current
/api/v2/expenses/     # Future changes
```

Update `urls.py`:
```python
urlpatterns = [
    path('v1/', include('expenses.urls')),
    path('v2/', include('expenses.v2.urls')),  # Future
]
```

## Logging

### Backend
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Expense created", extra={'expense_id': expense.id})
logger.error("Failed to create expense", exc_info=True)
```

### Frontend
```javascript
console.log('Expenses loaded:', expenses);
console.warn('API slow response:', responseTime);
console.error('Failed to load:', error.message);
```

## Release Checklist

Before releasing to production:

- [ ] All tests pass: `python manage.py test`, `npm test`
- [ ] Linting passes: `flake8`, `prettier`
- [ ] No secrets in code
- [ ] Database migrations run successfully
- [ ] Frontend builds without errors: `npm run build`
- [ ] README updated with new features
- [ ] Changelog updated
- [ ] Version bumped (MAJOR.MINOR.PATCH)
- [ ] All PR reviews approved
- [ ] Deployment documentation accurate
- [ ] Performance acceptable
- [ ] Security review passed

## Useful Commands

### Backend
```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Make migrations
python manage.py makemigrations

# Run shell
python manage.py shell

# Load sample data
python manage.py shell < sample_data.py

# Run tests
python manage.py test

# Check project
python manage.py check

# Collect static files
python manage.py collectstatic
```

### Frontend
```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Eject configuration (not recommended)
npm eject
```

### Both
```bash
# Git workflow
git status
git add .
git commit -m "Message"
git push origin branch-name
git pull origin main

# Virtual environment (backend)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
deactivate
```

## Architecture Decisions

### Why SQLite for Development?
- Zero setup, works immediately
- Full SQL compatibility
- Sufficient for small datasets
- Easy migration to PostgreSQL

### Why DRF ViewSets?
- Auto-generates standard CRUD endpoints
- Consistent API structure
- Built-in filtering, pagination, serialization
- Minimal boilerplate

### Why React Hooks?
- Simpler than class components
- Better code organization
- Easier to test
- Modern React standard

### Why Idempotency Keys?
- Prevents duplicate expenses on network retry
- Essential for financial correctness
- Follows API best practices
- Client-controlled uniqueness

## Future Improvements

### Priority 1 (Core Features)
- [ ] User authentication (JWT)
- [ ] Per-user expenses
- [ ] Edit/delete expenses

### Priority 2 (Enhanced Features)
- [ ] Budget limits and alerts
- [ ] Export to CSV
- [ ] Recurring expenses
- [ ] Receipt upload

### Priority 3 (Advanced)
- [ ] Charts and analytics
- [ ] Mobile app (React Native)
- [ ] Bank integration
- [ ] OCR for receipts
- [ ] Multi-currency support
- [ ] Offline mode

## Resources

- **Django**: https://docs.djangoproject.com/
- **DRF**: https://www.django-rest-framework.org/
- **React**: https://react.dev/
- **Python PEP 8**: https://pep8.org/
- **Web Security**: https://owasp.org/
- **SQL**: https://www.sqlite.org/

---

Happy coding! 🚀
