# TODO: invia email
import smtplib

from datetime import datetime as dt


# Define the SendEmail class to handle email sending
class SendEmail():
    # Initialize the email details
    def __init__(self, name, email, subject, message):
        self.name = name  # Sender's name
        self.email = email  # Sender's email
        self.subject = subject  # Email subject
        self.message = message.encode('utf-8')  # Message body encoded in UTF-8
        self.receiver = "YOUR_EMAIL@hotmail.it"  # Hardcoded receiver email
        self.my_email = "YOUR_SENDING_EMAIL@gmail.com"  # Sender email (used for authentication)
        self.my_pk = "YOUR EMAIL PASSKEY"  # Passkey for sender email (password for authentication)
        self.send_email()  # Call the method to send the email upon initialization

    # Method to send the email
    def send_email(self):
        # Set up a connection to the SMTP server (using Gmail in this case)
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()  # Start TLS encryption for the connection
        connection.login(user=self.my_email, password=self.my_pk)  # Login to the SMTP server
        # Send the email with a specified format for the message
        connection.sendmail(from_addr=self.my_email, to_addrs=self.receiver,
                            msg=f"Subject:{self.subject}\n\nname: {self.name}\nemail: {self.email}\nsubject: {self.subject}\n{self.message}")
