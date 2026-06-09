import pandas as pd
from database import get_connection

def generate_total_revenue_report():
    """
    Calculates the total revenue from all sales.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT SUM(total_amount) FROM Sales"
            cursor.execute(query)
            result = cursor.fetchone()
            
            total_revenue = result[0] if result[0] is not None else 0.0
            print(f"\n💰 Total Revenue Generated: ₹{total_revenue}")
            
        except Exception as e:
            print(f"\n❌ Error generating revenue report: {e}")
        finally:
            cursor.close()
            conn.close()

def generate_low_stock_alert():
    """
    Finds products that have stock less than 10.
    """
    conn = get_connection()
    if conn:
        try:
            query = "SELECT product_id, product_name, stock_quantity FROM Products WHERE stock_quantity < 10"
            df = pd.read_sql(query, conn)
            
            if df.empty:
                print("\n✅ All products have sufficient stock (10 or more).")
            else:
                print("\n⚠️ ALERT: Low Stock Products (Less than 10 units) ⚠️")
                print(df.to_string(index=False))
                
        except Exception as e:
            print(f"\n❌ Error fetching low stock data: {e}")
        finally:
            conn.close()
