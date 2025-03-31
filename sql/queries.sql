--1. ค่าฝุ่น AQI สูงสุดของสัปดาห์นี้ (สำหรับกรุงเทพฯ, นครปฐม และปทุมธานี)
SELECT MAX(aqi_value) AS highest_aqi 
FROM aqi_data 
WHERE timestamp >= NOW() - INTERVAL '7 days'
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani');

--2. ค่าฝุ่น AQI ต่ำสุดในช่วง 3 เดือนที่ผ่านมา (สำหรับกรุงเทพฯ, นครปฐม และปทุมธานี)
SELECT MIN(aqi_value) AS lowest_aqi 
FROM aqi_data 
WHERE timestamp >= NOW() - INTERVAL '3 months'
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani');

--3. ค่าเฉลี่ย AQI ของสัปดาห์นี้ (สำหรับกรุงเทพฯ, นครปฐม และปทุมธานี)
SELECT AVG(aqi_value) AS avg_aqi 
FROM aqi_data 
WHERE timestamp >= NOW() - INTERVAL '7 days'
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani');

--4. นับจำนวนวันที่ AQI เกิน 100 ในเดือนนี้ (สำหรับกรุงเทพฯ, นครปฐม และปทุมธานี)
SELECT COUNT(*) AS days_high_aqi 
FROM aqi_data 
WHERE aqi_value > 100 
AND timestamp >= DATE_TRUNC('month', NOW())
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani');

--5. ค่า AQI ของแต่ละวันในสัปดาห์นี้ (สำหรับกรุงเทพฯ, นครปฐม และปทุมธานี)
SELECT DATE(timestamp) AS date, AVG(aqi_value) AS avg_aqi
FROM aqi_data 
WHERE timestamp >= NOW() - INTERVAL '7 days'
AND city IN ('Bangkok', 'Nakhon Pathom', 'Pathum Thani')
GROUP BY DATE(timestamp)
ORDER BY date;