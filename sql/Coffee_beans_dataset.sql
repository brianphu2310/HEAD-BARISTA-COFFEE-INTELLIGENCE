
DROP TABLE IF EXISTS coffee_beans CASCADE;

CREATE TABLE coffee_beans (
    id SERIAL PRIMARY KEY,
    coffee_name TEXT NOT NULL,
    origin TEXT NOT NULL,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    roast_level TEXT,
    processing_method TEXT,
    brew_method TEXT,
    acidity TEXT,
    body TEXT,
    sweetness TEXT,
    flavor_notes TEXT,
    rating INTEGER
);


INSERT INTO coffee_beans (coffee_name, origin, latitude, longitude, roast_level, processing_method, brew_method, acidity, body, sweetness, flavor_notes, rating) VALUES
('Ethiopia Yirgacheffe', 'Ethiopia', 9.03, 38.74, 'Light', 'Washed', 'Pour Over', 'High', 'Light', 'High', 'floral, jasmine, citrus', 94),
('Ethiopia Sidamo', 'Ethiopia', 6.14, 38.84, 'Light', 'Washed', 'Aeropress', 'High', 'Light', 'High', 'berry, lemon, tea-like', 92),
('Kenya AA', 'Kenya', -0.02, 37.90, 'Light', 'Washed', 'Pour Over', 'High', 'Medium', 'High', 'berry, citrus', 91),
('Kenya Peaberry', 'Kenya', -0.52, 35.27, 'Light', 'Washed', 'Chemex', 'High', 'Medium', 'High', 'bright, fruity, grape', 90),
('Colombia Supremo', 'Colombia', 4.57, -74.30, 'Medium', 'Washed', 'French Press', 'Medium', 'Medium', 'Medium', 'chocolate, nutty', 88),
('Colombia Geisha', 'Colombia', 4.57, -74.30, 'Medium', 'Washed', 'Pour Over', 'Medium', 'Medium', 'High', 'floral, jasmine', 95),
('Costa Rica Tarrazu', 'Costa Rica', 9.75, -83.75, 'Medium', 'Honey', 'Cold Brew', 'Medium', 'Medium', 'High', 'fruity, bright', 89),
('Costa Rica Naranjo', 'Costa Rica', 10.05, -84.23, 'Medium', 'Honey', 'Clever Dripper', 'Medium', 'Medium', 'High', 'orange, chocolate', 88),
('Sumatra Mandheling', 'Indonesia', 2.53, 98.68, 'Dark', 'Wet Hulled', 'Espresso', 'Low', 'Full', 'Medium', 'earthy, spicy', 85),
('Sumatra Lintong', 'Indonesia', 2.37, 98.83, 'Dark', 'Wet Hulled', 'Moka Pot', 'Low', 'Full', 'Medium', 'earthy, mushroom', 84),
('Java Preanger', 'Indonesia', -7.40, 107.60, 'Dark', 'Wet Hulled', 'Turkish Coffee', 'Low', 'Full', 'Low', 'earthy, tobacco', 83),
('Vietnam Robusta', 'Vietnam', 14.06, 108.28, 'Dark', 'Natural', 'Vietnamese Phin', 'Low', 'Full', 'Low', 'earthy, bitter, dark chocolate', 78),
('Vietnam Arabica', 'Vietnam', 12.24, 108.57, 'Medium', 'Washed', 'Drip Machine', 'Medium', 'Medium', 'Medium', 'chocolate, nutty', 82),
('Brazil Santos', 'Brazil', -14.24, -51.93, 'Medium', 'Natural', 'Pour Over', 'Medium', 'Medium', 'Medium', 'nutty, chocolate', 84),
('Brazil Cerrado', 'Brazil', -18.33, -48.13, 'Medium', 'Natural', 'French Press', 'Medium', 'Full', 'Medium', 'chocolate, nutty', 85),
SELECT * FROM coffee_beans;
