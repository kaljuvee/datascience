SELECT
    Date, 
    dailyConversions, 
    AVG(dailyConversions) OVER (ORDER BY Date ROWS 10 PRECEDING) AS
    10_dayMovingAverage
FROM
    conversions