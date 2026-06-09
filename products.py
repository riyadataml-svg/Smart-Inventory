import pandas as pd
from database import get_connection

def add_product(name, category, price, quantity):
    """
    Inserts a new product into the Products table.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)"
            values = (name, category, price, quantity)
            cursor.execute(query, values)
            conn.commit()  # Save changes to the database
            print(f"\n✅ Success: Product '{name}' added successfully!")
        except Exception as e:
            print(f"\n❌ Error adding product: {e}")
        finally:
            cursor.close()
            conn.close()

def view_products():
    """
    Fetches all products and displays them nicely using Pandas DataFrame.
    """
    conn = get_connection()
    if conn:
        try:
            query = "SELECT * FROM Products"
            # Pandas helps in displaying the table beautifully in the console
            df = pd.read_sql(query, conn)
            if df.empty:
                print("\n📦 No products found in the inventory.")
            else:
                print("\n--- 📦 Inventory List ---")
                print(df.to_string(index=False)) # index=False removes the default 0,1,2 row numbers
        except Exception as e:
            print(f"\n❌ Error fetching products: {e}")
        finally:
            conn.close()

def update_product_stock(product_id, new_quantity):
    """
    Updates the stock quantity of an existing product.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE Products SET stock_quantity = %s WHERE product_id = %s"
            values = (new_quantity, product_id)
            cursor.execute(query, values)
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"\n✅ Success: Stock updated for Product ID {product_id}.")
            else:
                print(f"\n⚠️ Warning: Product ID {product_id} not found.")
        except Exception as e:
            print(f"\n❌ Error updating stock: {e}")
        finally:
            cursor.close()
            conn.close()

def delete_product(product_id):
    """
    Deletes a product from the inventory based on its ID.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM Products WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"\n✅ Success: Product ID {product_id} deleted successfully.")
            else:
                print(f"\n⚠️ Warning: Product ID {product_id} not found.")
        except Exception as e:
            print(f"\n❌ Error deleting product: {e}")
        finally:
            cursor.close()
            conn.close()
