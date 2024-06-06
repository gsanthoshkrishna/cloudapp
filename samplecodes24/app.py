from flask import Flask, request, jsonify, render_template
import json
import mysql.connector
from mysql.connector import pooling
from datetime import datetime


app = Flask(__name__)

# Load MySQL configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)['mysql']

# Create connection pool
cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **config
)

# Define index route
@app.route('/')
def index():
    cnx = None
    cursor = None
    try:
        # Get connection from connection pool
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        # Perform database operations here
        
        # Example: Fetch resources from the resource table
        query = "SELECT res_id AS id, res_name AS name, res_image AS image FROM resource"
        cursor.execute(query)
        resources = cursor.fetchall()
        
        # Example: Fetch images from the tr_template_load table
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

# Define get_properties route
@app.route('/get_properties', methods=['GET'])
def get_properties():
    cnx = None
    cursor = None
    try:
        # Get connection from connection pool
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        # Perform database operations here
        
        res_unique_id = request.args.get('selected_id')
        div_id = request.args.get('div_id')
        
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
def get_unique_id():
    now = datetime.now()
    return now.strftime("%m%d%H%M%S")

@app.route('/save_properties', methods=['POST'])
def save_properties():
    cnx = None
    cursor = None
    res_uniq_id = get_unique_id()
    print("Generated unique ID:", res_uniq_id)

    try:
        data = request.get_json()
        print("Received data:", data)
        
        # Establish connection to MySQL database
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        for prop in data:
            prop_name = prop['prop_name']
            prop_value = prop['prop_value']
            res_id = prop['res_id']

            print("Prop name:", prop_name)

            # Retrieve the res_prop_id from resource_prop
            # Assuming prop_name is a variable containing the value you want to search for
            #select  res_prop_id from resource_prop where prop_name = 'name' and  res_id = 3
            #"select  res_prop_id from resource_prop where prop_name = '" + p_name + "' and  res_id = " + r_id
            query = "SELECT res_prop_id FROM resource_prop WHERE prop_name = '" + prop_name + "' and res_id = '" + res_id + "' "
            cursor.execute(query)
            prop_det = cursor.fetchone()
            if prop_det:
                prop_id = prop_det[0]

                # Insert or update the property in tr_template_load
                query = """
                    INSERT INTO tr_template_load (res_unique_id, prop_id, prop_name, prop_value)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE prop_value = VALUES(prop_value)
                """
                cursor.execute(query, (res_uniq_id, prop_id, prop_name, prop_value))
                print("Property saved successfully")
            else:
                print("No result found for the given prop_name")

        cnx.commit()
        return jsonify({"status": "success"}), 200
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": str(err)}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if cursor:
            cursor.fetchall()  # Consume unread results
            cursor.close()
        if cnx:
            cnx.close()

if __name__ == "__main__":
    app.run(debug=True)



