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

@app.route('/load_properties', methods=['GET'])
def load_properties():
    res_unique_id = request.args.get('res_unique_id')
    cnx = None
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT prop_name, prop_value 
            FROM tr_template_load 
            WHERE res_unique_id = %s
        """
        cursor.execute(query, (res_unique_id,))
        props = cursor.fetchall()
        return jsonify(props)
    except mysql.connector.Error as err:
        return str(err)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

if __name__ == "__main__":
    app.run(debug=True)
