from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Zukaata_1245',
    database='demologin'
)
cursor = db.cursor()

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from the database
        query = "SELECT password_hash FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        # Check if user exists and the password is correct
        if user and bcrypt.check_password_hash(user[0], password):
            flash("Login successful!", "success")
            return redirect(url_for('home'))  # Redirect to home page
        else:
            flash(" 📀 Invalid username or password", "error")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash(" 📀 User already exists!", "error")
            return redirect(url_for('register'))

        # Hash the password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Store user in database
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        db.commit()

        flash("User registered successfully!", "success")
        return redirect(url_for('login'))  # Redirect to login page after registration

    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
