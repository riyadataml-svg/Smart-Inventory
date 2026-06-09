from database import get_connection

def record_sale(product_id, quantity_sold):
    """
    Records a sale and automatically reduces the product's stock.
    This demonstrates basic 'Business Logic'.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Step 1: Check if the product exists and has enough stock
            check_query = "SELECT price, stock_quantity, product_name FROM Products WHERE product_id = %s"
            cursor.execute(check_query, (product_id,))
            result = cursor.fetchone()
            
            if not result:
                print(f"\n⚠️ Warning: Product ID {product_id} not found.")
                return
            
            price, current_stock, product_name = result
            
            if current_stock < quantity_sold:
                print(f"\n❌ Insufficient Stock! Only {current_stock} units of '{product_name}' are available.")
                return
            
            # Step 2: Calculate total amount
            total_amount = price * quantity_sold
            
            # Step 3: Insert the sale record into Sales table
            insert_sale_query = "INSERT INTO Sales (product_id, quantity_sold, total_amount) VALUES (%s, %s, %s)"
            cursor.execute(insert_sale_query, (product_id, quantity_sold, total_amount))
            
            # Step 4: Reduce the stock in Products table
            new_stock = current_stock - quantity_sold
            update_stock_query = "UPDATE Products SET stock_quantity = %s WHERE product_id = %s"
            cursor.execute(update_stock_query, (new_stock, product_id))
            
            # Step 5: Commit both changes as a single transaction
            conn.commit()
            
            print(f"\n✅ Success: Sale recorded! {quantity_sold} x {product_name} sold for ₹{total_amount}.")
            print(f"   Remaining stock: {new_stock}")
            
        except Exception as e:
            print(f"\n❌ Error recording sale: {e}")
            # If anything goes wrong, rollback changes so data doesn't get corrupted
            conn.rollback() 
        finally:
            cursor.close()
            conn.close()
