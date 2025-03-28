from werkzeug.utils import secure_filename
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.database import create_connection
from backend.auth_utils import admin_login_required
from sqlite3 import Error

# Define the Blueprint for 'menu'
menu_bp = Blueprint('menu', __name__,
                    static_folder='static',  # Serve static files from the root 'static' folder
                    template_folder='../frontend')  # Template folder is inside 'frontend'

# Define the folder to save images (inside the 'static/images' directory)
UPLOAD_FOLDER = 'static/images'  # Path to the 'images' folder inside the 'static' folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists, and create it if not
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to view all menu items
@menu_bp.route('/admin/menu', methods=['GET', 'POST'])
@admin_login_required
def view_menu():
    search_query = request.form.get('search', '')

    conn = create_connection()
    items = []
    if conn:
        try:
            c = conn.cursor()
            if search_query:
                c.execute("SELECT * FROM menu_items WHERE name LIKE ?", ('%' + search_query + '%',))
            else:
                c.execute("SELECT * FROM menu_items")
            items = c.fetchall()
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return render_template('menu.html', items=items)

# Route to add a new menu item
@menu_bp.route('/admin/add_menu_item', methods=['GET', 'POST'])
@admin_login_required
def add_menu_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        price = request.form['price']
        category = request.form.get('category', '')
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, image_filename))  # Save the image file

        # Insert into the database
        conn = create_connection()
        if conn:
            try:
                c = conn.cursor()
                c.execute("""INSERT INTO menu_items (name, description, price, category, image_filename) 
                             VALUES (?, ?, ?, ?, ?)""",
                         (name, description, price, category, image_filename))
                conn.commit()
                flash('Menu item added successfully!', 'success')
                return redirect(url_for('menu.view_menu'))
            except Error as e:
                flash(f'Database error: {str(e)}', 'danger')
            finally:
                conn.close()
    
    return render_template('edit_menu.html', item=None)

# Route to edit an existing menu item
@menu_bp.route('/admin/edit_menu_item/<int:item_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_menu_item(item_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            if request.method == 'POST':
                name = request.form['name']
                description = request.form.get('description', '')
                price = request.form['price']
                category = request.form.get('category', '')
                is_available = 1 if request.form.get('is_available') else 0

                # Handle image upload
                image_filename = None
                if 'image' in request.files:
                    image = request.files['image']
                    if image and allowed_file(image.filename):
                        image_filename = secure_filename(image.filename)
                        image.save(os.path.join(UPLOAD_FOLDER, image_filename))  # Save the image file

                # Update the menu item in the database
                c.execute("""UPDATE menu_items SET 
                            name=?, description=?, price=?, category=?, is_available=?, image_filename=? 
                            WHERE id=?""",
                         (name, description, price, category, is_available, image_filename, item_id))
                conn.commit()
                flash('Menu item updated successfully!', 'success')
                return redirect(url_for('menu.view_menu'))

            c.execute("SELECT * FROM menu_items WHERE id=?", (item_id,))
            item = c.fetchone()
            return render_template('edit_menu.html', item=item)
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()

    return redirect(url_for('menu.view_menu'))

# Route to delete a menu item
@menu_bp.route('/admin/delete_menu_item/<int:item_id>')
@admin_login_required
def delete_menu_item(item_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM menu_items WHERE id=?", (item_id,))
            conn.commit()
            flash('Menu item deleted successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return redirect(url_for('menu.view_menu'))
