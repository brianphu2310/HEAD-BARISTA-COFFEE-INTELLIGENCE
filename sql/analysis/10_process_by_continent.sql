-- 10 Processing method share and average rating within each continent.
-- Techniques: GROUP BY, window SUM() OVER (PARTITION BY) for within-continent share, RANK() within partition.
SELECT continent, processing_method,
       COUNT(*)                                                                  AS coffees,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY continent), 1)  AS pct_of_continent,
       ROUND(AVG(rating), 2)                                                     AS avg_rating,
       RANK() OVER (PARTITION BY continent ORDER BY AVG(rating) DESC)            AS rating_rank_in_continent
FROM vw_coffee_flat
GROUP BY continent, processing_method
ORDER BY continent, rating_rank_in_continent, processing_method;
