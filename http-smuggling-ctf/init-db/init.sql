CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_reported BOOLEAN DEFAULT FALSE,
    report_count INTEGER DEFAULT 0
);

-- Create admin user with password 'complex_admin_pass_123'
INSERT INTO users (username, password_hash, role) 
VALUES (
    'admin', 
    'pbkdf2:sha256:260000$gqNMLGnEtXX8fM73$b5c9d761e5a52774cdb9b4dff60423bd7f34560f85c6ef49345d220f896cf9ee',
    'admin'
);