-- 04 Rating distribution: quartile, percentile rank and cumulative distribution for each coffee.
-- Techniques: NTILE(), PERCENT_RANK(), CUME_DIST(), CASE labelling.
SELECT coffee_name, origin, rating,
       NTILE(4) OVER (ORDER BY rating DESC)                  AS quartile_1_is_top,
       ROUND(PERCENT_RANK() OVER (ORDER BY rating), 3)       AS percent_rank,
       ROUND(CUME_DIST() OVER (ORDER BY rating), 3)          AS cume_dist,
       CASE WHEN rating >= 90 THEN 'Top tier'
            WHEN rating >= 85 THEN 'Upper middle'
            ELSE 'Lower' END                                 AS tier
FROM vw_coffee_flat
ORDER BY rating DESC, coffee_name;
