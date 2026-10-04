-- 09 For each origin: its best-rated coffee, how far it sits above the origin's average, and the origin's range.
-- Techniques: FIRST_VALUE(), window AVG/MIN/MAX over a partition, de-duplication with ROW_NUMBER().
WITH w AS (
    SELECT origin, coffee_name, brew_method, rating,
           FIRST_VALUE(coffee_name) OVER (PARTITION BY origin ORDER BY rating DESC, coffee_name) AS best_coffee,
           AVG(rating) OVER (PARTITION BY origin)  AS origin_avg,
           MIN(rating) OVER (PARTITION BY origin)  AS origin_min,
           MAX(rating) OVER (PARTITION BY origin)  AS origin_max,
           ROW_NUMBER() OVER (PARTITION BY origin ORDER BY rating DESC, coffee_name) AS rn
    FROM vw_coffee_flat
)
SELECT origin, best_coffee, brew_method AS served_with, rating AS best_rating,
       ROUND(rating - origin_avg, 2) AS above_origin_avg,
       origin_min, origin_max, origin_max - origin_min AS rating_spread
FROM w
WHERE rn = 1
ORDER BY best_rating DESC, origin;
