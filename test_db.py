import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host='localhost',
        database='inventory_db',
        user='root',
        password='pr2007'
    )
    if conn.is_connected():
        print("SUCCESS")
except Error as e:
    print(f"EXACT ERROR: {e}")
