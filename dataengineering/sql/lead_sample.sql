with monthly_costs as (
    SELECT
        date, 
        monthlycosts, LEAD(monthlycosts) OVER (ORDER BY date) as
        previousCosts
    FROM
        costs
)
SELECT
     date, 
    (monthlycosts - previousCosts) / previousCosts * 100 AS costPercentChange
FROM monthly_costs