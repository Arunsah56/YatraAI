# YatraAI Frontend - Quick Reference Guide

## 🎯 What's Available Now

### Three Beautiful Pages
1. **Home Page** (`/`) - Plan your trip with interactive form
2. **Results Page** (`/page/results/{id}/`) - View complete itinerary
3. **Explore Page** (`/explore/`) - Discover hidden gems and experiences

### Key Features ✨
- ✅ Fully responsive mobile-first design
- ✅ Beautiful travel-themed UI (Teal, Orange, Cyan)
- ✅ Live API integration with Django backend
- ✅ Loading spinners and error handling
- ✅ Budget breakdown calculator
- ✅ Day-by-day itinerary display
- ✅ Interest-based planning
- ✅ Search and filter capabilities

---

## 🚀 Getting Started

### Start the Server
```bash
cd c:\Users\sahar\Desktop\YatraAI
python manage.py runserver
```

### Access the App
```
http://localhost:8000/              # Home page
http://localhost:8000/explore/      # Explore page
http://localhost:8000/api/          # API docs
```

---

## 📋 Common Tasks

### Track User's Journey
1. User lands on home page
2. Fills out 8-field form
3. Selects travel interests (1+)
4. Clicks "Generate"
5. Waits for AI to create itinerary
6. Sees results with day-by-day plan
7. Check budget breakdown
8. Can plan another trip

### Understand the API Flow
```
Frontend (Browser)
    ↓
JavaScript API.js wrapper
    ↓
HTTP Request (CSRF token added)
    ↓
Django REST API
    ↓
OpenAI (if generation requested)
    ↓
Database
    ↓
JSON Response
    ↓
Frontend JavaScript renders
```

### Debug Issues
1. **Open DevTools**: F12 in browser
2. **Check Network Tab**: Watch API calls
3. **Check Console**: Look for JavaScript errors
4. **Check Elements**: Inspect HTML and CSS
5. **Check Application**: View localStorage

---

## 🎨 Design Reference

### Colors (Travel Theme)
```
🟢 Primary:    #2d9b7a (Teal - Mountains)
🟠 Secondary:  #f97316 (Orange - Adventure)
🔵 Accent:     #06b6d4 (Cyan - Water/Sky)
⬛ Dark:       #1a2332 (Navy)
⬜ Light:      #f5f5f5 (Gray)
```

### Typography
```
Headings:     Playfair Display (elegant, serif)
Body Text:    Poppins (clean, modern)
```

### Grid Breakpoints
```
Mobile:  < 768px   (1 column)
Tablet:  768-992px (2 columns)
Desktop: > 992px   (3+ columns)
```

---

## 💻 File Quick Reference

### Templates
| File | Purpose | Lines |
|------|---------|-------|
| base.html | Master with styles | 460 |
| index.html | Home planner form | 274 |
| results.html | Itinerary display | 400+ |
| explore.html | Browse destinations | 500+ |

### JavaScript
| File | Purpose | Lines |
|------|---------|-------|
| api.js | API wrapper functions | 250+ |
| main.js | Utility helpers | 350+ |

### Documentation
| File | Purpose |
|------|---------|
| FRONTEND_DOCUMENTATION.md | Comprehensive guide |
| FRONTEND_SETUP.md | Setup & testing |
| PROJECT_SUMMARY.md | Project overview |

---

## 🔧 Developer Tools

### Check If API Is Working
```javascript
// In browser console
API.getLocations(5).then(r => console.log(r))
// Should show list of locations
```

### Test Form Submission
```javascript
// In browser console
const testData = {
    destination: "Kathmandu",
    number_of_days: 5,
    budget_level: "mid",
    group_size: 2,
    travelers_type: "couple",
    interests: ["culture", "adventure"]
};
API.generateItinerary(testData).then(r => console.log(r))
```

### Check Utilities
```javascript
// In browser console
Utils.formatCurrency(50000, true)           // "NPR 50,000"
Utils.formatDate(new Date(), 'DD MMM YYYY') // "15 Jan 2024"
Utils.showToast("Test notification", "info") // Toast appears
```

### View Storage
```javascript
// In browser console
Utils.getFromStorage('lastItinerary')  // Get saved itinerary
localStorage.clear()                    // Clear all storage
```

---

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| API not responding | Backend not running | `python manage.py runserver` |
| CSRF token error | Missing header | Check API.getCsrfToken() |
| Styles look wrong | Cache issue | Ctrl+Shift+R |
| Icons not showing | Font Awesome not loaded | Check CDN |
| Form not submitting | Validation failing | Check console for errors |
| Blank results page | API error | Check Network tab |

---

## 📱 Responsive Testing

### Device Sizes to Test
```
iPhone 12:     390px width
iPad:          768px width  
Desktop:       1920px width
```

### How to Test in Browser
1. Open DevTools (F12)
2. Click mobile icon (top-left)
3. Select device or enter custom size
4. Refresh page

### What to Check
- [ ] Text readable on mobile
- [ ] Form inputs full width
- [ ] Buttons touch-friendly (44px+)
- [ ] Images scale correctly
- [ ] No horizontal scroll
- [ ] Navigation responds to screen size

---

## 🎯 Page-by-Page Guide

### Home Page (index.html)
**What User Sees**:
- Hero section with call-to-action
- Form with 8 input fields
- Clickable interest tags (8 options)
- Three info cards below form
- Loading spinner (hidden by default)
- Error alert (hidden by default)

**What Happens**:
1. User fills form
2. Clicks Generate
3. JavaScript validates form
4. API wrapper makes POST request
5. Loading spinner shows
6. On success: redirect to results
7. On error: show red alert

### Results Page (results.html)
**What User Sees**:
- Header with trip info
- Budget breakdown (sidebar on desktop)
- Day cards in timeline
- Activity list per day
- Packing tips per day
- Safety notes alert
- Emergency contacts
- Print button

**Information Displayed**:
- Itinerary title and days
- Total and daily budget
- Accommodation per day
- Activities with times
- Travel tips
- Local insights

### Explore Page (explore.html)
**What User Sees**:
- Tab navigation (3 tabs)
- Search/filter options
- Hidden gems grid (default)
- Modal for details
- Loading spinners while fetching

**Three Sections**:
1. Hidden Gems - Cards with ratings
2. Experiences - List with badges
3. Seasonal Tips - Seasonal info

---

## 🔗 API Endpoints Used

| Page | Endpoint | Method |
|------|----------|--------|
| Home | /api/itinerary/generate/ | POST |
| Results | /api/itinerary/{id}/ | GET |
| Explore | /api/hidden-gems/ | GET |
| Explore | /api/local-experiences/ | GET |
| Explore | /api/seasonal-tips/ | GET |

---

## 📊 Performance Tips

### For Users
- Wait message: "Generating your itinerary... (2-15 seconds)"
- Multiple clicks: Button disabled during loading
- Mobile: Works best on WiFi
- Cache: Browser caches page after first load

### For Developers
- AI generation takes 5-15 seconds (OpenAI)
- Results page loads in < 200ms
- Explore data loads in < 300ms
- Use browser DevTools Performance tab
- Monitor API response times

---

## 🔐 Security Notes

### What's Protected
- CSRF tokens on all POST requests
- Form validation on frontend
- Backend validation on all APIs
- Error messages don't expose details

### What's Not Yet Implemented
- User authentication
- Rate limiting
- File uploads
- Payment processing

---

## 📖 Documentation Map

```
Need to know about...       → Read this file
─────────────────────────────────────────────
Frontend architecture       → FRONTEND_DOCUMENTATION.md
Setting up & testing        → FRONTEND_SETUP.md
Project overview            → PROJECT_SUMMARY.md
Backend APIs                → API_DOCUMENTATION.md
Database structure          → DATABASE_SCHEMA.md
Deployment                  → DEPLOYMENT_GUIDE.md
```

---

## 🚀 What's Next?

### User Features (Phase 3)
- [ ] Save itineraries
- [ ] User accounts
- [ ] Share itineraries
- [ ] PDF export
- [ ] Map integration

### Developer Improvements
- [ ] Unit tests
- [ ] E2E tests
- [ ] Performance optimization
- [ ] SEO optimization
- [ ] PWA support

---

## 💡 Pro Tips

### Tip 1: Use DevTools Console
```javascript
// Quickly test any API method
API.getLocations().then(console.log)
Utils.showToast("Feature works!", "success")
```

### Tip 2: Check Network Requests
- F12 → Network tab
- Perform action
- Watch API calls in real-time
- Check response data

### Tip 3: Test on Mobile
- Use DevTools device emulation
- Or use actual phone on same WiFi
- Test different orientations
- Check touch interactions

### Tip 4: Monitor Performance
- F12 → Lighthouse tab
- Run audit
- Fix issues
- Retest

### Tip 5: Debug Styling
- F12 → Elements tab
- Inspect element
- Check computed styles
- Try changing live (Ctrl+` to edit)

---

## 📞 Quick Support

### Error: "API not responding"
```bash
# Check if server is running
python manage.py runserver

# Check browser console for details
# F12 → Console tab
```

### Error: "CSRF token missing"
```javascript
// Check if token is available
console.log(API.getCsrfToken())
// Should return a long string
```

### Results Page Blank
```javascript
// Check if itinerary loaded
console.log(sessionStorage.getItem('lastItinerary'))
// Should show itinerary data
```

---

## ✅ Launch Checklist

Before going live:
- [ ] Test all 3 pages in Chrome/Firefox/Safari
- [ ] Test on mobile device (actual phone)
- [ ] Run all API endpoints
- [ ] Check error handling
- [ ] Verify responsive design
- [ ] Test browser back button
- [ ] Test navigation links
- [ ] Check console for errors
- [ ] Verify CSS is loading
- [ ] Confirm icons displaying
- [ ] Test loading states
- [ ] Verify print button works

---

## 🎓 Learning Resources

### To Understand the Code
1. Read FRONTEND_DOCUMENTATION.md for architecture
2. Review base.html for CSS system
3. Study api.js for API patterns
4. Check main.js for utility functions
5. Look at index.html for form handling

### To Customize
1. Colors: Update :root CSS variables in base.html
2. Typography: Change font imports
3. Layout: Modify Bootstrap grid classes
4. Colors: All in one place (CSS variables)
5. API: Update base URL in api.js

---

## 🌟 Key Features Summary

| Feature | Status | Where |
|---------|--------|-------|
| Home form | ✅ Complete | index.html |
| Results display | ✅ Complete | results.html |
| Explore page | ✅ Complete | explore.html |
| Responsive | ✅ Complete | All pages |
| Mobile support | ✅ Complete | All pages |
| API integration | ✅ Complete | api.js |
| Error handling | ✅ Complete | All pages |
| Loading states | ✅ Complete | All pages |
| Beautiful UI | ✅ Complete | base.html |
| User auth | ⏳ Planned | Phase 3 |
| Save feature | ⏳ Planned | Phase 3 |

---

**Last Updated**: Phase 2 Complete ✅
**Version**: 2.0 (Frontend Ready)
**Status**: 🟢 Ready for Testing
