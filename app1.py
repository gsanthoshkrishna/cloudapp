from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configure your MySQL connection
db_config = {
    'user': 'root',
    'password': 'Pass@123',
    'host': 'localhost',
    'database': 'cloudapp'
}

@app.route('/')
def index():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute the query to get name and grade
    query = "SELECT res_id,res_name,res_image FROM resources"
    cursor.execute(query)

    # Fetch all the results
    res_list = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()
    print(res_list)

    # Pass the data to the template
    return render_template('prop.html', resources=res_list)

if __name__ == '__main__':
    app.run(debug=True)