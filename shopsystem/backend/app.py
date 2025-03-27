from flask import Flask, render_template, request, redirect, url_for, session
from utils import get_user_by_username, get_all_menu_items, add_to_cart, get_cart, get_sales_history, remove_from_cart, checkout, calculate_cart_total

app = Flask(__name__, template_folder='../frontend/templates')
app.secret_key = 'your_secret_key'

# Check if the user is logged in (a helper function)
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)

        # Access user tuple by index instead of using keys
        if user and user[2] == password:  # user[2] corresponds to password (based on your database schema)
            session['user_id'] = user[0]  # user[0] corresponds to the ID
            return redirect(url_for('home'))
        else:
            return "Invalid login credentials", 401
    return render_template('login.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/menu')
@login_required
def menu():
    items = get_all_menu_items()
    return render_template('menu.html', items=items)


@app.route('/add_to_cart/<item_id>', methods=['POST'])
@login_required
def add_to_cart_route(item_id):
    add_to_cart(item_id)
    return redirect(url_for('menu'))  # Redirect back to the menu page after adding an item to the cart


@app.route('/remove_from_cart/<item_id>', methods=['POST'])
@login_required
def remove_from_cart_route(item_id):
    # Call the function to remove the item from the cart
    remove_from_cart(item_id)
    
    # Redirect to the cart page after removing the item
    return redirect(url_for('cart'))


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'POST':
        item_id_to_remove = request.form['remove_item']
        remove_from_cart(item_id_to_remove)  # Remove item from cart
        return redirect(url_for('cart'))  # Refresh the cart page

    items = get_cart()
    total = calculate_cart_total()
    return render_template('cart.html', items=items, total=total)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_page():
    if request.method == 'POST':
        payment_method = request.form['payment_method']  # Get payment method from form
        sale_id = checkout(payment_method)  # Process the checkout and clear the cart
        return redirect(url_for('sales_history'))  # Redirect to the sales history page or any success page
    
    return render_template('checkout.html')


@app.route('/sales_history')
@login_required
def sales_history():
    sales = get_sales_history()
    return render_template('sales_history.html', sales=sales)


@app.route('/inventory')
@login_required
def inventory():
    return render_template('inventory.html')


if __name__ == '__main__':
    app.run(debug=True , port=8000)
