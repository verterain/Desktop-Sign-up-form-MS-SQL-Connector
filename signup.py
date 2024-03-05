from tkinter import *
from tkinter import messagebox
from sqlserver import *

def signup():
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    cursor.execute("""
                    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'User Data' AND type = 'U')
                    CREATE TABLE [User Data] (
                    UserID INT IDENTITY(1,1) PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    passwordcol VARCHAR(50) NOT NULL,
                    email VARCHAR(60) NOT NULL)
                """)

    username_in = username.get()
    password_in = password.get()
    email_in = email.get()

    
    cursor.execute("SELECT * FROM [User Data] WHERE username = ? OR email = ?", (username_in, email_in))
    if cursor.fetchone():
        messagebox.showinfo("Error", "Username or Email already exist")
    else:
        cursor.execute("""INSERT INTO [User Data] (username, passwordcol, email)
                      VALUES (?, ?, ?)
                      """, (username_in, password_in, email_in))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")

    conn.close()

window = Tk()

username_label = Label(window, text="Username")
username_label.pack()

username = Entry(window)
username.pack()

password_label = Label(window, text="Password")
password_label.pack()

password = Entry(window, show="*")
password.pack()

email_label = Label(window, text="Email")
email_label.pack()

email = Entry(window)
email.pack()

sign_up = Button(window, text="Sign up", command=signup)
sign_up.pack()


window.mainloop()
