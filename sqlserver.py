import pyodbc

server = 'DESKTOP-F9RFMJE\\SQLEXPRESS'
database = 'usernames'  

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
