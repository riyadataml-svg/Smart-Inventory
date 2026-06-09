import sys
import products
import sales
import reports

def print_menu():
    """Displays the main menu options."""
    print("\n" + "="*40)
    print(" 🛠️  Smart Inventory Management System")
    print("="*40)
    print("1. Add New Product")
    print("2. View All Products")
    print("3. Update Product Stock")
    print("4. Delete Product")
    print("5. Record a Sale")
    print("6. View Total Revenue")
    print("7. Check Low Stock Alerts")
    print("8. Exit")
    print("="*40)

def main():
    """The main application loop that waits for user input."""
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            name = input("Enter product name: ")
            category = input("Enter category: ")
            try:
                price = float(input("Enter price: "))
                quantity = int(input("Enter initial stock quantity: "))
                products.add_product(name, category, price, quantity)
            except ValueError:
                print("\n❌ Error: Price must be a number and Quantity must be an integer.")
                
        elif choice == '2':
            products.view_products()
            
        elif choice == '3':
            try:
                prod_id = int(input("Enter Product ID to update: "))
                new_qty = int(input("Enter new stock quantity: "))
                products.update_product_stock(prod_id, new_qty)
            except ValueError:
                print("\n❌ Error: ID and Quantity must be numbers.")
                
        elif choice == '4':
            try:
                prod_id = int(input("Enter Product ID to delete: "))
                products.delete_product(prod_id)
            except ValueError:
                print("\n❌ Error: ID must be a number.")
                
        elif choice == '5':
            try:
                prod_id = int(input("Enter Product ID sold: "))
                qty_sold = int(input("Enter quantity sold: "))
                sales.record_sale(prod_id, qty_sold)
            except ValueError:
                print("\n❌ Error: ID and Quantity must be numbers.")
                
        elif choice == '6':
            reports.generate_total_revenue_report()
            
        elif choice == '7':
            reports.generate_low_stock_alert()
            
        elif choice == '8':
            print("\n👋 Exiting Smart Inventory System. Goodbye!")
            sys.exit()
            
        else:
            print("\n❌ Invalid choice! Please select a valid option from 1 to 8.")

if __name__ == "__main__":
    # Start the application
    main()
