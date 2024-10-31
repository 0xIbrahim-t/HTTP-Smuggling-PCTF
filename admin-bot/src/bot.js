const puppeteer = require('puppeteer');
const auth = require('./utils/auth');
const config = require('./config');

class AdminBot {
    constructor() {
        this.browser = null;
        this.page = null;
    }

    async initialize() {
        try {
            this.browser = await puppeteer.launch(config.puppeteer);
            this.page = await this.browser.newPage();

            // Vulnerable: Accepts any SSL certificate
            await this.page.setBypassCSP(true);

            // Set admin cookie
            const headers = await auth.getHeaders();
            await this.page.setExtraHTTPHeaders(headers);

            console.log('Admin bot initialized');
        } catch (error) {
            console.error('Initialization error:', error);
            throw error;
        }
    }

    async reviewPost(postId) {
        try {
            // Vulnerable: No sanitization of post content
            await this.page.goto(
                `${config.frontendUrl}/post/${postId}`,
                { waitUntil: 'networkidle0', timeout: config.pageLoadTimeout }
            );

            // Vulnerable: Executes any JavaScript in the post
            await this.page.waitForTimeout(2000);

            // Mark as reviewed
            const headers = await auth.getHeaders();
            await fetch(`${config.backendUrl}/api/admin/posts/${postId}/review`, {
                method: 'POST',
                headers: headers
            });

            console.log(`Reviewed post ${postId}`);
        } catch (error) {
            console.error(`Error reviewing post ${postId}:`, error);
        }
    }

    async checkReports() {
        try {
            const headers = await auth.getHeaders();
            const response = await fetch(`${config.backendUrl}/api/admin/reports`, {
                headers: headers
            });

            if (!response.ok) {
                throw new Error('Failed to fetch reports');
            }

            const reports = await response.json();
            
            // Review each reported post
            for (const report of reports) {
                if (!report.reviewed) {
                    await this.reviewPost(report.post_id);
                }
            }
        } catch (error) {
            console.error('Error checking reports:', error);
        }
    }

    async start() {
        await this.initialize();
        
        // Vulnerable: Predictable review timing
        setInterval(async () => {
            await this.checkReports();
        }, config.reviewInterval);
    }
}

// Start the bot
const bot = new AdminBot();
bot.start().catch(error => {
    console.error('Bot startup error:', error);
    process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
    if (bot.browser) {
        await bot.browser.close();
    }
    process.exit(0);
});