# YatraAI Django Project Setup Guide

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- PostgreSQL 12+ (optional, SQLite works for development)
- Git

## 🚀 Step-by-Step Setup

### 1. Clone and Navigate to Project

```bash
cd /path/to/YatraAI
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` file with your settings:
- Generate a SECRET_KEY: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Add your OpenAI API key
- Configure database if using PostgreSQL

### 5. Create Logs Directory

```bash
mkdir logs
```

### 6. Initialize Database

```bash
# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
```

### 7. Load Sample Data (Optional)

```bash
# Will be created after you add sample fixtures
python manage.py loaddata fixtures/nepal_data.json
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Access the application:
- **Frontend**: http://localhost:8000/page/home/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/swagger/
- **API Root**: http://localhost:8000/api/

## 🗄️ Database Setup

### Option A: SQLite (Development)

Default configuration uses SQLite. No additional setup needed.

### Option B: PostgreSQL (Production)

1. Install PostgreSQL
2. Create database and user:

```sql
CREATE DATABASE yatrai_db;
CREATE USER yatrai_user WITH PASSWORD 'your_password';
ALTER ROLE yatrai_user SET client_encoding TO 'utf8';
ALTER ROLE yatrai_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE yatrai_user SET default_transaction_deferrable TO on;
ALTER ROLE yatrai_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE yatrai_db TO yatrai_user;
```

3. Update .env:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=yatrai_db
DB_USER=yatrai_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. Run migrations:

```bash
python manage.py migrate
```

## 📱 Adding Sample Data

Create fixtures for locations, tips, etc.:

```bash
# Create sample location
python manage.py shell
>>> from apps.locations.models import Location
>>> Location.objects.create(
...     name='Kathmandu',
...     region='kathmandu',
...     description='Capital city of Nepal',
...     altitude='mid',
...     latitude=27.7172,
...     longitude=85.3240,
...     best_time_visit='October-November',
...     weather_info='Cool and clear',
...     distance_from_kathmandu_km=0,
...     travel_time_hours=0,
...     primary_attraction='Pashupatinath Temple'
... )
>>> exit()
```

Or bulk import from JSON fixtures (see fixtures/ folder).

## 🔧 Common Commands

```bash
# Run tests
python manage.py test

# Create Django app
python manage.py startapp new_app

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic

# Clear cache
python manage.py clear_cache

# Django shell (interactive environment)
python manage.py shell

# Dump data to JSON
python manage.py dumpdata > backup.json

# Load data from JSON
python manage.py loaddata backup.json
```

## 🌐 API Endpoints Overview

### Locations API
- `GET /api/locations/` - List all locations
- `GET /api/locations/{id}/` - Get location details
- `GET /api/locations/by_region/?region=kathmandu` - Filter by region
- `GET /api/locations/popular/?limit=10` - Most popular locations
- `GET /api/hidden-gems/` - List hidden gems
- `GET /api/transport/` - List transport options

### Itinerary API
- `POST /api/itinerary/generate/` - Generate new itinerary
- `GET /api/itinerary/` - List itineraries
- `GET /api/itinerary/{id}/` - Get itinerary details
- `POST /api/itinerary/{id}/save/` - Save itinerary
- `GET /api/itinerary/recent/?limit=10` - Recent itineraries

### Tips API
- `GET /api/tips/budget/` - Budget tips
- `GET /api/tips/seasonal/` - Seasonal advice
- `GET /api/tips/experiences/` - Local experiences
- `GET /api/tips/budget/by_category/?category=food` - Tips by category

## 🔐 Security Checklist

Before production deployment:

- [ ] Update `SECRET_KEY` in .env
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL
- [ ] Enable CSRF protection
- [ ] Use strong database password
- [ ] Configure secure cookies
- [ ] Set up proper logging
- [ ] Use environment variables for all secrets
- [ ] Regular backups

Update `config/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'django'

```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### Database connection error

```bash
# Check PostgreSQL is running
# Update DATABASE settings in .env
python manage.py migrate
```

### OpenAI API errors

- Verify `OPENAI_API_KEY` is set correctly
- Check API quota and billing
- Ensure you're using a valid model name

### Static files not loading

```bash
python manage.py collectstatic --noinput
```

## 📖 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📞 Support

For issues, create a GitHub issue or contact: support@yatrai.com

## 📄 License

MIT License
