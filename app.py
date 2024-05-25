from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configure your MySQL connection
db_config = {
    'user': 'root',
    'password': 'Pass@123',
    'host': 'localhost',
    'database': 'cloudapp'
}

@app.route('/')
def index():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute the query to get name and grade
    query = "SELECT res_id,res_name,res_image FROM resources"
    cursor.execute(query)

    # Fetch all the results
    res_list = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()


    # Pass the data to the template
    return render_template('properties2.html', resources=res_list)

# Route for displaying student details
@app.route('/resource_details', methods=['POST'])
def resource_details():
    # Get the selected student name from the form
    resource_name = request.form['resource']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    
    # Query the database for the student details
    cursor.execute("SELECT * FROM resourse_prop WHERE res_id = %s", (resource_name,))
    resource = cursor.fetchall()
    print(resource)

    # Close the connection
    cursor.close()
    conn.close()

    return render_template('properties2.html', res_props=resource)

if __name__ == '__main__':
    app.run(debug=True)