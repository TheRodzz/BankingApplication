import DBConnection

conn=DBConnection.connect_to_database()
query = "SELECT * FROM customer WHERE phone_no = 1111111111"
rows = DBConnection.execute_select_query(conn,query)
trimmed_byte_array = rows[0][4].rstrip(b'\x00')

print(trimmed_byte_array.decode()=="pass")