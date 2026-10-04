-- 01 Origin leaderboard: average rating per origin vs the overall average, ranked.
-- Techniques: CTE, window AVG() OVER () benchmark, RANK() and DENSE_RANK().
WITH origin AS (
    SELECT origin, continent, COUNT(*) AS coffees, AVG(rating) AS avg_rating, MAX(rating) AS best_rating
    FROM vw_coffee_flat
    GROUP BY origin, continent
)
SELECT origin, continent, coffees,
       ROUND(avg_rating, 2)                                      AS avg_rating,
       best_rating,
       ROUND(avg_rating - (SELECT AVG(rating) FROM vw_coffee_flat), 2) AS vs_overall_avg,
       RANK() OVER (ORDER BY avg_rating DESC)                    AS rank_by_avg,
       DENSE_RANK() OVER (ORDER BY best_rating DESC)             AS dense_rank_by_best
FROM origin
ORDER BY rank_by_avg, origin;
