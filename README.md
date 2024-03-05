This simple program first sets up the database in SQL Server Management Studio, assuming the user has Windows Aunthentication set up during the connection process. Then, the user can open a simple registration panel in a window.
The sign up function is made to first create tables required for the storage of usernames, passwords and emails if their not present. Then, the function checks if username or email are already occupied. If so, the user is prompted to use another email or username.
If not, the user is prompted with the message about successful registration and their data is going directly to MS SQL database.
The sign in function on the other hand, present in toplevel window, checks if login data provided by the user is relevant and returns a messagebox with a specific prompt.
