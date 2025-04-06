import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import altair as alt
import folium
from streamlit_folium import folium_static

# เชื่อมต่อกับ PostgreSQL
connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5432/aqi_project"
engine = create_engine(connection_string)

def get_data_from_sql(query, params=None):
    try:
        connection = engine.raw_connection()
        df = pd.read_sql_query(query, con=connection, params=params)
        connection.close()
        return df
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
        return pd.DataFrame()

def show_dashboard():
    st.set_page_config(page_title="AQI Dashboard", layout="wide")
    st.title("📊 รายงานคุณภาพอากาศ (AQI)")
    
    # แสดงแผนที่ประเทศไทย
    st.subheader("🗺️ แผนที่คุณภาพอากาศประเทศไทย")
    m = folium.Map(location=[13.736717, 100.523186], zoom_start=7)  # ศูนย์กลางที่กรุงเทพฯ

    cities = {
        "Bangkok": [13.736717, 100.523186],
        "Nakhon Pathom": [13.819920, 100.062167],
        "Pathum Thani": [14.013813, 100.530457]
    }

    for city, coords in cities.items():
        folium.Marker(
            location=coords,
            popup=city,
            tooltip=f"เลือก {city}",
            icon=folium.Icon(color="blue")
        ).add_to(m)

    folium_static(m)
    
    selected_city = st.selectbox("🌍 เลือกจังหวัด:", list(cities.keys()))
    
    queries = {
        "🌡️ ค่าฝุ่น AQI สูงสุดของสัปดาห์นี้": """
            SELECT MAX(aqi_value) AS highest_aqi
            FROM aqi_data
            WHERE timestamp >= NOW() - INTERVAL '7 days' 
            AND city = %(city)s;
        """,
        "❄️ ค่าฝุ่น AQI ต่ำสุดในช่วง 3 เดือนที่ผ่านมา": """
            SELECT MIN(aqi_value) AS lowest_aqi
            FROM aqi_data
            WHERE timestamp >= NOW() - INTERVAL '3 months' 
            AND city = %(city)s;
        """,
        "📉 ค่าเฉลี่ย AQI ของสัปดาห์นี้": """
            SELECT ROUND(AVG(aqi_value), 2) AS avg_aqi
            FROM aqi_data
            WHERE timestamp >= NOW() - INTERVAL '7 days' 
            AND city = %(city)s;
        """,
        "⚠️ นับจำนวนวันที่ AQI เกิน 100 ในเดือนนี้": """
            SELECT COUNT(*) AS days_high_aqi
            FROM aqi_data
            WHERE aqi_value > 100
            AND timestamp >= DATE_TRUNC('month', NOW()) 
            AND city = %(city)s;
        """,
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    for col, (question, query) in zip([col1, col2, col3, col4], queries.items()):
        df = get_data_from_sql(query, {"city": selected_city})
        value = df.iloc[0, 0] if not df.empty and pd.notnull(df.iloc[0, 0]) else "ไม่มีข้อมูล"
        col.metric(question, value)
    
    st.subheader(f"📈 ค่า AQI ของแต่ละวันในสัปดาห์นี้ ({selected_city})")
    
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
        chart = alt.Chart(df_graph).mark_line(point=True).encode(
            x=alt.X("date:T", title="วันที่"),
            y=alt.Y("avg_aqi:Q", title="ค่าเฉลี่ย AQI"),
            tooltip=["date:T", "avg_aqi:Q"]
        ).properties(title="📌 แนวโน้มค่า AQI รายวัน")
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("⚠️ ไม่พบข้อมูลสำหรับสัปดาห์นี้")

if __name__ == "__main__":
    show_dashboard()