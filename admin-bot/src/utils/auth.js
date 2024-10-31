const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const config = require('../config');

class AuthService {
    constructor() {
        this.token = null;
        this.tokenExpiry = null;
    }

    // Vulnerable: Predictable service auth generation
    generateServiceAuth() {
        const timestamp = Math.floor(Date.now() / 1000);
        const signature = crypto
            .createHash('md5')
            .update(`${timestamp}${config.serviceAuthSecret}`)
            .digest('hex');
        return `${timestamp}-${signature}`;
    }

    // Vulnerable: Weak token validation
    isTokenValid() {
        if (!this.token || !this.tokenExpiry) return false;
        return Date.now() < this.tokenExpiry;
    }

    async login() {
        try {
            const response = await fetch(`${config.backendUrl}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: config.adminUsername,
                    password: config.adminPassword
                })
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            this.token = data.access_token;
            
            // Vulnerable: Long token expiry
            this.tokenExpiry = Date.now() + (24 * 60 * 60 * 1000); // 24 hours
            return this.token;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async getHeaders() {
        if (!this.isTokenValid()) {
            await this.login();
        }

        // Vulnerable: Predictable headers
        return {
            'Authorization': `Bearer ${this.token}`,
            'X-Service-Auth': this.generateServiceAuth(),
            'X-Frontend-Version': 'v1'
        };
    }
}

module.exports = new AuthService();