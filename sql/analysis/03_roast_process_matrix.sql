-- 03 Roast x processing matrix: sample size, average rating, and gap vs the roast-level average.
-- Techniques: GROUP BY two dimensions, window AVG() OVER (PARTITION BY) comparison, RANK().
WITH cell AS (
    SELECT roast_level, roast_order, processing_method,
           COUNT(*) AS coffees, AVG(rating) AS avg_rating
    FROM vw_coffee_flat
    GROUP BY roast_level, roast_order, processing_method
)
SELECT roast_level, processing_method, coffees,
       ROUND(avg_rating, 2)                                                    AS avg_rating,
       ROUND(avg_rating - AVG(avg_rating) OVER (PARTITION BY roast_level), 2)  AS vs_roast_mean_of_cells,
       RANK() OVER (ORDER BY avg_rating DESC)                                  AS overall_rank
FROM cell
ORDER BY roast_order, avg_rating DESC, processing_method;
