-- Drop existing tables if they exist
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS blog_posts CASCADE;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
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

-- Create admin and test users
INSERT INTO users (username, password_hash, role) 
VALUES 
    -- Admin user: admin:complex_admin_pass_123
    ('admin', 'pbkdf2:sha256:260000$gqNMLGnEtXX8fM73$b5c9d761e5a52774cdb9b4dff60423bd7f34560f85c6ef49345d220f896cf9ee', 'admin'),
    -- Regular user: user:user123
    ('user', 'pbkdf2:sha256:260000$xGXxUk8bxMyF$6dd684f90584b3af4280186d3468c8993159c20cd56995ff93d4f2f0c2607d45', 'user'),
    -- Test user: test:test123
    ('test', 'pbkdf2:sha256:260000$yHXzKv9bxNzG$7ee694f90584b3af4280186d3468c8993159c20cd56995ff93d4f2f0c2607e56', 'user');

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

-- Add some initial reports (optional, helps show the reporting feature)
UPDATE blog_posts 
SET report_count = 2, is_reported = true 
WHERE id = 2;