import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from backend.user_model import User
from backend.auth_utils import admin_login_required
from backend.database import create_connection


app = Flask(__name__, static_folder='../../static',template_folder='../frontend')
app.secret_key = os.urandom(24)  # ใช้ค่า secret_key ที่ปลอดภัย

# ตั้งค่า Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_admin.login'  # เมื่อไม่ได้ล็อกอินจะให้ไปที่หน้า login

# โหลดผู้ใช้จากฐานข้อมูล
@login_manager.user_loader
def load_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[2])  # ส่งกลับอ็อบเจกต์ User
    return None

# ---- REGISTER BLUEPRINTS ----
from backend.auth_admin import admin_auth_bp
from backend.inventory import inventory_bp
from backend.menu import menu_bp
from backend.discounts import discounts_bp
from backend.promotions import promotions_bp
from backend.sales import sales_bp
from backend.members import members_bp
from backend.manage_profile import users_bp


app.register_blueprint(admin_auth_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(discounts_bp)
app.register_blueprint(promotions_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(members_bp)
app.register_blueprint(users_bp)



@app.route('/admin')
@admin_login_required
def admin_dashboard():
    conn = create_connection()
    cursor = conn.cursor()

    # Fetch Inventory Items
    cursor.execute("SELECT COUNT(*) FROM inventory")
    inventory_count = cursor.fetchone()[0]

    # Fetch Menu Items
    cursor.execute("SELECT COUNT(*) FROM menu_items WHERE is_available = 1")
    menu_count = cursor.fetchone()[0]

    # Fetch Active Members
    cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = 'active'")  # Assuming you have a status column to check active members
    member_count = cursor.fetchone()[0]

    # Fetch Today's Sales (total_amount for today's date)
    cursor.execute("SELECT * FROM sales")

    sales = cursor.fetchall()

    total_sales = sum(sale[2] for sale in sales)
    conn.close()

    # Pass the fetched data to the template
    return render_template('dashboard.html', inventory_count=inventory_count,
                           menu_count=menu_count, member_count=member_count, 
                           total_sales=total_sales)



@app.route('/')
def home():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)  # เปลี่ยนเป็น False ใน production
