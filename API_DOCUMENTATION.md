# API Documentation - YatraAI

## Overview

YatraAI provides a comprehensive REST API for generating personalized travel itineraries for Nepal. The API is built with Django REST Framework and includes intelligent AI integration for dynamic itinerary generation.

**Base URL**: `http://localhost:8000/api`  
**API Version**: 1.0.0  
**Authentication**: Currently public (ready for token-based auth implementation)

## Response Format

All API responses are in JSON format:

```json
{
    "success": true/false,
    "data": { /* response data */ },
    "error": "error message if applicable"
}
```

---

## Itinerary Endpoints

### Generate Itinerary

Generate a new personalized travel itinerary using AI.

**Endpoint**: `POST /api/itinerary/generate/`

**Request Body**:
```json
{
    "destination": "Kathmandu",
    "number_of_days": 5,
    "budget_level": "mid",
    "interests": ["trekking", "culture", "food"],
    "group_size": 2,
    "travelers_type": "couple"
}
```

**Parameters**:
- `destination` (string, required): Name of destination in Nepal
- `number_of_days` (integer, required): Trip duration (1-365)
- `budget_level` (string, required): One of `low`, `mid`, `luxury`
- `interests` (array, required): List of interests (e.g., adventure, culture, trekking, relaxation, spiritual, food, shopping)
- `group_size` (integer, required): Number of travelers (1-100)
- `travelers_type` (string, required): One of `solo`, `couple`, `family`, `group`

**Response** (201 Created):
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "5-Day Kathmandu & Pokhara Adventure",
        "destination_primary": 1,
        "destination_primary_name": "Kathmandu",
        "number_of_days": 5,
        "budget_level": "mid",
        "budget_level_display": "Mid-range (NPR 2000-5000/day)",
        "interests": ["trekking", "culture"],
        "estimated_total_budget_npr": 50000,
        "budget_breakdown": {
            "accommodation": 15000,
            "meals": 12000,
            "transport": 8000,
            "activities": 12000,
            "miscellaneous": 3000
        },
        "daily_budget_npr": 10000,
        "group_size": 2,
        "travelers_type": "couple",
        "travelers_type_display": "Couple",
        "status": "generated",
        "status_display": "Generated",
        "days": [
            {
                "id": 1,
                "day_number": 1,
                "title": "Arrival in Kathmandu",
                "description": "Arrive and explore Thamel area...",
                "location": 1,
                "location_name": "Kathmandu",
                "accommodation_name": "Hotel Manang",
                "accommodation_type": "hotel",
                "accommodation_type_display": "Hotel",
                "accommodation_estimated_cost_npr": 3000,
                "meals_budget_npr": 2000,
                "activities_budget_npr": 1500,
                "transport_budget_npr": 500,
                "activity_details": [
                    {
                        "id": 1,
                        "time_start": "14:00",
                        "time_end": "18:00",
                        "activity_type": "cultural",
                        "activity_type_display": "Cultural",
                        "name": "Explore Thamel",
                        "description": "Wander through narrow streets...",
                        "estimated_cost_npr": 500,
                        "importance_level": "must",
                        "importance_level_display": "Must-See",
                        "tips": "Start early to avoid crowds..."
                    }
                ]
            }
        ],
        "notes": [],
        "created_at": "2024-04-03T10:30:00Z"
    }
}
```

**Error Response** (400/500):
```json
{
    "success": false,
    "error": "Location 'InvalidCity' not found"
}
```

---

### Get Itinerary

Retrieve a specific itinerary by ID.

**Endpoint**: `GET /api/itinerary/{id}/`

**Response** (200 OK):
Returns full itinerary details including all days and activities.

---

### List Itineraries

Retrieve all generated itineraries.

**Endpoint**: `GET /api/itinerary/`

**Query Parameters**:
- `session_id`: Filter by session
- `page`: Page number (default: 1)
- `limit`: Results per page (default: 20)

**Response** (200 OK):
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/itinerary/?page=2",
    "previous": null,
    "results": [
        { /* itinerary object */ }
    ]
}
```

---

### Save Itinerary

Save an itinerary for later reference.

**Endpoint**: `POST /api/itinerary/{id}/save/`

**Response** (200 OK):
Returns updated itinerary with status = "saved"

---

### Recent Itineraries

Get recently generated itineraries.

**Endpoint**: `GET /api/itinerary/recent/?limit=10`

**Response** (200 OK):
Returns array of recent itineraries.

---

## Location Endpoints

### List Locations

Get all available destinations in Nepal.

**Endpoint**: `GET /api/locations/`

**Query Parameters**:
- `search`: Search by name, region, attraction
- `ordering`: Sort by field (`name`, `distance_from_kathmandu_km`, `popularity_score`)
- `page`: Pagination

**Response** (200 OK):
```json
{
    "count": 50,
    "results": [
        {
            "id": 1,
            "name": "Kathmandu",
            "region": "kathmandu",
            "description": "Capital city of Nepal...",
            "altitude": "mid",
            "latitude": 27.7172,
            "longitude": 85.3240,
            "best_time_visit": "October-November",
            "distance_from_kathmandu_km": 0,
            "travel_time_hours": 0,
            "popularity_score": 10,
            "primary_attraction": "Pashupatinath Temple"
        }
    ]
}
```

---

### Get Location Details

Get detailed information about a location.

**Endpoint**: `GET /api/locations/{id}/`

**Response** (200 OK):
```json
{
    "id": 1,
    "name": "Kathmandu",
    // ... location fields ...
    "hidden_gems": [
        {
            "id": 5,
            "name": "Nagi Gompa",
            "description": "Hidden Buddhist monastery...",
            "rating": 4.7,
            "accessibility_level": 3
        }
    ]
}
```

---

### Filter Locations by Region

**Endpoint**: `GET /api/locations/by_region/?region=kathmandu`

**Valid regions**:
- `kathmandu` - Kathmandu Valley
- `east` - East Nepal
- `central` - Central Nepal (Pokhara, Chitwan)
- `west` - Western Nepal
- `northwest` - Northwest Nepal
- `northeast` - Northeast Nepal

---

### Filter Locations by Altitude

**Endpoint**: `GET /api/locations/by_altitude/?altitude=mid`

**Valid altitudes**:
- `lowland` - Below 500m
- `mid` - 500-2000m
- `highland` - 2000-4000m
- `alpine` - Above 4000m

---

### Popular Locations

**Endpoint**: `GET /api/locations/popular/?limit=10`

Returns most popular locations by popularity score.

---

## Hidden Gems Endpoints

### List Hidden Gems

**Endpoint**: `GET /api/hidden-gems/`

Returns off-beat destinations and local secrets.

**Query Parameters**:
- `search`: Search by name
- `ordering`: Sort by rating, accessibility

---

### Filter by Type

**Endpoint**: `GET /api/hidden-gems/by_type/?type=cultural`

**Valid types**:
- `natural`
- `cultural`
- `adventure`
- `spiritual`
- `local` - Local experiences

---

### Filter by Location

**Endpoint**: `GET /api/hidden-gems/by_location/?location_id=1`

Returns hidden gems in a specific location.

---

### Least Crowded

**Endpoint**: `GET /api/hidden-gems/least_crowded/?limit=5`

Returns empty locations suitable for travelers avoiding crowds.

---

## Transport Endpoints

### List Transport Options

**Endpoint**: `GET /api/transport/`

Returns all available transport methods between locations.

---

### Get Route Options

**Endpoint**: `GET /api/transport/route/?source_id=1&destination_id=2`

Returns all transport options for a specific route.

---

### Filter by Type

**Endpoint**: `GET /api/transport/by_type/?type=bus`

**Valid types**:
- `bus`
- `jeep`
- `flight`
- `train`
- `hiking`
- `private_vehicle`

---

### Cheapest Route

**Endpoint**: `GET /api/transport/cheapest_route/?source_id=1&destination_id=2`

Returns cheapest transport option for a route.

---

## Tips Endpoints

### Budget Tips

**Endpoint**: `GET /api/tips/budget/`

Returns money-saving tips for Nepal travel.

**Query Parameters**:
- `search`: Search by title/content
- `category`: Filter by category

---

### Filter Budget Tips by Category

**Endpoint**: `GET /api/tips/budget/by_category/?category=food`

**Valid categories**:
- `accommodation`
- `food`
- `transport`
- `activities`
- `shopping`
- `general`

---

### Filter by Budget Level

**Endpoint**: `GET /api/tips/budget/by_budget/?budget_level=low`

Returns tips relevant to a specific budget level.

---

### Seasonal Tips

**Endpoint**: `GET /api/tips/seasonal/`

Returns seasonal travel advice for Nepal.

---

### Filter by Season

**Endpoint**: `GET /api/tips/seasonal/by_season/?season=autumn`

**Valid seasons**:
- `spring` - February-May
- `summer` - June-August
- `autumn` - September-November
- `winter` - December-January

---

### Current Season Advice

**Endpoint**: `GET /api/tips/seasonal/current_season/`

Returns tips for the current month.

---

### Best Weather Months

**Endpoint**: `GET /api/tips/seasonal/best_conditions/`

Returns months with best weather (excellent visibility, low rainfall).

---

### Local Experiences

**Endpoint**: `GET /api/tips/experiences/`

Returns authentic local activities and cultural experiences.

---

### Filter by Category

**Endpoint**: `GET /api/tips/experiences/by_category/?category=homestay`

**Valid categories**:
- `homestay`
- `workshop`
- `festival`
- `market`
- `cuisine`
- `trekking`
- `spiritual`

---

### Kids-Friendly Experiences

**Endpoint**: `GET /api/tips/experiences/kids_friendly/`

Returns activities suitable for children.

---

### Budget-Friendly Experiences

**Endpoint**: `GET /api/tips/experiences/budget_friendly/`

Returns experiences under NPR 1000 per person.

---

## Error Handling

### Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

### Error Response Format

```json
{
    "error": "Detailed error message"
}
```

---

## Rate Limiting

**Currently**: No rate limiting (ready for implementation)

Future rate limits:
- 100 requests per minute per IP
- 10 itinerary generations per hour

---

## Authentication

**Currently**: Public access (no authentication required)

**Future**: Token-based authentication with Django REST Framework

```
Authorization: Token your-api-token
```

---

## Pagination

Default pagination: 20 items per page

**Example**:
```
GET /api/locations/?page=1&limit=50
```

---

## Filtering & Searching

Most endpoints support:
- **search**: Full-text search across relevant fields
- **ordering**: Sort by specific fields
- **filtering**: Filter by specific field values

**Example**:
```
GET /api/locations/?search=trekking&ordering=-popularity_score
```

---

## Requests & Examples

### cURL

Generate itinerary:
```bash
curl -X POST http://localhost:8000/api/itinerary/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Kathmandu",
    "number_of_days": 5,
    "budget_level": "mid",
    "interests": ["culture", "food"],
    "group_size": 1,
    "travelers_type": "solo"
  }'
```

### JavaScript Fetch

```javascript
const response = await fetch('http://localhost:8000/api/itinerary/generate/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    destination: 'Kathmandu',
    number_of_days: 5,
    budget_level: 'mid',
    interests: ['culture', 'food'],
    group_size: 1,
    travelers_type: 'solo'
  })
});

const data = await response.json();
console.log(data);
```

### Python Requests

```python
import requests

url = 'http://localhost:8000/api/itinerary/generate/'
data = {
    'destination': 'Kathmandu',
    'number_of_days': 5,
    'budget_level': 'mid',
    'interests': ['culture', 'food'],
    'group_size': 1,
    'travelers_type': 'solo'
}

response = requests.post(url, json=data)
itinerary = response.json()
print(itinerary)
```

---

## WebSocket Support (Future)

Real-time itinerary streaming during generation.

---

## API Documentation Interface

**Swagger UI**: http://localhost:8000/api/docs/swagger/  
**ReDoc**: http://localhost:8000/api/docs/redoc/  
**OpenAPI Schema**: http://localhost:8000/api/schema/

---

## Best Practices

1. **Implement caching** for frequently accessed locations
2. **Use pagination** for large datasets
3. **Handle API errors** gracefully in frontend
4. **Validate input** before sending requests
5. **Use appropriate HTTP methods** (GET for retrieval, POST for creation)
6. **Follow rate limiting** when implemented

---

## Support

For API issues: support@yatrai.com  
Documentation: https://github.com/yatrai/docs
