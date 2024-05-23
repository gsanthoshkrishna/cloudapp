from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Pass@123',
    'database': 'samples'
}

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor(dictionary=True)

# Route for the main page
@app.route('/')
def index():
    # Fetch student names from the database
    cursor.execute("SELECT name FROM students")
    students = [student['name'] for student in cursor.fetchall()]
    return render_template('index.html', students=students)

# Route for displaying student details
@app.route('/student_details', methods=['POST'])
def student_details():
    # Get the selected student name from the form
    student_name = request.form['student']

    # Query the database for the student details
    cursor.execute("SELECT * FROM students WHERE name = %s", (student_name,))
    student = cursor.fetchone()

    return render_template('index.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
