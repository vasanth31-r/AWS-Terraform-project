from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)

def get_connection():
    for i in range(10):
        try:
            conn = mysql.connector.connect(
                host='mysql_db',       # container name
                user='root',
                password='rootpassword',
                database='flask_app_db'
            )
            if conn.is_connected():
                return conn
        except:
            print("Waiting for MySQL to be ready...")
            time.sleep(3)
    raise Exception("Failed to connect to MySQL")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        message = "User added successfully"
    except Error as e:
        message = f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

    return jsonify({'message': message})

@app.route('/get_users', methods=['GET'])
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
