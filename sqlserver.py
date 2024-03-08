import pyodbc

server = 'your_server_name'
database = 'usernames'  

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
