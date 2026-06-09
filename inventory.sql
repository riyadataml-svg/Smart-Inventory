-- SQL Script to create the database and tables for the Smart Inventory Management System
-- You can run this file in your MySQL Workbench or Command Line.

-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS inventory_db;

-- 2. Use the Database
USE inventory_db;

-- 3. Create Products Table
-- Purpose: To store details of all the products available in the inventory.
CREATE TABLE IF NOT EXISTS Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each product
    product_name VARCHAR(255) NOT NULL,        -- Name of the product
    category VARCHAR(100),                     -- Category of the product (e.g., Electronics, Grocery)
    price DECIMAL(10, 2) NOT NULL,             -- Price per unit
    stock_quantity INT NOT NULL DEFAULT 0      -- Available quantity in stock
);

-- 4. Create Sales Table
-- Purpose: To keep track of all sales transactions.
CREATE TABLE IF NOT EXISTS Sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,    -- Unique ID for each sale transaction
    product_id INT,                            -- Which product was sold (links to Products table)
    quantity_sold INT NOT NULL,                -- How many units were sold
    total_amount DECIMAL(10, 2) NOT NULL,      -- Total revenue from this sale
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the sale happened
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
    -- If a product is deleted, its sales records will also be deleted (CASCADE)
);

-- Note: You can insert some dummy data if you want to test it immediately
-- INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('Laptop', 'Electronics', 55000.00, 10);
-- INSERT INTO Products (product_name, category, price, stock_quantity) VALUES ('Mouse', 'Accessories', 500.00, 50);
