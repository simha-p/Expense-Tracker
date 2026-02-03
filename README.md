# Expense Tracker Application

A full-stack personal finance application for tracking and analyzing personal expenses with a Django REST API backend and React frontend.

## Features

### Core Features ✅
- ✅ **Create Expenses** - Add new expenses with amount, category, description, and date
- ✅ **View Expenses** - Display all expenses in a formatted table
- ✅ **Filter by Category** - Filter expenses by category (Food, Transport, Entertainment, etc.)
- ✅ **Sort by Date** - Sort expenses with newest first (default) or oldest first
- ✅ **Calculate Totals** - See total and count of visible expenses
- ✅ **Idempotent Operations** - Safe retries with duplicate prevention using Idempotency-Key headers
- ✅ **Form Validation** - Client and server-side validation
- ✅ **Error Handling** - Graceful error messages and loading states
- ✅ **Responsive Design** - Works on desktop and mobile devices

### Nice-to-Have Features ✅
- ✅ **Input Validation** - Prevents negative amounts, validates dates and descriptions
- ✅ **Loading States** - Shows loading spinner while fetching data
- ✅ **Error States** - Clear error messages for failed operations
- ✅ **Duplicate Prevention** - Idempotency keys prevent duplicate charges on network retries

## Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (development) - easily upgradeable to PostgreSQL
- **CORS**: django-cors-headers for cross-origin requests
- **Python**: 3.8+

### Frontend
- **Framework**: React 18.2.0
- **HTTP Client**: Axios 1.6.2
- **CSS**: Custom responsive CSS (no external UI framework)
- **Node**: 14+, npm 6+

## Project Structure

```
expense-tracker/
├── backend/
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   ├── expense_tracker/          # Django project folder
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Project URLs
│   │   ├── wsgi.py              # WSGI application
│   │   └── asgi.py              # ASGI application
│   └── expenses/                 # Main app
│       ├── models.py             # Expense model with idempotency support
│       ├── views.py              # API views with filtering/sorting
│       ├── serializers.py        # DRF serializers with validation
│       ├── urls.py               # App URLs
│       ├── admin.py              # Django admin
│       └── migrations/           # Database migrations
├── frontend/
│   ├── package.json             # NPM dependencies
│   ├── public/
│   │   └── index.html           # HTML entry point
│   └── src/
│       ├── index.js             # React entry point
│       ├── index.css            # Global styles
│       ├── App.js               # Main component
│       └── components/
│           ├── ExpenseForm.js   # Form component
│           ├── ExpenseList.js   # List component
│           └── Alert.js         # Alert component
└── README.md                     # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm 6+
- Git

### Backend Setup

1. **Clone/Navigate to the repository:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for Django admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/api/`

### Frontend Setup

1. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   The app will open at `http://localhost:3000`

4. **Build for production:**
   ```bash
   npm run build
   ```

## API Endpoints

### Create Expense
```http
POST /api/expenses/
Content-Type: application/json
Idempotency-Key: unique-request-identifier

{
  "amount": 150.50,
  "category": "food",
  "description": "Lunch at restaurant",
  "date": "2024-02-01"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "amount": "150.50",
  "category": "food",
  "description": "Lunch at restaurant",
  "date": "2024-02-01",
  "created_at": "2024-02-01T10:30:00Z"
}
```

### List Expenses
```http
GET /api/expenses/?category=food&sort=date_desc
```

**Query Parameters:**
- `category` (optional): Filter by category (food, transport, entertainment, utilities, shopping, health, other, all)
- `sort` (optional): Sort order - `date_desc` (newest first, default) or `date_asc` (oldest first)

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "amount": "150.50",
      "category": "food",
      "description": "Lunch",
      "date": "2024-02-01",
      "created_at": "2024-02-01T10:30:00Z"
    }
  ]
}
```

### Get Total
```http
GET /api/expenses/total/?category=food
```

**Response:**
```json
{
  "total": "150.50",
  "currency": "₹",
  "count": 1
}
```

### Get Categories
```http
GET /api/expenses/categories/
```

**Response:**
```json
[
  {"value": "food", "label": "Food"},
  {"value": "transport", "label": "Transport"},
  ...
]
```

## Key Design Decisions

### 1. **Idempotency for Duplicate Prevention**
- **Decision**: Implemented idempotency using `Idempotency-Key` header and database unique constraint
- **Rationale**: In real-world conditions, network issues or user retries can cause duplicate requests. Without idempotency, multiple identical submissions would create duplicate expenses. This is especially important for financial applications.
- **Implementation**: The `Idempotency-Key` is stored in the database; the backend returns the same expense if the key is seen again.

### 2. **Decimal Fields for Money**
- **Decision**: Used `DecimalField` with `max_digits=10, decimal_places=2`
- **Rationale**: Floating-point arithmetic can lose precision. Decimals ensure accurate money handling. The schema supports up to ₹99,999,999.99.

### 3. **SQLite for Development, Upgradeable to Production**
- **Decision**: SQLite for simplicity; configuration supports easy migration to PostgreSQL
- **Rationale**: SQLite works well for prototyping and small deployments. For production with multiple concurrent users, PostgreSQL can be configured in `settings.py`.

### 4. **Client-Side and Server-Side Validation**
- **Decision**: Validate on both frontend and backend
- **Rationale**: Frontend validation improves UX; server-side prevents invalid data entry and protects against API manipulation.

### 5. **Optimistic UI Updates with Request Cancellation**
- **Decision**: Refresh data after successful submission; cancel in-flight requests on filter changes
- **Rationale**: Ensures data consistency and prevents race conditions.

### 6. **RESTful API Structure**
- **Decision**: Used Django REST Framework with viewsets and standard HTTP methods
- **Rationale**: Clear, predictable API design. Standard HTTP semantics (GET, POST, status codes) make it easy to test and maintain.

### 7. **Category Pre-defined, Not User-Created**
- **Decision**: Hard-coded categories (Food, Transport, etc.) fetched via API
- **Rationale**: Simpler UX, consistent filtering, no database constraints to manage user categories.

## Trade-offs & Intentional Limitations

### Trade-offs Made
1. **No Authentication/Authorization** - This is a personal expense tracker demo. In production, add Django authentication and JWT tokens.
2. **No Edit/Delete Operations** - Focused on core features. Can be added with soft deletes for audit trails.
3. **In-Memory Pagination** - Simple pagination using DRF defaults. For large datasets, implement cursor-based pagination.
4. **No Caching Layer** - Added Redis caching for GET requests would improve performance.
5. **Minimal CSS Framework** - Custom CSS instead of Bootstrap for lighter footprint. Trade-off: more CSS code to maintain.

### Not Implemented (Out of Scope)
- User authentication and per-user expenses
- Bulk import/export (CSV)
- Charts and analytics
- Email/SMS notifications
- Mobile app (web-only)
- Real database backups/recovery
- Multi-currency support

### Why These Trade-offs?
Given the timebox constraint and focus on correctness over features:
- **Idempotency** was prioritized because it directly addresses real-world network issues
- **Data validation** was emphasized for financial correctness
- **Testing and error handling** over feature count
- **Code clarity and maintainability** over advanced optimizations

## Testing & Usage

### Manual Testing
1. Start both servers (backend on 8000, frontend on 3000)
2. Add an expense using the form
3. Try submitting twice quickly - should only create one expense
4. Refresh the page - data persists
5. Filter by category - works correctly
6. Sort by date - newest first by default

### Example Workflow
```
1. Open http://localhost:3000
2. Fill form:
   - Amount: 250
   - Category: Food
   - Description: Groceries
   - Date: 2024-02-01
3. Click "Add Expense"
4. See expense in table below
5. Change filter to "Food"
6. See updated total
7. Refresh page - expense still there
```

## Deployment

### Backend Deployment (Production)
```bash
# Use gunicorn
pip install gunicorn
gunicorn expense_tracker.wsgi:application --bind 0.0.0.0:8000

# Or use any WSGI server (AWS Elastic Beanstalk, Heroku, Railway, etc.)
```

**Environment Variables:**
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@host/db
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Frontend Deployment (Production)
```bash
npm run build
# Deploy the 'build' folder to:
# - Vercel, Netlify, GitHub Pages, AWS S3 + CloudFront, etc.
```

## Troubleshooting

### CORS Error
**Problem**: Frontend can't reach backend
**Solution**: 
- Ensure backend is running on `http://localhost:8000`
- Check `CORS_ALLOWED_ORIGINS` in `settings.py`
- Update `.env` file if using a different backend URL

### Port Already in Use
```bash
# Backend (8000)
python manage.py runserver 8001

# Frontend (3000)
PORT=3001 npm start
```

### Database Issues
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
```

## Performance Considerations

- **Database Indexes**: Indexed on `category` and `date` fields for fast filtering
- **Query Optimization**: Using `.only()` and `.select_related()` where applicable
- **Pagination**: Limited to 100 results per page by default
- **Request Cancellation**: Frontend cancels previous requests when filters change

## Security Notes

### Current (Development)
- Debug mode enabled
- CORS allows all origins
- No authentication

### For Production
1. Set `DEBUG=False` in settings
2. Use strong `SECRET_KEY`
3. Add user authentication and permission checks
4. Validate and sanitize all inputs
5. Use HTTPS only
6. Add rate limiting
7. Implement CSRF protection properly
8. Use environment variables for secrets
9. Add database encryption at rest
10. Implement audit logging for financial changes

## Future Enhancements

1. **User Accounts** - Multi-user support with per-user expenses
2. **Budget Alerts** - Notify when spending exceeds budget
3. **Reports** - Monthly/yearly summaries
4. **Recurring Expenses** - Auto-create monthly/weekly expenses
5. **Receipt Upload** - Attach photos of receipts
6. **Mobile App** - React Native version
7. **Offline Support** - Service workers + IndexedDB
8. **Analytics Dashboard** - Charts, trends, spending patterns
9. **Bank Integration** - Import transactions automatically
10. **Multi-Currency** - Support for different currencies

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include steps to reproduce for bugs

## Author

Built as a full-stack assignment demonstrating production-like quality with Django & React.

---

**Last Updated**: February 2024
**Python Version**: 3.8+
**Node Version**: 14+
**Status**: Production Ready (Core Features)
