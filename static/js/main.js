/**
 * Main.js - Utility Functions
 * Common DOM manipulation, formatting, and helper functions used across the application
 */

const Utils = {
    // ============= DOM UTILITIES =============

    /**
     * Safely get element by ID
     * @param {string} id - Element ID
     * @returns {HTMLElement|null} Element or null if not found
     */
    getElement(id) {
        return document.getElementById(id) || null;
    },

    /**
     * Get all elements matching selector
     * @param {string} selector - CSS selector
     * @param {Element} parent - Parent element (default: document)
     * @returns {HTMLElement[]} Array of matching elements
     */
    getElements(selector, parent = document) {
        return Array.from(parent.querySelectorAll(selector));
    },

    /**
     * Show element
     * @param {HTMLElement|string} element - Element or ID
     */
    show(element) {
        if (typeof element === 'string') element = this.getElement(element);
        if (element) element.style.display = '';
    },

    /**
     * Hide element
     * @param {HTMLElement|string} element - Element or ID
     */
    hide(element) {
        if (typeof element === 'string') element = this.getElement(element);
        if (element) element.style.display = 'none';
    },

    /**
     * Toggle element visibility
     * @param {HTMLElement|string} element - Element or ID
     */
    toggle(element) {
        if (typeof element === 'string') element = this.getElement(element);
        if (element) {
            element.style.display = element.style.display === 'none' ? '' : 'none';
        }
    },

    /**
     * Add class to element
     * @param {HTMLElement|string} element - Element or ID
     * @param {string} className - Class name to add
     */
    addClass(element, className) {
        if (typeof element === 'string') element = this.getElement(element);
        if (element) element.classList.add(className);
    },

    /**
     * Remove class from element
     * @param {HTMLElement|string} element - Element or ID
     * @param {string} className - Class name to remove
     */
    removeClass(element, className) {
        if (typeof element === 'string') element = this.getElement(element);
        if (element) element.classList.remove(className);
    },

    /**
     * Toggle class on element
     * @param {HTMLElement|string} element - Element or ID
     * @param {string} className - Class name to toggle
     */
    toggleClass(element, className) {
        if (typeof element === 'string') element = this.getElement(element);
        if (element) element.classList.toggle(className);
    },

    /**
     * Check if element has class
     * @param {HTMLElement|string} element - Element or ID
     * @param {string} className - Class name to check
     * @returns {boolean} True if element has class
     */
    hasClass(element, className) {
        if (typeof element === 'string') element = this.getElement(element);
        return element ? element.classList.contains(className) : false;
    },

    /**
     * Set element text content
     * @param {HTMLElement|string} element - Element or ID
     * @param {string} text - Text to set
     */
    setText(element, text) {
        if (typeof element === 'string') element = this.getElement(element);
        if (element) element.textContent = text;
    },

    /**
     * Get element text content
     * @param {HTMLElement|string} element - Element or ID
     * @returns {string} Text content
     */
    getText(element) {
        if (typeof element === 'string') element = this.getElement(element);
        return element ? element.textContent : '';
    },

    /**
     * Set element HTML content
     * @param {HTMLElement|string} element - Element or ID
     * @param {string} html - HTML to set (sanitization should be done externally)
     */
    setHTML(element, html) {
        if (typeof element === 'string') element = this.getElement(element);
        if (element) element.innerHTML = html;
    },

    // ============= FORM UTILITIES =============

    /**
     * Get form input value
     * @param {string} inputId - Input element ID
     * @returns {string|boolean|string[]} Input value
     */
    getInputValue(inputId) {
        const input = this.getElement(inputId);
        if (!input) return '';

        if (input.type === 'checkbox') {
            return input.checked;
        } else if (input.type === 'radio') {
            const checked = document.querySelector(`input[name="${input.name}"]:checked`);
            return checked ? checked.value : '';
        } else if (input.tagName === 'SELECT') {
            if (input.multiple) {
                return Array.from(input.options)
                    .filter(opt => opt.selected)
                    .map(opt => opt.value);
            }
            return input.value;
        } else {
            return input.value || '';
        }
    },

    /**
     * Set form input value
     * @param {string} inputId - Input element ID
     * @param {any} value - Value to set
     */
    setInputValue(inputId, value) {
        const input = this.getElement(inputId);
        if (!input) return;

        if (input.type === 'checkbox') {
            input.checked = Boolean(value);
        } else if (input.type === 'radio') {
            const radio = document.querySelector(`input[name="${input.name}"][value="${value}"]`);
            if (radio) radio.checked = true;
        } else if (input.tagName === 'SELECT' && input.multiple) {
            Array.from(input.options).forEach(opt => {
                opt.selected = Array.isArray(value) ? value.includes(opt.value) : value === opt.value;
            });
        } else {
            input.value = value || '';
        }
    },

    /**
     * Clear form input
     * @param {string} inputId - Input element ID
     */
    clearInput(inputId) {
        const input = this.getElement(inputId);
        if (input) {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = false;
            } else {
                input.value = '';
            }
        }
    },

    /**
     * Disable form input
     * @param {string} inputId - Input element ID
     */
    disableInput(inputId) {
        const input = this.getElement(inputId);
        if (input) input.disabled = true;
    },

    /**
     * Enable form input
     * @param {string} inputId - Input element ID
     */
    enableInput(inputId) {
        const input = this.getElement(inputId);
        if (input) input.disabled = false;
    },

    /**
     * Get all form values
     * @param {string} formId - Form element ID
     * @returns {object} Key-value pairs of form inputs
     */
    getFormValues(formId) {
        const form = this.getElement(formId);
        if (!form) return {};

        const values = {};
        const inputs = form.querySelectorAll('[name]');

        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                if (input.checked) {
                    values[input.name] = input.value;
                }
            } else if (input.type === 'radio') {
                if (input.checked) {
                    values[input.name] = input.value;
                }
            } else if (input.tagName === 'SELECT' && input.multiple) {
                values[input.name] = this.getInputValue(input.id);
            } else if (input.value) {
                values[input.name] = input.value;
            }
        });

        return values;
    },

    // ============= FORMATTING UTILITIES =============

    /**
     * Format number as currency (NPR)
     * @param {number} value - Amount to format
     * @param {boolean} symbol - Include symbol (default: true)
     * @returns {string} Formatted currency string
     */
    formatCurrency(value, symbol = true) {
        const formatted = Math.round(value).toLocaleString('en-US');
        return symbol ? `NPR ${formatted}` : formatted;
    },

    /**
     * Format date
     * @param {Date|string} date - Date to format
     * @param {string} format - Format pattern (e.g., 'DD/MM/YYYY', 'DD MMM YYYY')
     * @returns {string} Formatted date
     */
    formatDate(date, format = 'DD/MM/YYYY') {
        if (typeof date === 'string') date = new Date(date);
        if (!(date instanceof Date)) return '';

        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();

        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const monthName = months[date.getMonth()];

        return format
            .replace('DD', day)
            .replace('MM', month)
            .replace('YYYY', year)
            .replace('MMM', monthName);
    },

    /**
     * Format time
     * @param {string|number} time - Time to format (HH:MM format)
     * @returns {string} Formatted time with AM/PM
     */
    formatTime(time) {
        if (!time) return '';
        const [hours, minutes] = time.split(':');
        const h = parseInt(hours);
        const m = parseInt(minutes);
        const ampm = h >= 12 ? 'PM' : 'AM';
        const displayHours = h % 12 || 12;
        return `${displayHours}:${String(m).padStart(2, '0')} ${ampm}`;
    },

    /**
     * Truncate text
     * @param {string} text - Text to truncate
     * @param {number} maxLength - Max length
     * @param {string} suffix - Suffix for truncated text (default: '...')
     * @returns {string} Truncated text
     */
    truncate(text, maxLength = 100, suffix = '...') {
        if (!text || text.length <= maxLength) return text;
        return text.substring(0, maxLength) + suffix;
    },

    /**
     * Format duration in hours and minutes
     * @param {number} minutes - Duration in minutes
     * @returns {string} Formatted duration
     */
    formatDuration(minutes) {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;

        if (hours === 0) return `${mins}m`;
        if (mins === 0) return `${hours}h`;
        return `${hours}h ${mins}m`;
    },

    // ============= STORAGE UTILITIES =============

    /**
     * Save data to localStorage
     * @param {string} key - Storage key
     * @param {any} value - Value to store
     */
    saveToStorage(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Storage error:', e);
        }
    },

    /**
     * Get data from localStorage
     * @param {string} key - Storage key
     * @param {any} defaultValue - Default value if not found
     * @returns {any} Stored value or default
     */
    getFromStorage(key, defaultValue = null) {
        try {
            const value = localStorage.getItem(key);
            return value ? JSON.parse(value) : defaultValue;
        } catch (e) {
            console.error('Storage error:', e);
            return defaultValue;
        }
    },

    /**
     * Remove data from localStorage
     * @param {string} key - Storage key
     */
    removeFromStorage(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Storage error:', e);
        }
    },

    /**
     * Clear all localStorage
     */
    clearAllStorage() {
        try {
            localStorage.clear();
        } catch (e) {
            console.error('Storage error:', e);
        }
    },

    // ============= NOTIFICATION UTILITIES =============

    /**
     * Show toast notification
     * @param {string} message - Message to display
     * @param {string} type - Type ('success', 'error', 'info', 'warning')
     * @param {number} duration - Duration in ms (default: 3000)
     */
    showToast(message, type = 'info', duration = 3000) {
        const toastContainer = document.getElementById('toastContainer') || this.createToastContainer();
        const toast = document.createElement('div');

        const bgColor = {
            'success': '#28a745',
            'error': '#dc3545',
            'info': '#17a2b8',
            'warning': '#ffc107'
        }[type] || '#17a2b8';

        toast.style.cssText = `
            background: ${bgColor};
            color: white;
            padding: 1rem 1.5rem;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            animation: slideInRight 0.3s ease;
        `;

        toast.textContent = message;
        toastContainer.appendChild(toast);

        if (duration > 0) {
            setTimeout(() => {
                toast.remove();
            }, duration);
        }

        return toast;
    },

    /**
     * Create toast container
     * @returns {HTMLElement} Container element
     */
    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(container);
        return container;
    },

    // ============= VALIDATION UTILITIES =============

    /**
     * Validate email
     * @param {string} email - Email to validate
     * @returns {boolean} True if valid
     */
    isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },

    /**
     * Validate phone number
     * @param {string} phone - Phone number to validate
     * @returns {boolean} True if valid
     */
    isValidPhone(phone) {
        const regex = /^(\+?\d{1,3}[-.\s]?)?\d{7,15}$/;
        return regex.test(phone);
    },

    /**
     * Validate URL
     * @param {string} url - URL to validate
     * @returns {boolean} True if valid
     */
    isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    },

    /**
     * Check if string is empty
     * @param {string} value - String to check
     * @returns {boolean} True if empty
     */
    isEmpty(value) {
        return !value || value.trim() === '';
    },

    // ============= ASYNC UTILITIES =============

    /**
     * Delay execution (sleep)
     * @param {number} ms - Milliseconds to wait
     * @returns {Promise<void>}
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    /**
     * Retry async function with exponential backoff
     * @param {Function} fn - Async function to retry
     * @param {number} maxAttempts - Max number of attempts
     * @param {number} delay - Initial delay in ms
     * @returns {Promise<any>} Function result
     */
    async retry(fn, maxAttempts = 3, delay = 1000) {
        for (let i = 0; i < maxAttempts; i++) {
            try {
                return await fn();
            } catch (error) {
                if (i === maxAttempts - 1) throw error;
                await this.sleep(delay * Math.pow(2, i));
            }
        }
    }
};

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Utils;
}
