"""Module to control email"""
from flask.ext.mail import Message
from beaver_manager import mail
from threading import Thread
from beaver_manager import app
from .decorators import async


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Sends email to recipent using the flasks email module

    Args:
    subject (str): Plain text
    sender (str): Sender of email in plain text
    recepients (str): Reciepent email. Can be list of strings
    text_body (str): Body of message without HTML formatting
    html_body (str): Body of message with HTML formattin
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)
