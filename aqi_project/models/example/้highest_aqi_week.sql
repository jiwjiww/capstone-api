-- models/highest_aqi_week.sql
SELECT MAX(aqi_value) AS highest_aqi 
FROM aqi_data 
WHERE timestamp >= NOW() - INTERVAL '7 days'
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani');

