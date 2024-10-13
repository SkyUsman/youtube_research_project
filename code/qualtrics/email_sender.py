import smtplib
from email.mime.text import MIMEText

def send_email(recipient, survey_link):
    sender_email = 'Jrubio062003@gmail.com'  # Replace with your actual OU email address
    sender_password = 'hkkm ulqy rbjw tbtz'     # Your Outlook password or App Password if 2FA is enabled

    subject = 'Your Survey Participation'
    body = f'Please participate in our survey: {survey_link}'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    # Use the correct SMTP server for Outlook
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Use TLS
        server.login(sender_email, sender_password)  # Login to the server
        server.send_message(msg)  # Send the email

    print(f"Email sent to {recipient}")
