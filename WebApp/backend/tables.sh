CREATE TABLE users (
    user_id UUID PRIMARY KEY NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    reset_token VARCHAR(50),
    reset_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_profiles (
    profile_id UUID PRIMARY KEY NOT NULL,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    profile_image_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE tasks (
    task_id UUID PRIMARY KEY NOT NULL,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    description VARCHAR(255) NOT NULL,
    due_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO users (user_id, username, email, password_hash)
VALUES (
    'b613bb6c-77e8-439d-890c-f9203f6bc70a',
    'testuser',
    'testuser@gmail.com',
    '$$2b$$12$$examplehash'
);
INSERT INTO users (user_id, username, email, password_hash)
VALUES (
    'b613bb6c-77e8-439d-890c-f9203f6bc70a',
    'userabc',
    'testuser@gmail.com',
    'abc123456'
);

INSERT INTO user_profiles (profile_id, user_id, first_name, last_name)
VALUES (
    '8c7d6bcf-1cbf-4202-9729-8f0acd833c41',
    'b613bb6c-77e8-439d-890c-f9203f6bc70a',
    'John',
    'Doe'
);