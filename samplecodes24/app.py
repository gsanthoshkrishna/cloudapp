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
        # Fetch resources from the resource table
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT res_id AS id, res_name AS name, res_image AS image FROM resource"
        cursor.execute(query)
        resources = cursor.fetchall()

        # Fetch images from the tr_template_load table
        query = """
            SELECT DISTINCT tr_template_load.res_unique_id, tr_template_load.res_id, resource.res_image
            FROM tr_template_load
            INNER JOIN resource ON tr_template_load.res_id = resource.res_id
        """
        cursor.execute(query)
        load_images = cursor.fetchall()

        cursor.close()
        cnx.close()

        return render_template('task24.html', resources=resources, load_images=load_images)
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
        props = cursor.fetchall()
        cursor.close()
        cnx.close()
        return jsonify(props)
    except mysql.connector.Error as err:
        return str(err)

if __name__ == "__main__":
    app.run(debug=True)
