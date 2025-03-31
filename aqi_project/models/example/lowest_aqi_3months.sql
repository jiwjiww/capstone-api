-- models/lowest_aqi_3months.sql
SELECT MIN(aqi_value) AS lowest_aqi 
FROM aqi_data 
WHERE timestamp >= NOW() - INTERVAL '3 months'
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani');

