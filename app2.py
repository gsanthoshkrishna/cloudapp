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





def prepare_template():
    cursor = db.cursor(dictionary=True)
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
            print(f"Error: The file {input_file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    app.run(debug=True)