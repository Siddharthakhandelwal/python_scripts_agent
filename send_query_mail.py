import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail_querry(recipient_email, subject,body):


    sender_email = "siddharthakhandelwal789@gmail.com"
    sender_password = "wkrb fiqx fpeq ctmc"  # Use an app password if using Gmail
    
    try:
        # Ensure the SMTP server address is correct
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to the SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()  # Secure the connection
            server.ehlo()
            
            # Use App Password for Gmail authentication
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication error: Ensure you are using an App Password instead of your regular password.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    
