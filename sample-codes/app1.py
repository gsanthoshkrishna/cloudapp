from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'gowri@311',
    'database': 'cloudapp'
}

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor(dictionary=True)

# Route for the main page
@app.route('/')
def index():
    # Fetch resource names and images from the database
    cursor.execute("SELECT res_name, res_image FROM resource")
    resources = cursor.fetchall()
    return render_template('resource.html', resources=resources)

# Route for displaying resource details
@app.route('/resource_details', methods=['POST'])
def resource_details():
    # Get the selected resource name from the form
    resource_name = request.form['resource']

    # Query the database for the resource properties
    cursor.execute('''
        SELECT rp.prop_name, rp.prop_input_type, rp.is_mandatory
        FROM resource_prop rp
        JOIN resource r ON rp.res_id = r.res_id
        WHERE r.res_name = %s
    ''', (resource_name,))
    properties = cursor.fetchall()

    return render_template('resource_details.html', resource_name=resource_name, properties=properties)

if __name__ == '__main__':
    app.run(debug=True)
