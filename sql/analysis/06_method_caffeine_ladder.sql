-- 06 Brewing-method ladder ordered by brew time: LAG to the previous method, running coffee coverage.
-- LEFT JOIN keeps methods that no bean in the dataset maps to (coverage = 0).
-- Techniques: LEFT JOIN, LAG(), running SUM() OVER, CASE, CTE.
WITH coverage AS (
    SELECT m.brew_method_key, m.method_name, m.brew_time_min, m.caffeine_mg, m.caffeine_level, m.sleep_impact,
           COUNT(f.coffee_key) AS coffees_mapped
    FROM dim_brew_method m
    LEFT JOIN fact_coffee_rating f ON f.brew_method_key = m.brew_method_key
    GROUP BY m.brew_method_key
)
SELECT method_name, brew_time_min, caffeine_mg, caffeine_level, sleep_impact, coffees_mapped,
       LAG(method_name)   OVER w AS previous_faster_method,
       caffeine_mg - LAG(caffeine_mg) OVER w AS caffeine_change_vs_previous,
       SUM(coffees_mapped) OVER (ORDER BY brew_time_min, method_name ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                            AS running_coffees_mapped,
       CASE WHEN coffees_mapped = 0 THEN 'No beans in dataset' ELSE 'Covered' END AS coverage_status
FROM coverage
WINDOW w AS (ORDER BY brew_time_min, method_name)
ORDER BY brew_time_min, method_name;
