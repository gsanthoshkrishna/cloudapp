import mysql.connector


db_config = {
    'user': 'root',
    'password': 'Pass@123',
    'host': 'localhost',
    'database': 'cloudapp'
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


template_query = "SELECT DISTINCT template_id FROM tr_template_load WHERE template_status = 'to_deploy';"

cursor.execute(template_query)
id_list = cursor.fetchall()


cursor = conn.cursor()
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
            #print(prop_query)
            cursor.execute(prop_query)
            res_prop_list = cursor.fetchall()
            with open('trfmvms.txt', 'r') as file:
                file_contents = file.read()
            updated_contents = file_contents
            for res_prop in res_prop_list:
                #print(res_prop)
                updated_contents = updated_contents.replace('"'+res_prop[0]+ '-replaceme"','"'+res_prop[1]+'"')
                #print("----------afterrepacin of "+ res_prop[0]+"--------")
                #print(updated_contents)
            with open('trfm-'+res[0]+'.tf', 'w') as file:
                file.write(updated_contents)    
            
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
   