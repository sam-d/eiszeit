CREATE TABLE ice (
    id INT NOT NULL UNIQUE PRIMARY KEY,
    name VARCHAR(255),
    lat DECIMAL(12,8),
    lon DECIMAL(12,8),
    country VARCHAR(255)
);

