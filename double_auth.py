import smtplib  # Simple Mail Transfer Protocol library for sending emails
from email.mime.multipart import MIMEMultipart  # MIME multipart message composition
from email.mime.text import MIMEText  # MIME text message composition
import pyotp  # Library for generating and verifying one-time passwords


def send_email(sender_email, sender_password, receiver_email, subject, message):
    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email  # Set the sender email address
    msg['To'] = receiver_email  # Set the receiver email address
    msg['Subject'] = subject  # Set the email subject

    # Attach the message content as plain text
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Login to the email server
        text = msg.as_string()  # Convert the message to a string
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        print("Email sent successfully")  # Print success message
    except Exception as e:
        print("Error: Unable to send email.")  # Print error message if sending fails
        print(e)  # Print the exception details
    finally:
        server.quit()  # Quit the SMTP server connection


def double_auth():
    # Generate a random secret for OTP generation
    secret = pyotp.random_base32()

    # Create a TOTP object with the secret
    otp = pyotp.TOTP(secret)
    otp_value = otp.now()  # Get the current OTP value

    # Sender and receiver email details
    sender_email = 'nova77230@gmail.com'
    sender_password = 'yfjq hsmj dwqp lcjx'
    receiver_email = 'anthony.guerand2001@gmail.com'
    subject = 'Email opt'  # Email subject
    message = f"opt : {otp_value}"  # Email message containing the OTP value

    # Send the email
    send_email(sender_email, sender_password, receiver_email, subject, message)

    # Prompt user for OTP input
    user_input = input("Entrez le token OTP : ")
    if otp_value == user_input:  # Verify the OTP entered by the user
        print("Token valide. Accès autorisé.")  # Print message for valid token
        return True  # Return True if token is valid
    else:
        print("Token invalide. Accès refusé.")  # Print message for invalid token
        return False  # Return False if token is invalid
