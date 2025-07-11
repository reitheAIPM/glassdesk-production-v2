
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gmail messages table
CREATE TABLE gmail_messages (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    thread_id VARCHAR(255),
    subject TEXT,
    sender TEXT,
    recipient TEXT,
    date TIMESTAMP,
    snippet TEXT,
    body TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Zoom meetings table
CREATE TABLE zoom_meetings (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    topic TEXT,
    start_time TIMESTAMP,
    duration INTEGER,
    recording_files JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Asana tasks table
CREATE TABLE asana_tasks (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT,
    completed BOOLEAN,
    assignee TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
