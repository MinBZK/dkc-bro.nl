SELECT concat (rule_object_type, rule_id) as Regel,
    count(*) AS Totaal,
    sum(
        case
            when result = 't' then 1
            else 0
        end
    ) AS Geslaagd,
    sum(
        case
            when result = 'f' then 1
            else 0
        end
    ) AS Mislukt
FROM finding
WHERE timestamp > CURRENT_DATE - INTERVAL '3 months'
GROUP BY (rule_object_type, rule_id)
ORDER BY Totaal DESC;
/ / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
SELECT concat (object_type, id) as Regel,
    explanation AS uitleg
FROM rule;
/ / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
SELECT count(distinct(batch_id))
FROM finding
WHERE timestamp > CURRENT_DATE - INTERVAL '3 months';