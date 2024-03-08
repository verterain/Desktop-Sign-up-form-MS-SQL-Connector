from tkinter import *
from tkinter import messagebox
from sqlserver import *
import smtplib
import random
from tkinter import simpledialog

def send_code(email, code):
    sender_email = "cipulina.devson@gmail.com"
    sender_password = "qwspqdqexoovdobm"
    receiver_email = email 
    message = f"From: {sender_email}\nTo: {receiver_email}\nSubject: Verification Code\n\nYour verification code is: {code}"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)

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
    else:
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM [User Data] WHERE username = ? AND passwordcol = ?""", (username_in, password_in))

        if cursor.fetchone():
            messagebox.showinfo("Success", "Login successful")
        else:
            messagebox.showerror("Error", "Username or password is incorrect")

        conn.close()

def reset_passwordfunc(email, password):
    email_in = email.get().strip()
    new_password_in = password.get().strip()

    if len(email_in) == 0 or len(new_password_in) == 0:
        messagebox.showerror("Error", "Incomplete input")
    else:
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM [User Data] WHERE email = ?", (email_in))
        if cursor.fetchone():
            verification_code = str(random.randint(1000, 9999))
            send_code(email_in, verification_code)

            user_code = simpledialog.askstring("Verification", "Enter a verification code sent to your email address:")
            if user_code == verification_code:
                cursor.execute("UPDATE [User Data] SET passwordcol = ? WHERE email = ?", (new_password_in, email_in))
                messagebox.showinfo("Success", "Password changed")
            else:
                messagebox.showerror("Error", "Incorrect verification code")
        else:
            messagebox.showerror("Error", "No email address in the database")

        conn.close()

def reset_password():
    password_reset_window = Toplevel()
    password_reset_window.title("Reset password")
    password_reset_window.geometry("500x300")

    reset_email_label = Label(password_reset_window, text="Email")
    reset_email_label.pack()

    reset_email_entry = Entry(password_reset_window)
    reset_email_entry.pack()

    reset_password_label = Label(password_reset_window, text="New password")
    reset_password_label.pack()

    reset_password_entry = Entry(password_reset_window)
    reset_password_entry.pack()

    reset_password_button = Button(password_reset_window, text="Reset password", command=lambda: reset_passwordfunc(reset_email_entry, reset_password_entry))
    reset_password_button.pack(pady=10)

    password_reset_window.mainloop()


def signin():
    sign_in_window = Toplevel()
    sign_in_window.title("Sign in panel")
    sign_in_window.geometry("500x300")
    
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

    forgot_password = Button(sign_in_window, text="Forgot password", command=reset_password)
    forgot_password.pack(pady=10)

    sign_in_window.mainloop()

window = Tk()

window.title("Sign up panel")
window.geometry("500x300")

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
sign_up.pack(pady=10)

signin_label = Label(window, text="Already have an account?").pack()
sign_in = Button(window, text="Sign in", command=signin)
sign_in.pack()

window.mainloop()
