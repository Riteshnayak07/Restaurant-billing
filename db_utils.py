import mysql.connector
from datetime import datetime
import csv
import os

# Establish MySQL connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # 🔁 replace with your MySQL username
        password="12345",  # 🔁 replace with your MySQL password
        database="restaurant_billing"
    )

# Fetch menu items (for UI)
def get_menu_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT item_id, name, category, price, gst FROM menu")
    menu = cursor.fetchall()
    conn.close()
    return menu

# Save order (for UI)
def save_order(order_data, items):
    conn = connect_db()
    cursor = conn.cursor()

    # Insert order
    cursor.execute("""
        INSERT INTO orders (order_type, total_amount, gst_amount, discount, payment_method, datetime)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        order_data['order_type'],
        order_data['total_amount'],
        order_data['gst_amount'],
        order_data['discount'],
        order_data['payment_method'],
        order_data['datetime']
    ))

    order_id = cursor.lastrowid

    # Insert order items
    for item_id, qty in items:
        cursor.execute("""
            INSERT INTO order_items (order_id, item_id, quantity)
            VALUES (%s, %s, %s)
        """, (order_id, item_id, qty))

    conn.commit()
    conn.close()
    return order_id

# Load menu from CSV to database
def load_menu_from_csv(csv_path="data/menu.csv"):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Clear existing menu data
    cursor.execute("DELETE FROM menu")
    
    # Read CSV and insert data
    with open(csv_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            cursor.execute("""
                INSERT INTO menu (item_id, name, category, price, gst)
                VALUES (%s, %s, %s, %s, %s)
            """, row)
    
    conn.commit()
    conn.close()
