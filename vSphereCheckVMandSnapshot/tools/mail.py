import smtplib
from email.message import EmailMessage


def send_mail(config, buf_msg):
    msg = EmailMessage()
    msg['Subject'] = config.get('subject')
    msg['From'] = config.get('from')
    msg['To'] = config.get('to')
    msg.set_content(f"<!DOCTYPE html><html><body>{buf_msg}</body></html>", subtype='html')
    with smtplib.SMTP_SSL(config.get('smtp')) as smtp:
        smtp.login(config.get('login'), config.get('password'))
        smtp.send_message(msg)
