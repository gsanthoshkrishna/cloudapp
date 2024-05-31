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

@app.route('/get_properties', methods=['GET'])
def get_properties():

    res_unique_id = request.args.get('selected_id')
    div_id = request.args.get('div_id')
    cnx = None
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
          SELECT prop_name, prop_input_type, is_mandatory 
          FROM resource_prop 
          WHERE res_id = %s
        """
        if div_id == "load-container":
            query = """
            SELECT tpl.prop_name, tpl.prop_value, rp.prop_input_type, rp.is_mandatory
            FROM tr_template_load tpl
            JOIN resource_prop rp ON tpl.prop_id = rp.res_prop_id
            WHERE tpl.res_unique_id = %s;

            """
        print(res_unique_id)
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