import tkinter as tk
from tkinter import messagebox
from sqlserver import *
from emailsender import *
import random
from tkinter import simpledialog

class BaseWindow(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry("500x300")

class SignUpWindow(BaseWindow):
    def __init__(self):
        super().__init__("Sign up panel")
        username_label = tk.Label(self, text="Username")
        username_label.pack()
        self.username = tk.Entry(self)
        self.username.pack()

        email_label = tk.Label(self, text="Email")
        email_label.pack()
        self.email = tk.Entry(self)
        self.email.pack()

        password_label = tk.Label(self, text="Password")
        password_label.pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        sign_up = tk.Button(self, text="Sign up", command=self.signup)
        sign_up.pack(pady=10)

        sign_in_label = tk.Label(self, text="Already have an account?")
        sign_in_label.pack()

        sign_in_button = tk.Button(self, text="Sign in", command=self.open_sign_in_window)
        sign_in_button.pack()

    def open_sign_in_window(self):
        sign_in_window = SignInWindow()
        sign_in_window.mainloop()

    def signup(self):
        username_in = self.username.get()
        email_in = self.email.get()
        password_in = self.password.get()
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
            cursor.execute("SELECT * FROM [User Data] WHERE username = ? or email = ?", (username_in, email_in))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username or email already exist")
            else:
                cursor.execute("""INSERT INTO [User Data] (username, passwordcol, email)
                               VALUES (?, ?, ?)""", (username_in, password_in, email_in))
                messagebox.showinfo("Success", "Registration successful")

            conn.close()


class SignInWindow(BaseWindow):
    def __init__(self):
        super().__init__("Sign in panel")
        username_label = tk.Label(self, text="Username")
        username_label.pack()
        self.username = tk.Entry(self)
        self.username.pack()

        password_label = tk.Label(self, text="Password")
        password_label.pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        sign_in = tk.Button(self, text="Sign in", command=self.signin)
        sign_in.pack(pady=10)

        reset_password = tk.Button(self, text="Reset password", command=self.open_reset_password_window)
        reset_password.pack()

    def open_reset_password_window(self):
        reset_password_window = ResetPasswordWindow()
        reset_password_window.mainloop()
    
    def signin(self):
        username_in = self.username.get()
        password_in = self.password.get()

        if len(username_in) == 0 or len(password_in) == 0:
            messagebox.showerror("Error", "Incomplete input")
        else:
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [User Data] WHERE username = ? AND passwordcol = ?", (username_in, password_in))
            
            if cursor.fetchone():
                messagebox.showinfo("Success", "Login successful")
            else:
                messagebox.showerror("Error", "Invalid username or password")

            conn.close()


class ResetPasswordWindow(BaseWindow):
    def __init__(self):
        super().__init__("Reset password panel")
        email_label = tk.Label(self, text="Email")
        email_label.pack()
        self.email = tk.Entry(self)
        self.email.pack()

        new_password_label = tk.Label(self, text="New password")
        new_password_label.pack()
        self.new_password = tk.Entry(self, show="*")
        self.new_password.pack()

        reset_button = tk.Button(self, text="Reset password", command=self.reset_password)
        reset_button.pack(pady=10)

    def reset_password(self):
        email_in = self.email.get()
        new_password_in = self.new_password.get()

        if len(email_in) == 0 or len(new_password_in) == 0:
            messagebox.showerror("Error", "Incomplete input")
        else:
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [User Data] WHERE email = ?", (email_in))
            
            if cursor.fetchone():
                verification_code = str(random.randint(1000, 9999))
                send_code(email_in, verification_code)
                user_code = simpledialog.askstring("Verification", "Enter a verification code sent to your email address: ")
                if user_code == verification_code:
                    cursor.execute("UPDATE [User Data] SET passwordcol = ? WHERE email = ?", (new_password_in, email_in))
                    messagebox.showinfo("Success", "Password changed")
                else:
                    messagebox.showerror("Error", "Incorrect verification code")
            else:
                messagebox.showerror("Error", "This email doesn't exist in the database")
        

if __name__ == '__main__':
    app = SignUpWindow()
    app.mainloop()
