from flask import Flask, render_template

# สร้าง Flask app และกำหนดเส้นทางสำหรับ static และ template
app = Flask(__name__, 
            static_folder='../frontend/static',  # ระบุเส้นทางสำหรับ static
            template_folder='../frontend/templates')  # ระบุเส้นทางสำหรับ templates

@app.route('/')
def home():
    return render_template('Home.html')  # Render หน้า Home.html จากโฟลเดอร์ templates

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/track-status')
def track_status():
    return render_template('follow.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('Signin.html')

@app.route('/cart')
def card():
    return render_template('basket.html')

@app.route('/myaccount')
def myaccount():
    return render_template('myaccount.html')


if __name__ == '__main__':
    app.run(debug=True , port=7000)
