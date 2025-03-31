-- models/days_high_aqi_month.sql
SELECT COUNT(*) AS days_high_aqi 
FROM aqi_data 
WHERE aqi_value > 100 
AND timestamp >= DATE_TRUNC('month', NOW())
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani');
