from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import pooling

app = Flask(__name__)

# Configure the MySQL connection pool
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "gowri@311",
    "database": "cloudapp"
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                      pool_size=5,
                                                      **dbconfig)

@app.route('/')
def index():
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT res_id AS id, res_name AS name, res_image AS image FROM resource"
        cursor.execute(query)
        resources = cursor.fetchall()
        cursor.close()
        cnx.close()
        return render_template('task24.html', resources=resources)
    except mysql.connector.Error as err:
        return str(err)

@app.route('/get_properties', methods=['POST'])
def get_properties():
    resource_id = request.form['resource_id']
    print("Received resource_id:", resource_id)
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT prop_name, prop_input_type, is_mandatory 
            FROM resource_prop 
            WHERE res_id = %s
        """
        cursor.execute(query, (resource_id,))
        prop = cursor.fetchall()
        cursor.close()
        cnx.close()
        return jsonify(prop)
    except mysql.connector.Error as err:
        return str(err)

@app.route('/load_properties', methods=['GET'])
def load_properties():
    resource_id = request.args.get('resource_id')
    print("Received resource_id for load:", resource_id)
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT prop_name, prop_value 
            FROM tr_template_load 
            WHERE res_id = %s
        """
        cursor.execute(query, (resource_id,))
        prop = cursor.fetchall()
        cursor.close()
        cnx.close()
        return jsonify(prop)
    except mysql.connector.Error as err:
        return str(err)

if __name__ == "__main__":
    app.run(debug=True)
