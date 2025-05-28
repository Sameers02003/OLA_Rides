import streamlit as st
import pandas as pd
import mysql.connector

# --- MySQL Database Connection ---
conn = mysql.connector.connect(
    host="localhost", 
    user="root",  
    password="Dijas@19110",  
    database="ola_rides"  
)
cursor = conn.cursor()

# --- Set Up Streamlit Page Layout ---
st.set_page_config(page_title="Ola Rides Dashboard", layout="wide")

# --- Sidebar Navigation ---
selected_page = st.sidebar.radio("Select Page", ["Home", "SQL Queries", "Summary Insights"])

# --- Home Page ---
if selected_page == "Home":
    st.title("🏠 Home - Overview & Key Metrics")
    st.write("Welcome! This dashboard provides insights into Ola ride trends, customer behaviors, and booking analytics.")

    # Query: Key Metrics
    query_metrics = """
    SELECT COUNT(DISTINCT booking_id) AS Total_Rides, 
           COUNT(DISTINCT customer_id) AS Total_Customers,
           ROUND(AVG(ride_distance), 2) AS Avg_Ride_Distance,
           COUNT(CASE WHEN booking_status = 'Canceled by driver' THEN 1 END) AS Total_Cancellations
    FROM ride_insights;
    """
    cursor.execute(query_metrics)
    df_metrics = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
    st.write("### 📊 Key Metrics")
    st.dataframe(df_metrics)

    # Query: Booking Trends Over Time
    query_trends = """
    SELECT YEAR(date) AS Year, MONTH(date) AS Month, COUNT(*) AS Total_Bookings
    FROM ride_insights
    GROUP BY Year, Month
    ORDER BY Year DESC, Month DESC;
    """
    cursor.execute(query_trends)
    df_trends = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
    st.write("### 📅 Booking Trends Over Time")
    st.line_chart(df_trends, x="Month", y="Total_Bookings", color="Year")

    # Query: Average Ride Distance by Vehicle Type
    query_distance = """
    SELECT vehicle_type, ROUND(AVG(ride_distance), 2) AS Avg_Ride_Distance
    FROM ride_insights
    GROUP BY vehicle_type;
    """
    cursor.execute(query_distance)
    df_distance = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
    st.write("### 🚘 Average Ride Distance by Vehicle Type")
    st.bar_chart(df_distance, x="vehicle_type", y="Avg_Ride_Distance")

# --- SQL Queries Page ---
elif selected_page == "SQL Queries":
    st.title("📊 SQL Queries - Ola Rides Data")

    queries = {
        "🚗 Total Number of Successful Rides": "SELECT COUNT(*) AS Successful_Rides FROM ride_insights WHERE booking_status = 'success';",
        "💰 Total Revenue Generated": "SELECT SUM(booking_value) AS Total_Revenue FROM ride_insights;",
        "❌ Total Number of Rides by Customers": "SELECT COUNT(*) AS Total_Number_Of_Rides FROM ride_insights;",
        "🚦 Rides Cancelled by Drivers Due to Personal & Car Issues": "SELECT DISTINCT incomplete_rides_reason FROM Ride_Insights WHERE incomplete_rides_reason IN ('vehicle Breakdown','Not Specified', 'Other Issues','Customer Demand');",
        "🚘 Most Popular Vehicle Type": "SELECT vehicle_type, COUNT(*) AS Total_Rides FROM ride_insights GROUP BY vehicle_type ORDER BY Total_Rides DESC;",
        "🏅 Top 5 Customers by Number of Rides": "SELECT customer_id, COUNT(booking_id) AS Total_Rides FROM ride_insights GROUP BY customer_id ORDER BY Total_Rides DESC LIMIT 5;",
        "📏 Average Ride Distance": "SELECT ROUND(AVG(ride_distance), 2) AS Avg_Ride_Distance FROM ride_insights;",
        "⭐ Driver Ratings Distribution": "SELECT driver_ratings, COUNT(*) AS Rating_Count FROM ride_insights GROUP BY driver_ratings ORDER BY driver_ratings DESC;",
        "⭐ Customer Ratings Distribution": "SELECT customer_rating, COUNT(*) AS Rating_Count FROM ride_insights GROUP BY customer_rating ORDER BY customer_rating DESC;",
        "💳 Total Rides Using UPI Payments": "SELECT COUNT(*) AS Total_UPI_Transactions FROM ride_insights WHERE payment_method = 'UPI';",
        "🚦 All Incomplete Rides": "SELECT booking_id, booking_status, incomplete_rides_reason FROM Ride_Insights WHERE booking_status != 'Completed';"
    }

    for title, query in queries.items():
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
        st.write(f"### {title}")
        st.dataframe(df)

# --- Summary Insights Page ---
elif selected_page == "Summary Insights":
    st.title("📈 Key Findings & Summary Insights")
    st.write("""
    ### 🚗 **Project Summary: Ola Rides Analysis**
    This project explores ride patterns, customer behaviors, and booking trends using SQL queries and data visualizations.

    #### 🔹 **Key Insights from the Dataset**
    - **Total Successful Rides:** Shows overall trip volume across all customers.
    - **Average Ride Distance:** Helps analyze vehicle efficiency and route optimization.
    - **Cancellation Trends:** Displays common reasons for ride cancellations, allowing improvement strategies.
    - **Customer Behavior:** Identifies top users with the highest number of bookings.
    - **Booking Patterns:** Monthly ride trends highlight peak periods for activity.

    #### 🔹 **Business Impact**
    - 🏆 **Top Customers** can be targeted for loyalty programs.
    - 🔄 **Ride Distance Insights** help optimize pricing and fuel usage.
    - 🚦 **Cancellation Tracking** supports operational improvements to reduce failed bookings.

    🔍 **Final Thoughts:**  
    This data-driven dashboard provides actionable insights for improving customer satisfaction, operational efficiency, and overall business strategy in ride-sharing services.
    """)

# --- Close Database Connection ---
conn.close()
