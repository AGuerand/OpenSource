import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
import pyotp  


def send_email(sender_email, sender_password, receiver_email, subject, message):

    msg = MIMEMultipart()
    msg['From'] = sender_email 
    msg['To'] = receiver_email 
    msg['Subject'] = subject 


    msg.attach(MIMEText(message, 'plain'))

    try:
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(sender_email, sender_password)  
        text = msg.as_string()  
        server.sendmail(sender_email, receiver_email, text)  
        print("Email sent successfully") 
    except Exception as e:
        print("Error: Unable to send email.") 
        print(e)
    finally:
        server.quit() 


def double_auth():

    secret = pyotp.random_base32()


    otp = pyotp.TOTP(secret)
    otp_value = otp.now()  

    
    sender_email = 'mel'
    sender_password = 'pass'
    receiver_email = 'mel'
    subject = 'Email opt'
    message = f"opt : {otp_value}"

    send_email(sender_email, sender_password, receiver_email, subject, message)


    user_input = input("Entrez le token OTP : ")
    if otp_value == user_input: 
        print("Token valide. Accès autorisé.")
        return True  
    else:
        print("Token invalide. Accès refusé.") 
        return False 
