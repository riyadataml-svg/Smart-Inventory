import mysql.connector

print("Connecting to Aiven Cloud Database...")
try:
    conn = mysql.connector.connect(
        host="mysql-3c69a618-riyariya3467-a6d9.e.aivencloud.com",
        port=24461,
        user="avnadmin",
        password="AVNS_QMjHUIME7jvSf5_7BHX",
        database="defaultdb"
    )
    if conn.is_connected():
        print("Connected to Aiven successfully!")
        cursor = conn.cursor()
        
        print("Creating Tables...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            category VARCHAR(100),
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INT NOT NULL DEFAULT 0
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sales (
            sale_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            quantity_sold INT NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
        )
        """)
        print("Tables created successfully!")
        
        # Insert sample data to check
        cursor.execute("SELECT COUNT(*) FROM Products")
        if cursor.fetchone()[0] == 0:
            print("Inserting sample data...")
            cursor.execute("INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('Wireless Mouse', 'Electronics', 25.00, 50)")
            cursor.execute("INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('Mechanical Keyboard', 'Electronics', 75.00, 15)")
            cursor.execute("INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('Desk Mat', 'Accessories', 15.00, 100)")
            conn.commit()
            print("Sample data inserted!")
        
        cursor.close()
        conn.close()
        print("All done! You can deploy on Streamlit now.")
except Exception as e:
    print(f"Failed to connect: {e}")
