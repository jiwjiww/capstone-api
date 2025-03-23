SELECT MAX(aqi_value) AS highest_aqi 
FROM {{ source('dpu', 'aqi_data') }} 
WHERE timestamp >= NOW() - INTERVAL '7 days';
