from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Configure the MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="cloudapp"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    query = "SELECT res_id AS id, res_name AS name, res_image AS image FROM resources"
    cursor.execute(query)
    resources = cursor.fetchall()
    cursor.close()
    return render_template('index.html', resources=resources)

@app.route('/get_properties', methods=['POST'])
def get_properties():
    resource_id = request.form['resource_id']
    print("Received resource_id:", resource_id)
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT prop_name, prop_input_type, is_mandatory 
        FROM resourse_prop 
        WHERE res_id = %s
    """
    cursor.execute(query, (resource_id,))
    prop = cursor.fetchall()
    cursor.close()
    return jsonify(prop)

if __name__ == "__main__":
    app.run(debug=True)