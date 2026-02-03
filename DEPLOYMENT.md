# Deployment Guide - Expense Tracker

This guide covers deploying the Expense Tracker application to production.

## Architecture Options

```
┌─────────────────┐
│   Frontend      │  (React SPA)
│ (Vercel/Netlify)│
└────────┬────────┘
         │ HTTPS
         │
┌────────▼────────┐
│   Backend API   │  (Django REST API)
│ (Heroku/Railway)│
└────────┬────────┘
         │
┌────────▼────────┐
│   Database      │  (PostgreSQL/SQLite)
│   (Managed)     │
└─────────────────┘
```

## Backend Deployment

### Option 1: Heroku (Easiest)

#### 1a. Prerequisites
- Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
- Heroku account: https://www.heroku.com/

#### 1b. Create Heroku App
```bash
heroku login
cd backend
heroku create expense-tracker-api
```

#### 1c. Add Gunicorn to requirements.txt
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 1d. Create Procfile
```bash
echo "web: gunicorn expense_tracker.wsgi" > Procfile
```

#### 1e. Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-super-secret-key-here
heroku config:set ALLOWED_HOSTS=expense-tracker-api.herokuapp.com
heroku config:set CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

#### 1f. Add Database
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### 1g. Deploy
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### 1h. View Logs
```bash
heroku logs --tail
```

### Option 2: Railway

#### 2a. Prerequisites
- Railway account: https://railway.app/
- GitHub account (for continuous deployment)

#### 2b. Push code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/expense-tracker.git
git push -u origin main
```

#### 2c. Connect to Railway
1. Go to https://railway.app/
2. Create new project
3. Connect GitHub repository
4. Select `backend` as root directory
5. Add PostgreSQL plugin
6. Set environment variables:
   - `DEBUG=False`
   - `SECRET_KEY=...`
   - `ALLOWED_HOSTS=yourdomain.com`
7. Deploy

### Option 3: AWS Elastic Beanstalk

#### 3a. Install EB CLI
```bash
pip install awsebcli
```

#### 3b. Initialize EB
```bash
cd backend
eb init -p python-3.11 expense-tracker
```

#### 3c. Create Environment
```bash
eb create production
```

#### 3d. Deploy
```bash
eb deploy
```

## Frontend Deployment

### Option 1: Vercel (Recommended for Next.js, but works with React)

#### 1a. Prerequisites
- Vercel account: https://vercel.com/
- GitHub account

#### 1b. Deploy
1. Push code to GitHub (if not already)
2. Go to https://vercel.com/new
3. Select your repository
4. Set `Root Directory` to `frontend`
5. Add Environment Variable:
   - `REACT_APP_API_URL=https://your-backend-domain.com/api`
6. Click "Deploy"

Vercel handles building and hosting automatically!

### Option 2: Netlify

#### 2a. Prerequisites
- Netlify account: https://netlify.com/
- GitHub account

#### 2b. Deploy
1. Go to https://app.netlify.com/
2. Click "New site from Git"
3. Connect GitHub
4. Select repository
5. Set build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `build`
6. Add environment variable:
   - `REACT_APP_API_URL=https://your-backend-domain.com/api`
7. Deploy

#### 2c. Add Redirect (for SPA routing)
Create `frontend/public/_redirects`:
```
/*  /index.html  200
```

### Option 3: GitHub Pages

#### 3a. Create GitHub Repository
- Create public repository: `expense-tracker`

#### 3b. Add Deploy Script
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy Frontend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
        working-directory: frontend
      - run: npm run build
        working-directory: frontend
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/build
```

#### 3c: Push to GitHub
```bash
git push origin main
```

### Option 4: AWS S3 + CloudFront

#### 4a. Create S3 Bucket
```bash
aws s3 mb s3://expense-tracker-frontend
aws s3 website s3://expense-tracker-frontend --index-document index.html
```

#### 4b. Upload Build
```bash
cd frontend
npm run build
aws s3 sync build/ s3://expense-tracker-frontend/
```

#### 4c: Create CloudFront Distribution
1. AWS CloudFront console
2. Create distribution with S3 origin
3. Set default root object to `index.html`
4. Configure error responses (404 → index.html)

## Docker Deployment

### Using Docker Compose (Recommended for small teams)

#### 1. Build Images
```bash
docker-compose build
```

#### 2. Run Locally
```bash
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API: http://localhost:8000/api/

### Push to Docker Hub

#### 1. Create Docker Hub Account
- https://hub.docker.com/

#### 2. Build and Push
```bash
docker build -f backend/Dockerfile -t yourname/expense-tracker-api:latest .
docker push yourname/expense-tracker-api:latest

docker build -f frontend/Dockerfile -t yourname/expense-tracker-frontend:latest .
docker push yourname/expense-tracker-frontend:latest
```

#### 3. Deploy on Any Docker Host
```bash
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=... \
  yourname/expense-tracker-api:latest

docker run -p 3000:3000 \
  -e REACT_APP_API_URL=https://api.yourdomain.com/api \
  yourname/expense-tracker-frontend:latest
```

## Database Configuration for Production

### Option 1: Heroku PostgreSQL (Managed)
```python
# settings.py - automatically configured by Heroku
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}
```

### Option 2: AWS RDS
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'expense_tracker',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'your-instance.c9akciq32.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}
```

### Option 3: AWS DynamoDB
Install: `pip install django-dynamodb-model`

### Running Migrations on Production
```bash
heroku run python manage.py migrate  # Heroku
eb setenv && eb deploy  # AWS EB
railway up  # Railway
```

## HTTPS & SSL

### Automatic (Recommended)
- Heroku, Vercel, Netlify: Automatic HTTPS
- GitHub Pages: Automatic HTTPS
- AWS CloudFront: Request certificate via ACM

### Manual
1. Get certificate: Let's Encrypt (certbot)
2. Install on web server (Nginx, Apache)
3. Configure Django: `SECURE_SSL_REDIRECT = True`

## Environment Variables for Production

Create `.env.production` or set via deployment platform:

```bash
# Backend
DEBUG=False
SECRET_KEY=your-very-secret-key-change-this
ALLOWED_HOSTS=api.expense-tracker.com,api.yourdomain.com
CORS_ALLOWED_ORIGINS=https://expense-tracker.com,https://yourdomain.com

# Database (if using external DB)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Frontend
REACT_APP_API_URL=https://api.expense-tracker.com/api
```

## Monitoring & Maintenance

### Application Monitoring
```bash
# Heroku
heroku logs -t  # Real-time logs
heroku ps       # Running dynos

# AWS
aws cloudwatch get-metric-statistics --namespace AWS/ECS

# Railway
railway logs
```

### Database Backups
```bash
# Heroku PostgreSQL
heroku pg:backups:capture
heroku pg:backups:download

# AWS RDS
aws rds create-db-snapshot --db-instance-identifier expense-tracker-db
```

### Performance Monitoring
- Add New Relic, DataDog, or Sentry for error tracking
- Monitor API response times
- Track database query performance

## Scaling

### Horizontal Scaling
```bash
# Heroku
heroku ps:scale web=2

# AWS EB
eb scale 3
```

### Vertical Scaling
- Increase dyno size (Heroku)
- Increase EC2 instance type (AWS)
- Increase Railway plan

### Database Optimization
- Add indexes (already done for category, date)
- Implement caching (Redis)
- Use read replicas for heavy traffic

## Security Checklist for Production

- [ ] Set `DEBUG=False`
- [ ] Change `SECRET_KEY` to strong random value
- [ ] Enable HTTPS/SSL
- [ ] Configure `SECURE_SSL_REDIRECT=True`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Configure CORS to specific domains only
- [ ] Use environment variables (no hardcoded secrets)
- [ ] Enable security headers:
  ```python
  SECURE_HSTS_SECONDS=31536000
  SECURE_HSTS_INCLUDE_SUBDOMAINS=True
  X_FRAME_OPTIONS='DENY'
  SECURE_CONTENT_SECURITY_POLICY={...}
  ```
- [ ] Set up rate limiting
- [ ] Add authentication and authorization
- [ ] Enable CSRF protection properly
- [ ] Use database backups
- [ ] Monitor for errors and performance

## Troubleshooting Deployment

### Backend won't start
1. Check logs: `heroku logs --tail`
2. Verify environment variables
3. Test migrations: `heroku run python manage.py showmigrations`
4. Check Python version compatibility

### CORS errors
1. Verify `CORS_ALLOWED_ORIGINS` includes frontend domain
2. Check if frontend is using correct API URL
3. Test with curl:
```bash
curl -H "Origin: https://yourdomain.com" \
  https://api.yourdomain.com/api/expenses/
```

### Database connection fails
1. Check DATABASE_URL format
2. Verify database credentials
3. Test connection: `python manage.py dbshell`
4. Check firewall/security groups allow connections

### Frontend not updating after deploy
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+F5 or Cmd+Shift+R)
3. Verify build completed successfully
4. Check network tab in DevTools

## Cost Estimation

| Service | Tier | Monthly Cost | Notes |
|---------|------|--------------|-------|
| Heroku | Hobby | $50-100 | Best for learning |
| Railway | Pro | $5-20 | Good value |
| Vercel | Hobby | Free | Frontend only |
| Netlify | Hobby | Free | Frontend only |
| AWS (t2.micro) | Free Tier | $0-20 | Limited free tier |

## Continuous Deployment

### GitHub Actions Pipeline
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: cd backend && pip install -r requirements.txt
      - run: cd backend && python manage.py test
      - run: cd backend && git push heroku main

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: cd frontend && npm install && npm test
      - run: npm run build
      - run: vercel --prod
```

## Next Steps After Deployment

1. Test production environment thoroughly
2. Set up monitoring and alerts
3. Create database backup schedule
4. Document deployment process
5. Train team on deployment
6. Set up CI/CD pipeline
7. Monitor costs
8. Plan scaling strategy

---

**Deployment Options Summary:**
- **Easiest**: Heroku + Vercel
- **Best Value**: Railway + Netlify
- **Most Control**: AWS + S3 + CloudFront
- **Best for Teams**: Docker + Kubernetes + RDS

Choose based on your budget, team expertise, and traffic expectations!
