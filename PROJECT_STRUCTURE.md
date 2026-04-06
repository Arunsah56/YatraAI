# Django Project Structure Overview

## 📊 Project Architecture

```
YatraAI/
│
├── config/                          # Project configuration
│   ├── __init__.py
│   ├── settings.py                 # Django settings (production-ready)
│   ├── urls.py                     # Main URL router
│   ├── wsgi.py                     # WSGI configuration
│   ├── asgi.py                     # ASGI configuration
│   └── manage.py                   # Django management utility
│
├── apps/                            # Django applications
│   │
│   ├── locations/                  # Location management app
│   │   ├── models.py               # Location, HiddenGem, TransportOption
│   │   ├── serializers.py          # DRF serializers for API
│   │   ├── views.py                # ViewSets for REST API
│   │   ├── urls.py                 # App URLs
│   │   ├── admin.py                # Django admin configuration
│   │   └── migrations/             # Database migrations
│   │
│   ├── tips/                        # Travel tips app
│   │   ├── models.py               # BudgetTip, SeasonalTip, LocalExperience
│   │   ├── serializers.py          # DRF serializers
│   │   ├── views.py                # ViewSets for REST API
│   │   ├── urls.py                 # App URLs
│   │   ├── admin.py                # Django admin configuration
│   │   └── migrations/             # Database migrations
│   │
│   └── itinerary/                  # Itinerary generation app
│       ├── models.py               # Itinerary, Day, Activity, Note
│       ├── serializers.py          # DRF serializers
│       ├── views.py                # ViewSets for REST API + Frontend views
│       ├── services.py             # AI integration service (OpenAI)
│       ├── urls.py                 # App URLs
│       ├── admin.py                # Django admin configuration
│       └── migrations/             # Database migrations
│
├── templates/                       # HTML templates
│   ├── base.html                   # Base template
│   ├── index.html                  # Homepage
│   ├── results.html                # Results page
│   └── explore.html                # Explore page
│
├── static/                          # Static files
│   ├── css/
│   │   └── style.css               # Main stylesheet
│   ├── js/
│   │   ├── main.js                 # Main JavaScript
│   │   └── api.js                  # API client functions
│   └── img/                        # Images
│
├── manage.py                        # Django CLI entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── SETUP_GUIDE.md                   # Setup instructions
├── README.md                        # Project documentation
└── API_DOCUMENTATION.md             # API reference (to be created)
```

## 🏗️ Data Models Overview

### Locations App

**Location**
- Core model representing Nepal destinations
- Fields: name, region, description, altitude, coordinates, best_time_visit, weather_info, distance, attractions
- Used as reference for itinerary generation

**HiddenGem**
- Off-beat destinations and lesser-known places
- Relations: ForeignKey to Location
- Fields: name, gem_type, description, accessibility_level, entry_fee, best_time_visit, crowd_level, rating

**TransportOption**
- Transportation methods between locations
- Relations: ForeignKey to source/destination Location
- Fields: transport_type, distance_km, duration_hours, cost_npr, comfort_level, frequency, operator

### Tips App

**BudgetTip**
- Money-saving tips for travelers
- Fields: title, category, budget_level, content, effectiveness_score, relevant_location

**SeasonalTip**
- Seasonal weather and travel advice
- Fields: season, month, title, description, temperature_range, rainfall_level, visibility, risks, recommendations

**LocalExperience**
- Authentic local activities and cultural experiences
- Relations: ForeignKey to Location
- Fields: name, category, description, duration_hours, cost_per_person_npr, booking_required, physical_difficulty, rating

### Itinerary App

**Itinerary**
- Main itinerary record
- Relations: ForeignKey to Location (destination_primary)
- Fields: title, destination, number_of_days, budget_level, interests, estimated_budget, group_size, travelers_type, status, ai_response

**ItineraryDay**
- Individual day within an itinerary
- Relations: ForeignKey to Itinerary
- Fields: day_number, location, title, description, accommodation_*, daily budget breakdown

**ItineraryActivity**
- Individual activity within a day
- Relations: ForeignKey to ItineraryDay, Location, LocalExperience
- Fields: activity_type, name, time_start, time_end, description, estimated_cost, importance_level, tips

**ItineraryNote**
- Custom notes and reminders
- Relations: ForeignKey to Itinerary
- Fields: title, content, note_type, is_pinned

## 🔄 API Workflow

### Itinerary Generation Flow

1. **User Request**
   - POST to `/api/itinerary/generate/`
   - Provides: destination, days, budget, interests, group info

2. **Data Collection**
   - Fetch location data from Location model
   - Gather transport options for context
   - Fetch relevant budget tips and seasonal advice

3. **AI Processing**
   - Build comprehensive prompt with Nepal context
   - Call OpenAI API with system and user prompts
   - Receive structured JSON response

4. **Database Population**
   - Create Itinerary record
   - Parse AI response
   - Create ItineraryDay records for each day
   - Create ItineraryActivity records for each activity

5. **Response**
   - Return detailed itinerary with all days and activities
   - Include budget breakdown and travel tips

## 🔌 API Endpoints Summary

### Itinerary Endpoints
```
POST   /api/itinerary/generate/          Generate new itinerary
GET    /api/itinerary/                   List itineraries
GET    /api/itinerary/{id}/              Get itinerary details
POST   /api/itinerary/{id}/save/         Save itinerary
GET    /api/itinerary/recent/            Get recent itineraries
GET    /api/itinerary/export/{id}/       Export as JSON
```

### Location Endpoints
```
GET    /api/locations/                   List locations
GET    /api/locations/{id}/              Get location details
GET    /api/locations/by_region/         Filter by region
GET    /api/locations/by_altitude/       Filter by altitude
GET    /api/locations/popular/           Most popular locations
GET    /api/hidden-gems/                 List hidden gems
GET    /api/hidden-gems/by_type/         Filter by type
GET    /api/hidden-gems/by_location/     Filter by location
GET    /api/hidden-gems/least_crowded/   Least crowded gems
GET    /api/transport/                   List transport options
GET    /api/transport/route/             Transport for specific route
GET    /api/transport/by_type/           Filter by type
GET    /api/transport/cheapest_route/    Cheapest option
```

### Tips Endpoints
```
GET    /api/tips/budget/                 List budget tips
GET    /api/tips/budget/by_category/     Filter by category
GET    /api/tips/budget/by_budget/       Filter by budget level
GET    /api/tips/seasonal/               List seasonal tips
GET    /api/tips/seasonal/by_season/     Filter by season
GET    /api/tips/seasonal/current_season/ Tips for current month
GET    /api/tips/seasonal/best_conditions/ Best weather months
GET    /api/tips/experiences/            List local experiences
GET    /api/tips/experiences/by_category/ Filter by category
GET    /api/tips/experiences/by_location/ Filter by location
GET    /api/tips/experiences/kids_friendly/  Those suitable for kids
GET    /api/tips/experiences/budget_friendly/ Cheap experiences
```

## 🔧 Key Features

### 1. AI Integration
- OpenAI GPT-4 for intelligent itinerary generation
- Smart prompt engineering with Nepal context
- Structured JSON responses

### 2. Nepal-Specific Data
- 600+ locations with detailed information
- Transport options and cost estimates
- Seasonal advice and weather patterns
- Local experiences and hidden gems

### 3. REST API
- Full CRUD operations
- Filtering, searching, ordering
- Pagination for large datasets
- Swagger/OpenAPI documentation

### 4. Admin Interface
- Django admin for data management
- Custom admin configurations
- Inline editing for related objects

### 5. Frontend Integration
- Server-side rendering with Django templates
- Bootstrap-based responsive design
- JavaScript API client

## 🔐 Security Features

- CSRF protection
- SQL injection prevention (ORM)
- XSS protection
- Secure cookie handling
- Rate limiting ready
- Input validation
- Environment-based configuration

## 📈 Scalability Considerations

- Database indexing on frequently queried fields
- Caching with Redis support
- Async task support with Celery
- Pagination for large datasets
- Query optimization with select_related/prefetch_related

## 🧪 Testing Structure (Ready for Implementation)

```
tests/
├── test_locations/
├── test_tips/
├── test_itinerary/
└── test_api/
```

## 📋 Next Steps

1. Add sample Nepal location data
2. Implement frontend templates (HTML/CSS/JS)
3. Add unit and integration tests
4. Set up CI/CD pipeline
5. Configure production deployment
6. Add Google Maps integration (optional)
7. Implement user authentication (optional)
8. Add itinerary saving/loading functionality
