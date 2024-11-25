from flask import Flask, request, render_template, redirect
from database import init_db, get_db_connection
from encryption import encrypt, decrypt
import sqlite3

app = Flask(__name__)

# Initialize Database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

# Vulnerable Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        connection.commit()
        connection.close()
        return redirect('/login')
    return render_template('register.html')

# Vulnerable Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use executescript to handle multiple SQL commands
            query = f"""
                SELECT * FROM users WHERE username = '{username}' AND password = '{password}';
            """
            cursor.executescript(query)

            # Fetch the result of the login query
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
            user = cursor.fetchone()

            connection.commit()
            return "Login successful!" if user else "Login failed!"
        except sqlite3.OperationalError as e:
            return f"Database error: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
        finally:
            if connection:
                connection.close()
    return render_template('login.html')



# Secure Registration
@app.route('/secure_login/register', methods=['GET', 'POST'])
def secure_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        encrypt_password = encrypt(password)  # Encrypt the password
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypt_password))
            connection.commit()
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            connection.close()
        return redirect('/secure_login/login')
    return render_template('secure_register.html')

# Secure Login
@app.route('/secure_login/login', methods=['GET', 'POST'])
def secure_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        connection.close()
        if user:
            stored_password = user[0]
            try:
                if decrypt(stored_password) == password:
                    return "Secure login successful!"
            except:
                pass
        return "Secure login failed!"
    return render_template('secure_login.html')

if __name__ == "__main__":
    app.run(debug=True)
