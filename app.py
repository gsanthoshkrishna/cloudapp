from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Pass@123',
    'database': 'cloudapp'
}

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor(dictionary=True)

# Route for the main page
@app.route('/')
def index():
    # Fetch resource-details names from the database
    cursor.execute("SELECT res_name  FROM resources")
    resources = [resources['res_name'] for resource in cursor.fetchall()]
    return render_template('resrc.html', resources=resources)

# Route for displaying student details
@app.route('/resource_details', methods=['POST'])
def resource_details():
    # Get the selected student name from the form
    resource_name = request.form['resource']

    # Query the database for the student details
    cursor.execute("SELECT * FROM resources WHERE name = %s", (res_name,))
    resource = cursor.fetchone()
    print(resource)

    return render_template('resrc.html', resource_details=resource)

if __name__ == '__main__':
    app.run(debug=True)