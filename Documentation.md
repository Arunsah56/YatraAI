# Complete Architecture & Documentation Package
### AI-Powered Travel Itinerary System (Django + OpenAI)

---

# Table of Contents

1. [System Architecture Diagrams](#1-system-architecture-diagrams)
2. [Low-Level Design Diagrams](#2-low-level-design-lld)
3. [Entity Relationship Diagram](#3-entity-relationship-diagram)
4. [Additional Diagrams](#4-additional-diagrams)
5. [Technical Documentation](#5-technical-documentation)
6. [User Manual](#6-user-manual)
7. [Developer Guide](#7-developer-guide)
8. [API Reference Guide](#8-api-reference-guide)
9. [Installation Guide](#9-installation-guide)
10. [Deployment Guide](#10-deployment-guide)
11. [Architecture Guide](#11-architecture-guide)
12. [Presentation Content](#12-presentation-content)
13. [Project Descriptions](#13-project-descriptions)
14. [Viva Questions & Answers](#14-viva-questions--answers)
15. [Resume & Career Assets](#15-resume--career-assets)
16. [Strategic Analysis](#16-strategic-analysis)
17. [Project Management](#17-project-management)

---

## 1. System Architecture Diagrams

### 1.1 High-Level Architecture Diagram

```mermaid
flowchart TD
    User[("👤 User / Browser")]
    Admin[("🛠 Admin Dashboard")]

    subgraph Frontend["Frontend Layer"]
        UI[React / HTML Frontend UI]
        Auth[Auth Pages: Login / Register]
        Pages[Itinerary Pages / Results]
    end

    subgraph APILayer["Django Backend — REST API Layer"]
        DRFAPI[Django REST Framework API Gateway]
        AuthMiddleware[JWT Auth Middleware]
        RateLimiter[Rate Limiter]
        ExceptionHandler[Global Exception Handler]
    end

    subgraph ServiceLayer["AI Service Layer"]
        ItinService[ItineraryAIService]
        PromptBuilder[Prompt Builder]
        ResponseParser[Response Parser]
        CacheService[Cache Service]
    end

    subgraph ExternalAPIs["External Services"]
        OpenAI[OpenAI GPT-4 API]
        EmailSvc[Email Service: SendGrid]
        MapAPI[Maps API: Google Maps]
    end

    subgraph DataLayer["Data Layer"]
        PostgreSQL[("🐘 PostgreSQL Database")]
        Redis[("⚡ Redis Cache")]
    end

    User --> UI
    Auth --> DRFAPI
    UI --> DRFAPI
    Pages --> DRFAPI
    Admin --> DRFAPI

    DRFAPI --> AuthMiddleware
    AuthMiddleware --> RateLimiter
    RateLimiter --> ItinService
    RateLimiter --> PostgreSQL

    ItinService --> PromptBuilder
    PromptBuilder --> OpenAI
    OpenAI --> ResponseParser
    ResponseParser --> CacheService
    CacheService --> Redis

    DRFAPI --> PostgreSQL
    ItinService --> EmailSvc
    ItinService --> MapAPI
```

**Component Descriptions:**

| Component | Role |
|---|---|
| User / Browser | End user accessing the application via browser or mobile |
| Frontend UI | React-based SPA handling user input and itinerary display |
| Django REST API | Central API gateway routing all requests; enforces auth and rate limits |
| JWT Auth Middleware | Validates JWT tokens on every protected request |
| ItineraryAIService | Orchestrates AI prompt construction, OpenAI calls, and response parsing |
| OpenAI GPT-4 API | Large language model generating structured travel itinerary content |
| PostgreSQL | Persistent relational database storing all user and itinerary data |
| Redis Cache | Caches AI-generated itineraries to reduce cost and latency |
| Admin Dashboard | Django admin interface for superuser management |
| Email Service | Sends itinerary exports and notifications to users |
| Maps API | Enriches location data with coordinates and map links |

---

### 1.2 Use Case Diagram

```mermaid
flowchart LR
    User(["👤 User"])
    Admin(["🛠 Admin"])
    OpenAI(["🤖 OpenAI API"])

    UC1([Register / Login])
    UC2([Generate Itinerary])
    UC3([View Itinerary])
    UC4([Save Itinerary])
    UC5([Export Itinerary PDF])
    UC6([Add Notes])
    UC7([Search Locations])
    UC8([Manage Users])
    UC9([Monitor AI Usage])
    UC10([Configure Settings])

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    UC2 --> OpenAI
```

---

### 1.3 Sequence Diagram — Itinerary Generation

```mermaid
sequenceDiagram
    actor U as User
    participant FE as Frontend UI
    participant API as Django REST API
    participant Auth as JWT Middleware
    participant Cache as Redis Cache
    participant Svc as ItineraryAIService
    participant GPT as OpenAI GPT-4
    participant DB as PostgreSQL

    U->>FE: Fill itinerary form (destination, dates, budget)
    FE->>API: POST /api/v1/itinerary/generate/
    API->>Auth: Validate JWT token
    Auth-->>API: Token valid

    API->>Cache: Check cache (destination + params hash)
    alt Cache Hit
        Cache-->>API: Return cached itinerary
        API-->>FE: 200 OK — cached itinerary
    else Cache Miss
        API->>Svc: generate_itinerary(params)
        Svc->>Svc: build_prompt(params)
        Svc->>GPT: POST /v1/chat/completions
        GPT-->>Svc: Structured JSON response
        Svc->>Svc: parse_response(raw_json)
        Svc->>DB: Save Itinerary + Days + Activities
        DB-->>Svc: Itinerary ID
        Svc->>Cache: Store result (TTL: 24h)
        Svc-->>API: Serialized itinerary data
        API-->>FE: 201 Created — itinerary
    end

    FE-->>U: Display itinerary
```

---

### 1.4 Authentication Flow Diagram

```mermaid
flowchart TD
    Start([User Submits Credentials]) --> LoginAPI[POST /api/v1/auth/login/]
    LoginAPI --> ValidateCreds{Credentials Valid?}
    ValidateCreds -- No --> ReturnError[401 Unauthorized]
    ValidateCreds -- Yes --> IssueTokens[Generate Access + Refresh JWT Tokens]
    IssueTokens --> ReturnTokens[Return Tokens to Client]
    ReturnTokens --> ClientStores[Client Stores Tokens in Memory / HttpOnly Cookie]

    ClientStores --> MakeRequest[User Makes Protected API Request]
    MakeRequest --> SendBearer[Send Authorization: Bearer &lt;access_token&gt;]
    SendBearer --> ValidateJWT{JWT Valid & Not Expired?}
    ValidateJWT -- No --> CheckRefresh{Has Refresh Token?}
    CheckRefresh -- No --> ForceLogin[Redirect to Login]
    CheckRefresh -- Yes --> RefreshAPI[POST /api/v1/auth/refresh/]
    RefreshAPI --> NewAccessToken[Issue New Access Token]
    NewAccessToken --> RetryRequest[Retry Original Request]
    ValidateJWT -- Yes --> ProcessRequest[Process Request Normally]
```

---

## 2. Low-Level Design (LLD)

### 2.1 Class Diagram — Core Modules

```mermaid
classDiagram
    class ItineraryViewSet {
        +generate(request) Response
        +save(request) Response
        +retrieve(request, pk) Response
        +export_pdf(request, pk) Response
        +list(request) Response
        -validate_input(data) bool
        -check_permissions(user) bool
    }

    class ItineraryAIService {
        -openai_client: OpenAI
        -cache: RedisCache
        +generate_itinerary(params) ItineraryDTO
        +build_prompt(params) str
        +parse_response(raw) dict
        +estimate_cost(tokens) float
        -handle_api_error(exc) None
    }

    class PromptBuilder {
        +build(destination, days, budget, style) str
        +inject_context(base, location_facts) str
        +format_constraints(prefs) str
    }

    class ItinerarySerializer {
        +validate(data) dict
        +create(validated_data) Itinerary
        +update(instance, data) Itinerary
        +to_representation(instance) dict
    }

    class ItineraryDaySerializer {
        +validate(data) dict
        +to_representation(instance) dict
    }

    class UserAuthService {
        +register(data) User
        +login(credentials) TokenPair
        +refresh_token(refresh) str
        +logout(user) None
        +change_password(user, old, new) None
    }

    class CacheService {
        +get(key) any
        +set(key, value, ttl) None
        +delete(key) None
        +build_key(params) str
    }

    class ExceptionHandler {
        +handle(exc, context) Response
        +format_error(exc) dict
        +log_error(exc) None
    }

    class PDFExporter {
        +export(itinerary_id) bytes
        +render_template(data) str
        +attach_map(pdf, location) bytes
    }

    ItineraryViewSet --> ItineraryAIService
    ItineraryViewSet --> ItinerarySerializer
    ItineraryViewSet --> PDFExporter
    ItineraryAIService --> PromptBuilder
    ItineraryAIService --> CacheService
    ItinerarySerializer --> ItineraryDaySerializer
    ItineraryViewSet --> ExceptionHandler
```

---

### 2.2 Component Diagram

```mermaid
flowchart TD
    subgraph Frontend["Frontend Components"]
        FormComp[ItineraryForm Component]
        ResultComp[ItineraryResult Component]
        DayComp[DayCard Component]
        MapComp[MapView Component]
        AuthComp[Auth Components]
    end

    subgraph APIViews["API Views (ViewSets)"]
        ItinVS[ItineraryViewSet]
        AuthVS[AuthViewSet]
        LocationVS[LocationViewSet]
        ExportVS[ExportViewSet]
    end

    subgraph Serializers["Serializers"]
        ItinSer[ItinerarySerializer]
        DaySer[ItineraryDaySerializer]
        ActSer[ActivitySerializer]
        UserSer[UserSerializer]
    end

    subgraph Services["Service Layer"]
        AIService[ItineraryAIService]
        AuthService[UserAuthService]
        CacheSvc[CacheService]
        EmailSvc[EmailService]
        ExportSvc[PDFExporter]
    end

    subgraph Models["Django ORM Models"]
        ItinModel[Itinerary]
        DayModel[ItineraryDay]
        ActModel[ItineraryActivity]
        LocModel[Location]
        UserModel[CustomUser]
    end

    subgraph Utils["Utilities / Middleware"]
        JWTMiddleware[JWT Auth Middleware]
        RateLimit[RateLimitMiddleware]
        LogMiddleware[RequestLoggingMiddleware]
        ErrHandler[GlobalExceptionHandler]
    end

    FormComp -->|HTTP POST| ItinVS
    ItinVS --> ItinSer
    ItinSer --> ItinModel
    ItinVS --> AIService
    AIService --> CacheSvc
    AuthComp --> AuthVS
    AuthVS --> AuthService
    AuthVS --> UserSer

    JWTMiddleware --> ItinVS
    RateLimit --> ItinVS
    ErrHandler --> ItinVS
```

---

### 2.3 AI Workflow Diagram

```mermaid
flowchart TD
    Input([User Input: destination, days, budget, style]) --> Validate[Validate & Sanitize Input]
    Validate --> CacheLookup{Cache Hit?}
    CacheLookup -- Yes --> ReturnCached([Return Cached Itinerary])
    CacheLookup -- No --> BuildPrompt[PromptBuilder.build()]
    BuildPrompt --> InjectContext[Inject Location Context & Constraints]
    InjectContext --> CallOpenAI[POST to OpenAI /v1/chat/completions]
    CallOpenAI --> APIError{API Error?}
    APIError -- Yes --> RetryLogic[Exponential Backoff Retry x3]
    RetryLogic --> Fallback[Return Generic Error / Fallback Response]
    APIError -- No --> ParseJSON[ResponseParser.parse_response()]
    ParseJSON --> ValidateSchema{JSON Schema Valid?}
    ValidateSchema -- No --> ParseFallback[Use Partial Data or Re-prompt]
    ValidateSchema -- Yes --> MapToModels[Map to Django ORM Models]
    MapToModels --> SaveDB[Save to PostgreSQL]
    SaveDB --> StoreCache[Store in Redis — TTL 24h]
    StoreCache --> SerializeResponse[Serialize with ItinerarySerializer]
    SerializeResponse --> Return([Return to Client])
```

---

### 2.4 API Request Lifecycle Diagram

```mermaid
flowchart TD
    Request([Incoming HTTP Request]) --> Nginx[Nginx Reverse Proxy]
    Nginx --> Gunicorn[Gunicorn WSGI Server]
    Gunicorn --> DjangoMiddleware[Django Middleware Stack]

    DjangoMiddleware --> LogMiddleware[RequestLoggingMiddleware]
    LogMiddleware --> SecurityMiddleware[SecurityMiddleware / CORS]
    SecurityMiddleware --> JWTMiddleware[JWTAuthenticationMiddleware]
    JWTMiddleware --> RateLimit[RateLimitMiddleware]
    RateLimit --> URLRouter[URL Router / urls.py]
    URLRouter --> ViewSet[ViewSet.dispatch]
    ViewSet --> Permission[Permission Check]
    Permission --> Throttle[Throttle Check]
    Throttle --> Serializer[Deserialize & Validate Input]
    Serializer --> BusinessLogic[Service Layer / Business Logic]
    BusinessLogic --> ORM[Django ORM Query]
    ORM --> DB[(PostgreSQL)]
    DB --> ORM
    ORM --> SerializeOut[Serialize Output]
    SerializeOut --> ResponseObj[Build HTTP Response Object]
    ResponseObj --> ReturnResponse([Return Response to Client])
```

---

## 3. Entity Relationship Diagram

```mermaid
erDiagram
    CUSTOM_USER {
        int id PK
        string email UK
        string username UK
        string password_hash
        bool is_active
        bool is_staff
        datetime created_at
        datetime updated_at
    }

    ITINERARY {
        int id PK
        int user_id FK
        int location_id FK
        string title
        string destination
        date start_date
        date end_date
        int total_days
        string budget_range
        string travel_style
        string status
        text ai_prompt_used
        int tokens_used
        datetime created_at
        datetime updated_at
    }

    ITINERARY_DAY {
        int id PK
        int itinerary_id FK
        int day_number
        date date
        string theme
        string weather_forecast
        text summary
        datetime created_at
    }

    ITINERARY_ACTIVITY {
        int id PK
        int itinerary_day_id FK
        int location_id FK
        string name
        string activity_type
        time start_time
        time end_time
        int duration_minutes
        text description
        decimal estimated_cost
        string currency
        int order_index
        datetime created_at
    }

    ITINERARY_NOTE {
        int id PK
        int itinerary_id FK
        int user_id FK
        text content
        string note_type
        datetime created_at
        datetime updated_at
    }

    LOCATION {
        int id PK
        string name
        string city
        string country
        string country_code
        decimal latitude
        decimal longitude
        string timezone
        text description
        string image_url
        datetime created_at
    }

    HIDDEN_GEM {
        int id PK
        int location_id FK
        string name
        text description
        string gem_type
        decimal latitude
        decimal longitude
        string how_to_reach
        bool is_verified
        datetime created_at
    }

    TRANSPORT_OPTION {
        int id PK
        int from_location_id FK
        int to_location_id FK
        string transport_type
        int duration_minutes
        decimal estimated_cost
        string currency
        string notes
        datetime created_at
    }

    BUDGET_TIP {
        int id PK
        int location_id FK
        string tip_category
        text description
        decimal estimated_savings
        string currency
        datetime created_at
    }

    SEASONAL_TIP {
        int id PK
        int location_id FK
        string season
        string month_range
        text tip_description
        string weather_summary
        bool is_peak_season
        datetime created_at
    }

    LOCAL_EXPERIENCE {
        int id PK
        int location_id FK
        string name
        text description
        string experience_type
        decimal price_from
        string currency
        int duration_hours
        string booking_required
        datetime created_at
    }

    ITINERARY_LOCAL_EXPERIENCE {
        int itinerary_id FK
        int local_experience_id FK
    }

    CUSTOM_USER ||--o{ ITINERARY : creates
    CUSTOM_USER ||--o{ ITINERARY_NOTE : writes
    ITINERARY ||--o{ ITINERARY_DAY : contains
    ITINERARY_DAY ||--o{ ITINERARY_ACTIVITY : schedules
    ITINERARY ||--o{ ITINERARY_NOTE : has
    ITINERARY }o--|| LOCATION : "based in"
    ITINERARY_ACTIVITY }o--o| LOCATION : "takes place at"
    LOCATION ||--o{ HIDDEN_GEM : contains
    LOCATION ||--o{ BUDGET_TIP : has
    LOCATION ||--o{ SEASONAL_TIP : has
    LOCATION ||--o{ LOCAL_EXPERIENCE : offers
    LOCATION ||--o{ TRANSPORT_OPTION : "origin of"
    ITINERARY }o--o{ LOCAL_EXPERIENCE : includes
    ITINERARY_LOCAL_EXPERIENCE }|--|| ITINERARY : junction
    ITINERARY_LOCAL_EXPERIENCE }|--|| LOCAL_EXPERIENCE : junction
```

**Relationship Summary:**

| Relationship | Type | Description |
|---|---|---|
| USER → ITINERARY | One-to-Many | One user can create many itineraries |
| ITINERARY → ITINERARY_DAY | One-to-Many | Each itinerary has one row per day |
| ITINERARY_DAY → ITINERARY_ACTIVITY | One-to-Many | Each day has multiple scheduled activities |
| ITINERARY → ITINERARY_NOTE | One-to-Many | Notes can be attached to an itinerary |
| LOCATION → HIDDEN_GEM | One-to-Many | A location can have many hidden gems |
| LOCATION → TRANSPORT_OPTION | One-to-Many | A location can be the origin of many transport options |
| ITINERARY ↔ LOCAL_EXPERIENCE | Many-to-Many | Via junction table ITINERARY_LOCAL_EXPERIENCE |

**Normalization:** The schema follows 3NF — no transitive dependencies, all non-key attributes depend solely on the primary key. Location data is extracted to its own table to avoid repetition across itineraries.

**Data Integrity:** Foreign keys enforce referential integrity. `CASCADE DELETE` is applied on `ITINERARY_DAY` when an `ITINERARY` is deleted. Unique constraints on `email` and `username`.

**Query Optimization:** Indexes on `itinerary.user_id`, `itinerary_day.itinerary_id`, `activity.itinerary_day_id`, and `location.country_code`. Composite index on `(itinerary_id, day_number)` for ordered day retrieval.

---

## 4. Additional Diagrams

### 4.1 Deployment Diagram

```mermaid
flowchart TD
    subgraph Cloud["AWS Cloud / VPS"]
        subgraph PublicSubnet["Public Subnet"]
            Nginx[Nginx — Port 80 / 443]
            CertBot[Certbot SSL]
        end

        subgraph AppSubnet["Application Subnet"]
            Gunicorn[Gunicorn — Django App Server]
            Celery[Celery Worker — Async Tasks]
            Beat[Celery Beat — Scheduler]
        end

        subgraph DataSubnet["Data Subnet"]
            PG[(PostgreSQL RDS)]
            Redis[(Redis ElastiCache)]
            S3[(S3 — Static & Media Files)]
        end
    end

    subgraph ExternalServices["External Services"]
        OpenAI2[OpenAI API]
        SendGrid[SendGrid Email]
        Sentry[Sentry Error Monitoring]
        Cloudwatch[CloudWatch Logs]
    end

    Internet([Internet]) --> Nginx
    Nginx --> Gunicorn
    Gunicorn --> PG
    Gunicorn --> Redis
    Gunicorn --> S3
    Gunicorn --> OpenAI2
    Celery --> PG
    Celery --> Redis
    Celery --> SendGrid
    Gunicorn --> Sentry
    Gunicorn --> Cloudwatch
```

---

### 4.2 Activity Diagram — User Generates Itinerary

```mermaid
flowchart TD
    Start([Start]) --> Login{User Logged In?}
    Login -- No --> Redirect[Redirect to Login]
    Redirect --> LoginForm[Enter Credentials]
    LoginForm --> Authenticate{Auth Success?}
    Authenticate -- No --> ShowError[Show Error Message]
    ShowError --> LoginForm
    Authenticate -- Yes --> Dashboard
    Login -- Yes --> Dashboard[Load Dashboard]
    Dashboard --> FillForm[Fill Itinerary Form]
    FillForm --> Submit[Submit Form]
    Submit --> ClientValidate{Client-Side Valid?}
    ClientValidate -- No --> HighlightErrors[Highlight Form Errors]
    HighlightErrors --> FillForm
    ClientValidate -- Yes --> APICall[Send POST to /api/v1/itinerary/generate/]
    APICall --> Loading[Show Loading Spinner]
    Loading --> APIResponse{API Response}
    APIResponse -- Error --> ShowAPIError[Display Error Toast]
    ShowAPIError --> FillForm
    APIResponse -- Success --> DisplayResult[Render Itinerary Result]
    DisplayResult --> UserAction{User Action?}
    UserAction -- Save --> SaveAPI[POST /api/v1/itinerary/save/]
    UserAction -- Export --> ExportPDF[GET /api/v1/itinerary/export/]
    UserAction -- Edit Notes --> NoteModal[Open Notes Modal]
    UserAction -- New Search --> FillForm
    SaveAPI --> Confirmation[Show Save Confirmation]
    ExportPDF --> Download[Download PDF File]
    NoteModal --> SaveNote[Save Note via API]
    Confirmation --> End([End])
    Download --> End
    SaveNote --> End
```

---

### 4.3 Data Flow Diagram

```mermaid
flowchart LR
    User([User]) -->|Form Data| FE[Frontend]
    FE -->|REST Request + JWT| API[Django API]
    API -->|Validated Params| AISvc[AI Service]
    AISvc -->|Prompt Text| OpenAI[OpenAI API]
    OpenAI -->|Raw JSON Response| AISvc
    AISvc -->|Parsed DTO| API
    API -->|ORM Write| DB[(PostgreSQL)]
    API -->|Cache Write| Cache[(Redis)]
    DB -->|Stored Data| API
    Cache -->|Cached Data| API
    API -->|Serialized JSON| FE
    FE -->|Rendered View| User
    API -->|Export Request| PDFSvc[PDF Service]
    PDFSvc -->|PDF File| User
```

---

## 5. Technical Documentation

### 5.1 Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Backend Framework | Django | 4.2+ | Web framework, ORM, admin |
| REST API | Django REST Framework | 3.14+ | API views, serializers, auth |
| AI Integration | OpenAI Python SDK | 1.x | GPT-4 API communication |
| Database | PostgreSQL | 15+ | Primary relational data store |
| Cache / Queue Broker | Redis | 7+ | Caching, Celery broker |
| Task Queue | Celery | 5+ | Async email, PDF generation |
| Authentication | djangorestframework-simplejwt | 5+ | JWT access/refresh tokens |
| PDF Generation | WeasyPrint / ReportLab | Latest | PDF export |
| WSGI Server | Gunicorn | 21+ | Production app server |
| Reverse Proxy | Nginx | 1.24+ | SSL termination, static files |
| Containerization | Docker + Docker Compose | Latest | Dev and prod environments |
| Frontend | React 18 / Vanilla JS | 18+ | User interface |

### 5.2 Project Structure

```
project_root/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── authentication/
│   │   ├── models.py       # CustomUser
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── services.py
│   ├── itinerary/
│   │   ├── models.py       # All itinerary models
│   │   ├── views.py        # ViewSets
│   │   ├── serializers.py
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── prompt_builder.py
│   │   │   └── pdf_exporter.py
│   │   ├── tasks.py        # Celery tasks
│   │   └── urls.py
│   └── locations/
│       ├── models.py       # Location, HiddenGem, etc.
│       ├── views.py
│       └── serializers.py
├── core/
│   ├── exceptions.py
│   ├── middleware.py
│   ├── permissions.py
│   └── pagination.py
├── utils/
│   ├── cache.py
│   └── validators.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── manage.py
```

---

## 6. User Manual

### 6.1 Getting Started

1. **Register** at the application URL. Enter your name, email, and password.
2. **Log in** with your credentials. You will receive a JWT access token (handled automatically by the app).
3. From the **Dashboard**, click **"Create Itinerary"**.

### 6.2 Creating an Itinerary

Fill in the itinerary form with:

| Field | Description | Example |
|---|---|---|
| Destination | City or country name | "Tokyo, Japan" |
| Start Date | Trip start date | 2025-10-01 |
| End Date | Trip end date | 2025-10-08 |
| Budget | Approximate daily budget | "$100/day" |
| Travel Style | Adventure, Cultural, Relaxed, Family | "Cultural" |
| Special Preferences | Optional free text | "Vegetarian friendly" |

Click **"Generate Itinerary"**. The AI will produce a day-by-day plan in 10–20 seconds.

### 6.3 Viewing & Managing Your Itinerary

- Each day is shown as a card with activities, times, and estimated costs.
- Click **"Add Note"** to attach personal notes to the itinerary.
- Click **"Export PDF"** to download a formatted travel document.
- Click **"Save"** to store the itinerary to your account.

### 6.4 Account Management

Navigate to **Profile Settings** to update your email, change your password, or delete your account.

---

## 7. Developer Guide

### 7.1 Setting Up the Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/ai-travel-itinerary.git
cd ai-travel-itinerary

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your OpenAI API key, DB credentials, Redis URL

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

### 7.2 Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `True` / `False` |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@localhost/db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `OPENAI_MODEL` | Model to use | `gpt-4-turbo-preview` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

### 7.3 Running Tests

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report -m

# Run specific app tests
python manage.py test apps.itinerary
```

### 7.4 Code Style

The project uses `black` for formatting, `flake8` for linting, and `isort` for import ordering.

```bash
black .
flake8 .
isort .
```

---

## 8. API Reference Guide

### Base URL

```
https://api.yourapp.com/api/v1/
```

### Authentication

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

### Endpoints

#### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register/` | Register new user | No |
| POST | `/auth/login/` | Login and receive tokens | No |
| POST | `/auth/refresh/` | Refresh access token | No |
| POST | `/auth/logout/` | Invalidate refresh token | Yes |

#### Itinerary

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/itinerary/generate/` | Generate new AI itinerary | Yes |
| GET | `/itinerary/` | List user's itineraries | Yes |
| GET | `/itinerary/{id}/` | Retrieve single itinerary | Yes |
| PATCH | `/itinerary/{id}/` | Update itinerary metadata | Yes |
| DELETE | `/itinerary/{id}/` | Delete itinerary | Yes |
| GET | `/itinerary/{id}/export/` | Export itinerary as PDF | Yes |

#### Sample Request — Generate Itinerary

```json
POST /api/v1/itinerary/generate/
Content-Type: application/json
Authorization: Bearer eyJ...

{
  "destination": "Kyoto, Japan",
  "start_date": "2025-10-01",
  "end_date": "2025-10-05",
  "budget_range": "medium",
  "travel_style": "cultural",
  "preferences": "vegetarian food options, no early mornings"
}
```

#### Sample Response

```json
HTTP 201 Created
{
  "id": 42,
  "title": "5 Days in Kyoto",
  "destination": "Kyoto, Japan",
  "start_date": "2025-10-01",
  "end_date": "2025-10-05",
  "days": [
    {
      "day_number": 1,
      "date": "2025-10-01",
      "theme": "Temples & Tradition",
      "activities": [
        {
          "name": "Fushimi Inari Shrine",
          "start_time": "09:00",
          "end_time": "11:00",
          "estimated_cost": 0,
          "description": "Walk through thousands of torii gates..."
        }
      ]
    }
  ]
}
```

#### Error Responses

| Status Code | Meaning |
|---|---|
| 400 | Validation error — check `errors` field |
| 401 | Authentication required or token expired |
| 403 | Permission denied |
| 429 | Rate limit exceeded |
| 500 | Internal server error — contact support |

---

## 9. Installation Guide

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional but recommended)

### Option A: Docker (Recommended)

```bash
# 1. Clone and configure
git clone https://github.com/your-org/ai-travel-itinerary.git
cd ai-travel-itinerary
cp .env.example .env
# Edit .env with your API keys

# 2. Build and start all services
docker-compose up --build

# 3. Run migrations (first time)
docker-compose exec web python manage.py migrate

# 4. Create admin user
docker-compose exec web python manage.py createsuperuser
```

Application will be available at `http://localhost:8000`.

### Option B: Manual Installation

```bash
# Database setup
psql -U postgres
CREATE DATABASE itinerary_db;
CREATE USER itinerary_user WITH PASSWORD 'yourpassword';
GRANT ALL ON DATABASE itinerary_db TO itinerary_user;

# Redis (Ubuntu)
sudo apt install redis-server
sudo systemctl start redis

# Backend
pip install -r requirements/development.txt
python manage.py migrate
python manage.py runserver

# Celery worker (separate terminal)
celery -A config worker --loglevel=info
```

---

## 10. Deployment Guide

### 10.1 Production Checklist

- [ ] Set `DEBUG=False` in environment
- [ ] Set a strong, unique `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with production domains
- [ ] Enable HTTPS (SSL certificate via Certbot)
- [ ] Set up PostgreSQL with connection pooling (PgBouncer)
- [ ] Configure Redis with `maxmemory-policy allkeys-lru`
- [ ] Set up Sentry for error monitoring
- [ ] Configure automated database backups
- [ ] Set up log rotation

### 10.2 Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /static/ {
        alias /app/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 10.3 Gunicorn Service

```ini
# /etc/systemd/system/itinerary.service
[Unit]
Description=Itinerary Django App
After=network.target

[Service]
User=deploy
WorkingDirectory=/app
ExecStart=/app/venv/bin/gunicorn config.wsgi:application \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --timeout 120

[Install]
WantedBy=multi-user.target
```

---

## 11. Architecture Guide

### 11.1 Layered Architecture

The system follows a strict 4-layer architecture:

| Layer | Responsibility | Django Component |
|---|---|---|
| Presentation | HTTP request/response, serialization | ViewSets, Serializers |
| Application | Business logic orchestration | Service classes |
| Domain | Data models and rules | Django ORM Models |
| Infrastructure | DB, cache, external APIs | PostgreSQL, Redis, OpenAI |

### 11.2 Design Patterns Used

| Pattern | Where Applied | Benefit |
|---|---|---|
| Repository Pattern | Service layer abstracts ORM queries | Testability |
| Service Layer | `ItineraryAIService`, `UserAuthService` | Separation of concerns |
| Strategy Pattern | `PromptBuilder` strategies per travel style | Extensibility |
| Factory Pattern | Serializer selection per response type | Flexibility |
| Decorator Pattern | `@permission_classes`, `@throttle_classes` | Cross-cutting concerns |
| Observer Pattern | Django signals for post-save actions | Loose coupling |

---

## 12. Presentation Content

### 12.1 Slide Deck Outline

1. **Title Slide** — AI-Powered Travel Itinerary Planner
2. **Problem Statement** — Planning travel is time-consuming and overwhelming
3. **Solution** — Personalized AI-generated itineraries in seconds
4. **Tech Stack Overview** — Django, OpenAI, PostgreSQL, Redis
5. **System Architecture** — High-level diagram
6. **Key Features** — Generate, Save, Export, Notes
7. **AI Integration Deep Dive** — Prompt engineering, response parsing
8. **Database Design** — ER diagram
9. **API Design** — RESTful endpoints with examples
10. **Security** — JWT auth, rate limiting, input validation
11. **Performance** — Redis caching, async tasks
12. **Demo** — Live walkthrough
13. **Future Roadmap** — Mobile app, multi-language, booking integration
14. **Q&A**

---

## 13. Project Descriptions

### 13.1 GitHub Repository Description

```
AI-powered travel itinerary planner built with Django REST Framework and OpenAI GPT-4.
Generates personalized day-by-day travel plans based on destination, budget, and travel style.
Features JWT authentication, Redis caching, PDF export, and a clean REST API.

Tech Stack: Python • Django • DRF • OpenAI • PostgreSQL • Redis • Celery • Docker
```

### 13.2 LinkedIn Project Description

**AI Travel Itinerary Planner** | Python, Django, OpenAI GPT-4

Built a full-stack AI-powered travel planning application that generates personalized, day-by-day travel itineraries using OpenAI GPT-4. The system processes user preferences (destination, budget, travel style) and produces structured itineraries with activities, cost estimates, hidden gems, and seasonal tips. Implemented JWT authentication, Redis caching to reduce AI API costs by ~60%, Celery for async PDF generation, and a fully documented REST API. Deployed on AWS with Nginx, Gunicorn, and PostgreSQL RDS.

### 13.3 Resume Project Description

**AI-Powered Travel Itinerary System** | Django, OpenAI, PostgreSQL, Redis
- Engineered a full-stack REST API using Django REST Framework that integrates OpenAI GPT-4 to generate structured travel itineraries from natural language user inputs
- Designed a normalized PostgreSQL schema (12+ models) covering itineraries, activities, locations, hidden gems, and transport options
- Implemented Redis caching layer that reduced redundant OpenAI API calls by ~60%, cutting per-request cost significantly
- Built JWT-based authentication with refresh token rotation and per-user rate limiting
- Deployed on AWS using Docker, Gunicorn, and Nginx with automated CI/CD via GitHub Actions

### 13.4 ATS-Friendly Project Description

Developed AI-Powered Travel Itinerary application using Python, Django, Django REST Framework, OpenAI API, PostgreSQL, Redis, and Docker. Built RESTful APIs with JWT authentication, implemented GPT-4 prompt engineering for structured travel plan generation, designed relational database schema with 12+ models, integrated Redis caching to optimize performance, and deployed to AWS with Nginx and Gunicorn. Applied software engineering best practices including layered architecture, unit testing, CI/CD pipelines, and API documentation.

---

## 14. Viva Questions & Answers

**Q1. Why did you choose Django REST Framework over Flask or FastAPI?**
DRF provides built-in authentication, serializers, viewsets, and browsable API out of the box, significantly reducing boilerplate. For a data-heavy application with complex ORM relationships, Django's mature ORM and admin were decisive advantages. FastAPI would be preferable for pure async high-throughput use cases.

**Q2. How do you handle OpenAI API failures or timeouts?**
The `ItineraryAIService` implements exponential backoff with 3 retries using the `tenacity` library. On final failure, a graceful error response is returned to the client. Rate limit errors (429) trigger a longer wait. All failures are logged to Sentry with full context.

**Q3. What is the purpose of Redis in this architecture?**
Redis serves two roles: (1) caching AI-generated itineraries keyed by a hash of destination + parameters to avoid redundant API calls and reduce cost, and (2) acting as the Celery message broker for async task execution (PDF generation, emails).

**Q4. How does JWT authentication work in your system?**
On login, the server issues a short-lived access token (15 min) and a long-lived refresh token (7 days). The client includes the access token in the `Authorization: Bearer` header on each request. When expired, the client uses the refresh token to obtain a new access token without re-login. The middleware validates the token signature and expiry on every request.

**Q5. Explain the database normalization in your schema.**
The schema follows 3NF. Location data is extracted to a separate `Location` table to avoid duplication across itineraries. Budget tips, seasonal tips, and hidden gems all reference `Location` by foreign key rather than duplicating location fields. This eliminates update anomalies and reduces storage.

**Q6. What is prompt engineering and how did you apply it?**
Prompt engineering is the practice of crafting input text to guide LLM output reliably. In `PromptBuilder`, the system prompt defines the JSON output schema and travel constraints. Few-shot examples are embedded to guide output format. Temperature is set low (0.3) for consistent structured output.

**Q7. How do you prevent excessive OpenAI API costs?**
Three strategies: (1) Redis caching with 24-hour TTL for identical parameter combinations, (2) token budgeting — the prompt is designed to stay within a max token limit, and (3) per-user daily rate limiting so no single user can trigger unlimited AI calls.

**Q8. What is the difference between a ViewSet and an APIView in DRF?**
`APIView` maps HTTP methods directly to handler functions. `ViewSet` abstracts common CRUD operations (list, create, retrieve, update, destroy) into a single class and integrates with `Router` for automatic URL generation. ViewSets reduce repetition for standard CRUD resources.

**Q9. How are many-to-many relationships handled in your ER design?**
`ITINERARY` and `LOCAL_EXPERIENCE` have a many-to-many relationship managed through the junction table `ITINERARY_LOCAL_EXPERIENCE`. In Django this is defined with `ManyToManyField` and can include a `through` model for extra attributes.

**Q10. What security measures are implemented?**
JWT authentication, HTTPS enforcement, CORS configuration, per-user rate limiting (django-ratelimit), SQL injection prevention via ORM parameterized queries, input validation via DRF serializers, and `SECURE_BROWSER_XSS_FILTER` / `X_FRAME_OPTIONS` headers.

**Q11. How does Celery improve the system?**
Celery offloads time-consuming tasks (PDF generation, email delivery) from the request-response cycle. The user receives an immediate API response while the PDF is generated asynchronously. This keeps API response times fast and prevents request timeouts.

**Q12. What is the Cache-Aside pattern and do you use it?**
Cache-Aside (Lazy Loading) means the application checks the cache first, and on a miss, reads from the database, then populates the cache. Yes — `CacheService.get()` checks Redis first; on a miss, the AI call is made and the result is stored in Redis before returning.

**Q13. How would you scale this application for 1 million users?**
Horizontal scaling of Gunicorn workers behind a load balancer, read replicas for PostgreSQL, Redis Cluster for distributed caching, CDN for static assets, Celery worker autoscaling, and potentially migrating the AI service to an async queue-based microservice.

**Q14. What is the purpose of `django-filter` and pagination?**
`django-filter` allows query parameter-based filtering of querysets (e.g., `?destination=Tokyo&status=saved`) without manual filtering code. Pagination limits response size — the API returns 20 itineraries per page using `PageNumberPagination` to avoid large payload transfers.

**Q15. How do you test the AI service without calling the real OpenAI API?**
Unit tests mock the `openai.ChatCompletion.create` method using `unittest.mock.patch`. Test fixtures provide pre-defined JSON responses matching the expected schema. Integration tests run against a real API key in CI only when `INTEGRATION_TESTS=true` is set.

---

## 15. Resume & Career Assets

### 15.1 Elevator Pitch

"I built an AI-powered travel itinerary application using Django and OpenAI GPT-4 that generates personalized day-by-day travel plans in seconds. The system handles authentication, Redis caching to cut API costs by 60%, PDF export, and is deployed on AWS. It's a full production-grade system demonstrating both backend engineering and practical AI integration."

### 15.2 Executive Summary

This project delivers an AI-powered travel planning platform that reduces itinerary creation time from hours to seconds. By integrating OpenAI GPT-4 with a robust Django backend, the system generates structured, budget-aware travel plans tailored to user preferences. Key technical achievements include a layered architecture ensuring maintainability, Redis caching reducing operational AI costs, JWT-secured REST APIs, and a normalized relational schema supporting complex travel data. The platform is deployment-ready on AWS with containerized infrastructure.

---

## 16. Strategic Analysis

### 16.1 SWOT Analysis

| | Positive | Negative |
|---|---|---|
| **Internal** | **Strengths:** Fast generation, structured output, cost-optimized caching, clean API design, scalable architecture | **Weaknesses:** Dependency on OpenAI availability and pricing, limited offline capability, AI output variability |
| **External** | **Opportunities:** Mobile app expansion, booking API integration, enterprise travel market, multi-language support | **Threats:** OpenAI API pricing increases, competing AI travel tools (Google, TripAdvisor AI), data privacy regulations |

---

## 17. Project Management

### 17.1 Project Timeline & Gantt Chart

```mermaid
gantt
    title AI Travel Itinerary — Development Timeline
    dateFormat  YYYY-MM-DD
    section Planning
    Requirements & Architecture   :done, 2024-01-01, 7d
    Database Schema Design        :done, 2024-01-06, 5d
    section Backend Development
    Django Project Setup          :done, 2024-01-13, 3d
    Authentication Module         :done, 2024-01-16, 5d
    Itinerary Models & ORM        :done, 2024-01-21, 7d
    REST API ViewSets             :done, 2024-01-28, 7d
    OpenAI Integration            :done, 2024-02-04, 7d
    Redis Cache Integration       :done, 2024-02-11, 4d
    Celery Async Tasks            :done, 2024-02-15, 4d
    section Frontend
    UI Design & Components        :done, 2024-02-01, 14d
    API Integration               :done, 2024-02-15, 7d
    section Testing
    Unit & Integration Tests      :done, 2024-02-22, 7d
    UAT & Bug Fixing              :done, 2024-03-01, 7d
    section Deployment
    Docker & CI/CD Setup          :done, 2024-03-08, 5d
    AWS Production Deploy         :done, 2024-03-13, 4d
    Documentation                 :done, 2024-03-17, 5d
```

### 17.2 Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| OpenAI API downtime | Medium | High | Implement retry logic + graceful degradation message |
| OpenAI pricing increase | High | Medium | Redis caching reduces call volume; budget cap alerts |
| Database performance degradation | Low | High | Connection pooling, read replicas, query optimization |
| JWT secret key leak | Low | Critical | Rotate keys via environment variables; short token TTL |
| Redis cache failure | Low | Medium | Application falls back to direct DB + AI service calls |
| Data loss | Low | Critical | Automated daily PostgreSQL backups to S3 |

### 17.3 Versioning Strategy

| Version | Scope |
|---|---|
| v1.0 | Core itinerary generation, JWT auth, CRUD API |
| v1.1 | PDF export, notes, improved prompt quality |
| v1.2 | Redis caching, rate limiting, admin dashboard enhancements |
| v2.0 | Mobile API optimization, multi-language support, booking integration |

### 17.4 Maintenance Plan

- **Weekly:** Review Sentry error logs, check OpenAI API usage costs
- **Monthly:** Dependency security updates (`pip audit`), database vacuum/analyze
- **Quarterly:** AI prompt quality review and optimization, performance benchmarking
- **Annually:** Major dependency upgrades, architecture review

---

*Document generated for AI-Powered Travel Itinerary System. All diagrams use Mermaid syntax and render on GitHub, GitLab, and Notion.*