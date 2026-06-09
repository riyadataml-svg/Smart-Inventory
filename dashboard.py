import streamlit as st
import pandas as pd
from database import get_connection

# Page Configuration
st.set_page_config(page_title="Smart Inventory Dashboard", page_icon="📦", layout="wide")

# Connect to database using existing database.py
@st.cache_resource
def init_connection():
    return get_connection()

conn = init_connection()

# --- LOGIN SYSTEM ---
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        username = st.session_state["username"]
        password = st.session_state["password"]
        
        if username == "admin" and password == "admin123":
            st.session_state["password_correct"] = True
            st.session_state["role"] = "admin"
            del st.session_state["password"]
        elif username == "staff" and password == "staff123":
            st.session_state["password_correct"] = True
            st.session_state["role"] = "staff"
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Login to Smart Inventory")
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔒 Login to Smart Inventory")
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        st.error("❌ Username or password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()  # Stop execution until login is successful

# --- MAIN DASHBOARD (Only shows if logged in) ---

# Sidebar Navigation
st.sidebar.title(f"Welcome, {st.session_state['role'].capitalize()}! 👋")

if st.sidebar.button("Logout 🚪"):
    del st.session_state["password_correct"]
    if "role" in st.session_state:
        del st.session_state["role"]
    st.rerun()

# Dynamic Menu Based on Role
if st.session_state["role"] == "admin":
    menu_options = ["Dashboard", "Manage Products", "Record Sales"]
else:
    menu_options = ["Record Sales"]

menu = st.sidebar.radio("Go to", menu_options)

if menu == "Dashboard":
    st.title("📊 Smart Inventory Dashboard")
    
    if conn:
        cursor = conn.cursor()
        
        # Top Cards for Key Metrics
        col1, col2, col3 = st.columns(3)
        
        # Total Revenue Metric
        cursor.execute("SELECT SUM(total_amount) FROM Sales")
        revenue = cursor.fetchone()[0]
        revenue = revenue if revenue else 0.0
        col1.metric("Total Revenue 💰", f"₹{revenue:,.2f}")
        
        # Total Products Metric
        cursor.execute("SELECT COUNT(*) FROM Products")
        total_products = cursor.fetchone()[0]
        col2.metric("Total Products 📦", total_products)
        
        # Low Stock Metric
        cursor.execute("SELECT COUNT(*) FROM Products WHERE stock_quantity < 10")
        low_stock_count = cursor.fetchone()[0]
        col3.metric("Low Stock Alerts ⚠️", low_stock_count)
        
        st.markdown("---")
        
        # Low Stock Table
        st.subheader("⚠️ Low Stock Products (Less than 10 units)")
        query = "SELECT product_id, product_name, stock_quantity FROM Products WHERE stock_quantity < 10"
        df_low_stock = pd.read_sql(query, conn)
        
        if df_low_stock.empty:
            st.success("All products have sufficient stock!")
        else:
            st.dataframe(df_low_stock, use_container_width=True)

        # --- NEW FEATURES: ANALYTICS & EXPORT ---
        st.markdown("---")
        st.subheader("📈 Inventory Analytics")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.write("**Stock by Category**")
            df_cat = pd.read_sql("SELECT category, SUM(stock_quantity) as Total_Stock FROM Products GROUP BY category", conn)
            if not df_cat.empty:
                st.bar_chart(df_cat.set_index("category"))
                
        with col_chart2:
            st.write("**Top 5 Selling Products**")
            query_top_sales = """
            SELECT p.product_name, SUM(s.quantity_sold) as Total_Sold 
            FROM Sales s 
            JOIN Products p ON s.product_id = p.product_id 
            GROUP BY s.product_id 
            ORDER BY Total_Sold DESC 
            LIMIT 5
            """
            df_top = pd.read_sql(query_top_sales, conn)
            if not df_top.empty:
                st.bar_chart(df_top.set_index("product_name"))
        
        st.markdown("---")
        st.subheader("📥 Export Data")
        df_full = pd.read_sql("SELECT * FROM Products", conn)
        if not df_full.empty:
            csv = df_full.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Full Inventory Report (CSV)",
                data=csv,
                file_name='inventory_report.csv',
                mime='text/csv',
            )

        cursor.close()
    else:
        st.error("Could not connect to the database. Please check your credentials.")

elif menu == "Manage Products":
    st.title("🛍️ Manage Products")
    
    # Tabs for different CRUD operations
    tab1, tab2, tab3 = st.tabs(["View Products", "Add Product", "Update/Delete"])
    
    with tab1:
        st.subheader("Current Inventory")
        if conn:
            df = pd.read_sql("SELECT * FROM Products", conn)
            st.dataframe(df, use_container_width=True)
            
    with tab2:
        st.subheader("Add New Product")
        with st.form("add_form", clear_on_submit=True):
            name = st.text_input("Product Name")
            category = st.text_input("Category")
            price = st.number_input("Price (₹)", min_value=0.0, step=1.0)
            quantity = st.number_input("Initial Stock Quantity", min_value=0, step=1)
            submitted = st.form_submit_button("Add Product")
            
            if submitted:
                if name and category:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO Products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)", 
                                       (name, category, price, quantity))
                        conn.commit()
                        cursor.close()
                        st.success(f"Product '{name}' added successfully! Go to 'View Products' to see it.")
                    except Exception as e:
                        st.error(f"Error adding product: {e}")
                else:
                    st.warning("Please fill out all text fields.")
                    
    with tab3:
        st.subheader("Update Stock or Delete Product")
        if conn:
            # Fetch products for the dropdown
            cursor = conn.cursor()
            cursor.execute("SELECT product_id, product_name FROM Products")
            products_list = cursor.fetchall()
            cursor.close()
            
            # Format product list for selection
            prod_dict = {f"{p[0]} - {p[1]}": p[0] for p in products_list}
            
            if prod_dict:
                selected_prod = st.selectbox("Select Product", options=list(prod_dict.keys()))
                prod_id = prod_dict[selected_prod]
                
                col1, col2 = st.columns(2)
                with col1:
                    new_qty = st.number_input("New Stock Quantity", min_value=0, step=1)
                    if st.button("Update Stock"):
                        try:
                            cursor = conn.cursor()
                            cursor.execute("UPDATE Products SET stock_quantity = %s WHERE product_id = %s", (new_qty, prod_id))
                            conn.commit()
                            cursor.close()
                            st.success(f"Stock updated for {selected_prod} to {new_qty}.")
                        except Exception as e:
                            st.error(f"Error updating stock: {e}")
                with col2:
                    st.write("") # Padding
                    st.write("") # Padding
                    if st.button("Delete Product ❌", type="primary"):
                        try:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM Products WHERE product_id = %s", (prod_id,))
                            conn.commit()
                            cursor.close()
                            st.success(f"Product {selected_prod} deleted.")
                        except Exception as e:
                            st.error(f"Error deleting product: {e}")
            else:
                st.info("No products available to update or delete.")

elif menu == "Record Sales":
    st.title("🛒 Record a Sale")
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, product_name, price, stock_quantity FROM Products WHERE stock_quantity > 0")
        products_list = cursor.fetchall()
        cursor.close()
        
        # Product dict: Name -> (ID, Price, Stock)
        prod_dict = {f"{p[1]} (₹{p[2]}, In Stock: {p[3]})": (p[0], p[2], p[3]) for p in products_list}
        
        if prod_dict:
            selected_prod = st.selectbox("Select Product to Sell", options=list(prod_dict.keys()))
            prod_id, price, stock = prod_dict[selected_prod]
            
            qty_sold = st.number_input("Quantity Sold", min_value=1, max_value=stock, step=1)
            
            if st.button("Record Sale", type="primary"):
                try:
                    total_amount = price * qty_sold
                    new_stock = stock - qty_sold
                    
                    cursor = conn.cursor()
                    # Insert Sale
                    cursor.execute("INSERT INTO Sales (product_id, quantity_sold, total_amount) VALUES (%s, %s, %s)", 
                                   (prod_id, qty_sold, total_amount))
                    # Reduce Stock
                    cursor.execute("UPDATE Products SET stock_quantity = %s WHERE product_id = %s", 
                                   (new_stock, prod_id))
                    conn.commit()
                    cursor.close()
                    
                    st.success(f"✅ Sale recorded successfully! Total Amount: ₹{total_amount}. Remaining Stock: {new_stock}")
                    st.balloons()
                except Exception as e:
                    conn.rollback()
                    st.error(f"Error recording sale: {e}")
        else:
            st.warning("No products available in stock to sell. Please add products or update stock first.")
