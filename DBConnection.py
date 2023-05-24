import mysql.connector

    
# Establish a database connection
def connect_to_database():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='7349',
        database='bank'
    )
    return conn

# Execute a SELECT query
def execute_select_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

# Execute an INSERT, UPDATE, or DELETE query
def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    # conn.commit()
    return cursor
    # cursor.close()

# Close the database connection
def close_connection(conn):
    conn.close()

