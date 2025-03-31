CREATE TABLE aqi_data (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    aqi_value INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

CREATE TABLE location (
    city TEXT PRIMARY KEY,
    country TEXT NOT NULL
);

-- เพิ่มข้อมูลจังหวัดที่ต้องการ
INSERT INTO location (city, country) VALUES 
    ('Bangkok', 'Thailand'),
    ('Nakhon Pathom', 'Thailand'),
    ('Pathum Thani', 'Thailand');
