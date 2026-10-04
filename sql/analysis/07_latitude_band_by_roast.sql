-- 07 Coffees by absolute-latitude band (distance from the equator): count and average rating, pivoted by roast.
-- Techniques: conditional aggregation (CASE pivot), derived dimension attribute, grand-total row via UNION ALL.
WITH banded AS (
SELECT latitude_band,
       COUNT(*)                                                         AS coffees,
       ROUND(AVG(rating), 2)                                            AS avg_rating,
       SUM(CASE WHEN roast_level = 'Light'  THEN 1 ELSE 0 END)          AS light_roast,
       SUM(CASE WHEN roast_level = 'Medium' THEN 1 ELSE 0 END)          AS medium_roast,
       SUM(CASE WHEN roast_level = 'Dark'   THEN 1 ELSE 0 END)          AS dark_roast,
       ROUND(AVG(CASE WHEN roast_level = 'Light'  THEN rating END), 2)  AS avg_rating_light,
       ROUND(AVG(CASE WHEN roast_level = 'Medium' THEN rating END), 2)  AS avg_rating_medium,
       ROUND(AVG(CASE WHEN roast_level = 'Dark'   THEN rating END), 2)  AS avg_rating_dark
FROM vw_coffee_flat
GROUP BY latitude_band
UNION ALL
SELECT 'All coffees', COUNT(*), ROUND(AVG(rating), 2),
       SUM(roast_level = 'Light'), SUM(roast_level = 'Medium'), SUM(roast_level = 'Dark'),
       ROUND(AVG(CASE WHEN roast_level = 'Light'  THEN rating END), 2),
       ROUND(AVG(CASE WHEN roast_level = 'Medium' THEN rating END), 2),
       ROUND(AVG(CASE WHEN roast_level = 'Dark'   THEN rating END), 2)
FROM vw_coffee_flat
)
SELECT * FROM banded
ORDER BY latitude_band = 'All coffees', latitude_band;
