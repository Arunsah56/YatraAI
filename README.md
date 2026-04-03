# 🌏 YatraAI - AI-Powered Tourism Itinerary Planner for Nepal

> *Yatra* (यात्रा) = Journey in Nepali

YatraAI is a production-ready web application that generates personalized travel itineraries for Nepal using AI, enriched with Nepal-specific local data. Built with modern web technologies and best practices.

## ✨ Features

- 🤖 **AI-Powered Generation** - OpenAI GPT integration for intelligent itinerary creation
- 🗺️ **Nepal-Specific Data** - Curated locations, hidden gems, seasonal tips, and local experiences
- 🎯 **Smart Personalization** - Filter by budget, duration, interests, and travel style
- 📱 **Responsive Design** - Mobile-first UI with beautiful gradients and smooth animations
- 🚀 **Modern REST API** - Django REST Framework with comprehensive documentation
- 💾 **Flexible Database** - PostgreSQL for production, SQLite for development
- ⚡ **Performance Optimized** - Caching, pagination, and async support
- 🔐 **Production Ready** - Security headers, CORS support, environment management
- 📊 **Admin Dashboard** - Django admin interface for data management
- 🎨 **Professional UI** - Tab navigation, day-by-day breakdown, rich formatting

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.2, Django REST Framework, Celery |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Database** | PostgreSQL (production), SQLite (development) |
| **AI** | OpenAI GPT API |
| **Hosting** | Gunicorn, Whitenoise, Environment-based config |
| **Development** | Black, Flake8, pytest |

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip and venv
- OpenAI API key (for AI features)
- PostgreSQL 12+ (optional, SQLite works for development)

### Installation (5 minutes)

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd YatraAI
   ```

2. **Set up Python virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Initialize database:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # Create admin user
   ```

6. **Load sample Nepal data (optional):**
   ```bash
   python manage.py loaddata fixtures/nepal_locations.json
   ```

7. **Start development server:**
   ```bash
   python manage.py runserver
   ```

   Visit `http://localhost:8000` in your browser

### 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
# For PostgreSQL:
# DATABASE_ENGINE=django.db.backends.postgresql
# DATABASE_NAME=yatraai
# DATABASE_USER=postgres
# DATABASE_PASSWORD=password
# DATABASE_HOST=localhost
# DATABASE_PORT=5432

# AI Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# App Settings
DEFAULT_BUDGET=moderate
DEFAULT_DURATION=7
```

## 📁 Project Structure

```
YatraAI/
├── manage.py                           # Django management script
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment template
├── db.sqlite3                         # Development database
│
├── config/                            # Project configuration
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # URL routing
│   ├── wsgi.py                       # WSGI configuration
│   └── asgi.py                       # ASGI configuration
│
├── apps/
│   ├── itinerary/                    # Core itinerary app
│   │   ├── models.py                # Itinerary ORM models
│   │   ├── views.py                 # API endpoints
│   │   ├── serializers.py           # DRF serializers
│   │   ├── services.py              # Business logic & AI integration
│   │   ├── urls.py                  # App URL routing
│   │   ├── admin.py                 # Admin configuration
│   │   └── migrations/              # Database migrations
│   │
│   ├── locations/                   # Nepal locations data
│   │   ├── models.py                # Location, Activity, Experience models
│   │   ├── views.py                 # Location API endpoints
│   │   ├── serializers.py           # Serializers for location data
│   │   ├── urls.py                  # Location URLs
│   │   ├── admin.py                 # Location admin
│   │   └── migrations/              # Database migrations
│   │
│   ├── api/                         # API version management
│   │   ├── urls.py                  # API URL routing
│   │   ├── views.py                 # Generic API views
│   │   └── permissions.py           # Custom permissions
│   │
│   └── common/                      # Shared utilities
│       ├── middleware.py            # Custom middleware
│       ├── utils.py                 # Helper functions
│       └── decorators.py            # Custom decorators
│
├── static/                          # Static files
│   ├── css/
│   │   └── style.css               # Main stylesheet (responsive design)
│   └── js/
│       ├── main.js                 # Main application logic
│       └── api.js                  # API communication layer
│
├── templates/                       # HTML templates
│   ├── base.html                   # Base template (navigation, footer)
│   ├── index.html                  # Home page with search form
│   ├── results.html                # Itinerary results display
│   └── explore.html                # Exploration page (tab views)
│
├── logs/                           # Application logs
│   └── app.log                     # Main application log
│
└── fixtures/                       # Sample data
    └── nepal_locations.json        # Nepal locations data
```

## 🔌 API Endpoints

### Generate Itinerary
```http
POST /api/v1/itineraries/generate/
Content-Type: application/json

{
  "destination": "Kathmandu",
  "duration": 7,
  "interests": ["culture", "nature", "adventure"],
  "budget": "moderate"
}

Response: 201 Created
{
  "id": "uuid",
  "destination": "Kathmandu",
  "duration": 7,
  "itinerary": [...],
  "tips": [...],
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Locations
```http
GET /api/v1/locations/?region=kathmandu&category=temple

Response: 200 OK
{
  "count": 25,
  "results": [
    {
      "id": "uuid",
      "name": "Pashupatinath Temple",
      "region": "kathmandu",
      "category": "temple",
      "description": "...",
      "rating": 4.8
    }
  ]
}
```

### Get Experiences
```http
GET /api/v1/experiences/?season=winter&activity_type=trekking

Response: 200 OK
{
  "count": 12,
  "results": [...]
}
```

## 🎯 Main Pages

### 🏠 Home Page (`/`)
- Beautiful hero section with gradient background
- Search form for itinerary generation
- Feature highlights
- Featured destinations

### 📋 Results Page (`/results/`)
- Generated itinerary display
- Day-by-day breakdown
- Practical tips section
- Budget breakdown
- Share and export options

### 🗺️ Explore Page (`/explore/`)
- Tabbed interface for discovery
- Hidden gems recommendations
- Seasonal experiences
- Local travel tips
- Photo gallery

## 🔐 Security Features

- ✅ CSRF protection
- ✅ SQL Injection prevention (ORM)
- ✅ XSS protection
- ✅ CORS security headers
- ✅ Environment-based secrets
- ✅ API key encryption
- ✅ Rate limiting ready

## 📊 Database Models

### Itinerary
```python
- destination (CharField)
- duration (IntegerField)
- budget (CharField)
- interests (JSONField)
- itinerary (JSONField)
- tips (JSONField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### Location
```python
- name (CharField)
- region (CharField)
- category (CharField)
- description (TextField)
- latitude/longitude (FloatField)
- rating (FloatField)
- image_url (URLField)
- best_season (CharField)
```

### Activity
```python
- name (CharField)
- description (TextField)
- category (CharField)
- difficulty (CharField)
- duration (CharField)
- location (ForeignKey)
- season (CharField)
```

## 🧪 Testing

Run the test suite:

```bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.itinerary

# Verbose output
python manage.py test --verbosity=2

# With coverage
pytest --cov=apps --cov-report=html --cov-report=term-missing
```

## 🐳 Docker Deployment

Build and run with Docker:

```bash
# Build image
docker build -t yatraai:latest .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  yatraai:latest

# With docker-compose
docker-compose up -d
```

## 🌐 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn

gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### Environment Configuration for Production

```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=generate-a-strong-random-key
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 📝 Code Quality Standards

- **Style Guide**: PEP 8 (via Black formatter)
- **Linting**: Flake8
- **Type Checking**: mypy ready
- **Formatting**: Run `black .` before commits
- **Pre-commit Hooks**: Use `pre-commit` to enforce standards

### Format Code Before Committing

```bash
# Format with black
black apps/ config/ static/ templates/

# Check with flake8
flake8 apps/ config/ --max-line-length=100

# Sort imports
isort apps/ config/
```

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'feat: add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Submit a pull request

### Commit Message Format

```
type(scope): description

feat(itinerary): add AI-powered location suggestions
fix(ui): resolve responsive layout on mobile
docs(readme): update installation instructions
style(css): improve button hover animations
refactor(api): optimize database queries
test(models): add Itinerary model tests
```

## 📚 Documentation

Additional documentation available in:

- [API Documentation](./API_DOCUMENTATION.md) - Detailed API reference
- [Frontend Setup](./FRONTEND_SETUP.md) - Frontend development guide
- [Project Summary](./PROJECT_SUMMARY.md) - High-level overview
- [Setup Guide](./SETUP_GUIDE.md) - Detailed installation steps
- [Quick Start](./QUICK_START.md) - Get running in 5 minutes

## 🎨 Design System

### Colors
- **Primary**: `#FF6B6B` (Coral)
- **Secondary**: `#4ECDC4` (Teal)
- **Dark**: `#2C3E50` (Dark Blue-Grey)
- **Light**: `#F7F9FC` (Off-White)
- **Accent**: `#FFE66D` (Golden)

### Typography
- **Heading Font**: Segoe UI, system sans-serif
- **Body Font**: Segoe UI, Tahoma, Verdana
- **Font Size**: 16px base (responsive scaling)

### Components
- Beautiful card layouts with hover effects
- Responsive grid system (mobile-first)
- Tab navigation interface
- Gradient backgrounds and animations
- Accessibility-focused design

## 🐛 Troubleshooting

### Common Issues

**Virtual environment not activating:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Port 8000 already in use:**
```bash
python manage.py runserver 8001
```

**Database migration errors:**
```bash
python manage.py migrate --fake-initial
```

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
```

## 📞 Support & Contact

- **Issues**: Create on GitHub Issues
- **Discussions**: Use GitHub Discussions
- **Email**: support@yatraai.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT API
- Django and DRF communities
- Nepal tourism board for inspiration

## 🗺️ Nepal Travel Resources

- [Nepal Tourism](https://www.welcomenepal.com/)
- [Kathmandu Valley](https://en.wikivoyage.org/wiki/Kathmandu_Valley)
- [Himalayan Regions](https://en.wikivoyage.org/wiki/Himalayas)

---

**Made with ❤️ for Nepal travelers everywhere**
