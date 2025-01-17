CREATE SCHEMA IF NOT EXISTS authguard_service;
SET search_path TO authguard_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
GRANT USAGE ON SCHEMA authguard_service TO authguard_user;
GRANT CREATE ON SCHEMA authguard_service TO authguard_user;
GRANT SELECT,
    INSERT,
    UPDATE,
    DELETE ON ALL TABLES IN SCHEMA authguard_service TO authguard_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA authguard_service
GRANT SELECT,
    INSERT,
    UPDATE,
    DELETE ON TABLES TO authguard_user;
CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    action VARCHAR(255) NOT NULL,
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE OR REPLACE FUNCTION log_user_updates() RETURNS TRIGGER AS $$ BEGIN
INSERT INTO audit_logs (user_id, action, action_timestamp)
VALUES (
        OLD.user_id,
        'Session updated',
        CURRENT_TIMESTAMP
    );
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER log_user_update_trigger
AFTER
UPDATE ON sessions FOR EACH ROW EXECUTE FUNCTION log_user_updates();
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM sessions
    WHERE token = 'test_token'
) THEN
INSERT INTO sessions (
        session_id,
        user_id,
        token,
        created_at,
        expires_at
    )
VALUES (
        uuid_generate_v4(),
        '00000000-0000-0000-0000-000000000000',
        'test_token',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP + INTERVAL '1 hour'
    );
END IF;
END $$;