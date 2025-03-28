from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.database import create_connection
from backend.auth_utils import admin_login_required
from sqlite3 import Error

users_bp = Blueprint('users', __name__, template_folder='../frontend')

# ดึงข้อมูลโปรไฟล์ทั้งหมด
@users_bp.route('/admin/profile')
@admin_login_required
def view_profile():
    conn = create_connection()
    users = []
    if conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE role != 'admin'")
            users = c.fetchall()
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return render_template('manage_profile.html', users=users)


# เพิ่มโปรไฟล์ใหม่
@users_bp.route('/admin/add_profile', methods=['GET', 'POST'])
@admin_login_required
def add_profile():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        is_active = 1 if request.form.get('is_active') else 0
        email = request.form['email']
        phone = request.form['phone']

        conn = create_connection()
        if conn:
            try:
                c = conn.cursor()
                # Insert a new user with email and phone fields
                c.execute("""INSERT INTO users (username, password, role, is_active, email, phone)
                              VALUES (?, ?, ?, ?, ?, ?)""",
                         (username, password, role, is_active, email, phone))
                conn.commit()
                flash('Profile added successfully!', 'success')
                return redirect(url_for('users.view_profile'))
            except Error as e:
                flash(f'Database error: {str(e)}', 'danger')
            finally:
                conn.close()
    
    return render_template('edit_manage_profile.html', user=None)


# แก้ไขโปรไฟล์
@users_bp.route('/admin/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_profile(user_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                role = request.form['role']
                is_active = 1 if request.form.get('is_active') else 0
                email = request.form['email']
                phone = request.form['phone']

                # Update user with email and phone fields
                c.execute("""UPDATE users SET 
                            username=?, password=?, role=?, is_active=?, email=?, phone=? 
                            WHERE id=?""",
                         (username, password, role, is_active, email, phone, user_id))
                conn.commit()
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('users.view_profile'))
            
            # Fetch all columns for the specific user by id for editing
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            user = c.fetchone()  # Get the user data
            return render_template('edit_manage_profile.html', user=user)
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()

    return redirect(url_for('users.view_profile'))


# ลบโปรไฟล์
@users_bp.route('/admin/delete_profile/<int:user_id>', methods=['POST'])
@admin_login_required
def delete_profile(user_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()
            flash('Profile deleted successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return redirect(url_for('users.view_profile'))
