-- create role
CREATE ROLE todoapp_user WITH CREATEDB LOGIN PASSWORD 'todoapp@786';

-- create main database
CREATE DATABASE todoapp_db WITH OWNER todoapp_user;

-- grant privileges
GRANT ALL PRIVILEGES ON DATABASE todoapp_db TO todoapp_user;

-- connect to database with todoapp_user
\c todoapp_db

-- create schema
CREATE SCHEMA todoapp AUTHORIZATION todoapp_user;


-- create user table
CREATE TABLE todoapp.tusertbl (
    user_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_tusertbl_email ON todoapp.tusertbl(email);
CREATE INDEX idx_tusertbl_name ON todoapp.tusertbl(name);

-- create task table
CREATE TABLE todoapp.ttasktbl (
    task_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES todoapp.tusertbl(user_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    due_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ttasktbl_user_id ON todoapp.ttasktbl(user_id);
CREATE INDEX idx_ttasktbl_due_date ON todoapp.ttasktbl(due_date);
CREATE INDEX idx_ttasktbl_is_completed ON todoapp.ttasktbl(is_completed);