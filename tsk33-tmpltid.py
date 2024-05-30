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
    for res in resources_to_deploy:
        prop_query = "select rp.prop_name, tl.prop_value from tr_template_load tl, resourse_prop rp where tl.prop_id = rp.res_prop_id and res_unique_id = '"+str(res[0])+"'"
        #print(prop_query)
        cursor.execute(prop_query)
        res_prop = cursor.fetchall()
        print(res_prop)