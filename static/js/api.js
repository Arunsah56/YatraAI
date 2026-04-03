/**
 * API.js - Reusable API Functions
 * Handles all backend API interactions with error handling and response standardization
 */

const API = {
    // Base URL - adjust based on your Django server
    BASE_URL: window.location.origin,

    /**
     * Get CSRF token from cookies
     */
    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    /**
     * Make a GET request to the API
     * @param {string} endpoint - API endpoint (e.g., '/api/locations/')
     * @param {object} params - Query parameters
     * @returns {Promise<object>} Response data
     */
    async get(endpoint, params = {}) {
        const url = new URL(`${this.BASE_URL}${endpoint}`);
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

        try {
            const response = await fetch(url.toString(), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('GET Error:', error);
            throw error;
        }
    },

    /**
     * Make a POST request to the API
     * @param {string} endpoint - API endpoint
     * @param {object} data - Request body data
     * @returns {Promise<object>} Response data
     */
    async post(endpoint, data = {}) {
        try {
            const response = await fetch(`${this.BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.error || errorData.detail || `HTTP ${response.status}`;
                throw new Error(errorMessage);
            }

            return await response.json();
        } catch (error) {
            console.error('POST Error:', error);
            throw error;
        }
    },

    /**
     * Make a PUT request to the API
     * @param {string} endpoint - API endpoint
     * @param {object} data - Request body data
     * @returns {Promise<object>} Response data
     */
    async put(endpoint, data = {}) {
        try {
            const response = await fetch(`${this.BASE_URL}${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.error || errorData.detail || `HTTP ${response.status}`;
                throw new Error(errorMessage);
            }

            return await response.json();
        } catch (error) {
            console.error('PUT Error:', error);
            throw error;
        }
    },

    /**
     * Make a DELETE request to the API
     * @param {string} endpoint - API endpoint
     * @returns {Promise<object>} Response data
     */
    async delete(endpoint) {
        try {
            const response = await fetch(`${this.BASE_URL}${endpoint}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (!response.ok && response.status !== 204) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.error || errorData.detail || `HTTP ${response.status}`;
                throw new Error(errorMessage);
            }

            return response.status === 204 ? {} : await response.json();
        } catch (error) {
            console.error('DELETE Error:', error);
            throw error;
        }
    },

    // ============= ITINERARY ENDPOINTS =============

    /**
     * Generate a new itinerary from user preferences
     * @param {object} preferences - Itinerary generation parameters
     * @returns {Promise<object>} Generated itinerary
     */
    async generateItinerary(preferences) {
        return this.post('/api/itinerary/generate/', preferences);
    },

    /**
     * Get a specific itinerary by ID
     * @param {number} id - Itinerary ID
     * @returns {Promise<object>} Itinerary data
     */
    async getItinerary(id) {
        return this.get(`/api/itinerary/${id}/`);
    },

    /**
     * Get all itineraries (paginated)
     * @param {number} page - Page number
     * @param {number} limit - Items per page
     * @returns {Promise<object>} List of itineraries
     */
    async listItineraries(page = 1, limit = 10) {
        return this.get('/api/itinerary/', { page, limit });
    },

    // ============= LOCATION ENDPOINTS =============

    /**
     * Get all locations
     * @param {number} limit - Number of results
     * @returns {Promise<object>} List of locations
     */
    async getLocations(limit = 20) {
        return this.get('/api/locations/', { limit });
    },

    /**
     * Search locations
     * @param {string} query - Search query
     * @returns {Promise<object>} Search results
     */
    async searchLocations(query) {
        return this.get('/api/locations/', { search: query });
    },

    /**
     * Get location details
     * @param {number} id - Location ID
     * @returns {Promise<object>} Location data
     */
    async getLocation(id) {
        return this.get(`/api/locations/${id}/`);
    },

    // ============= HIDDEN GEMS ENDPOINTS =============

    /**
     * Get hidden gems
     * @param {number} limit - Number of results
     * @param {string} location - Filter by location
     * @returns {Promise<object>} List of hidden gems
     */
    async getHiddenGems(limit = 20, location = null) {
        const params = { limit };
        if (location) params.location = location;
        return this.get('/api/hidden-gems/', params);
    },

    /**
     * Get hidden gem details
     * @param {number} id - Hidden gem ID
     * @returns {Promise<object>} Hidden gem data
     */
    async getHiddenGem(id) {
        return this.get(`/api/hidden-gems/${id}/`);
    },

    // ============= LOCAL EXPERIENCES ENDPOINTS =============

    /**
     * Get local experiences
     * @param {number} limit - Number of results
     * @param {string} category - Filter by category
     * @returns {Promise<object>} List of experiences
     */
    async getLocalExperiences(limit = 20, category = null) {
        const params = { limit };
        if (category) params.category = category;
        return this.get('/api/local-experiences/', params);
    },

    /**
     * Get experience details
     * @param {number} id - Experience ID
     * @returns {Promise<object>} Experience data
     */
    async getLocalExperience(id) {
        return this.get(`/api/local-experiences/${id}/`);
    },

    // ============= SEASONAL TIPS ENDPOINTS =============

    /**
     * Get seasonal tips
     * @param {number} limit - Number of results
     * @param {string} season - Filter by season
     * @returns {Promise<object>} List of seasonal tips
     */
    async getSeasonalTips(limit = 20, season = null) {
        const params = { limit };
        if (season) params.season = season;
        return this.get('/api/seasonal-tips/', params);
    },

    /**
     * Get seasonal tip details
     * @param {number} id - Seasonal tip ID
     * @returns {Promise<object>} Seasonal tip data
     */
    async getSeasonalTip(id) {
        return this.get(`/api/seasonal-tips/${id}/`);
    },

    // ============= BUDGET TIPS ENDPOINTS =============

    /**
     * Get budget tips
     * @param {number} limit - Number of results
     * @param {string} budget_level - Filter by budget level
     * @returns {Promise<object>} List of budget tips
     */
    async getBudgetTips(limit = 20, budget_level = null) {
        const params = { limit };
        if (budget_level) params.budget_level = budget_level;
        return this.get('/api/budget-tips/', params);
    },

    /**
     * Get budget tip details
     * @param {number} id - Budget tip ID
     * @returns {Promise<object>} Budget tip data
     */
    async getBudgetTip(id) {
        return this.get(`/api/budget-tips/${id}/`);
    },

    // ============= TRANSPORT OPTIONS ENDPOINTS =============

    /**
     * Get transport options
     * @param {number} limit - Number of results
     * @param {string} from_location - From location
     * @param {string} to_location - To location
     * @returns {Promise<object>} List of transport options
     */
    async getTransportOptions(limit = 20, from_location = null, to_location = null) {
        const params = { limit };
        if (from_location) params.from_location = from_location;
        if (to_location) params.to_location = to_location;
        return this.get('/api/transport-options/', params);
    },

    /**
     * Get transport option details
     * @param {number} id - Transport option ID
     * @returns {Promise<object>} Transport option data
     */
    async getTransportOption(id) {
        return this.get(`/api/transport-options/${id}/`);
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
