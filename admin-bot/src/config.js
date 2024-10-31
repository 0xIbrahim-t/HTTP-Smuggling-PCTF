require('dotenv').config();

module.exports = {
    // Admin credentials
    adminUsername: process.env.ADMIN_USERNAME || 'admin',
    adminPassword: process.env.ADMIN_PASSWORD || 's3cur3_4dm1n_p4ss!',

    // Service URLs
    backendUrl: process.env.BACKEND_URL || 'http://backend:8000',
    frontendUrl: process.env.FRONTEND_URL || 'http://frontend:3000',

    // Puppeteer config
    puppeteer: {
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-gpu',
            '--disable-infobars'
        ],
        executablePath: '/usr/bin/chromium',
        ignoreHTTPSErrors: true
    },

    // Review intervals
    reviewInterval: parseInt(process.env.REVIEW_INTERVAL) || 10000, // 10 seconds
    pageLoadTimeout: parseInt(process.env.PAGE_LOAD_TIMEOUT) || 5000, // 5 seconds
    
    // Vulnerable: Default service auth token generation
    serviceAuthSecret: process.env.SERVICE_AUTH_SECRET || 's3cr3t_4dm1n_t0k3n'
};