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
    pool_size=10,
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
        print(div_id)
        
        query = f"""
          SELECT prop_name, prop_input_type, is_mandatory 
          FROM resourse_prop 
          WHERE res_id = '{res_unique_id}'
        """
        if div_id == "load-container":
            query = f"""
                SELECT tpl.prop_name, tpl.prop_value, rp.prop_input_type, rp.is_mandatory
                FROM tr_template_load tpl
                JOIN resource_prop rp ON tpl.prop_id = rp.res_prop_id
                WHERE tpl.res_unique_id = '{res_unique_id}'
            """
        print("----------------test10----------")
        print(query)
        
        cursor.execute(query)
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

        sent_json = request.get_json()
        data = sent_json['properties']
        res_id = sent_json['res_id']
        print("Received data:", sent_json)
        
        # Establish connection to MySQL database
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        prefix_query = "SELECT prefix FROM resources WHERE res_id = '" + res_id + "'"
        print(prefix_query)
        cursor.execute(prefix_query)
        prefix_result = cursor.fetchone()
        print(prefix_result)
        if not prefix_result:
            return 'Resource ID not found', 400

        prefix = prefix_result[0]
        print(prefix)
        unique_id = get_unique_id()
        res_unique_id = prefix + "-" + unique_id #sqrl-0603195023
        print("Generated unique ID:", res_unique_id)
        template_id = unique_id
        print("Generated unique ID:",template_id )

        for prop in data:
            #print('test print')
            print(prop)
            prop_name = prop['prop_name']
            prop_value = prop['prop_value']
            
            
            
            print("Prop name:"+prop_name )

            # Retrieve the res_prop_id from resource_prop
            # Assuming prop_name is a variable containing the value you want to search for
            #select  res_prop_id from resource_prop where prop_name = 'name' and  res_id = 3
            #"select  res_prop_id from resource_prop where prop_name = '" + p_name + "' and  res_id = " + r_id
            query = "SELECT res_prop_id FROM resource_prop WHERE prop_name = '" + prop_name + "' and res_id = '" + res_id + "' "
            print('test')
            print(query)
            cursor.execute(query)
            prop_det = cursor.fetchone()
            print(prop_det)
            if prop_det:
                prop_id = prop_det[0]
                print(prop_id)
                # Insert or update the property in tr_template_load
                insert_query = f"""
                   INSERT INTO tr_template_load (template_id, res_id, prop_name, prop_value, res_unique_id, prop_id)
                   VALUES ('{template_id}', {res_id}, '{prop_name}', '{prop_value}', '{res_unique_id}', {prop_id})
                """
                print("Executing query:", insert_query)
                cursor.execute(insert_query)
                check = cursor.fetchone()
                print(check)
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

@app.route('/get_resource_cost', methods=['GET'])
def get_resource_cost():
    cnx = None
    cursor = None
   
    
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        res_id = request.args.get('res_id')
        print(res_id)
        query = f"SELECT cost FROM resource_cost WHERE res_unique_id = '{res_id}'"
        print(query)
    
        cursor.execute(query)
        cost = cursor.fetchall()
        print(cost)

        if cost:
            return jsonify({'cost': cost[0]})
        else:
            return jsonify({'error': 'Resource not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


@app.route('/get_properties_options', methods=['GET'])
def get_properties_options():    
    cnx = None
    cursor = None
  
    try:
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        res_unique_id = request.args.get('res_unique_id')
        print(res_unique_id)
        print("......test qry.......")
        query = "select tr_template_load.res_unique_id ,tr_template_load.prop_id, res_prop_list_value.list_value from tr_template_load left join res_prop_list_value on tr_template_load.prop_id = res_prop_list_value.res_prop_id where tr_template_load.res_unique_id ='" + str(res_unique_id) + "'order by tr_template_load.res_unique_id ;"
        cursor.execute(query)
        reslistvalues = cursor.fetchall()
        print(reslistvalues)
        return reslistvalues

        if realistvalues:
            return jsonify(reslistvalues)
        else:
            return jsonify({'error': 'Resource not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()




 
if __name__ == '__main__':
    app.run(debug=True)


