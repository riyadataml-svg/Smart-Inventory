import random
from faker import Faker
from database import get_connection

fake = Faker()

def generate_fake_data(num_products=30, num_sales=50):
    conn = get_connection()
    if not conn:
        print("❌ Could not connect to the database.")
        return

    try:
        cursor = conn.cursor()
        
        categories = ['Electronics', 'Grocery', 'Clothing', 'Furniture', 'Toys', 'Stationery', 'Books', 'Beauty']
        
        print(f"Generating {num_products} fake products...")
        for _ in range(num_products):
            # Generate a realistic sounding product name
            name = fake.company() + " " + random.choice(['Pro', 'Max', 'Ultra', 'Lite', 'Plus', 'Basic', 'Standard'])
            category = random.choice(categories)
            price = round(random.uniform(100.0, 15000.0), 2)
            quantity = random.randint(1, 150) # Some low stock items will be generated
            
            cursor.execute("INSERT INTO Products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)", 
                           (name, category, price, quantity))
        
        conn.commit()
        print("Fake products inserted successfully!")

        # Fetch product IDs to use for sales
        cursor.execute("SELECT product_id, price, stock_quantity FROM Products")
        products = cursor.fetchall()
        
        if products:
            print(f"Generating {num_sales} fake sales...")
            for _ in range(num_sales):
                # Pick a random product
                product_idx = random.randint(0, len(products) - 1)
                product_id, price, stock_quantity = products[product_idx]
                
                if stock_quantity <= 0:
                    continue # Skip if out of stock
                    
                # Sell a random quantity
                qty_sold = random.randint(1, min(10, stock_quantity))
                total_amount = round(price * qty_sold, 2)
                
                # Insert Sale
                cursor.execute("INSERT INTO Sales (product_id, quantity_sold, total_amount) VALUES (%s, %s, %s)", 
                               (product_id, qty_sold, total_amount))
                
                # Reduce Stock
                new_stock = stock_quantity - qty_sold
                cursor.execute("UPDATE Products SET stock_quantity = %s WHERE product_id = %s", (new_stock, product_id))
                
                # Update our local product list with the new stock so we don't go negative
                products[product_idx] = (product_id, price, new_stock)
                
            conn.commit()
            print("Fake sales generated and stock updated successfully!")
            
    except Exception as e:
        print(f"Error generating fake data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_fake_data()
