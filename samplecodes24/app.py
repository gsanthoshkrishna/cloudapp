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

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **dbconfig)

@app.route('/')
def index():
    cnx = None
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        
        # Fetch resources from the resource table
        query = "SELECT res_id AS id, res_name AS name, res_image AS image FROM resource"
        cursor.execute(query)
        resources = cursor.fetchall()
        
        # Fetch images from the tr_template_load table
        query = """
            SELECT DISTINCT tr_template_load.res_unique_id, tr_template_load.res_id, resource.res_image
            FROM tr_template_load
            INNER JOIN resource ON tr_template_load.res_id = resource.res_id
        """

        print(query);
        cursor.execute(query)
        load_images = cursor.fetchall()
        
        return render_template('task24.html', resources=resources, load_images=load_images)
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.route('/get_properties', methods=['GET'])
def get_properties():
    selected_id = request.args.get('selected_id')
    div_id = request.args.get('div_id')
    #TODO remove below temp code
    div_id = "drop-container"
    print("Selected ID:", selected_id)
    print("Div ID:", div_id)
    cnx = None
    cursor = None
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ""

        if div_id == "load-container":
            query = """
            SELECT prop_name, prop_value 
            FROM tr_template_load 
            WHERE res_unique_id = %s
            """
        elif div_id == "drop-container":
            query = """
            SELECT prop_name, prop_input_type, is_mandatory 
            FROM resource_prop 
            WHERE res_id = %s
            """
        else:
            return jsonify({"error": "Invalid div_id"}), 400

        print(query)
        cursor.execute(query, (selected_id,))
        props = cursor.fetchall()
        return jsonify(props)
    except mysql.connector.Error as err:
        return str(err), 500
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

if __name__ == "__main__":
    app.run(debug=True)
