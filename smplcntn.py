import mysql.connector

# Function to insert a record into a MySQL table
def insert_record(connection, st_name, st_id, st_marks):
    try:
        cursor = connection.cursor()
        # MySQL query to insert a record into a table
        insert_query = "INSERT INTO student(st_name, st_id, st_marks) VALUES (%s, %s, %s)"
        record_data = (st_name, st_id, st_marks)
        cursor.execute(insert_query, record_data)
        connection.commit()
        print("Record inserted successfully!")
    except mysql.connector.Error as e:
        print(f"Error inserting record: {e}")

# Main function to test the insertion
def main():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pass@123',
            database='uma'
        )
        if connection.is_connected():
            print("Connected to MySQL database")

            # Example: Insert a record
            insert_record(connection, "avitej", 300, "122")

            
            
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")

if __name__ == "__main__":
    main()
