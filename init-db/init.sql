-- Drop existing tables if they exist
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS blog_posts CASCADE;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create blog_posts table
CREATE TABLE blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_reported BOOLEAN DEFAULT FALSE,
    report_count INTEGER DEFAULT 0
);

-- Create admin user with simple hash
INSERT INTO users (username, password_hash, role) 
VALUES 
    -- Admin user: username = admin, password = admin123
    ('admin', 'pbkdf2:sha256:150000$lw9PORKq$d32c87b7457d2c52d61e8348f4197c10353998e87ebca3f97005d9cb6527d8a7', 'admin'),
    
    -- Regular user: username = user, password = user123
    ('user', 'pbkdf2:sha256:150000$Q58zGcYA$062f0a8357d1aa0ad7367348f2f8550e1cf415ad14e698201ac29ceb450827b4', 'user'),
    
    -- Test user: username = test, password = test123
    ('test', 'pbkdf2:sha256:150000$NmT7fprf$2ce986094c45eea24aabd8d9838abe52387ebd51739c82d54d0c32cb110289b2', 'user');

-- Create initial blog posts
INSERT INTO blog_posts (title, content, author_id, created_at) 
VALUES 
    (
        'Welcome to Our Security Blog Platform',
        'Hello everyone! Welcome to our security blog platform. This is a place where we share insights about cybersecurity, best practices, and industry news. Stay tuned for more interesting articles and updates!

Feel free to explore our posts and engage with the content. If you notice any issues or have concerns about any post, please use the report feature.',
        1,  -- Posted by admin
        NOW() - INTERVAL '3 days'
    ),
    (
        'Understanding Web Security Headers',
        'Today, we''ll discuss important security headers that every web application should implement:

1. Content-Security-Policy (CSP)
2. X-Frame-Options
3. X-Content-Type-Options
4. Strict-Transport-Security

These headers help protect against various attacks including XSS, clickjacking, and protocol downgrade attacks. 

In our next post, we''ll dive deeper into each of these headers.',
        1,  -- Posted by admin
        NOW() - INTERVAL '2 days'
    ),
    (
        'Latest Platform Updates',
        'We''ve recently implemented several new features to improve your experience:

• Enhanced user authentication
• Improved caching mechanism
• New blog reporting system
• Updated admin dashboard

Please test these features and let us know if you encounter any issues. Your security is our top priority!

Note: Admin users now have additional privileges for content management.',
        1,  -- Posted by admin
        NOW() - INTERVAL '1 day'
    );

-- Add some initial reports
UPDATE blog_posts 
SET report_count = 2, is_reported = true 
WHERE id = 2;