# Smart Inventory Management System

This is a beginner-friendly, Python and MySQL-based inventory management system created step-by-step from the project roadmap. It features a Command-Line Interface (CLI) and handles all basic CRUD operations, sales tracking, and reporting.

## Prerequisites

1. **Python 3.x**: Make sure Python is installed on your system.
2. **MySQL Server**: You need to have MySQL installed and running locally.
3. **Python Libraries**: Install the required libraries using pip:
   ```bash
   pip install mysql-connector-python pandas
   ```

## Setup Instructions

1. **Database Setup**:
   - Open your MySQL command line or MySQL Workbench.
   - Run the script provided in `inventory.sql`. This will create a database named `inventory_db` and tables for `Products` and `Sales`.
   
2. **Configure Database Connection**:
   - Open `database.py`.
   - Update the `password='password'` field to match your actual MySQL root password.

3. **Run the Application**:
   - Open your terminal or command prompt.
   - Navigate to this project directory.
   - To use the **Web Dashboard (New & Better)**:
     ```bash
     streamlit run dashboard.py
     ```
   - Alternatively, to use the Command Line Interface (CLI):
     ```bash
     python main.py
     ```

## Project Structure

- `inventory.sql`: SQL scripts for setting up the database.
- `database.py`: Handles connection logic to the MySQL database.
- `dashboard.py`: Modern Web GUI Interface built with Streamlit.
- `main.py`: The entry point with the interactive command line menu.
- `products.py`: Functions to handle Add, View, Update, and Delete operations for products.
- `sales.py`: Logic to record sales and automatically deduct stock.
- `reports.py`: Analytics functions like total revenue calculation and low stock alerts.

## Features Included (Based on Roadmap)
- Phase 1 & 2: Complete logic built out in modular files.
- Phase 3: Relational tables set up.
- Phase 7: CRUD capabilities fully implemented.
- Phase 8: Business logic for sales built.
- Phase 9: Reports and logic implemented using Pandas for clean display.

Enjoy exploring the code! It is heavily commented to help you understand what each block does.
