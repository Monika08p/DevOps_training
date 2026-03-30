from flask import Flask, request, jsonify
import mysql.connector
import time

app = Flask(__name__)

def get_db():
    for i in range(10):
        try:
            return mysql.connector.connect(
                host="database",
                user="root",
                password="root",
                database="mydb"
            )
        except:
            print("Waiting for DB...")
            time.sleep(2)

def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            college VARCHAR(50),
            email VARCHAR(50),
            phone VARCHAR(20),
            department VARCHAR(50),
            gender VARCHAR(10),
            interest VARCHAR(50)
        )
    """)

    db.commit()
    print("Table ready")

init_db()

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO students 
        (name, college, email, phone, department, gender, interest)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("name"),
        data.get("college"),
        data.get("email"),
        data.get("phone"),
        data.get("department"),
        data.get("gender"),
        data.get("interest")
    ))

    db.commit()

    return jsonify({"message": "Saved"})

@app.route("/students")
def students():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    return jsonify(cursor.fetchall())

app.run(host="0.0.0.0", port=5000)