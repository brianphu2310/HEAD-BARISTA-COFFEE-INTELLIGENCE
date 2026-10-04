-- 02 Top two coffees for each canonical brewing method (several bean labels map to one method).
-- Techniques: ROW_NUMBER() partitioned top-N, join to the method dimension, CTE.
WITH ranked AS (
    SELECT brew_method, coffee_name, origin, served_brew_method, rating,
           ROW_NUMBER() OVER (PARTITION BY brew_method ORDER BY rating DESC, coffee_name) AS rank_in_method,
           COUNT(*)     OVER (PARTITION BY brew_method)                                   AS coffees_for_method
    FROM vw_coffee_flat
)
SELECT brew_method, rank_in_method, coffee_name, origin, served_brew_method, rating, coffees_for_method
FROM ranked
WHERE rank_in_method <= 2
ORDER BY brew_method, rank_in_method;
