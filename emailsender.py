import smtplib

def send_code(email, code):
    sender_email = "cipulina.devson@gmail.com"
    sender_password = "qwspqdqexoovdobm"
    receiver_email = email 
    message = f"From: {sender_email}\nTo: {receiver_email}\nSubject: Verification Code\n\nYour verification code is: {code}"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
