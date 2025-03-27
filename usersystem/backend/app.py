from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder='../frontend')  # กำหนดเส้นทางที่ใช้ค้นหาเทมเพลต
app.secret_key = 'your_secret_key'  # รหัสลับสำหรับ session

# หน้าแรกที่จะแสดงหน้า Login
@app.route('/')
def index():
    return redirect(url_for('login'))  # รีไดเรคไปยังหน้า login

# หน้า Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ตรวจสอบข้อมูลผู้ใช้ที่ล็อกอิน (คุณสามารถใช้ฐานข้อมูลหรือฟังก์ชันต่างๆ)
        if username == 'admin' and password == 'password':  # ตัวอย่างการตรวจสอบแบบง่ายๆ
            session['username'] = username
            return redirect(url_for('home'))  # รีไดเรคไปยังหน้า Home
        else:
            return "Invalid login credentials", 401
    return render_template('login.html')  # แสดงฟอร์ม login

# หน้า Home หลังจากล็อกอินสำเร็จ
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))  # ถ้าไม่ได้ล็อกอิน จะให้ไปที่หน้า login
    return render_template('myaccount.html')  # แสดงหน้า Home (myaccount.html)

# หน้าเกี่ยวกับเรา
@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

# หน้าโปรไฟล์
@app.route('/profile')
def profile():
    return render_template('profile.html')

# หน้า FAQ
@app.route('/faq')
def faq():
    return render_template('faq.html')

# หน้า Coupon
@app.route('/coupon-discount')
def coupon_discount():
    return render_template('coupon-discount.html')

# หน้า Sign-in (Signin.html)
@app.route('/signin')
def signin():
    return render_template('Signin.html')

if __name__ == '__main__':
    app.run(debug=True , port=7000)
