import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="cloudapp"
)


def is_div_resource():
    cursor = db.cursor(dictionary=True)
    qry = "select res_id from  div_resources"
    cursor.execute(qry)
    list_div_res = cursor.fetchall()
    print(list_div_res)

is_div_resource()
    
