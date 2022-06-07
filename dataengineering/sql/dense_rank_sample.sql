SELECT
    customerId, 
    totalSales, 
    DENSE_RANK() OVER (ORDER BY totalSales DESC) as rank
FROM
    customers