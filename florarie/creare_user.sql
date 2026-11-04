CREATE USER andreea WITH PASSWORD 'florarie';

GRANT CONNECT ON DATABASE florarie TO andreea;

ALTER ROLE andreea SET search_path = django, public;

GRANT USAGE, CREATE ON SCHEMA django TO andreea;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA django TO andreea;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA django TO andreea;
