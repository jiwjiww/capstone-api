CREATE TABLE aqi_data (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    aqi_value INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

CREATE TABLE location (
    city TEXT PRIMARY KEY,
    country TEXT NOT NULL
);
