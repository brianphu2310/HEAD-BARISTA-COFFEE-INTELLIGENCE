-- 08 Does a bean's acidity label agree with the acidity score of the brewing method it is served with?
-- Method score is bucketed with the same three tiers as the bean label: <=3 Low, 4-6 Medium, >=7 High
-- (analyst-defined cut-offs). Techniques: join fact to dimension, CASE bucketing, conditional aggregation, CTE.
WITH pairs AS (
    SELECT f.coffee_key, m.method_name, f.acidity_level AS bean_acidity,
           CASE WHEN m.acidity_score <= 3 THEN 'Low'
                WHEN m.acidity_score <= 6 THEN 'Medium'
                ELSE 'High' END AS method_acidity_tier
    FROM fact_coffee_rating f
    JOIN dim_brew_method m ON m.brew_method_key = f.brew_method_key
)
SELECT method_name,
       COUNT(*)                                                        AS coffees,
       SUM(CASE WHEN bean_acidity = method_acidity_tier THEN 1 ELSE 0 END) AS matching_tier,
       ROUND(100.0 * SUM(CASE WHEN bean_acidity = method_acidity_tier THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_matching,
       MAX(method_acidity_tier)                                        AS method_acidity_tier
FROM pairs
GROUP BY method_name
ORDER BY pct_matching DESC, coffees DESC, method_name;
