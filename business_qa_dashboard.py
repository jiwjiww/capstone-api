import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import altair as alt  # ใช้สร้างกราฟ

# เชื่อมต่อกับ PostgreSQL ผ่าน SQLAlchemy
connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5432/aqi_project"
engine = create_engine(connection_string)

# ฟังก์ชันดึงข้อมูลจากฐานข้อมูล
def get_data_from_sql(query, params=None):
    try:
        connection = engine.raw_connection()
        df = pd.read_sql_query(query, con=connection, params=params)
        connection.close()
        return df
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
        return pd.DataFrame()  # คืนค่า DataFrame ว่างถ้ามีข้อผิดพลาด

# ฟังก์ชันแสดงข้อมูลบน Streamlit Dashboard
def show_dashboard():
    st.title("📊 รายงานคุณภาพอากาศ (AQI)")

    # ให้ผู้ใช้เลือกจังหวัด
    cities = ['Bangkok', 'Nakhon Pathom', 'Pathum Thani']
    selected_city = st.selectbox("เลือกจังหวัด:", cities)

    queries = {
        "ค่าฝุ่น AQI สูงสุดของสัปดาห์นี้": """
            SELECT MAX(aqi_value) AS highest_aqi
            FROM aqi_data
            WHERE timestamp >= NOW() - INTERVAL '7 days' 
            AND city = %(city)s;
        """,
        "ค่าฝุ่น AQI ต่ำสุดในช่วง 3 เดือนที่ผ่านมา": """
            SELECT MIN(aqi_value) AS lowest_aqi
            FROM aqi_data
            WHERE timestamp >= NOW() - INTERVAL '3 months' 
            AND city = %(city)s;
        """,
        "ค่าเฉลี่ย AQI ของสัปดาห์นี้": """
            SELECT AVG(aqi_value) AS avg_aqi
            FROM aqi_data
            WHERE timestamp >= NOW() - INTERVAL '7 days' 
            AND city = %(city)s;
        """,
        "นับจำนวนวันที่ AQI เกิน 100 ในเดือนนี้": """
            SELECT COUNT(*) AS days_high_aqi
            FROM aqi_data
            WHERE aqi_value > 100
            AND timestamp >= DATE_TRUNC('month', NOW()) 
            AND city = %(city)s;
        """,
    }

    # แสดงผลลัพธ์จาก Query
    for question, query in queries.items():
        st.subheader(question)
        df = get_data_from_sql(query, {"city": selected_city})
        if not df.empty:
            st.write(df)
        else:
            st.write("ไม่พบข้อมูล")

    # ✅ **ข้อที่ 5: แสดงกราฟ AQI รายวัน**
    st.subheader(f"📈 ค่า AQI ของแต่ละวันในสัปดาห์นี้ ({selected_city})")
    
    # คำสั่ง SQL ที่ใช้ดึงข้อมูล AQI รายวัน
    query_graph = """
        SELECT DATE(timestamp) AS date, AVG(aqi_value) AS avg_aqi
        FROM aqi_data
        WHERE timestamp >= NOW() - INTERVAL '7 days'  
        AND city = %(city)s
        GROUP BY DATE(timestamp)
        ORDER BY date;
    """
    
    df_graph = get_data_from_sql(query_graph, {"city": selected_city})
    
    if not df_graph.empty:
        # ใช้ Altair วาดกราฟ
        chart = alt.Chart(df_graph).mark_line(point=True).encode(
            x="date:T",
            y="avg_aqi:Q",
            tooltip=["date:T", "avg_aqi:Q"]
        ).properties(title="แนวโน้มค่า AQI รายวัน")

        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("ไม่พบข้อมูล")

if __name__ == "__main__":
    show_dashboard()
