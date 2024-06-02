from flask import Flask, request, jsonify, render_template
import json
import mysql.connector
from mysql.connector import pooling

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
def prepare_template():
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor(dictionary=True)
    template_query = "SELECT DISTINCT template_id FROM tr_template_load WHERE template_status = 'to_deploy';"
    cursor.execute(template_query)
    id_list = cursor.fetchall()
    for templates_to_deploy  in id_list:
        #print(templates_to_deploy[0])
        temp_id = templates_to_deploy[0]
        resrc_query = "select distinct res_unique_id from tr_template_load where template_id = '"+str(temp_id)+"';"
        cursor.execute(resrc_query)
        resources_to_deploy = cursor.fetchall()
        #TODO add exception
        try:        
            for res in resources_to_deploy:
                prop_query = "select rp.prop_name, tl.prop_value from tr_template_load tl, resourse_prop rp where tl.prop_id = rp.res_prop_id and res_unique_id = '"+str(res[0])+"'"
                
                cursor.execute(prop_query)
                res_prop_list = cursor.fetchall()
                with open('trfmvms.txt', 'r') as file:
                    file_contents = file.read()
                updated_contents = file_contents
                for res_prop in res_prop_list:
                    updated_contents = updated_contents.replace('"'+res_prop[0]+ '-replaceme"','"'+res_prop[1]+'"')
                with open('trfm-'+res[0]+'.tf', 'w') as file:
                    file.write(updated_contents)    
            cursor.close()
        except FileNotFoundError:
            print(f"Error: input file does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    app.run(debug=True)
