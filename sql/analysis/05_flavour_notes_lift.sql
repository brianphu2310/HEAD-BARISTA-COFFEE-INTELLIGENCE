-- 05 Flavour-note popularity and rating lift (many-to-many via the bridge table).
-- Techniques: multi-table join through bridge_coffee_flavor, HAVING, window RANK(), benchmark subquery.
SELECT fl.flavor_note,
       COUNT(*)                                              AS coffees,
       ROUND(AVG(f.rating), 2)                               AS avg_rating,
       ROUND(AVG(f.rating) - (SELECT AVG(rating) FROM fact_coffee_rating), 2) AS lift_vs_overall,
       RANK() OVER (ORDER BY AVG(f.rating) DESC)             AS rank_by_avg_rating,
       RANK() OVER (ORDER BY COUNT(*) DESC)                  AS rank_by_popularity
FROM bridge_coffee_flavor b
JOIN dim_flavor         fl ON fl.flavor_key = b.flavor_key
JOIN fact_coffee_rating f  ON f.coffee_key  = b.coffee_key
GROUP BY fl.flavor_note
HAVING COUNT(*) >= 3
ORDER BY rank_by_avg_rating, fl.flavor_note;
