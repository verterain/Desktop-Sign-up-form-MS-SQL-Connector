from tkinter import *
from tkinter import messagebox
from sqlserver import *

def signup():
    username_in = username.get()
    password_in = password.get()
    email_in = email.get()
        
    if len(username_in) == 0 or len(password_in) == 0 or len(email_in) == 0:
        messagebox.showerror("Error", "Input incomplete")
    else:
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

def siginfunc(username_entry, password_entry):
    username_in = username_entry.get().strip()
    password_in = password_entry.get().strip()

    if len(username_in) == 0 or len(password_in) == 0:
        messagebox.showerror("Error", "Incomplete input")
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()



    print(f"Attempting to sign in with username: '{username_in}' and password: '{password_in}'")

    cursor.execute("""SELECT * FROM [User Data] WHERE username = ? AND passwordcol = ?""", (username_in, password_in))
    user_data = cursor.fetchone()
    
    if user_data:
        messagebox.showinfo("Success", "Login successful")
        print(f"User found: {user_data}")
    else:
        messagebox.showerror("Error", "Username or password is incorrect")

    conn.close()


def signin():
    sign_in_window = Toplevel()

    sigin_username_label = Label(sign_in_window, text="Username")
    sigin_username_label.pack()
    sigin_username = Entry(sign_in_window)
    sigin_username.pack()

    sigin_password_label = Label(sign_in_window, text="Password")
    sigin_password_label.pack()
    sigin_password = Entry(sign_in_window, show="*")
    sigin_password.pack()

    sign_in2 = Button(sign_in_window, text="Sign in", command=lambda: siginfunc(sigin_username, sigin_password))
    sign_in2.pack()

    sign_in_window.mainloop()

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

signin_label = Label(window, text="Already have an account?").pack()
sign_in = Button(window, text="Sign in", command=signin)
sign_in.pack()

window.mainloop()
