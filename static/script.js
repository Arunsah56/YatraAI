// Form Handling
const searchForm = document.getElementById('searchForm');
if (searchForm) {
  searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const destination = document.getElementById('destination').value;
    const duration = document.getElementById('duration').value;
    const interests = document.getElementById('interests').value;
    const budget = document.getElementById('budget').value;
    
    if (!destination || !duration || !interests) {
      alert('Please fill in all required fields');
      return;
    }
    
    // Show loading state
    const submitBtn = searchForm.querySelector('button');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<div class="spinner"></div>';
    
    try {
      const response = await fetch('/generate-itinerary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          destination,
          duration: parseInt(duration),
          interests,
          budget
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        displayItinerary(data);
      } else {
        alert('Error generating itinerary. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    }
  });
}

// Display Itinerary Results
function displayItinerary(data) {
  const resultsContainer = document.getElementById('resultsContainer');
  if (!resultsContainer) {
    window.location.href = '/results?destination=' + encodeURIComponent(data.destination);
    return;
  }
  
  let html = `
    <div class="itinerary-header">
      <h2>Your ${data.duration}-Day Adventure in ${data.destination}</h2>
      <p>Personalized itinerary tailored to your interests: ${data.interests}</p>
    </div>
  `;
  
  if (data.itinerary && Array.isArray(data.itinerary)) {
    data.itinerary.forEach((day, index) => {
      html += `
        <div class="day-card">
          <h3>Day ${index + 1}</h3>
          <ul>
      `;
      
      if (Array.isArray(day)) {
        day.forEach(activity => {
          html += `<li>${activity}</li>`;
        });
      } else if (typeof day === 'string') {
        html += `<li>${day}</li>`;
      }
      
      html += `
          </ul>
        </div>
      `;
    });
  }
  
  resultsContainer.innerHTML = html;
  resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Tab Switching
function switchTab(tabName) {
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabButtons.forEach(button => {
    button.classList.remove('active');
  });
  
  tabContents.forEach(content => {
    content.classList.remove('active');
  });
  
  event.target.classList.add('active');
  document.getElementById(tabName).classList.add('active');
}

// Dark Mode Toggle (Optional)
const darkModeToggle = localStorage.getItem('darkMode') === 'true';
if (darkModeToggle) {
  document.body.style.backgroundColor = '#1a1a1a';
  document.body.style.color = '#fff';
}

// Analytics Tracking (Optional)
function trackEvent(eventName, eventData) {
  console.log(`Event: ${eventName}`, eventData);
  // Send to analytics service
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  // Add any initialization code here
  console.log('YatraAI Frontend Ready');
});
