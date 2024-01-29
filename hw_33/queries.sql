--**Создание таблицы `city`**:
CREATE TABLE city (
    id INTEGER PRIMARY KEY,
    city_name VARCHAR(255),
    lat INT,
    lon INT,
    population INT,
    subject_id INT,
    district_id INT,
    FOREIGN KEY (subject_id) REFERENCES subject(id),
    FOREIGN KEY (district_id) REFERENCES district(id)
);

-- Создание индекса для `city_name`
CREATE INDEX idx_city_name ON city (city_name);

-- Создание таблицы `subject`
CREATE TABLE subject (
    id INTEGER PRIMARY KEY,
    subject_name TEXT UNIQUE
);

-- Создание таблицы `district`
CREATE TABLE district (
    id INTEGER PRIMARY KEY,
    district_name TEXT UNIQUE
);