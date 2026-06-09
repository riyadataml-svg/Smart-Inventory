import mysql.connector
from mysql.connector import Error
import streamlit as st

def get_connection():
    """
    Establish and return a connection to the MySQL database.
    Checks Streamlit secrets first (for cloud deployment),
    then falls back to local configuration.
    """
    try:
        # 1. Cloud Deployment Setup (Streamlit Secrets)
        if hasattr(st, "secrets") and "mysql" in st.secrets:
            host = st.secrets["mysql"]["host"]
            database = st.secrets["mysql"]["database"]
            user = st.secrets["mysql"]["user"]
            password = st.secrets["mysql"]["password"]
            port = st.secrets["mysql"].get("port", 3306)
        # 2. Local Setup (Fallback)
        else:
            host = 'localhost'
            database = 'inventory_db'
            user = 'root'
            password = 'pr2007'
            port = 3306

        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
