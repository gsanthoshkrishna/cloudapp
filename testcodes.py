def show_cost():
    #data = request.json
    ruid = 'vm-1'
    #result = str1 + " " + str2
    #qry = select cost from resource_cost where res_unique_id = 'vm-1';
    qry = "select cost from resource_cost where res_unique_id = ' " + ruid + "';"
    print(qry)

    #name = "santhosh"
    

    #print_stmt1 = "hello  " + name + " how are you"
    #print_stmt = "my name is " + name
import json
import mysql.connector
from mysql.connector import pooling
with open('config.json') as config_file:
    config = json.load(config_file)['mysql']

# Create connection pool
cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    **config
)

def propopt():
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor(dictionary=True)
    qry = "select tr_template_load.res_unique_id ,tr_template_load.prop_id, res_prop_list_value.list_value from tr_template_load left join res_prop_list_value on tr_template_load.prop_id = res_prop_list_value.res_prop_id where tr_template_load.res_unique_id ='bus1'order by tr_template_load.res_unique_id ;"
    print(qry)
    cursor.execute(qry)
    result = cursor.fetchall()
    print(result)
    return(propopt)

propopt()


#show_cost()

    