import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error

def create_server_connection():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=st.secrets["mysql"]["port"],
            user=st.secrets["mysql"]["user"],
            passwd=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
        st.success("MySQL Database connection successful")
        return connection
    except Error as err:
        st.error(f"Database connection failed: {err}")
        return None

def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        st.error(f"Failed to read data from database: {err}")

def app():
    st.title('MySQL 데이터 표시')
    conn = create_server_connection()
    if conn is not None:
        data = execute_read_query(conn, "SELECT * FROM 국민연금")
        if data:
            st.write("데이터가 성공적으로 검색되었습니다:")
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("데이터를 찾을 수 없습니다.")
        conn.close()
    else:
        st.write("데이터베이스 연결에 실패했습니다.")

app()

