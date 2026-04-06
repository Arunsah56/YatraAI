# YatraAI Frontend - Setup & Testing Guide

## Quick Start

### Prerequisites
```
- Django 4.2+ (backend running)
- Python environment with all backend dependencies installed
- Modern browser (Chrome, Firefox, Safari, Edge)
```

### Running the Application

1. **Start Django Development Server**
```bash
# In the project root directory
python manage.py runserver
```

2. **Access the Application**
```
http://localhost:8000
```

3. **Navigation**
- Home (Plan Trip): `http://localhost:8000/`
- Explore: `http://localhost:8000/explore/`
- API Documentation: `http://localhost:8000/api/`

## File Structure Overview

### Frontend Files Created in Phase 2

**Templates** (3 HTML files):
```
templates/
├── base.html              (450 lines) - Master template with global styling
├── index.html             (274 lines) - Home page with planner form
├── results.html           (400+ lines) - Itinerary display page
└── explore.html           (500+ lines) - Hidden gems and experiences
```

**Static JavaScript** (2 files):
```
static/js/
├── api.js                 (250+ lines) - API wrapper functions
└── main.js                (350+ lines) - Utility functions
```

**Static CSS** (minimal):
```
static/css/
└── style.css              (empty/minimal) - Most styles in base.html
```

**Documentation** (2 files):
```
FRONTEND_DOCUMENTATION.md  - Comprehensive frontend guide
FRONTEND_SETUP.md          - This file
```

## Testing the Application

### Test Case 1: Home Page (index.html)
**Location**: `http://localhost:8000/`

**Steps**:
1. Page should load with hero section and form
2. Form has 8 fields visible
3. Interests should be displayed as clickable tags

**What to Check**:
- ✓ Responsive design on mobile/desktop
- ✓ Form inputs accept values
- ✓ Interest selection works (tags highlight when clicked)
- ✓ Submit button is enabled
- ✓ Colors match travel theme (teal, orange, cyan)

**Expected Behavior**:
```
User Action              Expected Result
─────────────────────────────────────────
Fill destination         5-8px padding input with focus state
Enter days              Number appears in field
Select budget           Option highlighted
Enter group size        Number appears
Select traveler type    Option highlighted
Click interests         Tags toggle on/off with background color
Click Generate          Loading spinner appears, button disables
API succeeds            Redirect to /page/results/{id}/
API fails               Red error alert appears, auto-hides after 5s
```

### Test Case 2: Results Page (results.html)
**Location**: `http://localhost:8000/page/results/{id}/` (after generating itinerary)

**Steps**:
1. Generate itinerary from home page
2. Automatically redirected after API response
3. View day-by-day itinerary

**What to Check**:
- ✓ Header shows correct title, duration, budget
- ✓ Budget breakdown displays correct amounts (sidebar)
- ✓ Day cards display with correct information
- ✓ Activities list shows all activities for each day
- ✓ Safety notes appear if present
- ✓ Travel tips display
- ✓ Emergency contacts visible
- ✓ Print button works
- ✓ Responsive layout on mobile

**Expected Behavior**:
```
Desktop View (>992px)           Mobile View (<768px)
─────────────────────           ─────────────────────
Content (8 cols)                Content (full width)
Sidebar (4 cols, fixed)         Sidebar below content
Horizontal layout               Vertical stack
Budget sticky on scroll         Budget scrolls
```

### Test Case 3: Explore Page (explore.html)
**Location**: `http://localhost:8000/explore/`

**Steps**:
1. Navigate to Explore page
2. Click through tabs
3. Search/filter options
4. Click on items to see details

**What to Check**:
- ✓ Hidden Gems tab loads and displays items
- ✓ Local Experiences tab accessible
- ✓ Seasonal Tips tab shows proper data
- ✓ Search filters work
- ✓ Modal opens with details
- ✓ Close modal functionality
- ✓ Loading spinners appear while fetching

**Tab Content**:
| Tab | Expected | Elements |
|-----|---------|----------|
| Hidden Gems | 3-col grid | Card image, title, location, rating, description |
| Experiences | List layout | Category badge, title, meta, description |
| Seasons | 2-col grid | Icon, title, months, info boxes |

### Test Case 4: API Integration
**Network Tab Test**:

1. **Open Browser DevTools** (F12)
2. **Go to Network Tab**
3. **Perform Actions** and watch requests:

**Expected API Calls**:
```
HOME PAGE (index.html)
POST /api/itinerary/generate/          ← Itinerary creation
Response: {data: {id: ..., ...}}

RESULTS PAGE (results.html)
GET /api/itinerary/{id}/                ← Fetch itinerary details
Response: {id: ..., title: ..., days: [...]}

EXPLORE PAGE (explore.html)
GET /api/hidden-gems/?limit=20          ← Hidden gems
GET /api/local-experiences/?limit=20    ← Experiences
GET /api/seasonal-tips/?limit=20        ← Seasonal tips
```

### Test Case 5: Responsive Design
**Mobile Testing**:

1. Open DevTools (F12)
2. Click device toggle (mobile icon in top-left)
3. Test different screen sizes:
   - iPhone 12 (390px)
   - iPad (768px)
   - Desktop (1920px)

**Check Points**:
```
Mobile (< 768px)
- Navigation collapses to hamburger
- 1-column layout for cards
- Form inputs full width
- Sidebar moves below content (results page)
- Text remains readable
- Buttons touch-friendly (44px+ height)

Tablet (768px - 992px)
- 2-column layouts for grids
- Navigation expands
- Sidebar visible with main content
- Spacing optimized

Desktop (> 992px)
- 3-column grids
- Full width utilization
- Sticky sidebar
- Horizontal navigation
```

## Console Errors to Check

**Open Browser Console** (F12 → Console tab)

**Expected State**: No errors (only warnings are acceptable)

**Common Issues to Debug**:

```javascript
// Issue: API not responding
Error: "Failed to load itinerary"
Fix: Ensure Django backend is running

// Issue: CSRF token missing
Error: "403 Forbidden"
Fix: Check API.getCsrfToken() is working

// Issue: Styles not loading
Symptom: Page renders unstyled
Fix: Check CSS paths, clear browser cache

// Issue: JavaScript errors
Appears in console
Fix: Check browser compatibility, look for syntax errors
```

## Performance Testing

### Page Load Time
**Steps**:
1. Open DevTools (F12)
2. Go to Performance tab
3. Click Record
4. Refresh page
5. Click Stop after page loads

**Targets**:
- First Contentful Paint (FCP): < 2 seconds
- Largest Contentful Paint (LCP): < 3 seconds
- Total Load: < 4 seconds

### API Response Time
**Expected Times**:
- `/api/itinerary/generate/`: 5-15 seconds (with AI processing)
- `/api/itinerary/{id}/`: < 200ms
- `/api/hidden-gems/`: < 300ms
- `/api/local-experiences/`: < 300ms

## Browser Compatibility

**Testing Checklist**:

| Browser | Version | Status | Notes |
|---------|---------|--------|-------|
| Chrome | Latest | ✓ Recommended | Best performance |
| Firefox | Latest | ✓ Supported | Excellent |
| Safari | Latest | ✓ Supported | Good |
| Edge | Latest | ✓ Supported | Good |
| Mobile Chrome | Latest | ✓ Tested | Mobile-first |
| Mobile Safari | Latest | ✓ Tested | iOS 14+ |

## Touch Events Testing

**Mobile Only**:
1. Test swipe/scroll functionality
2. Test button taps (no hover effects break)
3. Test form input focus on mobile keyboards
4. Test modal close on mobile

## Accessibility Testing

**Keyboard Navigation**:
```
Tab              - Move between form fields
Shift + Tab      - Move backward
Enter            - Submit form
Esc              - Close modal
Space            - Select checkbox
```

**Screen Reader**:
- Buttons have proper labels
- Form fields have associated labels
- Images have alt text
- Tab order is logical

## Common Issues & Solutions

### Issue: Form not submitting
**Symptoms**: Button click does nothing
**Solution**: 
- Check browser console for errors
- Verify API endpoint is correct
- Ensure Django server is running
- Check CSRF token is being sent

### Issue: Results page blank
**Symptoms**: Page loads but no content visible
**Solution**:
- Check Network tab for API errors
- Look at browser console for JavaScript errors
- Verify itinerary ID in URL
- Clear browser cache

### Issue: Styles look wrong
**Symptoms**: Colors off, layout broken, fonts wrong
**Solution**:
- Ctrl+Shift+R (hard refresh)
- Check CSS file is loading (Network tab)
- Verify Bootstrap CDN is accessible
- Check for CSS conflicts in browser

### Issue: Images/icons not showing
**Symptoms**: Blank spaces where icons should be
**Solution**:
- Check Font Awesome CDN is loading
- Verify emoji display support in browser
- Check image paths in CSS

## Deployment Checklist

Before deploying to production:

- [ ] Run Django tests: `python manage.py test`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Check DEBUG = False in settings.py
- [ ] Verify ALLOWED_HOSTS setting
- [ ] Test all API endpoints
- [ ] Verify CSRF token in production
- [ ] Test responsive design on real devices
- [ ] Check page load performance
- [ ] Verify error pages (404, 500)
- [ ] Test on multiple browsers
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure email for errors

## Development Tips

### Enable Django Debug Toolbar
```python
# For debugging API responses
pip install django-debug-toolbar
# Add to settings.py and urls.py
```

### Live Reload During Development
```bash
# Option 1: Use Django extensions
pip install django-extensions
python manage.py runserver --reload

# Option 2: Use VS Code Live Server extension
```

### Test API Directly
```bash
# Using curl
curl -X POST http://localhost:8000/api/itinerary/generate/ \
  -H "Content-Type: application/json" \
  -d '{"destination":"Kathmandu","number_of_days":5}'

# Using browser console
Utils.showToast("Testing", "info")
API.getLocations().then(r => console.log(r))
```

### Monitor API Calls
```javascript
// In browser console
// See all API calls made
API.get('/api/locations/')
API.post('/api/itinerary/generate/', {destination: 'Kathmandu'})
```

## Production Optimization

### Minification
```bash
# CSS minification
python manage.py compress

# JavaScript minification (use Terser in production build)
```

### Caching
```python
# Add browser caching headers
cache_control=max_age=86400  # 1 day

# Use CDN for static files
```

### Image Optimization
```bash
# Optimize images before production
for img in static/images/*; do
  convert $img -resize 1200x800 -quality 85 $img
done
```

## Maintenance

### Regular Updates
- [ ] Update Bootstrap to latest version
- [ ] Update Font Awesome version
- [ ] Monitor for security vulnerabilities
- [ ] Check Django version compatibility

### Monitor Performance
- [ ] Track page load times
- [ ] Monitor API response times
- [ ] Check error rates
- [ ] Analyze user behavior

### User Feedback
- [ ] Collect UI/UX feedback
- [ ] Track feature requests
- [ ] Monitor for bugs reported
- [ ] Iterate on design
