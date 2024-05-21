import mysql.connector as con
db=con.connect(host="localhost",user="root",password="gowri@311")
print("connection created")

cur=db.cursor()
cur.execute("create database gowri1")
print("database created")
cur.execute("use gowri1")

cur.execute("create table students(rollno int,name varchar(20),marks int)")
print("table created")


query="insert into students values(%s,%s,%s)"
list=[(1,"gowri",20),(2,"phani",30),(3,"gayu",40),(4,"ammu",50)]
cur.executemany(query,list)
db.commit()
print(cur.rowcount,"record inserted successfully")
