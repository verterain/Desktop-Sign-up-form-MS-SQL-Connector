import pyodbc

server = 'DESKTOP-LH1N80L\\SQLEXPRESS'
database = 'master'  

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try: 
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    cursor.execute("""CREATE DATABASE usernames
                   """)
    print("Connection successful.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cursor.close()
    conn.close()
