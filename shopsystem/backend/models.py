import sqlite3
import os

# ฟังก์ชันการเชื่อมต่อฐานข้อมูล
def create_connection(db_file='cafe.db'):
    """ สร้างการเชื่อมต่อฐานข้อมูล """
    db_path = os.path.join(os.path.dirname(__file__), '../../cafe.db')  # ใช้เส้นทางสัมพัทธ์
    conn = sqlite3.connect(db_path)  # เชื่อมต่อกับฐานข้อมูลตามเส้นทางที่ได้
    return conn


def get_user_by_username(username):
    conn = create_connection()  # ใช้การเชื่อมต่อฐานข้อมูล
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()  # Fetch the user (returns a tuple)
    conn.close()

    # ถ้าผู้ใช้มีอยู่ในฐานข้อมูล, คืนค่าเป็น dictionary
    if user:
        user_dict = {
            'id': user[0],         # สมมติว่า 'id' คือคอลัมน์แรก
            'username': user[1],   # สมมติว่า 'username' คือคอลัมน์ที่สอง
            'password': user[2],   # สมมติว่า 'password' คือคอลัมน์ที่สาม
            'role': user[3],       # สมมติว่า 'role' คือคอลัมน์ที่สี่
            'is_active': user[4]   # สมมติว่า 'is_active' คือคอลัมน์ที่ห้า
        }
        return user_dict
    return None

def get_all_menu_items():
    conn = create_connection()  # ใช้การเชื่อมต่อฐานข้อมูล
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE is_available=1")
    items = cursor.fetchall()
    conn.close()
    return items

def add_to_cart(item_id):
    conn = create_connection()  # ใช้การเชื่อมต่อฐานข้อมูล
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (item_id) VALUES (?)", (item_id,))
    conn.commit()
    conn.close()

def get_cart():
    conn = create_connection()  # ใช้การเชื่อมต่อฐานข้อมูล
    cursor = conn.cursor()
    cursor.execute("""
        SELECT menu_items.name, menu_items.price 
        FROM cart
        JOIN menu_items ON cart.item_id = menu_items.id
    """)
    cart_items = cursor.fetchall()
    conn.close()
    return cart_items

def get_sales_history():
    conn = create_connection()  # ใช้การเชื่อมต่อฐานข้อมูล
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY transaction_date DESC")
    sales = cursor.fetchall()
    conn.close()
    return sales
