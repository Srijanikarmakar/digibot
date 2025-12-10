import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "digibototp@gmail.com"  
APP_PASSWORD = "your_app_password_here"  

def send_otp(to_email, otp):
    subject = "Your DigiBot OTP Code"
    message = f"Your OTP is: {otp}"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()
