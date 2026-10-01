
WITH coffee_data AS (
    SELECT 'Ethiopia Yirgacheffe' AS Coffee_Name, 'Ethiopia' AS Origin, 9.03 AS Latitude, 38.74 AS Longitude, 'Light' AS Roast_Level, 'Washed' AS Processing_Method, 'Pour Over' AS Brew_Method, 'High' AS Acidity, 'Light' AS Body, 'High' AS Sweetness, 'floral, jasmine, citrus' AS Flavor_Notes, 94 AS Rating UNION ALL
    SELECT 'Ethiopia Sidamo', 'Ethiopia', 6.14, 38.84, 'Light', 'Washed', 'Aeropress', 'High', 'Light', 'High', 'berry, lemon, tea-like', 92 UNION ALL
    SELECT 'Kenya AA', 'Kenya', -0.02, 37.90, 'Light', 'Washed', 'Pour Over', 'High', 'Medium', 'High', 'berry, citrus', 91 UNION ALL
    SELECT 'Kenya Peaberry', 'Kenya', -0.52, 35.27, 'Light', 'Washed', 'Chemex', 'High', 'Medium', 'High', 'bright, fruity, grape', 90 UNION ALL
    SELECT 'Colombia Supremo', 'Colombia', 4.57, -74.30, 'Medium', 'Washed', 'French Press', 'Medium', 'Medium', 'Medium', 'chocolate, nutty', 88 UNION ALL
    SELECT 'Colombia Geisha', 'Colombia', 4.57, -74.30, 'Medium', 'Washed', 'Pour Over', 'Medium', 'Medium', 'High', 'floral, jasmine', 95 UNION ALL
    SELECT 'Costa Rica Tarrazu', 'Costa Rica', 9.75, -83.75, 'Medium', 'Honey', 'Cold Brew', 'Medium', 'Medium', 'High', 'fruity, bright', 89 UNION ALL
    SELECT 'Costa Rica Naranjo', 'Costa Rica', 10.05, -84.23, 'Medium', 'Honey', 'Clever Dripper', 'Medium', 'Medium', 'High', 'orange, chocolate', 88 UNION ALL
    SELECT 'Sumatra Mandheling', 'Indonesia', 2.53, 98.68, 'Dark', 'Wet Hulled', 'Espresso', 'Low', 'Full', 'Medium', 'earthy, spicy', 85 UNION ALL
    SELECT 'Sumatra Lintong', 'Indonesia', 2.37, 98.83, 'Dark', 'Wet Hulled', 'Moka Pot', 'Low', 'Full', 'Medium', 'earthy, mushroom', 84 UNION ALL
    SELECT 'Java Preanger', 'Indonesia', -7.40, 107.60, 'Dark', 'Wet Hulled', 'Turkish Coffee', 'Low', 'Full', 'Low', 'earthy, tobacco', 83 UNION ALL
    SELECT 'Vietnam Robusta', 'Vietnam', 14.06, 108.28, 'Dark', 'Natural', 'Vietnamese Phin', 'Low', 'Full', 'Low', 'earthy, bitter, dark chocolate', 78 UNION ALL
    SELECT 'Vietnam Arabica', 'Vietnam', 12.24, 108.57, 'Medium', 'Washed', 'Drip Machine', 'Medium', 'Medium', 'Medium', 'chocolate, nutty', 82 UNION ALL
    SELECT 'Brazil Santos', 'Brazil', -14.24, -51.93, 'Medium', 'Natural', 'Pour Over', 'Medium', 'Medium', 'Medium', 'nutty, chocolate', 84 UNION ALL
    SELECT 'Brazil Cerrado', 'Brazil', -18.33, -48.13, 'Medium', 'Natural', 'French Press', 'Medium', 'Full', 'Medium', 'chocolate, nutty', 85 UNION ALL
    SELECT 'Guatemala Antigua', 'Guatemala', 14.58, -90.52, 'Medium', 'Washed', 'Aeropress', 'Medium', 'Medium', 'High', 'chocolate, caramel', 87 UNION ALL
    SELECT 'Guatemala Huehuetenango', 'Guatemala', 15.47, -91.47, 'Medium', 'Washed', 'Chemex', 'High', 'Medium', 'High', 'bright, fruity', 88 UNION ALL
    SELECT 'Tanzania Peaberry', 'Tanzania', -6.29, 34.78, 'Light', 'Washed', 'Siphon', 'High', 'Light', 'High', 'bright, fruity, winey', 90 UNION ALL
    SELECT 'Mexico Chiapas', 'Mexico', 16.54, -92.74, 'Medium', 'Washed', 'French Press', 'Medium', 'Medium', 'Medium', 'chocolate, nutty', 86 UNION ALL
    SELECT 'Mexico Oaxaca', 'Mexico', 17.40, -96.50, 'Medium', 'Natural', 'Nel Drip', 'Medium', 'Full', 'High', 'fruity, chocolate', 87 UNION ALL
    SELECT 'India Monsooned Malabar', 'India', 13.19, 75.42, 'Dark', 'Monsooned', 'French Press', 'Low', 'Full', 'Low', 'earthy, spice, spicy', 82 UNION ALL
    SELECT 'India Mysore', 'India', 12.30, 76.65, 'Medium', 'Washed', 'Aeropress', 'Medium', 'Full', 'Medium', 'chocolate, nutty', 83 UNION ALL
    SELECT 'Jamaica Blue Mountain', 'Jamaica', 18.11, -77.30, 'Medium', 'Washed', 'Espresso', 'Medium', 'Medium', 'High', 'smooth, floral, nutty', 96 UNION ALL
    SELECT 'Hawaii Kona', 'USA', 19.90, -155.58, 'Medium', 'Washed', 'Pour Over', 'Medium', 'Medium', 'High', 'nutty, buttery, smooth', 94 UNION ALL
    SELECT 'Panama Geisha', 'Panama', 8.88, -80.60, 'Medium', 'Washed', 'Pour Over', 'High', 'Medium', 'High', 'floral, jasmine, bergamot', 96 UNION ALL
    SELECT 'Rwanda Bourbon', 'Rwanda', -1.94, 29.87, 'Light', 'Washed', 'Pour Over', 'High', 'Medium', 'High', 'cherry, floral', 89 UNION ALL
    SELECT 'Peru Chanchamayo', 'Peru', -10.94, -75.40, 'Medium', 'Washed', 'Clever Dripper', 'Medium', 'Medium', 'Medium', 'fruity, chocolate', 86 UNION ALL
    SELECT 'Bolivia Caranavi', 'Bolivia', -15.67, -67.57, 'Medium', 'Washed', 'Aeropress', 'Medium', 'Medium', 'High', 'caramel, fruity', 87 UNION ALL
    SELECT 'Papua New Guinea', 'Papua New Guinea', -6.16, 146.00, 'Medium', 'Washed', 'Drip Machine', 'Medium', 'Full', 'Medium', 'fruity, chocolate', 86 UNION ALL
    SELECT 'Thailand Doi Chang', 'Thailand', 19.97, 99.36, 'Medium', 'Washed', 'Cold Brew', 'Medium', 'Medium', 'High', 'fruity, floral', 85 UNION ALL
    SELECT 'Myanmar Ywangan', 'Myanmar', 21.89, 95.98, 'Medium', 'Washed', 'Moka Pot', 'Medium', 'Medium', 'High', 'chocolate, spice', 84 UNION ALL
    SELECT 'Uganda Bugisu', 'Uganda', 1.37, 34.35, 'Medium', 'Washed', 'French Press', 'Medium', 'Full', 'Medium', 'chocolate, berry', 84
),

brewing_methods AS (
    SELECT 'Ristretto' AS Method, 0.37 AS Brew_Time_min, 127 AS Caffeine_mg, 4 AS Antioxidant_Rank, 5 AS Acidity, 8 AS Bitterness, 9 AS Body, 'High' AS Complexity, 80.1 AS Score_Index UNION ALL
    SELECT 'Espresso', 0.47, 124, 3, 6, 7, 9, 'High', 79.5 UNION ALL
    SELECT 'Lungo', 0.67, 186, 5, 3, 8, 6, 'High', 76.0 UNION ALL
    SELECT 'AeroPress', 1.5, 60, 1, 5, 4, 5, 'Low', 81.0 UNION ALL
    SELECT 'Siphon', 3.5, 150, 2, 7, 3, 5, 'High', 85.5 UNION ALL
    SELECT 'Turkish', 3.5, 180, 3, 3, 8, 8, 'High', 82.0 UNION ALL
    SELECT 'Moka Pot', 4, 548, 3, 4, 6, 8, 'Medium', 78.5 UNION ALL
    SELECT 'Pour Over', 4.5, 173, 2, 8, 3, 4, 'High', 87.0 UNION ALL
    SELECT 'French Press', 4.5, 186, 3, 4, 6, 8, 'Low', 80.0 UNION ALL
    SELECT 'Batch Brew', 5, 150, 2, 5, 4, 5, 'Low', 83.0 UNION ALL
    SELECT 'Vietnamese Phin', 6.5, 450, 3, 3, 6, 7, 'Low', 76.5 UNION ALL
    SELECT 'Cold Drip', 480, 75, 5, 2, 2, 5, 'Low', 89.0 UNION ALL
    SELECT 'Cold Brew', 1080, 560, 2, 2, 2, 6, 'Low', 74.0
),


method_mapping AS (
    SELECT 'Turkish Coffee' AS coffee_method, 'Turkish' AS brewing_method UNION ALL
    SELECT 'Drip Machine', 'Batch Brew' UNION ALL
    SELECT 'Chemex', 'Pour Over' UNION ALL
    SELECT 'Clever Dripper', 'Pour Over' UNION ALL
    SELECT 'Nel Drip', 'Pour Over' UNION ALL
    SELECT 'Vietnamese Phin', 'Vietnamese Phin' UNION ALL
    SELECT 'Moka Pot', 'Moka Pot' UNION ALL
    SELECT 'Siphon', 'Siphon' UNION ALL
    SELECT 'Cold Brew', 'Cold Brew' UNION ALL
    SELECT 'Espresso', 'Espresso' UNION ALL
    SELECT 'Pour Over', 'Pour Over' UNION ALL
    SELECT 'Aeropress', 'AeroPress' UNION ALL
    SELECT 'French Press', 'French Press' UNION ALL
    SELECT 'Turkish Coffee', 'Turkish' 
),

combined_data AS (
    SELECT 
        c.Coffee_Name,
        c.Origin,
        c.Latitude,
        c.Longitude,
        c.Roast_Level,
        c.Processing_Method,
        c.Brew_Method,
        c.Acidity,
        c.Body AS Body_Description,
        c.Sweetness,
        c.Flavor_Notes,
        c.Rating,
        b.Brew_Time_min,
        b.Caffeine_mg,
        b.Antioxidant_Rank,
        b.Bitterness,
        b.Body AS Brew_Body_Score,
        b.Complexity,
        b.Score_Index,
        -- Add calculated fields from the original Excel
        CASE 
            WHEN b.Caffeine_mg <= 75 THEN '🟢 Low'
            WHEN b.Caffeine_mg <= 150 THEN '🟡 Medium'
            ELSE '🔴 High'
        END AS Caffeine_Level,
        CASE 
            WHEN b.Caffeine_mg <= 75 THEN 'Won''t disrupt sleep'
            WHEN b.Caffeine_mg <= 200 THEN 'May affect sleep'
            ELSE 'Avoid after 2 PM'
        END AS Sleep_Impact
    FROM coffee_data c
    LEFT JOIN method_mapping m ON c.Brew_Method = m.coffee_method
    LEFT JOIN brewing_methods b ON m.brewing_method = b.Method
)

SELECT 
    Coffee_Name,
    Origin,
    Latitude,
    Longitude,
    Roast_Level,
    Processing_Method,
    Brew_Method,
    Acidity,
    Body_Description AS Body,
    Sweetness,
    Flavor_Notes,
    Rating
FROM combined_data
ORDER BY Rating DESC;

SELECT * FROM coffee_data;
