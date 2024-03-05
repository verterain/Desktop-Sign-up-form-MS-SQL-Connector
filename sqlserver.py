import pyodbc

server = 'DESKTOP-LH1N80L\\SQLEXPRESS'
database = 'usernames'  

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
