import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define the sender and recipient email addresses
sender_email = "cipulina.devson@gmail.com"
receiver_email = "verterain@gmail.com"
password = "Szczupak@137"

# Create a MIMEMultipart object and set up the headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Python Email Test"

# Add the email body
body = "This is a test email sent from Python."
message.attach(MIMEText(body, "plain"))

# Create a secure SSL context
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Use the appropriate server and port
server.login(sender_email, password)

# Send the email and close the connection
server.sendmail(sender_email, receiver_email, message.as_string())
server.quit()
