-- models/avg_aqi_week.sql
SELECT AVG(aqi_value) AS avg_aqi 
FROM aqi_data 
WHERE timestamp >= NOW() - INTERVAL '7 days'
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani');
