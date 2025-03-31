-- models/daily_avg_aqi_week.sql
SELECT DATE(timestamp) AS date, AVG(aqi_value) AS avg_aqi
FROM aqi_data 
WHERE timestamp >= NOW() - INTERVAL '7 days'
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani')
GROUP BY DATE(timestamp)
ORDER BY date;