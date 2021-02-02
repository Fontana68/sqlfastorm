import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from pathlib import Path

import os

def mandaviaposta():
    ''' Send email to leonard68@libero.it'''
    
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"
    sender_email = "snowleonard68@gmail.com"
    receiver_email = "leonard68@libero.it"

    # password = input("Type your password and press enter:")
    password = 'udzsxzrtvuqqtjwk'

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message['Date'] = formatdate(localtime=True)
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    #----------------------------------------------------
    files = ['TestUfficialeGAS.csv', 'TestUfficialeOPA.csv', 'TestUfficialeOBD.csv']

    for path in files:
        if os.path.exists(path):
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                    part.set_payload(file.read())
                
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(Path(path).name))
            message.attach(part)

    #----------------------------------------------------
    # Add attachment to message and convert message to string
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        
if __name__ == "__main__":
    mandaviaposta()