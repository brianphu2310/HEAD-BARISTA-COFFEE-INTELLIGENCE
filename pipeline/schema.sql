-- Star/snowflake warehouse model (SQLite).
-- Facts: one row per coffee bean listing. Dimensions: origin, roast, process, brew method, coffee, flavour (via bridge).
PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS vw_coffee_flat;
DROP TABLE IF EXISTS bridge_coffee_flavor;
DROP TABLE IF EXISTS fact_coffee_rating;
DROP TABLE IF EXISTS dim_flavor;
DROP TABLE IF EXISTS dim_coffee;
DROP TABLE IF EXISTS dim_brew_method;
DROP TABLE IF EXISTS dim_process;
DROP TABLE IF EXISTS dim_roast;
DROP TABLE IF EXISTS dim_origin;

CREATE TABLE dim_origin (
    origin_key     INTEGER PRIMARY KEY,
    origin_country TEXT NOT NULL UNIQUE,
    continent      TEXT NOT NULL
);

CREATE TABLE dim_roast (
    roast_key   INTEGER PRIMARY KEY,
    roast_level TEXT NOT NULL UNIQUE CHECK (roast_level IN ('Light', 'Medium', 'Dark')),
    roast_order INTEGER NOT NULL UNIQUE          -- 1 = lightest
);

CREATE TABLE dim_process (
    process_key       INTEGER PRIMARY KEY,
    processing_method TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_brew_method (
    brew_method_key   INTEGER PRIMARY KEY,
    method_name       TEXT NOT NULL UNIQUE,
    brew_time_min     REAL NOT NULL CHECK (brew_time_min > 0),
    caffeine_mg       INTEGER NOT NULL CHECK (caffeine_mg > 0),
    antioxidant_rank  INTEGER NOT NULL CHECK (antioxidant_rank BETWEEN 1 AND 5),
    acidity_score     INTEGER NOT NULL CHECK (acidity_score BETWEEN 1 AND 10),
    bitterness_score  INTEGER NOT NULL CHECK (bitterness_score BETWEEN 1 AND 10),
    body_score        INTEGER NOT NULL CHECK (body_score BETWEEN 1 AND 10),
    complexity        TEXT NOT NULL CHECK (complexity IN ('Low', 'Medium', 'High')),
    equipment         TEXT NOT NULL,
    quick_guide       TEXT NOT NULL,
    primary_taste     TEXT NOT NULL,
    caffeine_level    TEXT NOT NULL CHECK (caffeine_level IN ('Low', 'Medium', 'High')),
    sleep_impact      TEXT NOT NULL,
    score_index_excel REAL NOT NULL
);

CREATE TABLE dim_coffee (
    coffee_key    INTEGER PRIMARY KEY,
    coffee_name   TEXT NOT NULL UNIQUE,
    latitude      REAL NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude     REAL NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    latitude_band TEXT NOT NULL CHECK (latitude_band IN ('0-10', '10-20', '20+'))   -- absolute degrees
);

CREATE TABLE dim_flavor (
    flavor_key  INTEGER PRIMARY KEY,
    flavor_note TEXT NOT NULL UNIQUE
);

CREATE TABLE fact_coffee_rating (
    coffee_key          INTEGER PRIMARY KEY REFERENCES dim_coffee (coffee_key),
    origin_key          INTEGER NOT NULL REFERENCES dim_origin (origin_key),
    roast_key           INTEGER NOT NULL REFERENCES dim_roast (roast_key),
    process_key         INTEGER NOT NULL REFERENCES dim_process (process_key),
    brew_method_key     INTEGER NOT NULL REFERENCES dim_brew_method (brew_method_key),
    served_brew_method  TEXT    NOT NULL,       -- label as written in the beans data (before mapping)
    acidity_level       TEXT    NOT NULL CHECK (acidity_level IN ('Low', 'Medium', 'High')),
    body_level          TEXT    NOT NULL CHECK (body_level IN ('Light', 'Medium', 'Full')),
    sweetness_level     TEXT    NOT NULL CHECK (sweetness_level IN ('Low', 'Medium', 'High')),
    acidity_ord         INTEGER NOT NULL,       -- Low=1, Medium=2, High=3
    body_ord            INTEGER NOT NULL,       -- Light=1, Medium=2, Full=3
    sweetness_ord       INTEGER NOT NULL,       -- Low=1, Medium=2, High=3
    flavor_note_count   INTEGER NOT NULL CHECK (flavor_note_count >= 1),
    rating              INTEGER NOT NULL CHECK (rating BETWEEN 0 AND 100),
    rating_band         TEXT    NOT NULL CHECK (rating_band IN ('90+', '85-89', 'Below 85'))
);

CREATE TABLE bridge_coffee_flavor (
    coffee_key INTEGER NOT NULL REFERENCES dim_coffee (coffee_key),
    flavor_key INTEGER NOT NULL REFERENCES dim_flavor (flavor_key),
    PRIMARY KEY (coffee_key, flavor_key)
);

CREATE INDEX ix_fact_origin  ON fact_coffee_rating (origin_key);
CREATE INDEX ix_fact_roast   ON fact_coffee_rating (roast_key);
CREATE INDEX ix_fact_process ON fact_coffee_rating (process_key);
CREATE INDEX ix_fact_method  ON fact_coffee_rating (brew_method_key);
CREATE INDEX ix_fact_rating  ON fact_coffee_rating (rating);
CREATE INDEX ix_bridge_flavor ON bridge_coffee_flavor (flavor_key);

CREATE VIEW vw_coffee_flat AS
SELECT c.coffee_name, o.origin_country AS origin, o.continent, c.latitude, c.longitude, c.latitude_band,
       r.roast_level, r.roast_order, p.processing_method,
       f.served_brew_method, m.method_name AS brew_method,
       f.acidity_level, f.body_level, f.sweetness_level, f.acidity_ord, f.body_ord, f.sweetness_ord,
       f.flavor_note_count, f.rating, f.rating_band
FROM fact_coffee_rating f
JOIN dim_coffee       c ON c.coffee_key       = f.coffee_key
JOIN dim_origin       o ON o.origin_key       = f.origin_key
JOIN dim_roast        r ON r.roast_key        = f.roast_key
JOIN dim_process      p ON p.process_key      = f.process_key
JOIN dim_brew_method  m ON m.brew_method_key  = f.brew_method_key;
