# YatraAI Frontend Documentation

## Overview
The YatraAI frontend is a responsive, mobile-first web application that connects to the Django backend REST API. It provides a beautiful user interface for planning Nepal travel itineraries.

## Project Structure

```
templates/
├── base.html           # Master template with global styling and navigation
├── index.html          # Home page with itinerary planner form
├── results.html        # Display generated itineraries
└── explore.html        # Browse hidden gems, experiences, and seasonal tips

static/
├── css/
│   └── style.css       # Additional CSS (currently minimal, most in base.html)
└── js/
    ├── api.js          # Reusable API wrapper functions
    └── main.js         # Utility functions for DOM, formatting, storage
```

## Template Files

### base.html (Master Template)
**Purpose**: Foundation template for all pages; defines navigation, footer, and global styling.

**Key Features**:
- responsive Bootstrap 5 grid system
- Travel-themed color scheme (CSS variables)
- Google Fonts: Playfair Display (headings), Poppins (body text)
- Font Awesome icon integration
- Sticky navigation bar with links to Plan Trip, Explore, and API Docs
- Footer with quick links and information
- Complete component styling system

**CSS Color Variables**:
- `--primary-color`: #2d9b7a (Teal)
- `--secondary-color`: #f97316 (Orange)
- `--accent-color`: #06b6d4 (Cyan)
- `--dark-color`: #1a2332 (Navy)
- `--light-color`: #f5f5f5 (Light Gray)

**Component Styles Included**:
- Cards with hover lift effect
- Buttons with gradient background
- Form controls with focus states
- Badges for tags and labels
- Timelines for day-by-day display
- Activity cards with left border accent
- Loading spinner animation

**Responsive Breakpoints**:
- Mobile: Default (< 768px)
- Tablet: `col-md-*` (768px - 992px)
- Desktop: `col-lg-*` (> 992px)

### index.html (Home / Planner Page)
**Purpose**: Main entry point for users; allows planning a new itinerary.

**User Flow**:
1. User fills out 8-field form
2. Selects 1+ travel interests
3. Clicks "Generate" button
4. Loading spinner shown during API call
5. Redirected to results page with generated itinerary

**Form Fields**:
| Field | Type | Values | Required |
|-------|------|--------|----------|
| Destination | Select | 10 Nepal cities | Yes |
| Duration | Number | 1-30 days | Yes |
| Budget Level | Select | Low/Mid/Luxury | Yes |
| Group Size | Number | 1+ people | Yes |
| Travelers Type | Select | Solo/Couple/Family/Group | Yes |
| Interests | Multi-select | 8 options (tags) | Yes (min 1) |

**Travel Interests** (8 options):
- 🏔️ Adventure
- 🏛️ Culture
- ⛰️ Trekking
- 🧘 Relaxation
- ✨ Spiritual
- 🍜 Food
- 🌿 Nature
- 📸 Photography

**JavaScript Logic**:
- Dynamic interest tag generation with JavaScript Set tracking
- Form validation (interests minimum 1)
- Loading state management (spinner, button disable)
- Error handling with 5-second auto-hide
- Session storage for fallback

**API Integration**:
```javascript
// Uses API.generateItinerary(data) from api.js
// Sends POST request to /api/itinerary/generate/
// Stores response in sessionStorage
// Redirects to /page/results/{id}/
```

### results.html (Itinerary Display Page)
**Purpose**: Display generated itinerary with day-by-day breakdown.

**Features**:
- Header with trip title, duration, budget
- Budget breakdown sidebar (accommodation, meals, activities, transport, misc)
- Day-by-day itinerary cards with:
  - Day number with gradient background
  - Location name
  - Accommodation details and cost
  - Activities timeline with times and descriptions
  - Packing tips
  - Local insights
- Safety notes alert box
- Travel tips callout
- Emergency contact reference card
- Print/Save button
- "Plan Another Trip" button

**Layout**:
- Main content (8/12 columns): Days timeline
- Sidebar (4/12 columns, sticky): Budget breakdown, travel tips, emergency contacts

**Data Fetched From**:
```javascript
GET /api/itinerary/{id}/
```

**Dynamic Content Population**:
```javascript
// Itinerary object structure expected:
{
    id: number,
    title: string,
    number_of_days: number,
    group_size: number,
    budget_level_display: string,
    estimated_total_budget_npr: number,
    budget_breakdown: {
        accommodation: number,
        meals: number,
        activities: number,
        transport: number,
        miscellaneous: number
    },
    days: [{
        title: string,
        location_name: string,
        accommodation_name: string,
        accommodation_type_display: string,
        accommodation_estimated_cost_npr: number,
        activity_details: [{
            activity_type_display: string,
            name: string,
            description: string,
            time_start: string,
            time_end: string,
            tips: string,
            estimated_cost_npr: number
        }],
        packing_tips: string,
        local_tips: string
    }],
    ai_response: {
        safety_notes: string,
        travel_tips: [string]
    }
}
```

**Styling**:
- Day number boxes: 80x80px with gradient background
- Activity cards: Flex layout with icon and time column
- Budget items: Flex justify-between for label and value
- Sticky sidebar for always-visible budget info

### explore.html (Discovery Page)
**Purpose**: Browse and discover travel destinations, experiences, and seasonal information.

**Three Tabs**:
1. **Hidden Gems** - Browse off-the-beaten-path locations
2. **Local Experiences** - Discover activities and cultural experiences
3. **Seasonal Tips** - Learn best times to visit by season

**Hidden Gems Tab**:
- Grid layout (3 columns on desktop, 1 on mobile)
- Filter by location and difficulty level
- Card design with emoji placeholder image
- Star rating display (1-5 stars)
- "Learn More" button opens modal with details

**Local Experiences Tab**:
- List layout (full width)
- Category badges (Cultural, Adventure, Food, Wellness, Nature)
- Budget level indicator
- Duration estimate
- Max group size display
- Click to see modal with full description

**Seasonal Tips Tab**:
- 2-column grid (responsive)
- 4 seasons: Spring, Summer, Autumn, Winter
- Season emoji and icon
- Temperature range
- Best-for indicator
- Seasonal tips text

**API Calls**:
```javascript
GET /api/hidden-gems/?limit=20
GET /api/local-experiences/?limit=20
GET /api/seasonal-tips/?limit=20
```

**Modal for Details**:
- Bootstrap modal that populates dynamically
- Shows full description, location, category, budget, ratings
- Responsive and accessible

## JavaScript Files

### api.js (API Wrapper)
**Purpose**: Centralized API client for all backend communications.

**Features**:
- Automatic CSRF token management
- Standardized error handling
- Request/response standardization
- Automatic JSON encoding/decoding

**Core Methods**:
```javascript
API.get(endpoint, params)           // GET request
API.post(endpoint, data)            // POST request
API.put(endpoint, data)             // PUT request
API.delete(endpoint)                // DELETE request
API.getCsrfToken()                  // Get CSRF token from cookies
```

**Itinerary Endpoints**:
```javascript
API.generateItinerary(preferences)  // POST /api/itinerary/generate/
API.getItinerary(id)                // GET /api/itinerary/{id}/
API.listItineraries(page, limit)    // GET /api/itinerary/
```

**Location Endpoints**:
```javascript
API.getLocations(limit)             // GET /api/locations/
API.searchLocations(query)          // GET /api/locations/?search=query
API.getLocation(id)                 // GET /api/locations/{id}/
```

**Hidden Gems Endpoints**:
```javascript
API.getHiddenGems(limit, location)  // GET /api/hidden-gems/
API.getHiddenGem(id)                // GET /api/hidden-gems/{id}/
```

**Experiences & Tips Endpoints**:
```javascript
API.getLocalExperiences(limit, category)
API.getSeasonalTips(limit, season)
API.getBudgetTips(limit, budget_level)
API.getTransportOptions(limit, from, to)
```

**Error Handling**: All methods throw errors with meaningful messages from API responses.

### main.js (Utility Functions)
**Purpose**: Common utilities for DOM manipulation, formatting, storage, and validation.

**DOM Utilities**:
```javascript
Utils.getElement(id)                // Get element by ID
Utils.getElements(selector, parent)  // Get multiple elements
Utils.show/hide/toggle(element)     // Show/hide elements
Utils.addClass/removeClass/toggleClass(element, className)
Utils.setText/getText/setHTML(element, content)
```

**Form Utilities**:
```javascript
Utils.getInputValue(inputId)        // Get value from any input
Utils.setInputValue(inputId, value) // Set any input value
Utils.clearInput(inputId)           // Clear input
Utils.disableInput/enableInput(inputId)
Utils.getFormValues(formId)         // Get all form values as object
```

**Formatting Utilities**:
```javascript
Utils.formatCurrency(value, symbol)     // NPR formatting
Utils.formatDate(date, format)          // Date formatting
Utils.formatTime(time)                  // Time formatting (HH:MM → H:MM AM/PM)
Utils.truncate(text, maxLength, suffix) // Truncate text
Utils.formatDuration(minutes)           // Minutes → "Xh Ym"
```

**Storage Utilities**:
```javascript
Utils.saveToStorage(key, value)         // localStorage.setItem (JSON)
Utils.getFromStorage(key, defaultValue) // localStorage.getItem (JSON parse)
Utils.removeFromStorage(key)            // localStorage.removeItem
Utils.clearAllStorage()                 // localStorage.clear
```

**Notification Utilities**:
```javascript
Utils.showToast(message, type, duration) // Show toast notification
Utils.createToastContainer()             // Create toast container
```

**Validation Utilities**:
```javascript
Utils.isValidEmail(email)           // Email validation
Utils.isValidPhone(phone)           // Phone validation
Utils.isValidUrl(url)               // URL validation
Utils.isEmpty(value)                // Check if empty
```

**Async Utilities**:
```javascript
Utils.sleep(ms)                     // Wait/delay
Utils.retry(fn, maxAttempts, delay) // Retry with exponential backoff
```

### style.css (Additional Styles)
**Purpose**: Supplementary styles beyond base.html (currently minimal).

**Note**: Most styling is in base.html using inline `<style>` tag for simplicity.

## How It Works Together

### Page Load Flow
1. Browser loads page (renders base.html)
2. base.html loads Bootstrap, Font Awesome, Google Fonts
3. base.html loads `api.js` (API wrapper available globally)
4. base.html loads `main.js` (Utils available globally)
5. Page template (index.html, results.html, explore.html) renders
6. Page's JavaScript in `{% block extra_js %}` executes

### Form Submission Flow (index.html)
```
User fills form
    ↓
Clicks "Generate"
    ↓
JavaScript form submit handler validates
    ↓
Calls generateItinerary(formData)
    ↓
Uses API.generateItinerary(data)
    ↓
API makes POST /api/itinerary/generate/
    ↓
Response stored in sessionStorage
    ↓
Redirect to /page/results/{id}/
```

### Results Page Load (results.html)
```
Page loads
    ↓
Extract itinerary ID from URL
    ↓
Call API.getItinerary(id)
    ↓
renderItinerary(data)
    ↓
Generate day cards, budget breakdown
    ↓
Display formatted content
```

### Explore Page Load (explore.html)
```
Page loads
    ↓
Load hidden gems (tab 1 default)
    ↓
User clicks tab
    ↓
Load relevant data from API
    ↓
Populate grid/list layout
```

## Responsive Design

### Mobile First Approach
- Base styles apply to mobile (< 768px)
- Tablet mixins: `col-md-*` classes
- Desktop mixins: `col-lg-*` classes

### Key Responsive Breakpoints
- Mobile: < 768px (1 column layouts)
- Tablet: 768px - 992px (2 columns)
- Desktop: > 992px (3+ columns)

### Touch Friendly
- Buttons: Minimum 44px height for touch targets
- Form inputs: Full width on mobile, optimized on larger screens
- Cards: Stack vertically on mobile, side-by-side on desktop

## Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Bootstrap 5 CSS framework handles most compatibility
- ES6 JavaScript features (async/await, fetch API)

## Future Enhancements
- User authentication (Django auth)
- Save/export itinerary functionality
- Google Maps integration
- Share itinerary on social media
- Rating and review system
- Advanced filtering options
- Real-time notification system

## Performance Considerations
- API responses cached in sessionStorage when appropriate
- Lazy loading for image-heavy pages (explore page)
- Minified CSS and JavaScript (in production)
- CDN for Bootstrap and Font Awesome
- Responsive images with proper sizing

## Accessibility
- Semantic HTML structure
- ARIA labels for icons and buttons
- Keyboard navigation support
- High contrast color scheme
- Form validation messages
- Alt text for images (can be enhanced)

## Security
- CSRF token automatically added to POST requests by API wrapper
- XSS protection via textContent where applicable
- Input validation before API calls
- Django backend handles authentication and authorization
