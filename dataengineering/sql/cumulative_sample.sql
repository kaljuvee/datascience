SELECT
    date, 
    monthlycosts, 
    SUM(monthlycosts) OVER (ORDER BY date) as cumCosts
FROM
    cost_table